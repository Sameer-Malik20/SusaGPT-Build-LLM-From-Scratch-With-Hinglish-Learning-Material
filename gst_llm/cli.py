"""
GST LLM — CLI & Inference Engine
Usage:
  python cli.py --question "What is GST rate for construction?"
  python cli.py --interactive
  python cli.py --benchmark
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Allow running from gst_llm/ root
sys.path.insert(0, str(Path(__file__).parent))

import torch
from src.config import (
    BASE_MODEL_PATH,
    FINETUNED_MODEL_PATH,
    TOKENIZER_PATH,
    GENERATION_CONFIG,
)
from src.model import SusaGPT
from src.tokenizer import Tokenizer


# ─────────────────────────────────────────────────────────────────────────────
# Model Loading
# ─────────────────────────────────────────────────────────────────────────────

def load_model_and_tokenizer(prefer_finetuned=True):
    """Load the best available model (finetuned > base)."""
    model_path = None
    if prefer_finetuned and FINETUNED_MODEL_PATH.exists():
        model_path = FINETUNED_MODEL_PATH
        model_label = "Fine-tuned"
    elif BASE_MODEL_PATH.exists():
        model_path = BASE_MODEL_PATH
        model_label = "Base"
    else:
        print("❌  No trained model found.")
        print("    Run:  cd gst_llm && python train.py")
        sys.exit(1)

    print(f"✅  Loading {model_label} model from: {model_path.name}")
    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)

    model = SusaGPT(
        vocab_size   = ckpt["vocab_size"],
        embed_dim    = ckpt["embed_dim"],
        num_heads    = ckpt["num_heads"],
        num_kv_heads = ckpt.get("num_kv_heads", ckpt["num_heads"]),
        num_layers   = ckpt["num_layers"],
        max_len      = ckpt.get("max_len", 128),
        dropout      = 0.0,     # no dropout at inference
    )
    model.load_state_dict(ckpt["model_state"])
    model.eval()

    tokenizer = Tokenizer()
    tokenizer.load(str(TOKENIZER_PATH))

    total_params = sum(p.numel() for p in model.parameters())
    size_mb = sum(p.numel() * p.element_size() for p in model.parameters()) / 1024 / 1024
    print(f"   Parameters : {total_params:,}")
    print(f"   Model size : {size_mb:.2f} MB")
    return model, tokenizer


# ─────────────────────────────────────────────────────────────────────────────
# Generation
# ─────────────────────────────────────────────────────────────────────────────

@torch.no_grad()
def generate_answer(model, tokenizer, prompt: str, config=None) -> str:
    if config is None:
        config = GENERATION_CONFIG

    # Format as Q&A prompt
    full_prompt = f"question {prompt} answer"
    ids = tokenizer.encode(full_prompt)

    max_new = config.get("max_new_words", 80)
    temperature = config.get("temperature", 0.7)
    top_k = config.get("top_k", 30)
    top_p = config.get("top_p", 0.9)
    rep_penalty = config.get("repetition_penalty", 1.15)

    input_ids = torch.tensor([ids], dtype=torch.long)
    generated = list(ids)
    kv_cache = None
    use_kv = config.get("use_kv_cache", True)

    for step in range(max_new):
        if use_kv and kv_cache is not None:
            x = torch.tensor([[generated[-1]]], dtype=torch.long)
            start_pos = len(generated) - 1
        else:
            x = torch.tensor([generated], dtype=torch.long)
            start_pos = 0

        out = model(x, kv_cache=kv_cache, use_cache=use_kv, start_pos=start_pos)
        if use_kv:
            logits, kv_cache = out
        else:
            logits = out

        logits = logits[0, -1, :].float()

        # Repetition penalty
        for tok_id in set(generated[-20:]):
            if logits[tok_id] > 0:
                logits[tok_id] /= rep_penalty
            else:
                logits[tok_id] *= rep_penalty

        # Temperature
        logits = logits / max(temperature, 1e-6)

        # Top-K
        if top_k > 0:
            kth = torch.topk(logits, min(top_k, logits.size(-1))).values[-1]
            logits[logits < kth] = float("-inf")

        # Top-P (nucleus)
        probs = torch.softmax(logits, dim=-1)
        sorted_probs, sorted_idx = torch.sort(probs, descending=True)
        cum_probs = torch.cumsum(sorted_probs, dim=0)
        remove_mask = cum_probs - sorted_probs > top_p
        sorted_probs[remove_mask] = 0.0
        sorted_probs /= sorted_probs.sum()

        next_token = sorted_idx[torch.multinomial(sorted_probs, 1)].item()
        generated.append(next_token)

        # Stop at EOS or if we see a repetitive loop
        if next_token == tokenizer.eos_token_id:
            break

    # Decode only the generated part (after the prompt)
    answer_ids = generated[len(ids):]
    answer = tokenizer.decode(answer_ids).strip()
    return answer


# ─────────────────────────────────────────────────────────────────────────────
# Benchmark Questions
# ─────────────────────────────────────────────────────────────────────────────

BENCHMARK_QUESTIONS = [
    # Short / Simple
    {
        "id": 1,
        "type": "Short",
        "question": "What is UTGST?",
        "expected": "UTGST stands for Union Territory Goods and Services Tax, levied on intra-state supply of goods and services in Union Territories under the UTGST Act, 2017 (Act No. 14 of 2017)."
    },
    {
        "id": 2,
        "type": "Short",
        "question": "What is the GST rate for construction services under Heading 9954?",
        "expected": "Construction services under Heading 9954 attract a UTGST rate of 9% as per Notification No. 11/2017-UTGST Rate."
    },
    {
        "id": 3,
        "type": "Short",
        "question": "What is Heading 9961 in GST?",
        "expected": "Heading 9961 covers services in wholesale trade including commission agents, commodity brokers, and auctioneers, attracting a 9% UTGST rate."
    },
    {
        "id": 4,
        "type": "Short",
        "question": "What is the GST rate for restaurant without AC?",
        "expected": "Restaurants without air-conditioning and without a liquor licence attract a UTGST rate of 6% under Heading 9963."
    },
    {
        "id": 5,
        "type": "Short",
        "question": "When was UTGST Act enacted?",
        "expected": "The UTGST Act was enacted in 2017 as Act No. 14 of 2017, effective from 1st July 2017."
    },
    # Long / Complex
    {
        "id": 6,
        "type": "Complex",
        "question": "Explain the GST rate applicable to accommodation services and how the rate changes based on the declared tariff per day.",
        "expected": "Under Heading 9963, accommodation services are taxed based on declared tariff: tariff below Rs.1000/day is nil; Rs.1000 to Rs.2499/day attracts 6% UTGST; Rs.2500 and above per day attracts 9% UTGST. The declared tariff includes all amenities provided in the unit."
    },
    {
        "id": 7,
        "type": "Complex",
        "question": "What is the reverse charge mechanism under UTGST and which services are covered under it?",
        "expected": "Under reverse charge mechanism in UTGST, the recipient of supply (not the supplier) is liable to pay the tax. Services like legal services by advocate, GTA services, and services by government are typically under reverse charge as notified under section 7(3) of the UTGST Act 2017."
    },
    {
        "id": 8,
        "type": "Complex",
        "question": "Describe the UTGST rate changes for construction services between 2017 and 2019 as per the notifications.",
        "expected": "In 2017, construction services under Heading 9954 attracted 9% UTGST. Subsequent notifications in 2018 and 2019 amended and clarified rates for sub-categories like affordable housing projects which were reduced to attract lower rates, while general construction works continued at 9%."
    },
    {
        "id": 9,
        "type": "Complex",
        "question": "What powers does the Central Government have under section 7 and section 8 of the UTGST Act to levy taxes on services?",
        "expected": "Under section 7(1) of the UTGST Act 2017, the Central Government has power to levy UTGST on intra-state supplies. Section 8(1) allows levy on composite and mixed supplies. These powers are exercised with recommendations of the GST Council and read with sections 15 and 16 of the CGST Act 2017."
    },
    {
        "id": 10,
        "type": "Complex",
        "question": "How does GST treat supply of food and beverages in hotels versus standalone restaurants, and what are the applicable UTGST rates?",
        "expected": "Food supply in hotels with room tariff above Rs.7500/day attracts 9% UTGST even for the restaurant within. Standalone restaurants without AC attract 6%, with AC attract 9%. Outdoor catering services also attract 9% UTGST. These are governed under Heading 9963 of the UTGST rate schedule."
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# CLI Modes
# ─────────────────────────────────────────────────────────────────────────────

def mode_single(model, tokenizer, question: str):
    print(f"\n{'─'*60}")
    print(f"Question: {question}")
    print(f"{'─'*60}")
    t0 = time.time()
    answer = generate_answer(model, tokenizer, question)
    elapsed = time.time() - t0
    print(f"Answer  : {answer}")
    print(f"Time    : {elapsed:.2f}s")


def mode_interactive(model, tokenizer):
    print("\n🤖  GST LLM — Interactive Mode  (type 'quit' to exit)")
    print("─" * 60)
    while True:
        try:
            q = input("\nYour question: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q or q.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break
        t0 = time.time()
        ans = generate_answer(model, tokenizer, q)
        print(f"Answer : {ans}")
        print(f"Time   : {time.time()-t0:.2f}s")


def mode_benchmark(model, tokenizer):
    print("\n" + "=" * 70)
    print("GST LLM — Benchmark Evaluation")
    print("=" * 70)

    results = []
    for item in BENCHMARK_QUESTIONS:
        print(f"\n[Q{item['id']}] ({item['type']}) {item['question']}")
        print(f"  Expected : {item['expected'][:120]}...")
        t0 = time.time()
        model_ans = generate_answer(model, tokenizer, item["question"])
        elapsed = time.time() - t0
        print(f"  Model    : {model_ans[:120]}...")
        print(f"  Time     : {elapsed:.2f}s")
        results.append({**item, "model_answer": model_ans, "time_sec": round(elapsed, 2)})

    # Save results
    out_path = Path(__file__).parent / "benchmark_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✅  Results saved → {out_path}")
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="GST Tiny LLM — Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --question "What is UTGST?"
  python cli.py --interactive
  python cli.py --benchmark
  python cli.py --question "GST rate for construction?" --base
        """
    )
    parser.add_argument("--question",     type=str, help="Single question to ask")
    parser.add_argument("--interactive",  action="store_true", help="Interactive chat mode")
    parser.add_argument("--benchmark",    action="store_true", help="Run all 10 benchmark questions")
    parser.add_argument("--base",         action="store_true", help="Force use base model (not finetuned)")
    parser.add_argument("--temperature",  type=float, default=None, help="Sampling temperature (0.1–1.0)")
    parser.add_argument("--max-tokens",   type=int,   default=None, help="Max tokens to generate")
    args = parser.parse_args()

    if not any([args.question, args.interactive, args.benchmark]):
        parser.print_help()
        return

    model, tokenizer = load_model_and_tokenizer(prefer_finetuned=not args.base)

    # Override generation config if CLI args provided
    gen_cfg = dict(GENERATION_CONFIG)
    if args.temperature:
        gen_cfg["temperature"] = args.temperature
    if args.max_tokens:
        gen_cfg["max_new_words"] = args.max_tokens

    # Monkey-patch generate_answer to use updated config
    import functools
    gen_fn = functools.partial(generate_answer, config=gen_cfg)

    if args.question:
        mode_single(model, tokenizer, args.question)
    elif args.interactive:
        mode_interactive(model, tokenizer)
    elif args.benchmark:
        mode_benchmark(model, tokenizer)


if __name__ == "__main__":
    main()
