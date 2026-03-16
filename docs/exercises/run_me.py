"""
╔══════════════════════════════════════════════════════════╗
║          MyLLM / SusaGPT — Interactive Exercises         ║
║              Yahan se koi bhi topic run karo!            ║
╚══════════════════════════════════════════════════════════╝

Ye file poore project ka exercise launcher hai.
Kisi bhi topic ka demo directly yahan se run karo.
"""

import os
import sys
import subprocess


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_script(script_name):
    """Script ko subprocess me run karo"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        print(f"\n❌ Script nahi mili: {script_path}")
        return
    subprocess.run([sys.executable, script_path])


def main():
    while True:
        clear()
        print("=" * 60)
        print("    🤖 MyLLM / SusaGPT — Interactive Learning Hub")
        print("=" * 60)
        print()
        print("  📦 SusaGPT Core Concepts:")
        print("    1. 🔤  Tokenizer & BPE Demo")
        print("    2. 🏗️  Architecture Concepts (RoPE, SwiGLU, GQA, RMSNorm)")
        print("    3. 🎯  Training Concepts (Loss, AdamW, Grad Clip, LR)")
        print("    4. 📝  Generation & Sampling (Top-K, Top-P, KV Cache)")
        print("    5. 📊  Evaluation (BLEU + Perplexity)")
        print()
        print("  🤖 AI Concepts:")
        print("    6. 🧩  AI Agents Demo (Weather Agent)")
        print("    7. 🌀  Agentic AI Demo (Research Agent)")
        print("    8. 🔌  MCP Demo (Notes Server)")
        print()
        print("    0. ❌  Exit")
        print()
        print("=" * 60)

        choice = input("  Kaunsa topic run karna hai? (0-8): ").strip()

        scripts = {
            "1": "tokenizer_demo.py",
            "2": "architecture_demo.py",
            "3": "training_demo.py",
            "4": "sampling_demo.py",
            "5": "evaluation_demo.py",
            "6": "ai_agents_demo.py",
            "7": "agentic_ai_demo.py",
            "8": "mcp_demo.py",
        }

        if choice == "0":
            print("\n👋 Bye! Keep learning!\n")
            break
        elif choice in scripts:
            run_script(scripts[choice])
            input("\n↩️  Press Enter to go back to main menu...")
        else:
            print("\n❌ Invalid choice! Please enter 0-8.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
