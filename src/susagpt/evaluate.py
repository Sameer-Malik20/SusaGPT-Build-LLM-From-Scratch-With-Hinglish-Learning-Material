import argparse
import json
import math
from collections import Counter
from pathlib import Path

import torch
import torch.nn.functional as F

from .config import DATA_PATH, QA_DATA_PATH, TRAIN_CONFIG
from .generate import generate as generate_text
from .generate import load_everything


# evaluate.py ka kaam model ko sirf "chal raha hai ya nahi" level par nahi,
# balki numbers ke through judge karna hai.
#
# Yahan 2 evaluation metrics add hain:
# 1. Perplexity
#    Ye batata hai next token predict karne me model kitna confident / confused hai.
# 2. BLEU score
#    Ye batata hai generated answer reference answer se kitna overlap karta hai.


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="SusaGPT evaluation metrics: BLEU score aur perplexity.",
    )
    parser.add_argument(
        "--metric",
        choices=["both", "bleu", "perplexity"],
        default="both",
        help="Kaunsa metric run karna hai.",
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "cuda"],
        default="auto",
        help="Evaluation kis device par chalani hai.",
    )
    parser.add_argument(
        "--prefer-quantized",
        action="store_true",
        help="Agar quantized model available ho to usse load karo.",
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="Agar specific checkpoint evaluate karna ho to uska path do.",
    )
    parser.add_argument(
        "--qa-limit",
        type=int,
        default=10,
        help="BLEU evaluation me kitne Q&A pairs use karne hain. 0 ka matlab sab.",
    )
    parser.add_argument(
        "--show-samples",
        type=int,
        default=3,
        help="Kitne sample predictions print karne hain.",
    )
    parser.add_argument(
        "--eval-split",
        type=float,
        default=1.0 - float(TRAIN_CONFIG["train_split"]),
        help="Perplexity ke liye data.txt ka kitna hissa holdout use karna hai.",
    )
    return parser


def resolve_device(device_name, loaded_model_path):
    # Quantized model normally CPU inference ke liye best hota hai.
    # Isliye agar int8 checkpoint load hua ho to safe side par CPU force kar dete hain.
    if "int8" in loaded_model_path.stem.lower():
        return "cpu"

    if device_name == "cuda":
        return "cuda"

    if device_name == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"

    return "cpu"


def load_text_file(path):
    return path.read_text(encoding="utf-8")


def normalize_for_bleu(text):
    # BLEU me hum usually text ko basic normalized form me compare karte hain.
    # Yahan lowercase + extra spaces cleanup enough hai.
    return " ".join(text.strip().lower().split())


def split_eval_tokens(tokens, eval_split):
    if len(tokens) < 2:
        raise ValueError("Perplexity ke liye data bahut chhota hai.")

    eval_split = min(max(eval_split, 0.05), 0.5)
    split_index = int(len(tokens) * (1.0 - eval_split))
    split_index = min(max(split_index, 1), len(tokens) - 1)
    return tokens[split_index:]


def iter_eval_windows(tokens, seq_len):
    # Language model ko fixed-size windows me evaluate karte hain.
    # Har window me input x aur uska next-token target y banta hai.
    for start in range(0, len(tokens) - 1, seq_len):
        window = tokens[start : start + seq_len + 1]
        if len(window) < 2:
            continue
        yield window[:-1], window[1:]


def calculate_perplexity(model, eval_tokens, device):
    # Perplexity ka base formula roughly exp(average negative log likelihood) hota hai.
    # Lower perplexity ka matlab model next token ko better predict kar raha hai.
    model.eval()
    total_negative_log_likelihood = 0.0
    total_target_tokens = 0

    with torch.no_grad():
        for x_tokens, y_tokens in iter_eval_windows(eval_tokens, model.max_len):
            x = torch.tensor([x_tokens], dtype=torch.long, device=device)
            y = torch.tensor([y_tokens], dtype=torch.long, device=device)

            logits = model(x)
            batch_size, time_steps, vocab_size = logits.shape
            loss = F.cross_entropy(
                logits.reshape(batch_size * time_steps, vocab_size),
                y.reshape(batch_size * time_steps),
                reduction="sum",
            )

            total_negative_log_likelihood += float(loss.item())
            total_target_tokens += int(y.numel())

    if total_target_tokens == 0:
        raise ValueError("Perplexity calculate karne ke liye valid eval tokens nahi mile.")

    average_nll = total_negative_log_likelihood / total_target_tokens
    return math.exp(average_nll)


def get_ngram_counts(tokens, ngram_order):
    if len(tokens) < ngram_order:
        return Counter()

    return Counter(
        tuple(tokens[index : index + ngram_order])
        for index in range(len(tokens) - ngram_order + 1)
    )


def calculate_corpus_bleu(references, candidates, max_order=4):
    # BLEU exact meaning match nahi batata.
    # Ye bas n-gram overlap measure karta hai, isliye ise ek helpful signal samjho.
    matches_by_order = [0] * max_order
    possible_matches_by_order = [0] * max_order
    reference_length = 0
    candidate_length = 0

    for reference_tokens, candidate_tokens in zip(references, candidates):
        reference_length += len(reference_tokens)
        candidate_length += len(candidate_tokens)

        for ngram_order in range(1, max_order + 1):
            reference_counts = get_ngram_counts(reference_tokens, ngram_order)
            candidate_counts = get_ngram_counts(candidate_tokens, ngram_order)

            overlap_count = sum(
                min(count, reference_counts[ngram])
                for ngram, count in candidate_counts.items()
            )

            matches_by_order[ngram_order - 1] += overlap_count
            possible_matches_by_order[ngram_order - 1] += max(
                len(candidate_tokens) - ngram_order + 1,
                0,
            )

    smoothed_precisions = []
    valid_precisions = []
    for matches, possible in zip(matches_by_order, possible_matches_by_order):
        if possible == 0:
            smoothed_precisions.append(0.0)
            continue

        # Add-one smoothing short outputs ke case me BLEU ko zero hone se bachati hai.
        precision = (matches + 1.0) / (possible + 1.0)
        smoothed_precisions.append(precision)
        valid_precisions.append(precision)

    if not valid_precisions:
        geo_mean = 0.0
    else:
        geo_mean = math.exp(
            sum(math.log(precision) for precision in valid_precisions)
            / len(valid_precisions)
        )

    if candidate_length == 0:
        brevity_penalty = 0.0
    elif candidate_length > reference_length:
        brevity_penalty = 1.0
    else:
        brevity_penalty = math.exp(1.0 - (reference_length / candidate_length))

    bleu_score = brevity_penalty * geo_mean
    return {
        "bleu": bleu_score,
        "brevity_penalty": brevity_penalty,
        "precisions": smoothed_precisions,
        "reference_length": reference_length,
        "candidate_length": candidate_length,
    }


def extract_answer_only(full_text, prompt):
    # Generation function full prompt + continuation return karti hai.
    # BLEU ke liye hume sirf answer wala part compare karna hai.
    normalized_full = full_text.strip()
    normalized_prompt = prompt.strip()

    if normalized_full.lower().startswith(normalized_prompt.lower()):
        return normalized_full[len(normalized_prompt) :].strip()

    marker = " answer "
    marker_index = normalized_full.lower().rfind(marker)
    if marker_index != -1:
        return normalized_full[marker_index + len(marker) :].strip()

    return normalized_full


def load_qa_pairs(limit):
    qa_pairs = json.loads(QA_DATA_PATH.read_text(encoding="utf-8"))
    if limit > 0:
        return qa_pairs[:limit]
    return qa_pairs


def calculate_bleu_on_qa(model, tokenizer, qa_pairs):
    references = []
    candidates = []
    sample_rows = []

    for pair in qa_pairs:
        prompt = f"question {pair['question']} answer "
        reference_answer = normalize_for_bleu(pair["answer"])
        reference_tokens = reference_answer.split()

        # BLEU ke liye deterministic decoding helpful hoti hai,
        # isliye yahan beam search use kar rahe hain.
        generated_text = generate_text(
            model=model,
            tokenizer=tokenizer,
            prompt=prompt,
            max_new_tokens=max(12, len(tokenizer.encode(pair["answer"])) + 4),
            temperature=0.7,
            repetition_penalty=1.05,
            use_beam_search=True,
            use_kv_cache=True,
        )
        predicted_answer = normalize_for_bleu(
            extract_answer_only(generated_text, prompt)
        )
        candidate_tokens = predicted_answer.split()

        references.append(reference_tokens)
        candidates.append(candidate_tokens)
        sample_rows.append(
            {
                "question": pair["question"],
                "reference": reference_answer,
                "prediction": predicted_answer,
            }
        )

    return calculate_corpus_bleu(references, candidates), sample_rows


def print_bleu_report(bleu_result, sample_rows, sample_count):
    print("\n" + "=" * 72)
    print("BLEU Evaluation")
    print("=" * 72)
    print(f"Corpus BLEU       : {bleu_result['bleu']:.4f}")
    print(f"Brevity Penalty   : {bleu_result['brevity_penalty']:.4f}")
    print(
        "Modified Precision: "
        f"1-gram={bleu_result['precisions'][0]:.4f}, "
        f"2-gram={bleu_result['precisions'][1]:.4f}, "
        f"3-gram={bleu_result['precisions'][2]:.4f}, "
        f"4-gram={bleu_result['precisions'][3]:.4f}"
    )
    print(
        f"Reference Tokens  : {bleu_result['reference_length']} | "
        f"Candidate Tokens: {bleu_result['candidate_length']}"
    )

    if sample_count <= 0:
        return

    print("\nSample Predictions")
    print("-" * 72)
    for row in sample_rows[:sample_count]:
        print(f"Q   : {row['question']}")
        print(f"Ref : {row['reference']}")
        print(f"Pred: {row['prediction']}\n")


def print_perplexity_report(perplexity, token_count):
    print("\n" + "=" * 72)
    print("Perplexity Evaluation")
    print("=" * 72)
    print(f"Eval Tokens : {token_count}")
    print(f"Perplexity  : {perplexity:.4f}")


def main():
    args = build_argument_parser().parse_args()

    try:
        model, tokenizer, loaded_model_path = load_everything(
            model_path=args.model_path,
            prefer_quantized=args.prefer_quantized,
            return_path=True,
        )
    except RuntimeError as error:
        raise SystemExit(
            "Checkpoint current architecture se match nahi kar raha. "
            "Fresh checkpoint ke liye `python train.py` ya apna compatible "
            "`--model-path` use karo."
        ) from error

    loaded_model_path = Path(loaded_model_path)
    device = resolve_device(args.device, loaded_model_path)

    if device != "cpu":
        model = model.to(device)

    print(f"Loaded model : {loaded_model_path}")
    print(f"Device       : {device}")

    if args.metric in {"both", "perplexity"}:
        raw_text = load_text_file(DATA_PATH)
        all_tokens = tokenizer.encode(raw_text)
        eval_tokens = split_eval_tokens(all_tokens, args.eval_split)
        perplexity = calculate_perplexity(model, eval_tokens, device)
        print_perplexity_report(perplexity, len(eval_tokens))

    if args.metric in {"both", "bleu"}:
        qa_pairs = load_qa_pairs(args.qa_limit)
        bleu_result, sample_rows = calculate_bleu_on_qa(model, tokenizer, qa_pairs)
        print_bleu_report(bleu_result, sample_rows, args.show_samples)


if __name__ == "__main__":
    main()
