"""
SusaGPT — CLI & Inference Engine
Usage:
  python susagpt/cli.py --question "What does SusaLabs do?"
  python susagpt/cli.py --interactive
  python susagpt/cli.py --benchmark
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
from susagpt.src.config import (
    BASE_MODEL_PATH,
    FINETUNED_MODEL_PATH,
    RLHF_MODEL_PATH,
    TOKENIZER_PATH,
    GENERATION_CONFIG,
)
from susagpt.src.model import SusaGPT
from susagpt.src.tokenizer import Tokenizer


# ─────────────────────────────────────────────────────────────────────────────
# Model Loading
# ─────────────────────────────────────────────────────────────────────────────

def load_model_and_tokenizer(prefer_rlhf=True, force_base=False):
    """Load the best available model (rlhf > finetuned > base)."""
    model_path = None
    model_label = ""
    if force_base:
        if BASE_MODEL_PATH.exists():
            model_path = BASE_MODEL_PATH
            model_label = "Base"
        else:
            print("❌  No base model found.")
            print("    Run:  python train.py")
            sys.exit(1)
    elif prefer_rlhf and RLHF_MODEL_PATH.exists():
        model_path = RLHF_MODEL_PATH
        model_label = "RLHF Aligned"
    elif FINETUNED_MODEL_PATH.exists():
        model_path = FINETUNED_MODEL_PATH
        model_label = "Fine-tuned"
    elif BASE_MODEL_PATH.exists():
        model_path = BASE_MODEL_PATH
        model_label = "Base"
    else:
        print("❌  No trained model found.")
        print("    Run:  python train.py")
        sys.exit(1)

    print(f"✅  Loading {model_label} model from: {model_path.name}")
    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)

    model = SusaGPT(
        vocab_size   = ckpt["vocab_size"],
        embed_dim    = ckpt["embed_dim"],
        num_heads    = ckpt["num_heads"],
        num_kv_heads = ckpt.get("num_kv_heads", ckpt["num_heads"]),
        num_layers   = ckpt["num_layers"],
        max_len      = ckpt.get("max_len", 64),
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
    from susagpt.src.generate import generate_hybrid
    if config is None:
        config = GENERATION_CONFIG

    return generate_hybrid(
        prompt=prompt,
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=config.get("max_new_words"),
        temperature=config.get("temperature"),
        top_k=config.get("top_k"),
        top_p=config.get("top_p"),
        repetition_penalty=config.get("repetition_penalty"),
        use_kv_cache=config.get("use_kv_cache"),
        sampling_mode=config.get("sampling_mode"),
        mirostat_tau=config.get("mirostat_tau"),
        mirostat_eta=config.get("mirostat_eta"),
    )


@torch.no_grad()
def generate_answer_stream(model, tokenizer, prompt: str, config=None):
    from susagpt.src.generate import generate_hybrid_stream
    if config is None:
        config = GENERATION_CONFIG

    return generate_hybrid_stream(
        prompt=prompt,
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=config.get("max_new_words"),
        temperature=config.get("temperature"),
        top_k=config.get("top_k"),
        top_p=config.get("top_p"),
        repetition_penalty=config.get("repetition_penalty"),
        use_kv_cache=config.get("use_kv_cache"),
        sampling_mode=config.get("sampling_mode"),
        mirostat_tau=config.get("mirostat_tau"),
        mirostat_eta=config.get("mirostat_eta"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Benchmark Questions
# ─────────────────────────────────────────────────────────────────────────────

BENCHMARK_QUESTIONS = [
    {
        "id": 1,
        "type": "Short",
        "question": "what does susalabs do",
        "expected": "susalabs builds custom software development ai solutions crm platforms and healthcare technology systems"
    },
    {
        "id": 2,
        "type": "Short",
        "question": "what kind of company is susalabs",
        "expected": "susalabs is a custom software development company powered by ai"
    },
    {
        "id": 3,
        "type": "Short",
        "question": "what services does susalabs offer",
        "expected": "susalabs offers ai solutions custom software development crm services web apps mobile apps and healthcare platforms"
    },
    {
        "id": 4,
        "type": "Short",
        "question": "does susalabs build crm systems",
        "expected": "yes susalabs builds custom crm systems tailored for business workflows customer management and growth"
    },
    {
        "id": 5,
        "type": "Short",
        "question": "does susalabs work in healthcare",
        "expected": "yes susalabs builds healthcare software ai diagnostics medical data platforms and secure digital solutions"
    },
    {
        "id": 6,
        "type": "Complex",
        "question": "does susalabs build mobile apps",
        "expected": "yes susalabs designs and builds ai powered mobile apps for android ios and enterprise use"
    },
    {
        "id": 7,
        "type": "Complex",
        "question": "does susalabs build web apps",
        "expected": "yes susalabs creates scalable web apps dashboards portals and business platforms"
    },
    {
        "id": 8,
        "type": "Complex",
        "question": "what industries does susalabs serve",
        "expected": "susalabs serves telecom energy finance education retail healthcare and enterprise technology sectors"
    },
    {
        "id": 9,
        "type": "Complex",
        "question": "why is custom software useful",
        "expected": "custom software fits business needs better than one size solutions and supports growth"
    },
    {
        "id": 10,
        "type": "Complex",
        "question": "what is a crm",
        "expected": "crm means customer relationship management and helps teams track leads customers tasks and communication"
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# CLI Modes
# ─────────────────────────────────────────────────────────────────────────────

def stream_print(prefix: str, text: str, delay: float = 0.012):
    import sys
    import time
    sys.stdout.write(prefix)
    sys.stdout.flush()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def mode_single(model, tokenizer, question: str, config=None):
    print(f"\n{'─'*60}")
    print(f"Question: {question}")
    print(f"{'─'*60}")
    t0 = time.time()
    sys.stdout.write("Answer  : ")
    sys.stdout.flush()
    for chunk in generate_answer_stream(model, tokenizer, question, config=config):
        sys.stdout.write(chunk)
        sys.stdout.flush()
    print()
    elapsed = time.time() - t0
    print(f"Time    : {elapsed:.2f}s")


def mode_interactive(model, tokenizer, config=None):
    print("\n🤖  SusaGPT — Interactive Mode  (type 'quit' to exit)")
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
        sys.stdout.write("Answer : ")
        sys.stdout.flush()
        for chunk in generate_answer_stream(model, tokenizer, q, config=config):
            sys.stdout.write(chunk)
            sys.stdout.flush()
        print()
        elapsed = time.time() - t0
        print(f"Time   : {elapsed:.2f}s")


def mode_benchmark(model, tokenizer, config=None):
    print("\n" + "=" * 70)
    print("SusaGPT — Benchmark Evaluation")
    print("=" * 70)

    results = []
    for item in BENCHMARK_QUESTIONS:
        print(f"\n[Q{item['id']}] ({item['type']}) {item['question']}")
        print(f"  Expected : {item['expected'][:120]}...")
        t0 = time.time()
        model_ans = generate_answer(model, tokenizer, item["question"], config=config)
        elapsed = time.time() - t0
        print(f"  Model    : {model_ans[:120]}...")
        print(f"  Time     : {elapsed:.2f}s")
        results.append({**item, "model_answer": model_ans, "time_sec": round(elapsed, 2)})

    # Save results
    out_path = Path(__file__).parent.parent / "benchmark_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✅  Results saved → {out_path}")
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="SusaGPT — Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python susagpt/cli.py --question "What does SusaLabs do?"
  python susagpt/cli.py --interactive
  python susagpt/cli.py --benchmark
        """
    )
    parser.add_argument("--question",     type=str, help="Single question to ask")
    parser.add_argument("--interactive",  action="store_true", help="Interactive chat mode")
    parser.add_argument("--benchmark",    action="store_true", help="Run all 10 benchmark questions")
    parser.add_argument("--base",         action="store_true", help="Force use base model (not finetuned/rlhf)")
    parser.add_argument("--temperature",  type=float, default=None, help="Sampling temperature")
    parser.add_argument("--max-tokens",   type=int,   default=None, help="Max tokens to generate")
    args = parser.parse_args()

    if not any([args.question, args.interactive, args.benchmark]):
        parser.print_help()
        return

    model, tokenizer = load_model_and_tokenizer(prefer_rlhf=not args.base, force_base=args.base)

    # Override generation config if CLI args provided
    gen_cfg = dict(GENERATION_CONFIG)
    if args.temperature:
        gen_cfg["temperature"] = args.temperature
    if args.max_tokens:
        gen_cfg["max_new_words"] = args.max_tokens

    # Generate function with config override
    import functools
    gen_fn = functools.partial(generate_answer, config=gen_cfg)

    if args.question:
        mode_single(model, tokenizer, args.question, config=gen_cfg)
    elif args.interactive:
        mode_interactive(model, tokenizer, config=gen_cfg)
    elif args.benchmark:
        mode_benchmark(model, tokenizer, config=gen_cfg)


if __name__ == "__main__":
    main()
