import copy
import json
import math
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

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from susagpt.src.config import (
    BASE_MODEL_PATH,
    FINE_TUNE_CONFIG,
    FINETUNED_MODEL_PATH,
    QA_DATA_PATH,
    TOKENIZER_PATH,
    ARTIFACTS_DIR,
)
from susagpt.src.model import SusaGPT
from susagpt.src.tokenizer import Tokenizer

LOG_FILE = ARTIFACTS_DIR / "susagpt_train_log.txt"
log = logging.getLogger("susagpt_finetune")


# fine_tune.py ka kaam base language model ko Q&A behavior sikhana hai.
# Is step ke baad model generic text continuation se thoda aage badhkar
# zyada direct jawab dene lagta hai.


def build_scheduler(optimizer, total_steps, warmup_ratio):
    warmup_steps = max(1, int(total_steps * warmup_ratio))

    def lr_lambda(current_step):
        if current_step < warmup_steps:
            return float(current_step + 1) / float(warmup_steps)

        progress = (current_step - warmup_steps) / max(1, total_steps - warmup_steps)
        cosine_value = 0.5 * (1.0 + math.cos(math.pi * progress))
        return max(0.1, cosine_value)

    return LambdaLR(optimizer, lr_lambda)


def make_autocast_context(use_amp, device):
    if use_amp:
        return torch.autocast(device_type=device, dtype=torch.float16)
    return nullcontext()


def load_tokenizer():
    tokenizer = Tokenizer()
    tokenizer.load(str(TOKENIZER_PATH))
    return tokenizer


def load_base_model():
    checkpoint = torch.load(BASE_MODEL_PATH, map_location="cpu", weights_only=False)
    model = SusaGPT(
        vocab_size=checkpoint["vocab_size"],
        embed_dim=checkpoint["embed_dim"],
        num_heads=checkpoint["num_heads"],
        num_kv_heads=checkpoint.get("num_kv_heads", checkpoint["num_heads"]),
        num_layers=checkpoint["num_layers"],
        max_len=checkpoint.get("max_len", 32),
        dropout=checkpoint.get("dropout", 0.1),
    )
    model.load_state_dict(checkpoint["model_state"])
    return model


class QADataset(Dataset):
    # Har Q&A pair ko ek short teaching example me convert karte hain.
    # Model ko prompt ke baad answer pattern dekhne ki habit padti hai.
    def __init__(self, qa_pairs, tokenizer, seq_len):
        self.samples = []
        pad_id = tokenizer.pad_token_id

        for pair in qa_pairs:
            text = f"question {pair['question']} answer {pair['answer']}"
            ids = tokenizer.encode(text)

            if len(ids) < 2:
                continue

            ids = ids[: seq_len + 1]
            x = ids[:-1]
            y = ids[1:]

            pad_count = seq_len - len(x)
            if pad_count > 0:
                x = x + [pad_id] * pad_count
                y = y + [pad_id] * pad_count

            self.samples.append(
                (
                    torch.tensor(x, dtype=torch.long),
                    torch.tensor(y, dtype=torch.long),
                )
            )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


def save_finetuned_model(model, tokenizer, path=FINETUNED_MODEL_PATH):
    from pathlib import Path
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
    log.info(f"Fine-tuned model saved -> {path}")


def fine_tune_model(model, train_loader, val_loader, config, pad_id, device="cpu"):
    model = model.to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config["learning_rate"],
        weight_decay=config["weight_decay"],
    )
    criterion = nn.CrossEntropyLoss(ignore_index=pad_id)
    accumulation_steps = max(1, config["gradient_accumulation_steps"])
    scheduler = build_scheduler(
        optimizer,
        total_steps=config["epochs"] * math.ceil(len(train_loader) / accumulation_steps),
        warmup_ratio=config["warmup_ratio"],
    )
    use_amp = bool(config["mixed_precision"]) and device == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    best_val_loss = float("inf")
    best_weights = None
    wait = 0

    log.info("=" * 70)
    log.info("SusaGPT — Q&A Fine-Tuning Start")
    log.info(f"  Train QA samples : {len(train_loader.dataset)}")
    log.info(f"  Val QA samples   : {len(val_loader.dataset)}")
    log.info(f"  Device           : {device}")
    log.info(f"  Epochs           : {config['epochs']}")
    log.info("=" * 70)

    header = f"{'Epoch':>6} | {'Train Loss':>10} | {'Val Loss':>10} | {'GradNorm':>10} | {'LR':>10}"
    log.info(header)
    log.info("-" * 70)

    for epoch in range(config["epochs"]):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        train_loss = 0.0
        train_batches = 0
        last_grad_norm = 0.0

        epoch_iter = tqdm(train_loader, desc=f"Epoch {epoch+1:3}", leave=False) if HAS_TQDM else train_loader

        for batch_index, (x, y) in enumerate(epoch_iter):
            x = x.to(device)
            y = y.to(device)

            autocast_context = make_autocast_context(use_amp, device)
            with autocast_context:
                logits = model(x)
                batch_size, time_steps, vocab_size = logits.shape
                raw_loss = criterion(
                    logits.reshape(batch_size * time_steps, vocab_size),
                    y.reshape(batch_size * time_steps),
                )
                loss = raw_loss / accumulation_steps

            scaler.scale(loss).backward()

            should_step = (
                (batch_index + 1) % accumulation_steps == 0
                or (batch_index + 1) == len(train_loader)
            )
            if should_step:
                scaler.unscale_(optimizer)
                grad_norm = torch.nn.utils.clip_grad_norm_(
                    model.parameters(), config["max_grad_norm"]
                )
                last_grad_norm = float(grad_norm)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
                scheduler.step()

            train_loss += raw_loss.item()
            train_batches += 1

        avg_train = train_loss / train_batches

        model.eval()
        val_loss = 0.0
        val_batches = 0
        with torch.no_grad():
            for x, y in val_loader:
                x = x.to(device)
                y = y.to(device)
                autocast_context = make_autocast_context(use_amp, device)
                with autocast_context:
                    logits = model(x)
                    batch_size, time_steps, vocab_size = logits.shape
                    loss = criterion(
                        logits.reshape(batch_size * time_steps, vocab_size),
                        y.reshape(batch_size * time_steps),
                    )
                val_loss += loss.item()
                val_batches += 1

        avg_val = val_loss / val_batches
        lr_now = optimizer.param_groups[0]["lr"]

        log.info(
            f"{epoch + 1:6d} | {avg_train:10.4f} | {avg_val:10.4f} | "
            f"{last_grad_norm:10.4f} | {lr_now:10.6f}"
        )

        if avg_val < best_val_loss:
            best_val_loss = avg_val
            best_weights = copy.deepcopy(model.state_dict())
            wait = 0
        else:
            wait += 1
            if wait >= config["patience"]:
                log.info(f"Fine-tuning early stop at epoch {epoch + 1}")
                break

    if best_weights is not None:
        model.load_state_dict(best_weights)
        log.info(f"Best fine-tuned model loaded (val loss: {best_val_loss:.4f})")

    return model


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Setup basic logging config if run standalone
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ]
    )

    tokenizer = load_tokenizer()
    model = load_base_model()

    # Apply LoRA parameter-efficient fine-tuning
    from susagpt.src.model import inject_lora, merge_and_unload_lora
    inject_lora(model, r=8, alpha=16, dropout=0.05)
    
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    all_params = sum(p.numel() for p in model.parameters())
    log.info(f"Trainable params: {trainable_params:,} || All params: {all_params:,} ({100 * trainable_params / all_params:.4f}%)")

    log.info(f"Loading QA dataset from: {QA_DATA_PATH}")
    with open(QA_DATA_PATH, "r", encoding="utf-8") as file:
        qa_pairs = json.load(file)

    split_idx = int(len(qa_pairs) * FINE_TUNE_CONFIG["train_split"])
    train_pairs = qa_pairs[:split_idx]
    val_pairs = qa_pairs[split_idx:]

    seq_len = model.max_len
    train_dataset = QADataset(train_pairs, tokenizer, seq_len)
    val_dataset = QADataset(val_pairs, tokenizer, seq_len)

    train_loader = DataLoader(
        train_dataset,
        batch_size=FINE_TUNE_CONFIG["batch_size"],
        shuffle=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=FINE_TUNE_CONFIG["batch_size"],
        shuffle=False,
    )

    pad_id = tokenizer.pad_token_id
    model = fine_tune_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        config=FINE_TUNE_CONFIG,
        pad_id=pad_id,
        device=device,
    )
    # Merge LoRA weights back for a standard inference model
    merge_and_unload_lora(model)
    save_finetuned_model(model, tokenizer)


if __name__ == "__main__":
    main()
