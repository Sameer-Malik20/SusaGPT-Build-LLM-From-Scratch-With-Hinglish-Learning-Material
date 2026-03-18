"""
╔══════════════════════════════════════════════════════════╗
║      🤖  AI AGENTS — Interactive Demo & Exercises        ║
║      Docs: docs/ai/AI_Agents_Guide.md                    ║
╚══════════════════════════════════════════════════════════╝

Run: python ai_agents_demo.py
No extra dependencies required!
"""

import os
import time
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# ─────────────────────────────────────────────────────────
# TOOLS (Simulated)
# ─────────────────────────────────────────────────────────

def weather_tool(city):
    """Simulated weather API"""
    fake_weather = {
        "Mumbai": {"temp": 30, "condition": "Sunny ☀️", "rain": False},
        "Delhi": {"temp": 25, "condition": "Cloudy ⛅", "rain": False},
        "Bangalore": {"temp": 22, "condition": "Rainy 🌧️", "rain": True},
        "Chennai": {"temp": 33, "condition": "Hot 🔥", "rain": False},
        "Kolkata": {"temp": 28, "condition": "Rainy 🌧️", "rain": True},
    }
    data = fake_weather.get(city, {"temp": 25, "condition": "Clear 🌤️", "rain": False})
    print(f"    🌐 [Weather API called for '{city}'] → {data}")
    return data


def web_search_tool(query):
    """Simulated web search"""
    fake_results = {
        "python tutorials": ["Python.org docs", "Real Python", "W3Schools Python"],
        "machine learning": ["Coursera ML", "Fast.ai", "Kaggle Courses"],
        "ai trends 2026": ["MIT Tech Review", "Wired AI", "VentureBeat"],
    }
    for key in fake_results:
        if key in query.lower():
            results = fake_results[key]
            print(f"    🔍 [Web search: '{query}'] → {results}")
            return results
    results = [f"Result 1 for '{query}'", f"Result 2 for '{query}'"]
    print(f"    🔍 [Web search: '{query}'] → {results}")
    return results


def calculator_tool(expression):
    """Simple calculator"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        print(f"    🧮 [Calculator: '{expression}'] → {result}")
        return result
    except Exception as e:
        return f"Error: {e}"


def reminder_tool(message):
    """Simulated reminder"""
    print(f"    📅 [Reminder set: '{message}']")
    return f"Reminder created: {message}"


# ─────────────────────────────────────────────────────────
# DEMO 1: Simple Weather Agent (Think → Act → Observe)
# ─────────────────────────────────────────────────────────
def demo_weather_agent():
    clear()
    print("=" * 60)
    print("  🌤️   DEMO 1: Weather Agent (Think → Act → Observe)")
    print("=" * 60)

    print("\n  Ye agent 3 cities ka weather check karega")
    print("  aur baarish hone par umbrella reminder dega.\n")

    cities_input = input("  Cities (comma separated, Enter = default 3): ").strip()
    if cities_input:
        cities = [c.strip() for c in cities_input.split(",")]
    else:
        cities = ["Mumbai", "Bangalore", "Delhi"]

    print(f"\n{'─'*55}")
    print(f"  🎯 Goal: {cities} ka weather check karo, rain? → reminder do")
    print(f"{'─'*55}\n")

    rainy_cities = []
    sunny_cities = []

    for step, city in enumerate(cities, 1):
        print(f"\n  📍 STEP {step}: {city}")
        print(f"  ─────────────────────────────────")

        # THINK
        print(f"  🤔 THINK: '{city}' ka weather fetch karna hai")
        time.sleep(0.5)

        # ACT
        print(f"  ⚡ ACT: weather_tool('{city}')")
        data = weather_tool(city)
        time.sleep(0.3)

        # OBSERVE
        print(f"  👁️  OBSERVE: {city} = {data['temp']}°C, {data['condition']}")

        if data["rain"]:
            rainy_cities.append(city)
            print(f"  🤔 THINK: Baarish hai! Reminder set karo")
            print(f"  ⚡ ACT: reminder_tool('☂️ {city}: Umbrella le jao!')")
            reminder_tool(f"☂️ {city}: Umbrella zaroor le jao!")
        else:
            sunny_cities.append(city)
        time.sleep(0.5)

    # GOAL COMPLETE
    print(f"\n{'─'*55}")
    print(f"  ✅ GOAL COMPLETE!")
    print(f"\n  📊 Final Report:")
    if rainy_cities:
        print(f"  🌧️  Baarish: {', '.join(rainy_cities)} → Umbrella reminder set!")
    if sunny_cities:
        print(f"  ☀️  Clear:   {', '.join(sunny_cities)} → Enjoy the weather!")
    print(f"\n  Total steps: {len(cities) * 2 + len(rainy_cities)}")


# ─────────────────────────────────────────────────────────
# DEMO 2: Research Agent (Multi-Step)
# ─────────────────────────────────────────────────────────
def demo_research_agent():
    clear()
    print("=" * 60)
    print("  🔍  DEMO 2: Research Agent (Multi-Step Task)")
    print("=" * 60)

    topic = input("\n  Research topic kya hai? (Enter = 'machine learning'): ").strip()
    if not topic:
        topic = "machine learning"

    print(f"\n  🎯 Goal: '{topic}' ke baare me research karo aur summary do\n")
    print(f"{'─'*55}")

    memory = {"topic": topic, "results": [], "summary": ""}

    # Step 1: Search
    print(f"\n  📋 PLAN:")
    print(f"    Step 1 → Web search karo")
    print(f"    Step 2 → Related terms search karo")
    print(f"    Step 3 → Summary banao")
    time.sleep(1)

    print(f"\n{'─'*55}")
    print(f"  🔄 EXECUTION:\n")

    # Step 1
    print(f"  STEP 1: Main search")
    print(f"  🤔 Think: '{topic}' search karo")
    print(f"  ⚡ Act: web_search('{topic}')")
    results1 = web_search_tool(topic)
    memory["results"].extend(results1)
    print(f"  👁️  Observe: {len(results1)} results mili")
    time.sleep(0.5)

    # Step 2
    print(f"\n  STEP 2: Related search")
    related_query = f"{topic} best resources"
    print(f"  🤔 Think: Related topics bhi search karo")
    print(f"  ⚡ Act: web_search('{related_query}')")
    results2 = web_search_tool(related_query)
    memory["results"].extend(results2)
    print(f"  👁️  Observe: {len(results2)} more results mili")
    time.sleep(0.5)

    # Step 3: Summarize
    print(f"\n  STEP 3: Summary banana")
    print(f"  🤔 Think: {len(memory['results'])} results se summary banao")
    print(f"  ⚡ Act: generate_summary(results)")
    time.sleep(0.5)

    # Simulated summary
    summary = f"""
    📖 Research Summary for '{topic}':
    
    Sources found: {len(memory['results'])}
    Top sources:
    {chr(10).join(f'  • {r}' for r in memory['results'][:4])}
    
    Key insight: Multiple high-quality resources available.
    Recommended starting point: {memory['results'][0] if memory['results'] else 'N/A'}
    """
    print(f"  👁️  Observe: Summary generated!")

    print(f"\n{'─'*55}")
    print(f"  ✅ GOAL COMPLETE!")
    print(summary)


# ─────────────────────────────────────────────────────────
# DEMO 3: Build Your Own Agent
# ─────────────────────────────────────────────────────────
def demo_build_agent():
    clear()
    print("=" * 60)
    print("  🔨  DEMO 3: Apna Agent Banao!")
    print("=" * 60)

    available_tools = {
        "1": ("weather_tool", "City ka weather batao", weather_tool),
        "2": ("web_search_tool", "Web search karo", web_search_tool),
        "3": ("calculator_tool", "Math calculate karo", calculator_tool),
        "4": ("reminder_tool", "Reminder set karo", reminder_tool),
    }

    print(f"\n  Available Tools:")
    for k, (name, desc, _) in available_tools.items():
        print(f"    {k}. {name} → {desc}")

    print(f"\n  Apna goal likho:")
    goal = input("  Goal: ").strip()
    if not goal:
        goal = "Bangalore ka weather check karo aur calculator se 2+2 nikalo"

    print(f"\n  🎯 Goal: {goal}")
    print(f"\n  Ab manually steps design karo (Think → Act → Observe loop):\n")

    step = 1
    total_results = []

    while True:
        print(f"\n  {'─'*50}")
        print(f"  STEP {step}:")
        print(f"  🤔 Think karo — kya karna chahiye?")
        think = input(f"    Thought: ").strip()
        if not think or think.lower() in ["done", "complete", "finish"]:
            break

        print(f"\n  ⚡ Kaunsa tool use karna hai?")
        for k, (name, desc, _) in available_tools.items():
            print(f"    {k}. {name}")
        tool_choice = input(f"    Tool (1-4, Enter = skip): ").strip()

        if tool_choice in available_tools:
            tool_name, desc, func = available_tools[tool_choice]
            param = input(f"    Tool input (parameter): ").strip()
            if param:
                print(f"\n  ⚡ ACT: {tool_name}('{param}')")
                result = func(param)
                total_results.append(result)
                print(f"  👁️  OBSERVE: {result}")

        step += 1
        cont = input(f"\n  Continue? (Enter=yes, 'done'=finish): ").strip()
        if cont.lower() in ["done", "no", "n", "quit"]:
            break

    print(f"\n{'─'*55}")
    print(f"  ✅ Agent Complete! Total steps: {step-1}")
    print(f"  📊 Results collected: {len(total_results)}")


# ─────────────────────────────────────────────────────────
# EXERCISE + TEST
# ─────────────────────────────────────────────────────────
def exercise():
    clear()
    print("=" * 60)
    print("  ✏️   EXERCISE: AI Agents Concept Test")
    print("=" * 60)

    questions = [
        {
            "q": "Q1: AI Agent aur Chatbot me main fark kya hai?",
            "options": ["A) Cost me fark hai",
                        "B) Agent tools use kar sakta hai, multi-step kaam kar sakta hai", 
                        "C) Chatbot zyada intelligent hota hai",
                        "D) Agent sirf images process karta hai"],
            "answer": "B",
            "exp": "Chatbot sirf text generate karta hai. Agent plan banata hai, tools use karta hai, actions leta hai!"
        },
        {
            "q": "Q2: Agent ka core loop kya hai?",
            "options": ["A) Read → Write → Save",
                        "B) Train → Evaluate → Deploy",
                        "C) Think → Act → Observe → Repeat",
                        "D) Input → Output → Done"],
            "answer": "C",
            "exp": "Think (kya karna hai?) → Act (tool chalao) → Observe (result dekho) → Repeat till goal complete!"
        },
        {
            "q": "Q3: Memory ka role kya hai AI agent me?",
            "options": ["A) Training speed badhana",
                        "B) Past context, task state aur user preferences yaad rakhna",
                        "C) Model compress karna",
                        "D) API calls reduce karna"],
            "answer": "B",
            "exp": "Memory se agent repetitive context nahi poochta, long workflows handle kar sakta hai!"
        },
        {
            "q": "Q4: Multi-agent system kab use karo?",
            "options": ["A) Simple Q&A ke liye",
                        "B) Single tool use ke liye",
                        "C) Jab task complex ho, multiple specialized skills chahiye hon",
                        "D) GPU save karne ke liye"],
            "answer": "C",
            "exp": "Complex tasks, specialization needed, parallel work possible → Multi-agent best hai!"
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
        print("  🏆 PERFECT! AI Agents concept clear hai!")
    elif score >= 3:
        print("  👍 Bahut achha! Demos try karo.")
    else:
        print("  📖 AI_Agents_Guide.md phir se padho!")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
def main():
    while True:
        clear()
        print("=" * 60)
        print("  🤖  AI AGENTS — Interactive Demo")
        print("  📄  Ref: docs/ai/AI_Agents_Guide.md")
        print("=" * 60)
        print()
        print("    1. 🌤️   Weather Agent (Think→Act→Observe loop dekho)")
        print("    2. 🔍   Research Agent (Multi-step task)")
        print("    3. 🔨   Apna Agent Banao! (khud design karo)")
        print("    4. ✏️   AI Agents MCQ Test (score dekho!)")
        print()
        print("    0. 🔙  Back / Exit")
        print()

        choice = input("  Choice (0-4): ").strip()

        if choice == "1":
            demo_weather_agent()
            input("\n↩️  Enter dabao...")
        elif choice == "2":
            demo_research_agent()
            input("\n↩️  Enter dabao...")
        elif choice == "3":
            demo_build_agent()
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
