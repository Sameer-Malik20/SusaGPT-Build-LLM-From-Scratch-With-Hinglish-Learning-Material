"""
╔══════════════════════════════════════════════════════════╗
║    🏗️  ARCHITECTURE — RoPE, SwiGLU, GQA, RMSNorm        ║
║    Docs: docs/susagpt/SusaGPT_Architecture.md            ║
╚══════════════════════════════════════════════════════════╝

Run: python architecture_demo.py
Requires: torch  (pip install torch)
"""

import os
import math

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_torch():
    try:
        import torch
        return torch
    except ImportError:
        print("\n⚠️  PyTorch nahi mila!")
        print("   Install karo: pip install torch")
        return None


# ─────────────────────────────────────────────────────────
# DEMO 1: Attention — Basic Concept
# ─────────────────────────────────────────────────────────
def demo_attention(torch):
    clear()
    print("=" * 60)
    print("  👁️  DEMO 1: Self-Attention — Kaise Kaam Karta Hai")
    print("=" * 60)

    import torch.nn.functional as F

    print("\n📝 Scenario: '**it** was tired' me 'it' kya hai?")
    print("   Attention decide karta hai 'it' kaunse past word ko refer karta hai.\n")

    # Simple 3-token example
    seq_len = 3
    d_model = 4
    torch.manual_seed(42)

    # Token embeddings (simplified)
    tokens = ["cat", "was", "it"]
    embeddings = torch.randn(1, seq_len, d_model)

    # Q, K, V projections
    Wq = torch.randn(d_model, d_model)
    Wk = torch.randn(d_model, d_model)
    Wv = torch.randn(d_model, d_model)

    Q = embeddings @ Wq
    K = embeddings @ Wk
    V = embeddings @ Wv

    # Attention scores
    scores = (Q @ K.transpose(-2, -1)) / math.sqrt(d_model)
    attn_weights = F.softmax(scores, dim=-1)

    print(f"  Tokens: {tokens}")
    print(f"\n  Attention Matrix (rows = query token, cols = key token):")
    print(f"  (Each row shows: query token ne kin tokens par kitna focus kiya)\n")

    # Display matrix
    print(f"  {'':10}", end="")
    for t in tokens:
        print(f"  {t:>8}", end="")
    print()
    print("  " + "-" * 42)

    for i, t_row in enumerate(tokens):
        row_weights = attn_weights[0, i].detach().tolist()
        print(f"  {t_row:10}", end="")
        for w in row_weights:
            bar = "█" * int(w * 12)
            print(f"  {w:.3f}{bar:<4}", end="")
        print()

    print(f"\n  💡 'it' (row 2) zyada focus karta hai jo word zyada relevant laga!")
    print(f"  💡 Ye weights learnable hain — model training me improve karta hai.")

    print(f"\n  Output shape: {(Q @ K.transpose(-2,-1) @ V[..., :1]).shape}")
    print(f"  Context-aware vectors generate hote hain!")


# ─────────────────────────────────────────────────────────
# DEMO 2: GQA vs MHA Memory Comparison
# ─────────────────────────────────────────────────────────
def demo_gqa(torch):
    clear()
    print("=" * 60)
    print("  🔗  DEMO 2: GQA vs MHA — Memory Calculator")
    print("=" * 60)

    print("\n  GQA (Grouped Query Attention) SusaGPT me use hota hai.")
    print("  Ye KV cache memory bachata hai.\n")

    try:
        q_heads = int(input("  Query heads kitne? (Enter = 8): ").strip() or "8")
        kv_heads_mha = q_heads  # Standard MHA
        kv_heads_gqa = max(1, int(input(f"  GQA me KV heads kitne? (Enter = 2): ").strip() or "2"))
        head_dim = int(input("  Head dimension? (Enter = 64): ").strip() or "64")
    except ValueError:
        q_heads, kv_heads_gqa, head_dim = 8, 2, 64

    print(f"\n  📐 Configuration:")
    print(f"     Query heads:   {q_heads}")
    print(f"     MHA KV heads:  {kv_heads_mha} (standard)")
    print(f"     GQA KV heads:  {kv_heads_gqa} (reduced)")
    print(f"     Head dim:      {head_dim}")

    print(f"\n  📊 KV Cache Size per Sequence Length:")
    print(f"\n  {'Seq Len':<12} {'MHA (KB)':<14} {'GQA (KB)':<14} {'Savings':<10}")
    print("  " + "-" * 52)

    for seq_len in [50, 100, 200, 500, 1000]:
        bytes_per_val = 4  # float32
        mha_cache = 2 * seq_len * kv_heads_mha * head_dim * bytes_per_val / 1024
        gqa_cache = 2 * seq_len * kv_heads_gqa * head_dim * bytes_per_val / 1024
        saving_pct = (1 - gqa_cache / mha_cache) * 100

        bar_mha = "█" * int(mha_cache / 50)
        bar_gqa = "█" * int(gqa_cache / 50)

        print(f"  {seq_len:<12} {mha_cache:<8.1f} {bar_mha}")
        print(f"  {'':12} {gqa_cache:<8.1f} {bar_gqa} ← GQA ({saving_pct:.0f}% saved!)")
        print()

    print(f"\n  ✅ GQA = Same quality, much less memory!")


# ─────────────────────────────────────────────────────────
# DEMO 3: SwiGLU vs SimpleFFN
# ─────────────────────────────────────────────────────────
def demo_swiglu(torch):
    clear()
    print("=" * 60)
    print("  ⚡  DEMO 3: SwiGLU vs Simple FFN")
    print("=" * 60)

    import torch.nn as nn
    import torch.nn.functional as F

    class SimpleFFN(nn.Module):
        def __init__(self, dim):
            super().__init__()
            self.fc1 = nn.Linear(dim, dim * 4)
            self.fc2 = nn.Linear(dim * 4, dim)

        def forward(self, x):
            return self.fc2(F.gelu(self.fc1(x)))

    class SwiGLU(nn.Module):
        def __init__(self, dim):
            super().__init__()
            hidden = dim * 4 // 3
            self.w1 = nn.Linear(dim, hidden, bias=False)  # Gate
            self.w2 = nn.Linear(hidden, dim, bias=False)  # Output
            self.w3 = nn.Linear(dim, hidden, bias=False)  # Content

        def forward(self, x):
            gate = F.silu(self.w1(x))   # Swish activation
            content = self.w3(x)
            return self.w2(gate * content)  # Gating!

    dim = 64
    old = SimpleFFN(dim)
    new = SwiGLU(dim)

    old_params = sum(p.numel() for p in old.parameters())
    new_params = sum(p.numel() for p in new.parameters())

    print(f"\n  Dim size: {dim}")
    print(f"\n  📦 Parameters Count:")
    print(f"     SimpleFFN:  {old_params:>8,} params")
    print(f"     SwiGLU:     {new_params:>8,} params")
    print(f"     Difference: {old_params - new_params:>8,} params")

    x = torch.randn(1, 10, dim)

    import time
    runs = 1000

    t0 = time.time()
    for _ in range(runs):
        _ = old(x)
    old_time = (time.time() - t0) * 1000

    t0 = time.time()
    for _ in range(runs):
        _ = new(x)
    new_time = (time.time() - t0) * 1000

    print(f"\n  ⏱️  Speed ({runs} runs):")
    print(f"     SimpleFFN: {old_time:.1f} ms")
    print(f"     SwiGLU:    {new_time:.1f} ms")

    print(f"\n  💡 SwiGLU ka advantage:")
    print(f"     Gate = F.silu(w1(x))  → Swish activation")
    print(f"     Content = w3(x)")
    print(f"     Output = w2(gate * content)  ← Gating controls info flow!")


# ─────────────────────────────────────────────────────────
# DEMO 4: RMSNorm vs LayerNorm
# ─────────────────────────────────────────────────────────
def demo_rmsnorm(torch):
    clear()
    print("=" * 60)
    print("  📏  DEMO 4: RMSNorm vs LayerNorm")
    print("=" * 60)

    import torch.nn as nn

    class LayerNorm(nn.Module):
        def __init__(self, dim, eps=1e-6):
            super().__init__()
            self.weight = nn.Parameter(torch.ones(dim))
            self.bias = nn.Parameter(torch.zeros(dim))
            self.eps = eps

        def forward(self, x):
            mean = x.mean(-1, keepdim=True)
            var = x.var(-1, keepdim=True, unbiased=False)
            return self.weight * (x - mean) / (var + self.eps).sqrt() + self.bias

    class RMSNorm(nn.Module):
        def __init__(self, dim, eps=1e-6):
            super().__init__()
            self.weight = nn.Parameter(torch.ones(dim))
            self.eps = eps

        def forward(self, x):
            rms = x.pow(2).mean(-1, keepdim=True).add(self.eps).sqrt()
            return self.weight * (x / rms)

    dim = 8
    ln = LayerNorm(dim)
    rn = RMSNorm(dim)

    ln_params = sum(p.numel() for p in ln.parameters())
    rn_params = sum(p.numel() for p in rn.parameters())

    print(f"\n  📦 Parameters: LayerNorm={ln_params} (W+B), RMSNorm={rn_params} (W only)")

    print(f"\n  🧪 Ek unstable vector ko normalize karo:")
    unstable = torch.tensor([[100.0, -500.0, 0.001, 1000.0, -0.1, 300.0, -200.0, 50.0]])
    print(f"\n  Input range: [{unstable.min().item():.1f}, {unstable.max().item():.1f}]")
    print(f"  Input:  {unstable[0].tolist()}")

    with torch.no_grad():
        ln_out = ln(unstable)
        rn_out = rn(unstable)

    print(f"\n  After LayerNorm: min={ln_out.min().item():.3f}, max={ln_out.max().item():.3f}")
    print(f"  After RMSNorm:  min={rn_out.min().item():.3f}, max={rn_out.max().item():.3f}")
    print(f"\n  ✅ Dono normalize karte hain!")
    print(f"  ✅ RMSNorm: no mean subtraction → less computation!")
    print(f"  ✅ Modern LLMs (LLaMA, Mistral) RMSNorm prefer karte hain")


# ─────────────────────────────────────────────────────────
# DEMO 5: RoPE — Positional Rotation
# ─────────────────────────────────────────────────────────
def demo_rope(torch):
    clear()
    print("=" * 60)
    print("  🌀  DEMO 5: RoPE — Rotary Positional Embedding")
    print("=" * 60)

    def apply_rope(q, position, head_dim):
        half = head_dim // 2
        freq = torch.tensor([position / (10000 ** (2 * i / head_dim)) for i in range(half)])
        cos_f = torch.cos(freq)
        sin_f = torch.sin(freq)
        q_r = q[:half]
        q_i = q[half:]
        rot_r = q_r * cos_f - q_i * sin_f
        rot_i = q_r * sin_f + q_i * cos_f
        return torch.cat([rot_r, rot_i])

    head_dim = 8
    torch.manual_seed(0)
    q = torch.randn(head_dim)

    print(f"\n  Original Query vector: {q.round(decimals=2).tolist()}")
    print(f"\n  RoPE rotation at different positions:")
    print(f"\n  {'Position':<12} {'Rotated Vector (first 4 dims)'}")
    print("  " + "-" * 55)

    for pos in [0, 1, 5, 10, 50]:
        rotated = apply_rope(q.clone(), pos, head_dim)
        print(f"  pos={pos:<8}  {rotated[:4].round(decimals=3).tolist()}")

    print(f"\n  💡 Har position par vector differently rotated hota hai.")
    print(f"  💡 Attention compute karte waqt Q·Kᵀ → relative position capture hoti hai!")
    print(f"  💡 GPT-2 ka sinusoidal encoding sirf add karta tha — RoPE multiply+rotate karta hai.")


# ─────────────────────────────────────────────────────────
# EXERCISE + TEST
# ─────────────────────────────────────────────────────────
def exercise():
    clear()
    print("=" * 60)
    print("  ✏️   EXERCISE: Architecture MCQ Test")
    print("=" * 60)

    questions = [
        {
            "q": "Q1: GQA (Grouped Query Attention) ka main fayda kya hai?",
            "options": ["A) Better accuracy", "B) Reduced KV cache memory, faster generation",
                        "C) Larger vocabulary", "D) More attention heads"],
            "answer": "B",
            "exp": "GQA fewer KV heads use karta hai — KV cache chhota hota hai, generation fast hoti hai!"
        },
        {
            "q": "Q2: SwiGLU me 'gating' ka kya matlab hai?",
            "options": ["A) Door band karna", "B) Random dropout",
                        "C) Ek branch doosri branch ko control karta hai (multiply)",
                        "D) Learning rate control"],
            "answer": "C",
            "exp": "Gate branch × Content branch = information flow control. Model decide karta hai kya pass karna hai."
        },
        {
            "q": "Q3: RMSNorm, LayerNorm se kaise alag hai?",
            "options": ["A) RMSNorm zyada params use karta hai",
                        "B) RMSNorm mean subtract nahi karta — sirf RMS se divide karta hai",
                        "C) RMSNorm GPU par nahi chalta",
                        "D) Koi fark nahi"],
            "answer": "B",
            "exp": "LayerNorm: mean + variance. RMSNorm: sirf root mean square. Simpler = faster!"
        },
        {
            "q": "Q4: RoPE kya improve karta hai traditional positional encoding se?",
            "options": ["A) Vocabulary size badhata hai",
                        "B) Training fast karta hai",
                        "C) Position info ko rotate karke Q,K me inject karta hai — relative positions better",
                        "D) Model chhota karta hai"],
            "answer": "C",
            "exp": "RoPE rotation se relative position information attention computation me directly encode hoti hai!"
        },
    ]

    score = 0
    for q in questions:
        print(f"\n{'─'*55}")
        print(f"\n  {q['q']}")
        for opt in q['options']:
            print(f"    {opt}")
        ans = input(f"\n  Answer (A/B/C/D): ").strip().upper()

        if ans == q['answer']:
            print(f"  ✅ SAHI! 🎉")
            score += 1
        else:
            print(f"  ❌ Galat! Sahi: {q['answer']}")
        print(f"  💡 {q['exp']}")

    total = len(questions)
    print(f"\n{'='*55}")
    print(f"  📊 Score: {score}/{total}")
    if score == total:
        print("  🏆 PERFECT SCORE! Architecture clear hai!")
    elif score >= total * 0.75:
        print("  👍 Bahut achha! Ek-do revisit karo.")
    else:
        print("  📖 Demos phir se chalao — sab clear ho jayega!")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
def main():
    torch = check_torch()

    while True:
        clear()
        print("=" * 60)
        print("  🏗️  ARCHITECTURE DEMO — RoPE, SwiGLU, GQA, RMSNorm")
        print("  📄  Ref: docs/susagpt/SusaGPT_Architecture.md")
        print("=" * 60)

        if not torch:
            print("\n  ⚠️  PyTorch required! Run: pip install torch")
            print("  Bina torch ke sirf Q4 (exercise) chala sakte ho.")

        print()
        print("    1. 👁️   Self-Attention Visualizer")
        print("    2. 🔗   GQA vs MHA — Memory Calculator")
        print("    3. ⚡   SwiGLU vs SimpleFFN Comparison")
        print("    4. 📏   RMSNorm vs LayerNorm Demo")
        print("    5. 🌀   RoPE Rotation Visualizer")
        print("    6. ✏️   Architecture MCQ Test (score dekho!)")
        print()
        print("    0. 🔙  Back / Exit")
        print()

        choice = input("  Choice (0-6): ").strip()

        if torch:
            demos = {
                "1": lambda: demo_attention(torch),
                "2": lambda: demo_gqa(torch),
                "3": lambda: demo_swiglu(torch),
                "4": lambda: demo_rmsnorm(torch),
                "5": lambda: demo_rope(torch),
            }
            if choice in demos:
                demos[choice]()
                input("\n↩️  Enter dabao...")
                continue

        if choice == "6":
            exercise()
            input("\n↩️  Enter dabao...")
        elif choice == "0":
            break
        elif choice not in ["1", "2", "3", "4", "5"]:
            print("❌ Invalid! 0-6 enter karo.")
            input("Enter dabao...")


if __name__ == "__main__":
    main()
