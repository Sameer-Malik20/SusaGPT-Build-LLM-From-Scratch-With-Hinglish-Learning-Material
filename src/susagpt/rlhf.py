import json

import torch
import torch.nn.functional as F

from .config import (
    BASE_MODEL_PATH,
    FINETUNED_MODEL_PATH,
    PREFERENCE_DATA_PATH,
    RLHF_CONFIG,
    RLHF_MODEL_PATH,
    TOKENIZER_PATH,
)
from .model import SusaGPT
from .tokenizer import Tokenizer


# Important honesty note:
# Ye file full industrial PPO-based RLHF nahi hai.
# Ye ek simplified RLHF-style preference tuning stage hai,
# jahan hum chosen vs rejected answers ke basis par model behavior ko nudge karte hain.
# Learning purpose ke liye ye practical aur samajhne layak version hai.


def load_tokenizer():
    tokenizer = Tokenizer()
    tokenizer.load(str(TOKENIZER_PATH))
    return tokenizer


def load_starting_model():
    # RLHF-style alignment ideally fine-tuned model ke upar chalti hai.
    # Agar fine-tuned file available nahi ho to base model se start karenge.
    model_path = FINETUNED_MODEL_PATH if FINETUNED_MODEL_PATH.exists() else BASE_MODEL_PATH
    checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)

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
    return model, model_path


def average_answer_logprob(model, prompt_ids, answer_ids, device):
    # Yahan hum measure kar rahe hain ke model chosen answer ko rejected answer ke
    # muqable kitna pasand karta hai.
    full_ids = prompt_ids + answer_ids

    # Model ka context limited hota hai, isliye very long sequence ko tail side se crop karte hain.
    if len(full_ids) > model.max_len + 1:
        full_ids = full_ids[-(model.max_len + 1) :]

    input_ids = torch.tensor([full_ids[:-1]], dtype=torch.long, device=device)
    target_ids = torch.tensor(full_ids[1:], dtype=torch.long, device=device)

    logits = model(input_ids)
    log_probs = F.log_softmax(logits, dim=-1)

    # Answer tokens ko hi score karna hai, prompt ko nahi.
    answer_len = min(len(answer_ids), target_ids.size(0))
    answer_positions = torch.arange(
        target_ids.size(0) - answer_len,
        target_ids.size(0),
        device=device,
    )

    selected = log_probs[0, answer_positions, target_ids[answer_positions]]
    return selected.mean()


def save_rlhf_model(model, tokenizer, path=RLHF_MODEL_PATH):
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
    print(f"\nRLHF-style aligned model saved -> {path}")


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = load_tokenizer()
    model, start_path = load_starting_model()
    model = model.to(device)

    with open(PREFERENCE_DATA_PATH, "r", encoding="utf-8") as file:
        preference_pairs = json.load(file)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=RLHF_CONFIG["learning_rate"],
        weight_decay=RLHF_CONFIG["weight_decay"],
    )

    print(f"RLHF-style alignment start from -> {start_path}")
    print(f"Preference pairs               -> {len(preference_pairs)}")
    print(f"Using device                   -> {device}")
    print("-" * 72)
    print(f"{'Epoch':>6} | {'Pref Loss':>10} | {'Chosen-Reward':>14}")
    print("-" * 72)

    for epoch in range(RLHF_CONFIG["epochs"]):
        model.train()
        total_loss = 0.0
        total_reward_gap = 0.0

        for pair in preference_pairs:
            optimizer.zero_grad()

            prompt_ids = tokenizer.encode(pair["prompt"])
            chosen_ids = tokenizer.encode(pair["chosen"])
            rejected_ids = tokenizer.encode(pair["rejected"])

            chosen_score = average_answer_logprob(model, prompt_ids, chosen_ids, device)
            rejected_score = average_answer_logprob(
                model, prompt_ids, rejected_ids, device
            )

            # Pairwise preference loss:
            # model ko chosen answer ko rejected se zyada probability dena sikhate hain.
            reward_gap = chosen_score - rejected_score
            loss = -F.logsigmoid(RLHF_CONFIG["beta"] * reward_gap)
            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                model.parameters(), RLHF_CONFIG["max_grad_norm"]
            )
            optimizer.step()

            total_loss += loss.item()
            total_reward_gap += reward_gap.item()

        avg_loss = total_loss / len(preference_pairs)
        avg_reward_gap = total_reward_gap / len(preference_pairs)
        print(f"{epoch + 1:6d} | {avg_loss:10.4f} | {avg_reward_gap:14.4f}")

    print("-" * 72)
    print("RLHF-style alignment complete!")

    save_rlhf_model(model, tokenizer)


if __name__ == "__main__":
    main()
