"""
╔══════════════════════════════════════════════════════════╗
║       🔤  TOKENIZER & BPE — Interactive Demo             ║
║       Docs: docs/susagpt/SusaGPT_Diagram_Guide.md        ║
╚══════════════════════════════════════════════════════════╝

Is file ko run karo:  python tokenizer_demo.py
"""

import os
import math
from collections import Counter


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# ─────────────────────────────────────────────────────────
# DEMO 1: Text → Bytes → Chars
# ─────────────────────────────────────────────────────────
def demo_text_to_bytes():
    clear()
    print("=" * 60)
    print("  🔤  DEMO 1: Text → UTF-8 Bytes → Characters")
    print("=" * 60)

    text = input("\n  Koi bhi text type karo (Enter = 'AI kya hai?'): ").strip()
    if not text:
        text = "AI kya hai?"

    print(f"\n📝 Tumhara text: '{text}'")
    print(f"   Length: {len(text)} characters")

    # UTF-8 bytes
    byte_data = text.encode('utf-8')
    print(f"\n📊 UTF-8 Bytes ({len(byte_data)} bytes):")
    print(f"   {list(byte_data)}")

    # Characters
    chars = []
    for b in byte_data:
        if 32 <= b <= 126:
            chars.append(chr(b))
        else:
            chars.append(f"<{b}>")
    print(f"\n🔡 Characters / Byte pieces:")
    print(f"   {chars}")

    print(f"\n💡 Note: Hindi text jaise 'नमस्ते' = zyada bytes (3 bytes per char!)")
    hindi = "नमस्ते"
    print(f"   'नमस्ते' → {len(hindi)} chars → {len(hindi.encode('utf-8'))} bytes")


# ─────────────────────────────────────────────────────────
# DEMO 2: BPE Algorithm Step by Step
# ─────────────────────────────────────────────────────────
def demo_bpe():
    clear()
    print("=" * 60)
    print("  🔄  DEMO 2: BPE Algorithm — Step by Step")
    print("=" * 60)

    default_corpus = ["hello", "hell", "help", "helping", "helped"]
    print(f"\n📄 Default corpus: {default_corpus}")
    custom = input("  Custom corpus chahiye? (y/n, Enter = n): ").strip().lower()

    if custom == 'y':
        words_input = input("  Words likho (space-separated): ").strip()
        corpus = words_input.split() if words_input else default_corpus
    else:
        corpus = default_corpus

    print(f"\n🚀 BPE Training Start! Corpus: {corpus}")
    print(f"   Initial vocab = individual characters\n")

    # Char-level start
    word_tokens = [list(w) for w in corpus]

    merges_done = []
    num_merges = min(5, len(corpus) * 2)

    for merge_num in range(1, num_merges + 1):
        # Count all pairs
        pair_counts = Counter()
        for tokens in word_tokens:
            for i in range(len(tokens) - 1):
                pair = (tokens[i], tokens[i + 1])
                pair_counts[pair] += 1

        if not pair_counts:
            print("  No more pairs to merge!")
            break

        # Best pair
        best_pair, best_count = pair_counts.most_common(1)[0]
        new_token = ''.join(best_pair)
        merges_done.append((best_pair, new_token))

        print(f"  Merge #{merge_num}:")
        print(f"    Top pairs: {dict(list(pair_counts.most_common(3)))}")
        print(f"    ✅ Best: '{best_pair[0]}' + '{best_pair[1]}' → '{new_token}' (count={best_count})")

        # Apply merge
        new_word_tokens = []
        for tokens in word_tokens:
            new_toks = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == best_pair:
                    new_toks.append(new_token)
                    i += 2
                else:
                    new_toks.append(tokens[i])
                    i += 1
            new_word_tokens.append(new_toks)
        word_tokens = new_word_tokens

        print(f"    Words now: {[''.join(w) + '=' + '+'.join(w) for w in word_tokens]}")
        print()

        cont = input("  Next merge? (Enter = yes, 'q' = quit): ").strip()
        if cont.lower() == 'q':
            break

    print(f"\n📋 Total merges done: {len(merges_done)}")
    print("   Merge history:")
    for i, (pair, merged) in enumerate(merges_done, 1):
        print(f"   {i}. '{pair[0]}' + '{pair[1]}' → '{merged}'")


# ─────────────────────────────────────────────────────────
# DEMO 3: Tokenizer Benefits
# ─────────────────────────────────────────────────────────
def demo_tokenizer_benefits():
    clear()
    print("=" * 60)
    print("  🌟  DEMO 3: Byte-level BPE ke Fayde")
    print("=" * 60)

    samples = {
        "English": "Hello AI World",
        "Hindi": "नमस्ते दुनिया",
        "Mixed (Hinglish)": "AI bahut अच्छा hai",
        "Code": "def neural_network():",
        "Rare word": "supercalifragilistic",
        "Symbol": "1+2=3, (x²+y²=z²)",
    }

    print(f"\n{'Language/Type':<25} {'Text':<30} {'Chars':<8} {'Bytes':<8}")
    print("-" * 75)
    for lang, text in samples.items():
        chars = len(text)
        byte_count = len(text.encode('utf-8'))
        print(f"{lang:<25} {text[:28]:<30} {chars:<8} {byte_count:<8}")

    print(f"\n💡 Why Byte-level BPE wins:")
    print(f"   ✅ Hindi 'दुनिया' → bytes → BPE merge → no <UNK>!")
    print(f"   ✅ Mixed Hinglish → handled naturally")
    print(f"   ✅ Rare words → toot ke tokenize hote hain")
    print(f"   ✅ Koi bhi language → supported!")


# ─────────────────────────────────────────────────────────
# EXERCISE: Aap khud try karo
# ─────────────────────────────────────────────────────────
def exercise():
    clear()
    print("=" * 60)
    print("  ✏️   EXERCISE: Tokenizer Concepts Test")
    print("=" * 60)

    questions = [
        {
            "q": "Q1: Byte-level BPE ki sabse badi advantage kya hai?",
            "options": ["A) Fast hai", "B) Kisi bhi language ko bina <UNK> ke tokenize kar sakta hai",
                        "C) Sirf English ke liye kaam karta hai", "D) Model chhota hota hai"],
            "answer": "B",
            "explanation": "Byte-level BPE UTF-8 bytes se start karta hai, isliye Hindi, Urdu, Code — sab tokenize ho sakta hai!"
        },
        {
            "q": "Q2: BPE training me 'best pair' kaise choose hota hai?",
            "options": ["A) Shortest pair", "B) Random pair",
                        "C) Most frequent pair in corpus", "D) Alphabetically first pair"],
            "answer": "C",
            "explanation": "BPE har iteration me sabse zyada baar aane wala pair choose karta hai aur ek new token banata hai."
        },
        {
            "q": "Q3: Tokenizer encode aur decode dono karta hai. Decode ka matlab?",
            "options": ["A) Token compress karna", "B) Token IDs ko wapas text me convert karna",
                        "C) Model ko train karna", "D) Bytes count karna"],
            "answer": "B",
            "explanation": "[12, 97, 234] → 'hello world' — ye Token IDs se Original text banta hai."
        },
    ]

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\n{'─'*55}")
        print(f"\n  {q['q']}")
        for opt in q['options']:
            print(f"    {opt}")

        ans = input(f"\n  Tumhara answer (A/B/C/D): ").strip().upper()

        if ans == q['answer']:
            print(f"  ✅ SAHI HAI! 🎉")
            score += 1
        else:
            print(f"  ❌ Galat! Sahi answer: {q['answer']}")

        print(f"  💡 Explanation: {q['explanation']}")

    print(f"\n{'='*55}")
    print(f"  📊 Final Score: {score}/{len(questions)}")
    if score == len(questions):
        print("  🏆 PERFECT! Tokenizer concept clear hai!")
    elif score >= 2:
        print("  👍 Achha! Thoda aur padho.")
    else:
        print("  📖 Demo 1 aur 2 phir se dekho!")


# ─────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────
def main():
    while True:
        clear()
        print("=" * 60)
        print("  🔤  TOKENIZER & BPE — Interactive Demo")
        print("  📄  Ref: docs/susagpt/SusaGPT_Diagram_Guide.md")
        print("=" * 60)
        print()
        print("    1. 📊  Text → Bytes → Chars (khud try karo!)")
        print("    2. 🔄  BPE Algorithm Step-by-Step (live demo)")
        print("    3. 🌟  Byte-level BPE ke Fayde")
        print("    4. ✏️   Exercise + Test (score dekho!)")
        print()
        print("    0. 🔙  Back / Exit")
        print()

        choice = input("  Choice (0-4): ").strip()

        if choice == "1":
            demo_text_to_bytes()
            input("\n↩️  Enter dabao...")
        elif choice == "2":
            demo_bpe()
            input("\n↩️  Enter dabao...")
        elif choice == "3":
            demo_tokenizer_benefits()
            input("\n↩️  Enter dabao...")
        elif choice == "4":
            exercise()
            input("\n↩️  Enter dabao...")
        elif choice == "0":
            break
        else:
            print("❌ Invalid! 0-4 enter karo.")
            input("Enter dabao...")


if __name__ == "__main__":
    main()
