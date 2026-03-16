"""
╔══════════════════════════════════════════════════════════╗
║     📊  EVALUATION — BLEU Score + Perplexity Demo        ║
║     Docs: docs/susagpt/SusaGPT_Skills.md                 ║
╚══════════════════════════════════════════════════════════╝

Run: python evaluation_demo.py
No extra dependencies required (math only)!
"""

import os
import math
import re
from collections import Counter

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# ─────────────────────────────────────────────────────────
# DEMO 1: Perplexity — What It Means
# ─────────────────────────────────────────────────────────
def demo_perplexity():
    clear()
    print("=" * 60)
    print("  📉  DEMO 1: Perplexity — Model Kitna Confident Hai?")
    print("=" * 60)

    print("""
  Perplexity = Model ka "confusion level"
  Formula: exp(average negative log probability)

  Low perplexity  = Confident model     = Better!
  High perplexity = Confused model      = Worse
""")

    def perplexity(probs):
        """Calculate perplexity from list of probabilities"""
        if any(p <= 0 for p in probs):
            return float('inf')
        avg_neg_log = -sum(math.log(p) for p in probs) / len(probs)
        return math.exp(avg_neg_log)

    scenarios = {
        "🏆 Expert Model (very confident)":  [0.92, 0.88, 0.95, 0.90, 0.85],
        "👍 Good Model (usually correct)":   [0.70, 0.65, 0.75, 0.68, 0.72],
        "😐 Average Model (uncertain)":      [0.35, 0.40, 0.30, 0.38, 0.42],
        "❌ Weak Model (mostly wrong)":       [0.10, 0.12, 0.08, 0.15, 0.11],
    }

    print(f"  {'Model Type':<40} {'Avg Prob':<12} {'Perplexity':<12} {'Rating'}")
    print("  " + "-" * 75)

    for name, probs in scenarios.items():
        ppl = perplexity(probs)
        avg_p = sum(probs) / len(probs)
        bar = "█" * max(1, int(50 - ppl * 0.5))
        rating = "🏆" if ppl < 2 else "👍" if ppl < 5 else "😐" if ppl < 15 else "❌"
        print(f"  {name:<40} {avg_p:.2f}       {ppl:<12.2f} {rating}")

    print(f"\n  ─────────────────────────────────────────────────────")
    print(f"\n  📊 Manual Calculation:")
    print(f"     p(token1)=0.90 → -log(0.90) = {-math.log(0.90):.4f}")
    print(f"     p(token2)=0.85 → -log(0.85) = {-math.log(0.85):.4f}")
    print(f"     p(token3)=0.88 → -log(0.88) = {-math.log(0.88):.4f}")
    avg_nl = (-math.log(0.90) + -math.log(0.85) + -math.log(0.88)) / 3
    ppl_ex = math.exp(avg_nl)
    print(f"     Average neg log = {avg_nl:.4f}")
    print(f"     Perplexity = exp({avg_nl:.4f}) = {ppl_ex:.4f}")

    print(f"\n  ─────────────────────────────────────────────────────")
    own = input("\n  Apni probabilities enter karo (comma separated, Enter = skip): ").strip()
    if own:
        try:
            user_probs = [float(x.strip()) for x in own.split(",")]
            user_ppl = perplexity(user_probs)
            print(f"\n  Tumhara input: {user_probs}")
            print(f"  Perplexity: {user_ppl:.4f}")
            if user_ppl < 3:
                print(f"  Rating: 🏆 Bahut confident model!")
            elif user_ppl < 10:
                print(f"  Rating: 👍 Accha model")
            elif user_ppl < 50:
                print(f"  Rating: 😐 Average model")
            else:
                print(f"  Rating: ❌ Confused model")
        except:
            print("  ❌ Invalid numbers!")


# ─────────────────────────────────────────────────────────
# DEMO 2: BLEU Score — Word Overlap
# ─────────────────────────────────────────────────────────
def demo_bleu():
    clear()
    print("=" * 60)
    print("  📊  DEMO 2: BLEU Score — Answer Quality Measure")
    print("=" * 60)

    print("""
  BLEU = Bilingual Evaluation Understudy
  
  Measure karta hai: Generated text aur reference text me
  kaunse n-grams (word sequences) common hain.
  
  Range: 0.0 (no match) → 1.0 (perfect match)
  Higher BLEU = Better answer
""")

    def simple_bleu(generated, reference, n=1):
        """Simplified n-gram BLEU"""
        gen_words = re.findall(r'\b\w+\b', generated.lower())
        ref_words = re.findall(r'\b\w+\b', reference.lower())

        if len(gen_words) < n:
            return 0.0

        # Get n-grams
        def get_ngrams(words, n):
            return Counter(tuple(words[i:i+n]) for i in range(len(words) - n + 1))

        gen_ngrams = get_ngrams(gen_words, n)
        ref_ngrams = get_ngrams(ref_words, n)

        # Count matches
        matches = sum(min(count, ref_ngrams[gram]) for gram, count in gen_ngrams.items())
        total = sum(gen_ngrams.values())

        if total == 0:
            return 0.0

        precision = matches / total

        # Brevity penalty
        bp = 1.0 if len(gen_words) >= len(ref_words) else math.exp(1 - len(ref_words)/len(gen_words))
        return bp * precision

    reference = "PyTorch ek open source deep learning framework hai jo Python me use hota hai"
    print(f"  📖 Reference Answer: '{reference}'\n")

    candidates = {
        "🏆 Near-perfect":   "PyTorch ek open source machine learning framework hai jo Python me use hota hai",
        "👍 Good":           "PyTorch ek deep learning library hai Python ke liye",
        "😐 Partial":        "PyTorch framework hai jo learning ke liye use hota hai",
        "❌ Unrelated":      "Python mujhe bahut pasand hai kyunki ye easy hai aur fast bhi hai",
    }

    print(f"  {'Answer Type':<22} {'1-gram BLEU':<15} {'Quality Bar'}")
    print("  " + "-" * 60)

    for name, cand in candidates.items():
        bleu1 = simple_bleu(cand, reference, 1)
        bar = "█" * int(bleu1 * 40)
        print(f"  {name:<22} {bleu1:.4f}         {bar}")

    print(f"\n  ─────────────────────────────────────────────────────")
    print(f"\n  🧪 Apna answer test karo:")
    print(f"  Reference: '{reference}'")
    user_ans = input(f"\n  Tumhara answer: ").strip()
    if user_ans:
        bleu = simple_bleu(user_ans, reference, 1)
        bar = "█" * int(bleu * 40)
        print(f"\n  BLEU Score: {bleu:.4f}")
        print(f"  Quality:    |{bar:<40}|")
        if bleu > 0.6:
            print(f"  🏆 Excellent! Reference se bahut similar")
        elif bleu > 0.35:
            print(f"  👍 Good overlap!")
        elif bleu > 0.15:
            print(f"  😐 Kuch overlap hai")
        else:
            print(f"  ❌ Very different from reference")

    print(f"\n  ⚠️  Note: BLEU perfect judge nahi hai.")
    print(f"  'PyTorch is an ML library for Python' ka BLEU low ho sakta hai")
    print(f"  lekin meaning same hai! BLEU sirf word overlap dekhta hai.")


# ─────────────────────────────────────────────────────────
# DEMO 3: Compare Two Models
# ─────────────────────────────────────────────────────────
def demo_model_comparison():
    clear()
    print("=" * 60)
    print("  🔬  DEMO 3: Do Models Ko Compare Karo")
    print("=" * 60)

    def perplexity(probs):
        avg_neg_log = -sum(math.log(max(p, 1e-10)) for p in probs) / len(probs)
        return math.exp(avg_neg_log)

    def simple_bleu(generated, reference):
        gen_words = set(re.findall(r'\b\w+\b', generated.lower()))
        ref_words = set(re.findall(r'\b\w+\b', reference.lower()))
        intersection = gen_words & ref_words
        return len(intersection) / len(gen_words) if gen_words else 0

    print(f"\n  Yahan do hypothetical models ke data hain:\n")

    models = {
        "Base SusaGPT (before fine-tuning)": {
            "token_probs": [0.25, 0.30, 0.20, 0.28, 0.22],
            "answers": [
                "AI machine deep neural network learning system compute",
                "Python language programming code develop"
            ]
        },
        "Fine-tuned SusaGPT (after Q&A training)": {
            "token_probs": [0.72, 0.68, 0.75, 0.70, 0.65],
            "answers": [
                "AI matlab Artificial Intelligence jo machines ko intelligent banata hai",
                "Python ek high-level programming language hai jo easy to learn hai"
            ]
        }
    }

    references = [
        "AI matlab Artificial Intelligence ek computer science field hai",
        "Python ek popular high-level programming language hai"
    ]

    for model_name, model_data in models.items():
        print(f"  📦 {model_name}")
        print(f"  {'─'*55}")

        ppl = perplexity(model_data["token_probs"])
        print(f"  Perplexity: {ppl:.2f}")

        bleu_scores = [simple_bleu(ans, ref)
                       for ans, ref in zip(model_data["answers"], references)]
        avg_bleu = sum(bleu_scores) / len(bleu_scores)
        print(f"  BLEU Score (avg): {avg_bleu:.4f}")
        print(f"  Sample answer: '{model_data['answers'][0][:60]}...'")

        ppl_bar = "🟢" * max(1, min(5, int(5 - ppl / 5))) + "🔴" * max(0, int(ppl / 5))
        bleu_bar = "█" * int(avg_bleu * 20)
        print(f"  Perplexity bar: {ppl_bar} (lower=better)")
        print(f"  BLEU bar:       |{bleu_bar:<20}| {avg_bleu:.2f}")
        print()

    print(f"  ✅ Fine-tuned model ka BLEU zyada, Perplexity kam = BETTER!")


# ─────────────────────────────────────────────────────────
# EXERCISE + TEST
# ─────────────────────────────────────────────────────────
def exercise():
    clear()
    print("=" * 60)
    print("  ✏️   EXERCISE: Evaluation Metrics Test")
    print("=" * 60)

    questions = [
        {
            "q": "Q1: Model A ka Perplexity = 3.2, Model B = 12.5. Kounsa better hai?",
            "options": ["A) Model B — zyada perplexity matlab zyada capable",
                        "B) Model A — kam perplexity matlab zyada confident",
                        "C) Dono equal hain",
                        "D) Training epochs par depend karta hai"],
            "answer": "B",
            "exp": "Lower perplexity = more confident predictions = better language model!"
        },
        {
            "q": "Q2: BLEU Score = 0.0 ka matlab?",
            "options": ["A) Perfect answer",
                        "B) Average answer",
                        "C) Generated text aur reference me koi common word nahi",
                        "D) Model train nahi hua"],
            "answer": "C",
            "exp": "BLEU=0 = zero n-gram overlap. Generated answer aur reference bilkul alag hain."
        },
        {
            "q": "Q3: BLEU Score ka ek important limitation kya hai?",
            "options": ["A) Sirf English me kaam karta hai",
                        "B) Meaning check nahi karta, sirf word overlap dekhta hai",
                        "C) Calculate karna bahut hard hai",
                        "D) Zyada memory use karta hai"],
            "answer": "B",
            "exp": "Same meaning, different words → low BLEU. BLEU = word overlap measure, not semantic!"
        },
        {
            "q": "Q4: Perplexity formula me 'exp' kyu use karte hain?",
            "options": ["A) Random element add karna",
                        "B) Negative log probabilities ko human-readable scale par laana",
                        "C) Training speed badhana",
                        "D) Vocabulary size normalize karna"],
            "answer": "B",
            "exp": "exp(-avg_log_prob) → intuitive scale. Perplexity ≈ 'kitne tokens me se guess karna hai'."
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
        print("  🏆 PERFECT! Evaluation metrics clear hain!")
    else:
        print("  📖 Demos phir se chalao!")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
def main():
    while True:
        clear()
        print("=" * 60)
        print("  📊  EVALUATION — BLEU & Perplexity Demo")
        print("  📄  Ref: docs/susagpt/SusaGPT_Skills.md + README.md")
        print("=" * 60)
        print()
        print("    1. 📉   Perplexity Demo (apni probabilities try karo!)")
        print("    2. 📊   BLEU Score Demo (apna answer test karo!)")
        print("    3. 🔬   Model Comparison (base vs fine-tuned)")
        print("    4. ✏️   Evaluation MCQ Test (score dekho!)")
        print()
        print("    0. 🔙  Back / Exit")
        print()

        choice = input("  Choice (0-4): ").strip()

        if choice == "1":
            demo_perplexity()
            input("\n↩️  Enter dabao...")
        elif choice == "2":
            demo_bleu()
            input("\n↩️  Enter dabao...")
        elif choice == "3":
            demo_model_comparison()
            input("\n↩️  Enter dabao...")
        elif choice == "4":
            exercise()
            input("\n↩️  Enter dabao...")
        elif choice == "0":
            break
        else:
            print("❌ Invalid!")
            input("Enter dabao...")


if __name__ == "__main__":
    main()
