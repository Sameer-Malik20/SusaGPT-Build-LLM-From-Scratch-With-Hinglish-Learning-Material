"""
╔══════════════════════════════════════════════════════════╗
║   🎯  TRAINING CONCEPTS — Loss, AdamW, Gradient, LR     ║
║   Docs: docs/susagpt/SusaGPT_Skills.md                   ║
╚══════════════════════════════════════════════════════════╝

Run: python training_demo.py
Requires: torch  (pip install torch)
"""

import os
import math
import time

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
# DEMO 1: Loss — What It Means
# ─────────────────────────────────────────────────────────
def demo_loss(torch):
    clear()
    print("=" * 60)
    print("  📉  DEMO 1: Loss — Model Kitna Galat Hai?")
    print("=" * 60)

    import torch.nn.functional as F

    vocab_size = 5
    token_names = ["AI", "kya", "hai", "robot", "computer"]

    print(f"\n  Vocabulary: {dict(enumerate(token_names))}")
    print(f"  Next token ka sahi answer: 'hai' (index 2)\n")

    scenarios = {
        "🤖 Confident + Correct": [0.02, 0.02, 0.90, 0.03, 0.03],
        "😐 Uncertain": [0.20, 0.20, 0.25, 0.18, 0.17],
        "❌ Wrong (Confident)": [0.85, 0.04, 0.04, 0.04, 0.03],
    }

    print(f"  {'Scenario':<30} {'Probs':<40} {'Loss':<8}")
    print("  " + "-" * 80)

    for name, probs in scenarios.items():
        logits = torch.tensor([math.log(p) for p in probs])
        target = torch.tensor([2])  # "hai" = index 2
        loss = F.nll_loss(logits.unsqueeze(0), target).item()

        bar = "█" * int(probs[2] * 20)
        print(f"  {name:<30} 'hai'={probs[2]:.2f} {bar:<22} {loss:.4f}")

    print(f"\n  💡 Loss formula: -log(probability of correct token)")
    print(f"     p=0.90 → loss = {-math.log(0.90):.4f}  (LOW = GOOD)")
    print(f"     p=0.25 → loss = {-math.log(0.25):.4f}  (MEDIUM)")
    print(f"     p=0.04 → loss = {-math.log(0.04):.4f}  (HIGH = BAD)")


# ─────────────────────────────────────────────────────────
# DEMO 2: Training Loop — Live Simulation
# ─────────────────────────────────────────────────────────
def demo_training_loop(torch):
    clear()
    print("=" * 60)
    print("  🔄  DEMO 2: Training Loop — Live Simulation")
    print("=" * 60)

    import torch.nn as nn
    import torch.optim as optim

    print("\n  Ek simple linear model train kar rahe hain...")
    print("  Task: y = 2x + 1 seekhna (simple linear regression)\n")

    try:
        epochs = int(input("  Kitne epochs? (Enter = 30): ").strip() or "30")
        lr = float(input("  Learning rate? (Enter = 0.1): ").strip() or "0.1")
    except ValueError:
        epochs, lr = 30, 0.1

    # Simple model
    model = nn.Linear(1, 1)
    optimizer = optim.SGD(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    # True relationship: y = 2x + 1
    X = torch.linspace(-2, 2, 20).unsqueeze(1)
    y = 2 * X + 1

    print(f"\n  Training {epochs} epochs with LR={lr}...\n")
    print(f"  {'Epoch':<8} {'Loss':<12} {'Weight':<12} {'Bias':<12} {'Progress'}")
    print("  " + "-" * 65)

    for epoch in range(1, epochs + 1):
        pred = model(X)
        loss = criterion(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % max(1, epochs // 10) == 0 or epoch == 1:
            w = model.weight.item()
            b = model.bias.item()
            loss_val = loss.item()

            # Visual bar (loss bar)
            bar_len = max(0, min(30, int(30 - loss_val * 2)))
            bar = "█" * bar_len

            print(f"  {epoch:<8} {loss_val:<12.4f} {w:<12.4f} {b:<12.4f} |{bar:<30}|")
            time.sleep(0.1)

    final_w = model.weight.item()
    final_b = model.bias.item()
    print(f"\n  ✅ Training Complete!")
    print(f"  📊 Learned: y = {final_w:.3f}x + {final_b:.3f}")
    print(f"  🎯 Target:  y = 2.000x + 1.000")
    print(f"  Difference: weight={abs(final_w-2):.4f}, bias={abs(final_b-1):.4f}")


# ─────────────────────────────────────────────────────────
# DEMO 3: Gradient Clipping
# ─────────────────────────────────────────────────────────
def demo_gradient_clipping(torch):
    clear()
    print("=" * 60)
    print("  ✂️   DEMO 3: Gradient Clipping — Explosion Rokna")
    print("=" * 60)

    import torch.nn as nn

    print("\n  Kabhi-kabhi gradients bahut bade ho jaate hain.")
    print("  Gradient clipping unhe limit karta hai.\n")

    dim = 10
    model = nn.Linear(dim, 1)

    # Artificial big gradients simulate karo
    x = torch.randn(1, dim) * 100  # Very large input
    y = torch.tensor([[1.0]])

    pred = model(x)
    loss = (pred - y).pow(2).mean()
    loss.backward()

    # Calculate gradient norm before clipping
    total_norm_before = 0
    for p in model.parameters():
        if p.grad is not None:
            total_norm_before += p.grad.data.norm(2).item() ** 2
    total_norm_before = total_norm_before ** 0.5

    print(f"  Gradient norm BEFORE clipping: {total_norm_before:.4f}")
    bar = "█" * min(50, int(total_norm_before / 10))
    print(f"  {'':40} |{bar}|")

    # Apply clipping
    max_norm = float(input(f"\n  Max norm limit? (Enter = 1.0): ").strip() or "1.0")
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_norm)

    total_norm_after = 0
    for p in model.parameters():
        if p.grad is not None:
            total_norm_after += p.grad.data.norm(2).item() ** 2
    total_norm_after = total_norm_after ** 0.5

    print(f"\n  Gradient norm AFTER clipping:  {total_norm_after:.4f}")
    bar2 = "█" * min(50, int(total_norm_after * 5))
    print(f"  {'':40} |{bar2}|")

    print(f"\n  ✅ Clipping ne gradient ko {total_norm_before:.1f} → {total_norm_after:.4f} kar diya!")
    print(f"  ✅ Training ab explode nahi karega!")


# ─────────────────────────────────────────────────────────
# DEMO 4: LR Scheduler Visualization
# ─────────────────────────────────────────────────────────
def demo_lr_scheduler():
    clear()
    print("=" * 60)
    print("  📊  DEMO 4: LR Scheduler — Warmup + Cosine Decay")
    print("=" * 60)

    print("\n  SusaGPT me Warmup + Cosine LR schedule use hota hai.")

    try:
        total_steps = int(input("\n  Total training steps? (Enter = 100): ").strip() or "100")
        warmup = int(input("  Warmup steps? (Enter = 10): ").strip() or "10")
        max_lr = float(input("  Max LR? (Enter = 0.001): ").strip() or "0.001")
        min_lr = max_lr * 0.1
    except ValueError:
        total_steps, warmup, max_lr, min_lr = 100, 10, 0.001, 0.0001

    def get_lr(step):
        if step < warmup:
            return max_lr * step / max(1, warmup)
        progress = (step - warmup) / max(1, total_steps - warmup)
        return min_lr + (max_lr - min_lr) * 0.5 * (1 + math.cos(math.pi * progress))

    print(f"\n  {'Step':<8} {'LR':<12} {'Phase':<12} {'Visualization'}")
    print("  " + "-" * 70)

    shown_steps = sorted(set(
        list(range(0, min(total_steps, warmup + 1))) +
        list(range(warmup, total_steps + 1, max(1, total_steps // 12)))
        + [total_steps]
    ))

    for step in shown_steps:
        if step > total_steps:
            continue
        lr = get_lr(step)
        phase = "Warmup 🔥" if step < warmup else "Decay ❄️"
        bar_len = int(lr / max_lr * 40)
        bar = "█" * bar_len
        print(f"  {step:<8} {lr:.6f}   {phase:<12} |{bar:<40}|")

    print(f"\n  💡 Warmup: Training start me LR badhao (stable convergence)")
    print(f"  💡 Cosine: Dheere dheere ghatao (fine adjustments at end)")


# ─────────────────────────────────────────────────────────
# DEMO 5: Curriculum Learning
# ─────────────────────────────────────────────────────────
def demo_curriculum():
    clear()
    print("=" * 60)
    print("  📚  DEMO 5: Data Curriculum — Easy to Hard")
    print("=" * 60)

    chunks = [
        "AI is good.",
        "Machine learning algorithms process data sequentially.",
        "Deep neural networks with attention mechanisms process sequences effectively.",
        "Transformers ने NLP को revolutionize किया है, particularly for long-range dependencies.",
        "The self-attention mechanism in transformer models computes query-key-value interactions.",
        "Hello.",
        "Generative models create content.",
        "PyTorch autograd computes gradients automatically via dynamic computational graphs.",
    ]

    def score(chunk):
        length = len(chunk.split())
        punct = chunk.count(',') + chunk.count(';') + chunk.count('(')
        multilingual = sum(1 for c in chunk if ord(c) > 127)
        return length + punct * 2 + multilingual * 3

    print(f"\n  {len(chunks)} text chunks hain — curriculum sort kar rahe hain...\n")
    print(f"  {'Score':<8} {'Difficulty':<15} {'Chunk'}")
    print("  " + "-" * 70)

    scored = sorted([(c, score(c)) for c in chunks], key=lambda x: x[1])

    for chunk, s in scored:
        if s <= 5:
            diff = "🟢 Easy"
        elif s <= 15:
            diff = "🟡 Medium"
        else:
            diff = "🔴 Hard"
        print(f"  {s:<8} {diff:<15} '{chunk[:45]}...'")

    print(f"\n  ✅ Model pehle easy examples dekhe → stable learning!")
    print(f"  ✅ Phir hard examples → complex patterns absorb!")


# ─────────────────────────────────────────────────────────
# EXERCISE + TEST
# ─────────────────────────────────────────────────────────
def exercise():
    clear()
    print("=" * 60)
    print("  ✏️   EXERCISE: Training Concepts Test")
    print("=" * 60)

    questions = [
        {
            "q": "Q1: Model ka loss HIGH hai. Iska matlab...?",
            "options": ["A) Model achha train ho gaya", "B) Model galat predictions kar raha hai",
                        "C) Learning rate zero hai", "D) Overfitting ho raha hai"],
            "answer": "B",
            "exp": "High loss = model ka prediction far from correct. Train karte rehna chahiye."
        },
        {
            "q": "Q2: Gradient clipping kyu zaroori hai?",
            "options": ["A) Memory save karna",
                        "B) Exploding gradients rokna — training unstable ho jaati hai agar gradients bahut bade hon",
                        "C) Batch size control karna", "D) Vocabulary limit karna"],
            "answer": "B",
            "exp": "Bade gradients = unstable training = loss explode. Clipping prevents this!"
        },
        {
            "q": "Q3: LR Warmup phase me kya hota hai?",
            "options": ["A) LR suddenly high se low hota hai",
                        "B) LR zero se dheere dheere max tak badhta hai",
                        "C) Model weights reset hote hain",
                        "D) Batch size badhti hai"],
            "answer": "B",
            "exp": "Warmup: 0 → max LR. Isse training start me stability aati hai."
        },
        {
            "q": "Q4: AdamW me 'weight decay' kya karta hai?",
            "options": ["A) Learning rate adjust karta hai",
                        "B) Weights ko explode hone se rokta hai (regularization)",
                        "C) Epochs count karta hai",
                        "D) Vocabulary size ghatata hai"],
            "answer": "B",
            "exp": "Weight decay = L2 regularization. Weights bahut bade na hon — overfitting control!"
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
    print(f"  📊 Score: {score}/{total}")
    stars = "⭐" * score + "☆" * (total - score)
    print(f"  {stars}")
    if score == total:
        print("  🏆 PERFECT! Training concepts crystal clear!")
    elif score >= 3:
        print("  👍 Bahut achha! Almost there.")
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
        print("  🎯  TRAINING CONCEPTS DEMO")
        print("  📄  Ref: docs/susagpt/SusaGPT_Skills.md + README.md")
        print("=" * 60)
        print()
        print("    1. 📉   Loss — Model Kitna Galat Hai? (Live)")
        print("    2. 🔄   Training Loop Simulation (watch loss go down!)")
        print("    3. ✂️   Gradient Clipping Demo")
        print("    4. 📊   LR Scheduler Visualization")
        print("    5. 📚   Data Curriculum — Easy to Hard")
        print("    6. ✏️   Training MCQ Test (score dekho!)")
        print()
        print("    0. 🔙  Back / Exit")
        print()

        choice = input("  Choice (0-6): ").strip()

        if choice == "6":
            exercise()
            input("\n↩️  Enter dabao...")
        elif choice == "4":
            demo_lr_scheduler()
            input("\n↩️  Enter dabao...")
        elif choice == "5":
            demo_curriculum()
            input("\n↩️  Enter dabao...")
        elif torch and choice == "1":
            demo_loss(torch)
            input("\n↩️  Enter dabao...")
        elif torch and choice == "2":
            demo_training_loop(torch)
            input("\n↩️  Enter dabao...")
        elif torch and choice == "3":
            demo_gradient_clipping(torch)
            input("\n↩️  Enter dabao...")
        elif choice == "0":
            break
        elif choice in ["1", "2", "3"] and not torch:
            print("\n⚠️  PyTorch required for this demo!")
            print("   pip install torch")
            input("Enter dabao...")
        else:
            print("❌ Invalid!")
            input("Enter dabao...")


if __name__ == "__main__":
    main()
