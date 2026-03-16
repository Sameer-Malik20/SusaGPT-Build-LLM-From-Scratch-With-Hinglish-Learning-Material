import copy
import math
import re
from contextlib import nullcontext

import torch
import torch.nn as nn
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader, Dataset

from config import (
    BASE_MODEL_PATH,
    DATA_PATH,
    MODEL_CONFIG,
    TOKENIZER_CONFIG,
    TOKENIZER_PATH,
    TRAIN_CONFIG,
)
from model import SusaGPT
from tokenizer import Tokenizer


# train.py ka kaam base language model ko stable tarike se train karna hai.
# Yahan 2 extra important ideas bhi add hain:
# 1. curriculum learning
# 2. BPE tokenizer support


class TextDataset(Dataset):
    def __init__(self, tokens, seq_len=32):
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


def split_into_curriculum_chunks(text):
    # Curriculum learning ka idea:
    # model ko pehle easy samples dikhaye jayein, phir gradually harder.
    # Easy chunks = short, clean, less punctuation, less multilingual complexity.
    raw_chunks = [chunk.strip() for chunk in re.split(r"\n+", text) if chunk.strip()]
    if not raw_chunks:
        return [text]
    return raw_chunks


def chunk_difficulty_score(chunk):
    # Difficulty ko perfect measure karna possible nahi hota,
    # lekin simple heuristic kaafi useful ho sakti hai.
    #
    # Factors:
    # 1. length zyada -> harder
    # 2. punctuation zyada -> harder
    # 3. non-ascii chars zyada -> multilingual complexity zyada
    punctuation_count = sum(1 for char in chunk if not char.isalnum() and not char.isspace())
    non_ascii_count = sum(1 for char in chunk if ord(char) > 127)
    return (
        len(chunk.split()) * 1.0
        + punctuation_count * 0.5
        + non_ascii_count * 0.25
    )


def build_curriculum_text(text):
    chunks = split_into_curriculum_chunks(text)
    sorted_chunks = sorted(chunks, key=chunk_difficulty_score)

    # Easy -> hard order me concatenate kar rahe hain.
    # Isse initial training simpler patterns par hoti hai.
    curriculum_text = "\n".join(sorted_chunks)
    return curriculum_text, sorted_chunks


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


def train_model(model, train_loader, val_loader, config, device="cpu"):
    model = model.to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config["learning_rate"],
        weight_decay=config["weight_decay"],
    )
    criterion = nn.CrossEntropyLoss(ignore_index=0)

    accumulation_steps = max(1, config["gradient_accumulation_steps"])
    optimizer_steps_per_epoch = math.ceil(len(train_loader) / accumulation_steps)
    total_steps = config["epochs"] * optimizer_steps_per_epoch
    scheduler = build_scheduler(
        optimizer=optimizer,
        total_steps=total_steps,
        warmup_ratio=config["warmup_ratio"],
    )

    use_amp = bool(config["mixed_precision"]) and device == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    best_val_loss = float("inf")
    best_weights = None
    wait = 0

    print("\nBase training shuru!")
    print(f"Train samples : {len(train_loader.dataset)}")
    print(f"Val samples   : {len(val_loader.dataset)}")
    print(f"Accumulation  : {accumulation_steps} mini-batches")
    print(f"MixedPrecision: {use_amp}")
    print("-" * 92)
    print(
        f"{'Epoch':>6} | {'Train Loss':>10} | {'Val Loss':>10} | "
        f"{'GradNorm':>10} | {'LR':>10} | Status"
    )
    print("-" * 92)

    for epoch in range(config["epochs"]):
        model.train()
        optimizer.zero_grad(set_to_none=True)

        train_loss = 0.0
        train_batches = 0
        last_grad_norm = 0.0

        for batch_index, (x, y) in enumerate(train_loader):
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

        gap = avg_val - avg_train
        if gap > 1.5:
            status = "ratta ho raha hai"
        elif gap > 0.8:
            status = "thoda overfit"
        else:
            status = "stable learning"

        print(
            f"{epoch + 1:6d} | {avg_train:10.4f} | {avg_val:10.4f} | "
            f"{last_grad_norm:10.4f} | {lr_now:10.6f} | {status}"
        )

        if avg_val < best_val_loss:
            best_val_loss = avg_val
            best_weights = copy.deepcopy(model.state_dict())
            wait = 0
        else:
            wait += 1
            if wait >= config["patience"]:
                print(f"\nEarly stopping at epoch {epoch + 1}")
                print(f"Best val loss : {best_val_loss:.4f}")
                break

    print("-" * 92)
    print("Base training complete!")

    if best_weights is not None:
        model.load_state_dict(best_weights)
        print(f"Best model wapas load kiya (val loss: {best_val_loss:.4f})")

    return model


def save_model(model, tokenizer, path=BASE_MODEL_PATH):
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
    print(f"\nBase model saved -> {path}")


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print("Data padh raha hun...")
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        original_text = file.read()

    curriculum_text, sorted_chunks = build_curriculum_text(original_text)
    print(f"Curriculum chunks : {len(sorted_chunks)}")
    print("Easy to hard ordering applied")

    tokenizer = Tokenizer(target_vocab_size=TOKENIZER_CONFIG["target_vocab_size"])
    tokenizer.build_vocab(original_text)
    tokenizer.save(str(TOKENIZER_PATH))

    tokens = tokenizer.encode(curriculum_text)
    print(f"Total BPE tokens : {len(tokens)}")

    split_idx = int(len(tokens) * TRAIN_CONFIG["train_split"])
    train_tokens = tokens[:split_idx]
    val_tokens = tokens[split_idx:]

    seq_len = MODEL_CONFIG["max_len"]
    train_dataset = TextDataset(train_tokens, seq_len=seq_len)
    val_dataset = TextDataset(val_tokens, seq_len=seq_len)

    train_loader = DataLoader(
        train_dataset,
        batch_size=TRAIN_CONFIG["batch_size"],
        shuffle=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=TRAIN_CONFIG["batch_size"],
        shuffle=False,
    )

    model = SusaGPT(
        vocab_size=tokenizer.vocab_size,
        embed_dim=MODEL_CONFIG["embed_dim"],
        num_heads=MODEL_CONFIG["num_heads"],
        num_kv_heads=MODEL_CONFIG["num_kv_heads"],
        num_layers=MODEL_CONFIG["num_layers"],
        max_len=MODEL_CONFIG["max_len"],
        dropout=MODEL_CONFIG["dropout"],
    )

    total_params = sum(param.numel() for param in model.parameters())
    print(f"Model parameters: {total_params:,}")
    print(f"Using device    : {device}")

    trained_model = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        config=TRAIN_CONFIG,
        device=device,
    )
    save_model(trained_model, tokenizer)
