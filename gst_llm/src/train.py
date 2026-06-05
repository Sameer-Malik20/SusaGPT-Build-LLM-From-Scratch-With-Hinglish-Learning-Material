import copy
import math
import re
import time
import logging
from contextlib import nullcontext
from pathlib import Path

import torch
import torch.nn as nn
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader, Dataset

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

from .config import (
    BASE_MODEL_PATH,
    DATA_PATH,
    MODEL_CONFIG,
    TOKENIZER_CONFIG,
    TOKENIZER_PATH,
    TRAIN_CONFIG,
    ARTIFACTS_DIR,
)
from .model import SusaGPT
from .tokenizer import Tokenizer


# ─────────────────────────────────────────────────────────
# Logging setup — console + file
# ─────────────────────────────────────────────────────────
LOG_FILE = ARTIFACTS_DIR / "train_log.txt"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
log = logging.getLogger("gst_train")


# ─────────────────────────────────────────────────────────
# Dataset
# ─────────────────────────────────────────────────────────
class TextDataset(Dataset):
    def __init__(self, tokens, seq_len=128):
        self.tokens = tokens
        self.seq_len = seq_len

    def __len__(self):
        return len(self.tokens) - self.seq_len

    def __getitem__(self, idx):
        x = self.tokens[idx : idx + self.seq_len]
        y = self.tokens[idx + 1 : idx + self.seq_len + 1]
        return (
            torch.tensor(x, dtype=torch.long),
            torch.tensor(y, dtype=torch.long),
        )


# ─────────────────────────────────────────────────────────
# Curriculum Learning
# ─────────────────────────────────────────────────────────
def split_into_chunks(text):
    chunks = [c.strip() for c in re.split(r"\n{2,}", text) if c.strip()]
    return chunks or [text]


def chunk_difficulty(chunk):
    punct = sum(1 for c in chunk if not c.isalnum() and not c.isspace())
    non_ascii = sum(1 for c in chunk if ord(c) > 127)
    return len(chunk.split()) + punct * 0.5 + non_ascii * 0.25


def build_curriculum_text(text):
    chunks = split_into_chunks(text)
    sorted_chunks = sorted(chunks, key=chunk_difficulty)
    return "\n\n".join(sorted_chunks), sorted_chunks


# ─────────────────────────────────────────────────────────
# Scheduler
# ─────────────────────────────────────────────────────────
def build_scheduler(optimizer, total_steps, warmup_ratio):
    warmup_steps = max(1, int(total_steps * warmup_ratio))

    def lr_lambda(step):
        if step < warmup_steps:
            return float(step + 1) / float(warmup_steps)
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return max(0.1, 0.5 * (1.0 + math.cos(math.pi * progress)))

    return LambdaLR(optimizer, lr_lambda)


# ─────────────────────────────────────────────────────────
# Checkpointing
# ─────────────────────────────────────────────────────────
CKPT_DIR = ARTIFACTS_DIR / "checkpoints"
CKPT_DIR.mkdir(parents=True, exist_ok=True)


def save_checkpoint(model, tokenizer, epoch, val_loss):
    path = CKPT_DIR / f"ckpt_epoch{epoch:03d}_val{val_loss:.4f}.pt"
    torch.save(
        {
            "epoch": epoch,
            "val_loss": val_loss,
            "model_state": model.state_dict(),
            "vocab_size": tokenizer.vocab_size,
            "embed_dim": model.embed_dim,
            "num_heads": model.num_heads,
            "num_kv_heads": model.num_kv_heads,
            "num_layers": model.num_layers,
            "max_len": model.max_len,
            "dropout": model.dropout,
        },
        path,
    )
    log.info(f"Checkpoint saved → {path.name}")
    return path


def save_model(model, tokenizer, path=BASE_MODEL_PATH):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state": model.state_dict(),
            "vocab_size": tokenizer.vocab_size,
            "embed_dim": model.embed_dim,
            "num_heads": model.num_heads,
            "num_kv_heads": model.num_kv_heads,
            "num_layers": model.num_layers,
            "max_len": model.max_len,
            "dropout": model.dropout,
        },
        path,
    )
    log.info(f"Base model saved → {path}")


# ─────────────────────────────────────────────────────────
# Training Loop
# ─────────────────────────────────────────────────────────
def make_autocast(use_amp, device):
    if use_amp:
        return torch.autocast(device_type=device, dtype=torch.float16)
    return nullcontext()


def train_model(model, train_loader, val_loader, config, tokenizer, device="cpu"):
    model = model.to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config["learning_rate"],
        weight_decay=config["weight_decay"],
    )
    criterion = nn.CrossEntropyLoss(ignore_index=0)

    accum = max(1, config["gradient_accumulation_steps"])
    steps_per_epoch = math.ceil(len(train_loader) / accum)
    total_steps = config["epochs"] * steps_per_epoch
    scheduler = build_scheduler(optimizer, total_steps, config["warmup_ratio"])

    use_amp = bool(config["mixed_precision"]) and device == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    best_val_loss = float("inf")
    best_weights = None
    wait = 0
    start_time = time.time()

    log.info("=" * 70)
    log.info("GST LLM — Base Pretraining Start")
    log.info(f"  Train samples : {len(train_loader.dataset):,}")
    log.info(f"  Val samples   : {len(val_loader.dataset):,}")
    log.info(f"  Device        : {device}")
    log.info(f"  Epochs        : {config['epochs']}")
    log.info(f"  Eff. batch    : {config['batch_size'] * accum}")
    log.info(f"  Mixed Prec.   : {use_amp}")
    log.info("=" * 70)

    header = f"{'Epoch':>6} | {'Train':>8} | {'Val':>8} | {'GNorm':>7} | {'LR':>9} | Status"
    log.info(header)
    log.info("-" * 70)

    for epoch in range(config["epochs"]):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        train_loss, train_batches, last_gnorm = 0.0, 0, 0.0

        epoch_iter = tqdm(train_loader, desc=f"Epoch {epoch+1:3}", leave=False) if HAS_TQDM else train_loader

        for i, (x, y) in enumerate(epoch_iter):
            x, y = x.to(device), y.to(device)

            with make_autocast(use_amp, device):
                logits = model(x)
                B, T, V = logits.shape
                raw_loss = criterion(logits.reshape(B * T, V), y.reshape(B * T))
                loss = raw_loss / accum

            scaler.scale(loss).backward()

            if (i + 1) % accum == 0 or (i + 1) == len(train_loader):
                scaler.unscale_(optimizer)
                gnorm = torch.nn.utils.clip_grad_norm_(model.parameters(), config["max_grad_norm"])
                last_gnorm = float(gnorm)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
                scheduler.step()

            train_loss += raw_loss.item()
            train_batches += 1

        avg_train = train_loss / train_batches

        # Validation
        model.eval()
        val_loss, val_batches = 0.0, 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                with make_autocast(use_amp, device):
                    logits = model(x)
                    B, T, V = logits.shape
                    val_loss += criterion(logits.reshape(B * T, V), y.reshape(B * T)).item()
                val_batches += 1
        avg_val = val_loss / val_batches
        lr_now = optimizer.param_groups[0]["lr"]

        gap = avg_val - avg_train
        status = "overfit⚠" if gap > 1.5 else ("watch" if gap > 0.8 else "stable✓")
        log.info(f"{epoch+1:6d} | {avg_train:8.4f} | {avg_val:8.4f} | {last_gnorm:7.4f} | {lr_now:9.6f} | {status}")

        # Checkpoint every 10 epochs
        if (epoch + 1) % 10 == 0:
            save_checkpoint(model, tokenizer, epoch + 1, avg_val)

        if avg_val < best_val_loss:
            best_val_loss = avg_val
            best_weights = copy.deepcopy(model.state_dict())
            wait = 0
        else:
            wait += 1
            if wait >= config["patience"]:
                log.info(f"Early stopping at epoch {epoch+1} (best val: {best_val_loss:.4f})")
                break

    elapsed = time.time() - start_time
    log.info("-" * 70)
    log.info(f"Training complete! Time: {elapsed/60:.1f} min | Best val loss: {best_val_loss:.4f}")

    if best_weights:
        model.load_state_dict(best_weights)
    return model


# ─────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────
def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    log.info(f"Reading corpus from: {DATA_PATH}")
    text = DATA_PATH.read_text(encoding="utf-8")

    curriculum_text, chunks = build_curriculum_text(text)
    log.info(f"Curriculum chunks  : {len(chunks):,}")

    tokenizer = Tokenizer(target_vocab_size=TOKENIZER_CONFIG["target_vocab_size"])
    tokenizer.build_vocab(text)
    TOKENIZER_DIR = TOKENIZER_PATH.parent
    TOKENIZER_DIR.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(TOKENIZER_PATH))
    log.info(f"Tokenizer saved    : vocab_size={tokenizer.vocab_size}")

    tokens = tokenizer.encode(curriculum_text)
    log.info(f"Total BPE tokens   : {len(tokens):,}")

    split = int(len(tokens) * TRAIN_CONFIG["train_split"])
    train_tokens, val_tokens = tokens[:split], tokens[split:]

    seq_len = MODEL_CONFIG["max_len"]
    train_ds = TextDataset(train_tokens, seq_len)
    val_ds   = TextDataset(val_tokens,   seq_len)

    train_loader = DataLoader(train_ds, batch_size=TRAIN_CONFIG["batch_size"], shuffle=True,  num_workers=0, pin_memory=(device=="cuda"))
    val_loader   = DataLoader(val_ds,   batch_size=TRAIN_CONFIG["batch_size"], shuffle=False, num_workers=0)

    model = SusaGPT(
        vocab_size  = tokenizer.vocab_size,
        embed_dim   = MODEL_CONFIG["embed_dim"],
        num_heads   = MODEL_CONFIG["num_heads"],
        num_kv_heads= MODEL_CONFIG["num_kv_heads"],
        num_layers  = MODEL_CONFIG["num_layers"],
        max_len     = MODEL_CONFIG["max_len"],
        dropout     = MODEL_CONFIG["dropout"],
    )
    total_params = sum(p.numel() for p in model.parameters())
    log.info(f"Model parameters   : {total_params:,}")

    model = train_model(model, train_loader, val_loader, TRAIN_CONFIG, tokenizer, device)
    save_model(model, tokenizer)


if __name__ == "__main__":
    main()
