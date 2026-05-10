# 🕵️ Production Debugging Scenarios — Real-World Problem Solving
> **Goal:** Master the "Troubleshooting" round of interviews by learning how to fix common production failures in agentic systems.

---

## 🧭 Scenario 1: "The Agent is Looping"
**Problem:** A user reports that the researcher agent is searching for the same topic 50 times in a row.
- **Hinglish Analysis:** Agent ko lag raha hai ki use "Better info" chahiye, par wo mil nahi rahi.
- **Solution:** 
    1. Set a hard `max_iterations` limit.
    2. Check the "Supervisor" logic—maybe the feedback loop is too strict?
    3. Update the prompt to say: "If you don't find data in 3 tries, stop and report what you have."

---

## 🕵️ Scenario 2: "Sudden Cost Spike"
**Problem:** Your OpenAI bill jumped from $10/day to $500/day overnight.
- **Hinglish Analysis:** Ya toh koi DDoS attack hai, ya kisi agent ne infinite loop mein GPT-4 ko call karna shuru kiya hai.
- **Solution:**
    1. Check LangSmith traces for the highest token usage threads.
    2. Implement **Rate Limiting** per user.
    3. Switch to a cheaper model for non-critical reasoning steps.

---

## 🐢 Scenario 3: "High Latency (The 30-second delay)"
**Problem:** Users are complaining that the agent takes too long to respond.
- **Hinglish Analysis:** Pipeline mein kahin "Bottleneck" hai—ya toh search tool slow hai ya model response.
- **Solution:**
    1. Use **Streaming** so users see text immediately.
    2. Run tool calls in **Parallel** (`asyncio.gather`).
    3. Check if the "System Prompt" is too long (Parsing overhead).

---

## 👻 Scenario 4: "Hallucinated Tool Parameters"
**Problem:** The agent is trying to call `search_web(query='...', year=2026)` but the tool doesn't accept a `year` parameter.
- **Hinglish Analysis:** AI hoshiyari dikha raha hai aur parameters invent kar raha hai.
- **Solution:**
    1. Use **Pydantic** for strict schema validation.
    2. Send the "Schema Error" back to the AI: "Invalid parameter 'year'. Please try again with valid ones."
    3. Improve the tool description to explicitly say: "Do NOT use other parameters."

---

## 🔒 Scenario 5: "Data Leakage Alert"
**Problem:** User A reported they saw User B's private documents in the agent's response.
- **Hinglish Analysis:** Thread isolation fail ho gayi hai ya Vector DB mein filtering nahi hai.
- **Solution:**
    1. Implement **Namespace filtering** in the Vector DB.
    2. Ensure every RAG query includes a `user_id` metadata filter.
    3. Clear the agent's short-term memory after every session.

---

## 📝 6. How to approach these in an interview?
1. **Clarify:** "Is this happening for all users or just one?"
2. **Hypothesize:** "It could be a prompt issue or a race condition in the state."
3. **Trace:** "I would check the LangSmith logs for the specific Thread ID."
4. **Fix:** "I would implement [Solution] and then run a regression test."

---

> **Expert Tip:** In production, **"It works on my machine"** means nothing. Show that you think about **Telemetry, Logs, and Safety** above all else.
