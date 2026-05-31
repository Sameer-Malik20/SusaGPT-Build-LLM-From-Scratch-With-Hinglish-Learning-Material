# 🕵️ Production Debugging Scenarios — Real-World Problem Solving
> **Goal:** Agentic systems mein common production failures ko fix karna seekh kar interviews ke "Troubleshooting" round ko master karein.

---

## 🧭 Scenario 1: "The Agent is Looping"
**Problem:** Ek user report karta hai ki researcher agent same topic ko ek sath 50 times search kar raha hai.
- **Hinglish Analysis:** Agent ko lag raha hai ki use "Better info" chahiye, par wo mil nahi rahi.
- **Solution:** 
    1. Set a hard `max_iterations` limit.
    2. "Supervisor" logic check karein—ho sakta hai feedback loop bahut strict ho?
    3. Prompt ko update karein: "If you don't find data in 3 tries, stop and report what you have."

---

## 🕵️ Scenario 2: "Sudden Cost Spike"
**Problem:** Aapka OpenAI bill overnight $10/day se badhkar $500/day ho gaya.
- **Hinglish Analysis:** Ya toh koi DDoS attack hai, ya kisi agent ne infinite loop mein GPT-4 ko call karna shuru kiya hai.
- **Solution:**
    1. Highest token usage threads ke liye LangSmith traces check karein.
    2. Per user **Rate Limiting** implement karein.
    3. Non-critical reasoning steps ke liye cheaper model par switch karein.

---

## 🐢 Scenario 3: "High Latency (The 30-second delay)"
**Problem:** Users complain kar rahe hain ki agent respond karne mein bahut time leta hai.
- **Hinglish Analysis:** Pipeline mein kahin "Bottleneck" hai—ya toh search tool slow hai ya model response.
- **Solution:**
    1. **Streaming** ka use karein taaki users ko text immediately dikhe.
    2. Tool calls ko **Parallel** (`asyncio.gather`) mein run karein.
    3. Check karein ki kya "System Prompt" bahut long hai (Parsing overhead).

---

## 👻 Scenario 4: "Hallucinated Tool Parameters"
**Problem:** Agent `search_web(query='...', year=2026)` call karne ki koshish kar raha hai par tool `year` parameter accept nahi karta.
- **Hinglish Analysis:** AI hoshiyari dikha raha hai aur parameters invent kar raha hai.
- **Solution:**
    1. Strict schema validation ke liye **Pydantic** use karein.
    2. "Schema Error" wapas AI ko bhejein: "Invalid parameter 'year'. Please try again with valid ones."
    3. Tool description ko improve karein aur explicitly likhein: "Do NOT use other parameters."

---

## 🔒 Scenario 5: "Data Leakage Alert"
**Problem:** User A ne report kiya ki unhe agent ke response mein User B ke private documents dikhe.
- **Hinglish Analysis:** Thread isolation fail ho gayi hai ya Vector DB mein filtering nahi hai.
- **Solution:**
    1. Vector DB mein **Namespace filtering** implement karein.
    2. Ensure karein ki har RAG query mein `user_id` metadata filter shamil ho.
    3. Every session ke baad agent ki short-term memory clear karein.

---

## 📝 6. How to approach these in an interview?
1. **Clarify:** "Kya ye sabhi users ke liye ho raha hai ya sirf ek ke liye?"
2. **Hypothesize:** "Ye prompt issue ho sakta hai ya state mein race condition."
3. **Trace:** "Main specific Thread ID ke liye LangSmith logs check karunga."
4. **Fix:** "Main [Solution] implement karunga aur fir regression test run karunga."

---

> **Expert Tip:** In production, **"It works on my machine"** means nothing. Show that you think about **Telemetry, Logs, and Safety** above all else.
