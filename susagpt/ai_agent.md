# SusaGPT AI Agent — Web Search Architecture

SusaGPT incorporates a lightweight, zero-dependency metasearch agent designed to automatically resolve queries that are not present in SusaLabs' local knowledge base (e.g. today's date, weather, general world facts) without manual intervention.

---

## 🚀 Key Features & Performance

### 1. Sub-Second Speed (Ultra-Fast)
Unlike traditional search agents that spin up heavy headless browsers (like Selenium, Playwright, or Puppeteer) or run complex javascript runtimes, this agent sends a raw HTTP POST request directly to the DuckDuckGo static HTML endpoint. 
- **Latency**: Typically **500ms - 900ms** total query execution time.
- **Efficiency**: Pure string splits and regex-based content extraction minimize CPU overhead, rendering immediate answers to the user.

### 2. Cloudflare & Bot Protection Bypass
Search engines like Google and DuckDuckGo's main AJAX interfaces enforce heavy Cloudflare verification, JS challenges, and CAPTCHAs for automated scripts. SusaGPT bypasses this because:
- It targets the DuckDuckGo **HTML-only fallback engine** (`html.duckduckgo.com/html/`) designed specifically for low-bandwidth and legacy browsers.
- This legacy form action does not load or require JavaScript execution, preventing standard anti-bot fingerprinting from triggering.
- Requests mimic standard browser form submissions (using POST requests with configured header strings), making it indistinguishable from human searches.

### 3. Open-Source & Zero-Dependency
- SusaGPT uses pure Python standard libraries (`urllib.request`, `urllib.parse`, `re`) for all network operations and HTML parsers.
- No heavy third-party packages (like `requests`, `beautifulsoup4`, or `scrapy`) are required.

---

## 🛠️ How It Works

### Step 1: Query Intent Detection
When the user submits a prompt, SusaGPT runs a local TF-IDF overlap check against SusaLabs' service dataset (`data.txt`). 
- If the overlap score is **`> 0.15`**, it triggers standard SusaLabs RAG context routing.
- If the score is **`<= 0.15`**, it detects that the query is outside SusaLabs' knowledge base and flags it for web search (`is_web = True`).

### Step 2: Visual Searching Label
To ensure premium UX (similar to Gemini and ChatGPT), the agent instantly yields:
```
🔍 Web searching...
```
This serves as a visual loading state while the background POST request is happening.

### Step 3: Direct Answer & Snippet Parsing
1. It queries `https://html.duckduckgo.com/html/` with a POST parameter `q=query`.
2. It extracts the **Zero Click Abstract** (direct instant answer box) if present (e.g., for queries like "today's date" or basic definitions).
3. If no abstract is found, it extracts the top 3 organic result snippets from `class="result__snippet"` tags.

### Step 4: Hybrid Completion Summarization
The retrieved snippets are compiled and routed to the active LLM context:
- **Ollama completion**: If a local Ollama instance (`qwen3.5:0.8b`) is running, it feeds the web text as context and streams a concise Hinglish summary.
- **Cloud models**: If Gemini or OpenAI API keys are configured, they generate and stream the final Hinglish completion.
- **Offline raw fallback**: If no active LLM completes the task, SusaGPT streams the exact extracted web sources directly to the terminal.

---

## ❓ Why Not CrewAI, LangChain, or Other GitHub Open-Source Agent Frameworks?

SusaGPT purposely avoids using frameworks like **CrewAI**, **LangChain Agentic Loops**, or **AutoGen** due to the following critical architectural constraints:

| Metric / Feature | SusaGPT Custom Metasearch Agent | CrewAI / LangChain Agents |
| :--- | :--- | :--- |
| **Execution Latency** | **Sub-second (500ms - 900ms)** | **5 to 15+ seconds** (due to multiple sequential LLM planning calls) |
| **Dependencies** | **Zero external dependencies** (uses standard python libraries) | **Heavy dependency tree** (Pydantic, ChromaDB, Langchain core, etc.) |
| **API Keys** | **None required** (free static fallback POST requests) | **Required** (assumes paid search APIs like SerpAPI or Tavily) |
| **Resource Footprint** | **Minimal (less than 1KB of memory overhead)** | **Heavy (tens of MBs of memory overhead)** |
| **Bypass Stability** | **High** (uses legacy endpoints resembling standard form inputs) | **Low** (standard automated library headers trigger bot-protection walls) |

