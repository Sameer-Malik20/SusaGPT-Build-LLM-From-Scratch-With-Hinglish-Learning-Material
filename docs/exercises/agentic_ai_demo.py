"""
╔══════════════════════════════════════════════════════════╗
║      🧩  AGENTIC AI — Live Demo & Exercises             ║
║      Docs: docs/ai/Agentic_AI_Guide.md                   ║
╚══════════════════════════════════════════════════════════╝

Run: python agentic_ai_demo.py
No extra dependencies required!
"""

import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# ─────────────────────────────────────────────────────────
# Simulated Tools
# ─────────────────────────────────────────────────────────
def web_search(query):
    """Simulated web search"""
    fake_results = {
        "openai": {"product": "ChatGPT", "users": "500M+", "pricing": "$20/month", "founded": 2015},
        "anthropic": {"product": "Claude", "users": "50M+", "pricing": "$15/month", "founded": 2021},
        "google": {"product": "Gemini", "users": "1B+", "pricing": "Free + Pro $20", "founded": 1998},
        "meta": {"product": "Llama", "users": "Millions", "pricing": "Open Source Free", "founded": 2004},
        "mistral": {"product": "Mistral AI", "users": "Growing", "pricing": "API based", "founded": 2023},
    }
    for company, data in fake_results.items():
        if company.lower() in query.lower():
            print(f"    🔍 [Search: '{query}'] → Found data!")
            return data
    print(f"    🔍 [Search: '{query}'] → Generic result")
    return {"product": query, "users": "Unknown", "pricing": "Unknown", "founded": "Unknown"}


def analyze_data(data, metric="market_position"):
    """Analyze company data"""
    if "users" in data:
        users_str = data["users"]
        if "B+" in users_str or "500M" in users_str:
            position = "Dominant 🏆"
        elif "50M" in users_str or "Millions" in users_str:
            position = "Strong 💪"
        else:
            position = "Growing 🌱"
    else:
        position = "Unknown"

    print(f"    📊 [Analyze: {data.get('product', '?')}] → {position}")
    return {"market_position": position, "pricing_model": data.get("pricing", "?")}


def write_report_section(company, data, analysis):
    """Write a report section"""
    section = f"""
  ## {company}
  - Product: {data.get('product', '?')}
  - Market Position: {analysis['market_position']}
  - Pricing: {analysis['pricing_model']}
  - Founded: {data.get('founded', '?')}"""
    print(f"    ✍️  [Writing section for {company}]")
    return section


# ─────────────────────────────────────────────────────────
# DEMO 1: Competitor Research Agent
# ─────────────────────────────────────────────────────────
def demo_competitor_research():
    clear()
    print("=" * 60)
    print("  🔍  DEMO 1: Competitor Research Agentic System")
    print("=" * 60)

    print("\n  Ye agentic system competitors research karke")
    print("  ek full report generate karega — automatically!\n")

    default = "OpenAI,Anthropic,Google"
    companies_input = input(f"  Companies (comma separated, Enter = '{default}'): ").strip()
    companies = [c.strip() for c in (companies_input or default).split(",")]

    print(f"\n  🎯 Goal: {companies} ki research report banao")
    print(f"\n{'─'*55}")
    print(f"  📋 PLAN:")
    print(f"    Step 1: Har company ka data search karo")
    print(f"    Step 2: Data analyze karo")
    print(f"    Step 3: Report section likho")
    print(f"    Step 4: Final report assemble karo")
    print(f"{'─'*55}\n")

    time.sleep(1)
    report_sections = []
    state = {"processed": 0, "total": len(companies)}

    for company in companies:
        print(f"\n  🏢 Processing: {company}")
        print(f"  ─────────────────────────────")

        # Think
        print(f"  🤔 Think: '{company}' ka data chahiye")
        time.sleep(0.3)

        # Act: Search
        print(f"  ⚡ Act: web_search('{company}')")
        data = web_search(company)
        time.sleep(0.3)

        # Observe
        print(f"  👁️  Observe: Data mila — {data.get('product', '?')}")

        # Think again
        print(f"  🤔 Think: Data analyze karo")
        time.sleep(0.3)

        # Act: Analyze
        print(f"  ⚡ Act: analyze_data({company})")
        analysis = analyze_data(data)
        time.sleep(0.3)

        # Act: Write
        print(f"  ⚡ Act: write_section({company})")
        section = write_report_section(company, data, analysis)
        report_sections.append(section)
        time.sleep(0.2)

        state["processed"] += 1
        print(f"  ✅ [{state['processed']}/{state['total']}] {company} done!")
        time.sleep(0.5)

    # Final report
    print(f"\n{'─'*55}")
    print(f"  🤔 Think: Saare sections ready hain, report assemble karo")
    time.sleep(0.5)
    print(f"\n{'='*55}")
    print(f"  📄 FINAL RESEARCH REPORT")
    print(f"{'='*55}")
    for section in report_sections:
        print(section)
    print(f"\n{'='*55}")
    print(f"  ✅ GOAL COMPLETE! {len(companies)} companies analyzed.")
    print(f"  Total agentic steps: {len(companies) * 3 + 1}")


# ─────────────────────────────────────────────────────────
# DEMO 2: Autonomy Levels Interactive
# ─────────────────────────────────────────────────────────
def demo_autonomy_levels():
    clear()
    print("=" * 60)
    print("  🎛️   DEMO 2: Autonomy Levels — Kya Difference Hai?")
    print("=" * 60)

    goal = "Delete old log files to free up disk space"
    print(f"\n  🎯 Goal: '{goal}'\n")

    print(f"  Autonomy ka level choose karo:\n")
    print(f"    1. 🟢 Low Autonomy    (har step pe confirm)")
    print(f"    2. 🟡 Medium Autonomy (sirf risky actions me confirm)")
    print(f"    3. 🔴 High Autonomy   (khud hi sab kare)")

    level = input("\n  Choice (1/2/3): ").strip() or "2"

    actions = [
        {"step": "List all log files", "risky": False},
        {"step": "Filter files older than 30 days", "risky": False},
        {"step": "DELETE 15 log files (permanent!)", "risky": True},
        {"step": "Send completion report", "risky": False},
    ]

    print(f"\n{'─'*55}")

    for i, action in enumerate(actions, 1):
        risk = "⚠️ Risky" if action["risky"] else "✅ Safe"
        print(f"\n  Step {i}: {action['step']} [{risk}]")

        if level == "1":
            # Low: har step pe confirm
            confirm = input(f"  Proceed? (y/n): ").strip().lower()
            if confirm == "y":
                print(f"  ✅ Executing...")
                time.sleep(0.3)
            else:
                print(f"  ⛔ Step skipped by user")

        elif level == "2":
            # Medium: sirf risky actions me confirm
            if action["risky"]:
                confirm = input(f"  ⚠️  Risky action! Confirm? (y/n): ").strip().lower()
                if confirm != "y":
                    print(f"  ⛔ Risky step skipped!")
                    continue
            print(f"  ✅ Executing...")
            time.sleep(0.3)

        else:
            # High: khud hi sab kare
            print(f"  🤖 Auto-executing...")
            time.sleep(0.5)
            if action["risky"]:
                print(f"  ⚠️  WARNING: Risky action khud complete ho gaya!")

    print(f"\n{'─'*55}")
    print(f"  📊 Summary:")
    if level == "1":
        print(f"  🟢 Low Autonomy: Full human control, safest!")
    elif level == "2":
        print(f"  🟡 Medium: Routine tasks auto, risky ones confirm.")
    else:
        print(f"  🔴 High: Fast but dangerous! Careful use karo.")


# ─────────────────────────────────────────────────────────
# DEMO 3: Reflection Loop
# ─────────────────────────────────────────────────────────
def demo_reflection():
    clear()
    print("=" * 60)
    print("  🔄  DEMO 3: Reflection Loop — Agent Apni Galti Pakadta Hai")
    print("=" * 60)

    goal = "Write a Python function to reverse a string"
    print(f"\n  🎯 Goal: {goal}\n")
    print(f"  Agentic system reflection ke saath sochega...\n")
    time.sleep(0.5)

    iterations = [
        {
            "attempt": 1,
            "think": "String reverse karne ke liye loop use karo",
            "act": "Write code",
            "code": "def reverse(s):\n    result = ''\n    for i in range(len(s)):\n        result = s[i] + result\n    return result",
            "observe": "Code works but verbose",
            "reflect": "Kya better way hai? Python me slicing use kar sakte hain!",
            "done": False
        },
        {
            "attempt": 2,
            "think": "Python slicing [::-1] use karo — cleaner!",
            "act": "Rewrite code",
            "code": "def reverse(s):\n    return s[::-1]",
            "observe": "Clean, Pythonic, works perfectly!",
            "reflect": "Ye much better hai. Goal complete!",
            "done": True
        }
    ]

    for iteration in iterations:
        print(f"\n  {'─'*50}")
        print(f"  🔁 ITERATION {iteration['attempt']}:")
        print(f"\n  🤔 THINK: {iteration['think']}")
        time.sleep(0.5)

        print(f"\n  ⚡ ACT: {iteration['act']}")
        print(f"  Code:")
        for line in iteration["code"].split("\n"):
            print(f"    {line}")
        time.sleep(0.5)

        print(f"\n  👁️  OBSERVE: {iteration['observe']}")
        time.sleep(0.3)

        print(f"\n  🤔 REFLECT: {iteration['reflect']}")
        time.sleep(0.5)

        if iteration["done"]:
            print(f"\n  ✅ GOAL COMPLETE! Reflection ne better solution dhundha.")
        else:
            print(f"\n  🔄 Improve kar rahe hain → Next iteration...")
            input("  Enter dabao next iteration ke liye...")


# ─────────────────────────────────────────────────────────
# EXERCISE + TEST
# ─────────────────────────────────────────────────────────
def exercise():
    clear()
    print("=" * 60)
    print("  ✏️   EXERCISE: Agentic AI Concept Test")
    print("=" * 60)

    questions = [
        {
            "q": "Q1: Generative AI aur Agentic AI me main fark?",
            "options": ["A) Koi fark nahi",
                        "B) Generative AI content banata hai, Agentic AI goals pursue karta hai",
                        "C) Agentic AI sirf images banata hai",
                        "D) Generative AI zyada expensive hai"],
            "answer": "B",
            "exp": "GenAI = content generation. Agentic AI = goal achievement, tools, multi-step actions!"
        },
        {
            "q": "Q2: Reflection ka purpose kya hai agentic system me?",
            "options": ["A) Memory clear karna",
                        "B) Action ke result dekhkar next step improve karna",
                        "C) Temperature adjust karna",
                        "D) Model restart karna"],
            "answer": "B",
            "exp": "Reflection = result evaluate karo → kya galat tha? → next step better banao. Self-correction!"
        },
        {
            "q": "Q3: Agentic AI, Workflow Automation se kaise alag hai?",
            "options": ["A) Agentic AI faster hai",
                        "B) Workflow automation dynamic decisions leta hai",
                        "C) Agentic AI dynamic decisions leta hai, uncertain cases handle karta hai",
                        "D) Koi fark nahi"],
            "answer": "C",
            "exp": "Automation = fixed predefined path. Agentic AI = adaptive path, unexpected cases handle karta hai!"
        },
        {
            "q": "Q4: Kab Agentic AI suitable nahi hota?",
            "options": ["A) Complex multi-step task",
                        "B) Simple FAQ answering (chatbot better hai)",
                        "C) Research report generation",
                        "D) Multi-tool workflow"],
            "answer": "B",
            "exp": "Simple Q&A ke liye plain chatbot better hai. Agentic AI overhead add karta hai unnecessarily!"
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
        print("  🏆 PERFECT! Agentic AI concepts clear hain!")
    else:
        print("  📖 Agentic_AI_Guide.md + demos phir se dekho!")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
def main():
    while True:
        clear()
        print("=" * 60)
        print("  🧩  AGENTIC AI — Interactive Demo")
        print("  📄  Ref: docs/ai/Agentic_AI_Guide.md")
        print("=" * 60)
        print()
        print("    1. 🔍   Competitor Research Agent (full agentic loop)")
        print("    2. 🎛️   Autonomy Levels Demo (Low/Medium/High)")
        print("    3. 🔄   Reflection Loop (agent apni galti pakadta hai)")
        print("    4. ✏️   Agentic AI MCQ Test (score dekho!)")
        print()
        print("    0. 🔙  Back / Exit")
        print()

        choice = input("  Choice (0-4): ").strip()

        if choice == "1":
            demo_competitor_research()
            input("\n↩️  Enter dabao...")
        elif choice == "2":
            demo_autonomy_levels()
            input("\n↩️  Enter dabao...")
        elif choice == "3":
            demo_reflection()
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
