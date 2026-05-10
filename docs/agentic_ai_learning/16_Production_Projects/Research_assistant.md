# 🔍 Project: Autonomous Research Assistant (Beginner)
> **Goal:** Build an agent that takes a topic, searches the internet, and writes a structured summary report.

---

## 🏗️ 1. Architecture
We use a **Looping Search Pattern**.
- **Input:** User query (e.g., "Future of EVs in 2026").
- **Tools:** Tavily Search API or DuckDuckGo.
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
- **Tool Tracing:** Monitor how many search calls were made and the quality of URLs found.
- **Cost Tracking:** Logging tokens used for summarization.

---

## 📊 5. Evaluation
- **Hallucination Check:** Verify if the facts in the report match the search snippets.
- **Completeness:** Does the report cover all sub-topics mentioned in the query?

---

## 🛡️ 6. Security
- **API Key Protection:** Use environment variables.
- **Source Filtering:** Prevent the agent from visiting "Blacklisted" or harmful domains.

---

## 🚀 7. Deployment
- **GitHub Actions:** Automate testing.
- **Platform:** Vercel (Python Runtime) or AWS Lambda.

---

## 📈 8. Scaling
- **Async Execution:** Use `asyncio.gather` to search 5 topics simultaneously.
- **Concurrency:** Allow multiple users to run research tasks in the background.

---

## 💰 9. Cost Optimization
- **Summarization Tiering:** Use GPT-4o-mini for initial summaries and GPT-4o only for the final polishing.
- **Snippet Limiting:** Only send the most relevant 200 words from each search result.

---

## ⚠️ 10. Failure Handling
- **No Results Found:** If search returns empty, ask the user to provide more keywords.
- **Rate Limit:** If Tavily is down, fallback to DuckDuckGo search tool.

---
