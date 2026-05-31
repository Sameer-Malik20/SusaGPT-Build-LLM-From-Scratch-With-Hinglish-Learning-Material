# 🔍 Project: Autonomous Research Assistant (Beginner)
> **Level:** Beginner | **Language:** Hinglish | **Goal:** Ek aisa agent banayein jo ek topic leta hai, internet par search karta hai, aur ek structured summary report likhta hai.

---

## 🏗️ 1. Architecture
Hum ek **Looping Search Pattern** use karte hain.
- **Input:** User query (e.g., "Future of EVs in 2026").
- **Tools:** Tavily Search API ya DuckDuckGo.
- **Workflow:** Search -> Extract Text -> Summarize -> Format.
- **Output:** Markdown report.

---

## 📂 2. Folder Structure
```text
research_assistant/
├── agents/
│   ├── researcher.py    # Search & Extraction
│   └── writer.py        # Summarization logic
├── tools/
│   └── search_tool.py   # Tavily API Wrapper
├── reports/             # Generated markdown files
├── main.py              # Entry point
└── .env                 # API Keys
```

---

## 💻 3. Full Code (Core Logic)
```python
# Hinglish Logic: Pehle internet se search karo, fir data compile karo
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

def run_research(topic):
    search = TavilySearchResults(max_results=3)
    results = search.run(topic)
    
    context = "\n".join([r['content'] for r in results])
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = f"Based on this info: {context}, write a professional report on {topic}."
    
    report = llm.invoke(prompt)
    return report.content
```

---

## 🔍 4. Observability
- **Tool Tracing:** Monitor karein ki kitne search calls kiye gaye aur mile huye URLs ki quality kaisi thi.
- **Cost Tracking:** Summarization ke liye use huye tokens ko log karna.

---

## 📊 5. Evaluation
- **Hallucination Check:** Verify karein ki kya report ke facts search snippets se match karte hain.
- **Completeness:** Kya report query mein mentioned sabhi sub-topics ko cover karti hai?

---

## 🛡️ 6. Security
- **API Key Protection:** Environment variables ka use karein.
- **Source Filtering:** Agent ko "Blacklisted" ya harmful domains par jaane se prevent karein.

---

## 🚀 7. Deployment
- **GitHub Actions:** Testing ko automate karein.
- **Platform:** Vercel (Python Runtime) ya AWS Lambda.

---

## 📈 8. Scaling
- **Async Execution:** Ek sath 5 topics search karne ke liye `asyncio.gather` ka use karein.
- **Concurrency:** Multiple users ko background mein research tasks run karne ki permission dein.

---

## 💰 9. Cost Optimization
- **Summarization Tiering:** Initial summaries ke liye GPT-4o-mini aur final polishing ke liye hi sirf GPT-4o ka use karein.
- **Snippet Limiting:** Har search result se sirf most relevant 200 words hi bhejein.

---

## ⚠️ 10. Failure Handling
- **No Results Found:** Agar search empty return kare, toh user se aur keywords provide karne ke liye kahein.
- **Rate Limit:** Agar Tavily down ho, toh DuckDuckGo search tool par fallback karein.

---
