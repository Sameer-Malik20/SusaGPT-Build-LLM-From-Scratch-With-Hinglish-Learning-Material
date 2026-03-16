"""
╔══════════════════════════════════════════════════════════╗
║   📝  SAMPLING & GENERATION — Top-K, Top-P, KV Cache    ║
║   Docs: docs/susagpt/SusaGPT_Diagram_Guide.md            ║
╚══════════════════════════════════════════════════════════╝

Run: python sampling_demo.py
Requires: torch  (pip install torch)
"""

import os
import math
import time
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_torch():
    try:
        import torch
        return torch
    except ImportError:
        print("\n⚠️  PyTorch nahi mila! pip install torch")
        return None


# ─────────────────────────────────────────────────────────
# DEMO 1: Sampling Strategies Side-by-Side
# ─────────────────────────────────────────────────────────
def demo_sampling_strategies(torch):
    clear()
    print("=" * 60)
    print("  🎲  DEMO 1: Sampling Strategies — Live Comparison")
    print("=" * 60)

    import torch.nn.functional as F

    # Simulated vocabulary
    vocab = ["AI", "machine", "learning", "robot", "computer",
             "neural", "network", "data", "model", "training",
             "deep", "code", "python", "the", "is"]

    vocab_size = len(vocab)

    print(f"\n  Vocabulary ({vocab_size} tokens): {vocab}")
    print(f"\n  Model logits (scores) simulate kar rahe hain...")

    torch.manual_seed(42)
    logits = torch.tensor([2.5, 1.5, 2.0, 0.5, 1.0,
                           1.8, 1.2, 0.8, 1.7, 0.3,
                           1.1, 0.6, 0.9, 0.2, 0.4])

    probs = F.softmax(logits, dim=-1)

    print(f"\n  Token Probabilities:")
    sorted_pairs = sorted(enumerate(probs.tolist()), key=lambda x: -x[1])
    for idx, prob in sorted_pairs[:8]:
        bar = "█" * int(prob * 40)
        print(f"    '{vocab[idx]}':{prob:.3f} {bar}")
    print(f"    ... {vocab_size - 8} more tokens")

    print(f"\n  {'─'*55}")
    print(f"  🔬 Sampling kar rahe hain (5 runs each):\n")

    # 1. Greedy
    greedy = vocab[torch.argmax(logits).item()]

    # 2. Top-K
    def top_k(k):
        top_vals, top_idx = torch.topk(logits, k)
        top_probs = F.softmax(top_vals, dim=-1)
        chosen = torch.multinomial(top_probs, 1).item()
        return vocab[top_idx[chosen].item()]

    # 3. Top-P
    def top_p(p):
        sorted_probs, sorted_idx = torch.sort(F.softmax(logits, dim=-1), descending=True)
        cumsum = torch.cumsum(sorted_probs, dim=-1)
        mask = (cumsum - sorted_probs) < p
        filtered = sorted_probs * mask.float()
        if filtered.sum() == 0:
            filtered = sorted_probs
        chosen = torch.multinomial(filtered, 1).item()
        return vocab[sorted_idx[chosen].item()]

    print(f"  {'Method':<15} {'Runs (5 samples)':>45}")
    print("  " + "-" * 62)

    # Greedy — always same
    greedy_results = [greedy] * 5
    print(f"  Greedy:         {' | '.join(f'{r:>8}' for r in greedy_results)}")

    # Top-K = 3
    torch.manual_seed(None)
    k3_results = [top_k(3) for _ in range(5)]
    print(f"  Top-K (k=3):    {' | '.join(f'{r:>8}' for r in k3_results)}")

    # Top-K = 8
    k8_results = [top_k(8) for _ in range(5)]
    print(f"  Top-K (k=8):    {' | '.join(f'{r:>8}' for r in k8_results)}")

    # Top-P = 0.7
    p7_results = [top_p(0.7) for _ in range(5)]
    print(f"  Top-P (p=0.7):  {' | '.join(f'{r:>8}' for r in p7_results)}")

    # Top-P = 0.95
    p95_results = [top_p(0.95) for _ in range(5)]
    print(f"  Top-P (p=0.95): {' | '.join(f'{r:>8}' for r in p95_results)}")

    print(f"\n  💡 Greedy: hamesha same → deterministic (math/code ke liye)")
    print(f"  💡 Top-K (small k): thoda random → focused creativity")
    print(f"  💡 Top-K (large k): zyada random → diverse output")
    print(f"  💡 Top-P (high p): zyada tokens allowed → diverse")


# ─────────────────────────────────────────────────────────
# DEMO 2: Interactive Sampling
# ─────────────────────────────────────────────────────────
def demo_interactive_sampling(torch):
    clear()
    print("=" * 60)
    print("  🎮  DEMO 2: Apna Sampling Try Karo!")
    print("=" * 60)

    import torch.nn.functional as F

    vocab = ["AI", "machine", "learning", "robot", "computer",
             "neural", "network", "data", "model", "training",
             "deep", "code", "python", "the", "is", "good", "bad",
             "fast", "slow", "smart"]

    torch.manual_seed(42)
    logits = torch.randn(len(vocab))

    probs = F.softmax(logits, dim=-1)
    sorted_pairs = sorted(zip(vocab, probs.tolist()), key=lambda x: -x[1])

    print(f"\n  Top 10 tokens by probability:")
    for name, prob in sorted_pairs[:10]:
        bar = "█" * int(prob * 50)
        print(f"    '{name}': {prob:.3f} {bar}")

    print(f"\n  Methods:")
    print(f"    1. Top-K sampling")
    print(f"    2. Top-P (nucleus) sampling")
    print(f"    3. Temperature scaling")

    method = input("\n  Method choose karo (1/2/3, Enter=1): ").strip() or "1"

    if method == "1":
        try:
            k = int(input("  K value? (Enter = 5): ").strip() or "5")
        except ValueError:
            k = 5
        top_vals, top_idx = torch.topk(logits, k)
        print(f"\n  Top-{k} tokens: {[vocab[i] for i in top_idx.tolist()]}")
        top_probs = F.softmax(top_vals, dim=-1)
        print(f"\n  5 samples:")
        for _ in range(5):
            chosen = torch.multinomial(top_probs, 1).item()
            print(f"    → '{vocab[top_idx[chosen].item()]}'")

    elif method == "2":
        try:
            p = float(input("  P value (0-1)? (Enter = 0.9): ").strip() or "0.9")
        except ValueError:
            p = 0.9
        sorted_probs, sorted_idx = torch.sort(probs, descending=True)
        cumsum = torch.cumsum(sorted_probs, dim=-1)
        mask = (cumsum - sorted_probs) < p
        n_included = mask.sum().item()
        print(f"\n  P={p} → Top {n_included} tokens included")
        filtered = sorted_probs * mask.float()
        print(f"\n  5 samples:")
        for _ in range(5):
            chosen = torch.multinomial(filtered, 1).item()
            print(f"    → '{vocab[sorted_idx[chosen].item()]}'")

    elif method == "3":
        try:
            temp = float(input("  Temperature (0.1=focused, 2.0=creative)? (Enter = 1.0): ").strip() or "1.0")
        except ValueError:
            temp = 1.0
        scaled_logits = logits / temp
        scaled_probs = F.softmax(scaled_logits, dim=-1)
        print(f"\n  Temperature={temp}")
        print(f"  5 samples:")
        for _ in range(5):
            chosen = torch.multinomial(scaled_probs, 1).item()
            print(f"    → '{vocab[chosen]}'")
        print(f"\n  Low temp → deterministic | High temp → random")


# ─────────────────────────────────────────────────────────
# DEMO 3: KV Cache Speed Comparison
# ─────────────────────────────────────────────────────────
def demo_kv_cache():
    clear()
    print("=" * 60)
    print("  🔑  DEMO 3: KV Cache — Speed Calculator")
    print("=" * 60)

    print(f"\n  KV Cache generation ko fast karta hai.")
    print(f"  Purane tokens ke K,V recompute nahi karne padte.\n")

    def compute_without_cache(n_tokens):
        """Total flops = sum 1 to n = triangular number"""
        return n_tokens * (n_tokens + 1) // 2

    def compute_with_cache(n_tokens):
        """Each step = 1 new token computation"""
        return n_tokens

    print(f"  {'Tokens':<10} {'Without Cache':<18} {'With Cache':<15} {'Speedup':<10}")
    print("  " + "-" * 58)

    token_counts = [10, 25, 50, 100, 200, 500]
    for n in token_counts:
        wo = compute_without_cache(n)
        wi = compute_with_cache(n)
        speedup = wo / wi
        speedup_bar = "█" * min(25, int(speedup / 5))
        print(f"  {n:<10} {wo:<18} {wi:<15} {speedup:.0f}x {speedup_bar}")

    print(f"\n  💡 Without cache: Token 100 ke liye 1+2+3...+100 = 5050 steps!")
    print(f"  💡 With cache:    Token 100 ke liye sirf 1 step!")

    # Simulate generation speed
    print(f"\n  🎬  Generation Speed Simulation (200 tokens):")
    n = 200
    print(f"\n  Token ", end="", flush=True)

    t_start = time.time()
    for i in range(1, min(n + 1, 51)):
        print(f"{i}", end=" ", flush=True)
        time.sleep(0.02)  # Fast (with cache)
    t_fast = time.time() - t_start

    print(f"\n  ✅ With KV Cache: {t_fast:.2f}s (simulated fast)")
    print(f"  🐢 Without Cache: ~{t_fast * (n/2):.1f}s (would take much longer)")


# ─────────────────────────────────────────────────────────
# DEMO 4: Repetition Penalty
# ─────────────────────────────────────────────────────────
def demo_repetition_penalty(torch):
    clear()
    print("=" * 60)
    print("  🔁  DEMO 4: Repetition Penalty")
    print("=" * 60)

    import torch.nn.functional as F

    vocab = ["the", "cat", "sat", "on", "mat", "and", "was", "happy", "very", "quite"]
    logits = torch.tensor([2.0, 1.8, 1.5, 1.2, 1.0, 1.7, 1.3, 0.9, 0.7, 0.5])

    print(f"\n  Vocabulary: {vocab}")
    print(f"\n  BINA Repetition Penalty:")
    probs_before = F.softmax(logits, dim=-1)
    for name, prob in sorted(zip(vocab, probs_before.tolist()), key=lambda x: -x[1])[:5]:
        bar = "█" * int(prob * 40)
        print(f"    '{name}': {prob:.3f} {bar}")

    # Now apply penalty for already-used tokens
    already_used = [0, 1]  # 'the' and 'cat' already appeared
    penalty = float(input(f"\n  Penalty value? (Enter = 1.5): ").strip() or "1.5")

    penalized_logits = logits.clone()
    for idx in already_used:
        if penalized_logits[idx] > 0:
            penalized_logits[idx] /= penalty
        else:
            penalized_logits[idx] *= penalty

    print(f"\n  Already used: {[vocab[i] for i in already_used]}")
    print(f"\n  PENALTY={penalty} lagane ke BAAD:")
    probs_after = F.softmax(penalized_logits, dim=-1)
    for name, prob in sorted(zip(vocab, probs_after.tolist()), key=lambda x: -x[1])[:5]:
        bar = "█" * int(prob * 40)
        marker = " ← penalized!" if name in [vocab[i] for i in already_used] else ""
        print(f"    '{name}': {prob:.3f} {bar}{marker}")

    print(f"\n  ✅ 'the' aur 'cat' ki probability kam ho gayi!")
    print(f"  ✅ Ab model naye tokens prefer karega!")


# ─────────────────────────────────────────────────────────
# EXERCISE + TEST
# ─────────────────────────────────────────────────────────
def exercise():
    clear()
    print("=" * 60)
    print("  ✏️   EXERCISE: Sampling & Generation Test")
    print("=" * 60)

    questions = [
        {
            "q": "Q1: Math problem solve karne ke liye kaunsa sampling best hai?",
            "options": ["A) Top-P (high p=0.99)", "B) Top-K (k=1) ya Greedy",
                        "C) Random sampling", "D) Temperature=2.0"],
            "answer": "B",
            "exp": "Math = deterministic! Greedy ya k=1 → same correct answer, no randomness."
        },
        {
            "q": "Q2: KV Cache kya store karta hai?",
            "options": ["A) Generated tokens ka text",
                        "B) Previous tokens ke Key aur Value tensors",
                        "C) Loss values",
                        "D) Model weights"],
            "answer": "B",
            "exp": "KV Cache K,V tensors save karta hai — next token me recompute nahi karna padta!"
        },
        {
            "q": "Q3: Top-P=0.9 ka matlab?",
            "options": ["A) Sirf top 9 tokens use karo",
                        "B) 90% probability tak ke tokens include karo, baaki remove karo",
                        "C) 90% chance se same token choose karo",
                        "D) Temperature = 0.9 set karo"],
            "answer": "B",
            "exp": "Nucleus sampling: cumulative probability 0.9 tak ke tokens rakh, baaki ignore karo."
        },
        {
            "q": "Q4: Repetition penalty kab use karte hain?",
            "options": ["A) Model training me",
                        "B) Jab model same words baar-baar repeat kare",
                        "C) Vocabulary size badhane ke liye",
                        "D) KV cache clear karne ke liye"],
            "answer": "B",
            "exp": "Repetition penalty already-used tokens ke logits ko reduce karta hai — variety badhti hai!"
        },
    ]

    score = 0
    for q in questions:
        print(f"\n{'─'*55}")
        print(f"\n  {q['q']}")
        for opt in q["options"]:
            print(f"    {opt}")
        ans = input(f"\n  Answer (A/B/C/D): ").strip().upper()

        if ans == q["answer"]:
            print(f"  ✅ SAHI! 🎉")
            score += 1
        else:
            print(f"  ❌ Galat! Sahi: {q['answer']}")
        print(f"  💡 {q['exp']}")

    total = len(questions)
    print(f"\n{'='*55}")
    print(f"  📊 Score: {score}/{total}  {'⭐'*score}{'☆'*(total-score)}")
    if score == total:
        print("  🏆 PERFECT! Sampling concepts clear hai!")
    else:
        print("  📖 Demos phir se chalao!")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
def main():
    torch = check_torch()

    while True:
        clear()
        print("=" * 60)
        print("  📝  SAMPLING & GENERATION DEMO")
        print("  📄  Ref: docs/susagpt/SusaGPT_Diagram_Guide.md")
        print("=" * 60)
        print()
        print("    1. 🎲   Sampling Strategies Side-by-Side (Greedy/Top-K/Top-P)")
        print("    2. 🎮   Interactive Sampling — Apna Try Karo!")
        print("    3. 🔑   KV Cache Speed Calculator")
        print("    4. 🔁   Repetition Penalty Demo")
        print("    5. ✏️   Sampling MCQ Test (score dekho!)")
        print()
        print("    0. 🔙  Back / Exit")
        print()

        choice = input("  Choice (0-5): ").strip()

        if choice == "3":
            demo_kv_cache()
            input("\n↩️  Enter dabao...")
        elif choice == "5":
            exercise()
            input("\n↩️  Enter dabao...")
        elif torch and choice == "1":
            demo_sampling_strategies(torch)
            input("\n↩️  Enter dabao...")
        elif torch and choice == "2":
            demo_interactive_sampling(torch)
            input("\n↩️  Enter dabao...")
        elif torch and choice == "4":
            demo_repetition_penalty(torch)
            input("\n↩️  Enter dabao...")
        elif choice == "0":
            break
        elif choice in ["1", "2", "4"] and not torch:
            print("\n⚠️  PyTorch required! pip install torch")
            input("Enter dabao...")
        else:
            print("❌ Invalid!")
            input("Enter dabao...")


if __name__ == "__main__":
    main()
