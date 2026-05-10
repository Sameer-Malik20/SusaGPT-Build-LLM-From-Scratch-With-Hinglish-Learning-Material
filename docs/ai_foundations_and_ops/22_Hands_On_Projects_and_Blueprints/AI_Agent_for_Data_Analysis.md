# 📈 Project: AI Agent for Data Analysis (PandasAgent)
> **Level:** Advanced | **Language:** Hinglish | **Goal:** Build an AI agent that can take a CSV file, understand the user's question, write Python code, execute it, and show charts, exploring Code Interpreters, LangChain Agents, and the 2026 strategies for "Autonomous Analysts."

---

## 🧭 1. Project Overview
Hum ek **"AI Data Scientist"** banayeinge. 
- **The Task:** User ek Excel/CSV file upload karega aur puchega: *"Sales aur Profit ka graph banao."*
- **The Solution:** Ek Agent jo:
  1. File ko scan karta hai.
  2. Python (Pandas + Matplotlib) code likhta hai.
  3. Code ko "Local Environment" mein run karta hai.
  4. Result (Text or Image) user ko dikhata hai.

---

## 🛠️ 2. The Tech Stack
- **Framework:** LangChain (Pandas Dataframe Agent)
- **LLM:** GPT-4o (Best for coding logic)
- **Library:** Pandas, Matplotlib, Seaborn
- **Frontend:** Streamlit (Best for data apps)
- **Environment:** Jupyter Kernel or local Python REPL.

---

## 🏗️ 3. Step 1: Loading the Data
CSV load karke use Agent ke context mein dena.
```python
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

# 1. Load Data
df = pd.read_csv("sales_2026.csv")

# 2. Create the Agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_pandas_dataframe_agent(llm, df, verbose=True)
```

---

## 🧠 4. Step 2: The 'Reasoning' Loop
Jab user puchta hai: *"Sabse zyada sales kis mahine mein hui?"*
1. **Agent Thought:** "I need to group by month and find the max sales."
2. **Agent Action:** `df.groupby('month')['sales'].sum().idxmax()`
3. **Agent Observation:** "June"
4. **Final Answer:** "June mahine mein sabse zyada sales hui thi."

---

## 🚀 5. Step 3: Visualization (The Pro Feature)
Agent ko bolna ki graph banaye.
```python
query = "Monthly profit ka bar chart banao aur save karo as 'profit.png'"
agent.run(query)
# The agent will write: plt.bar(df['month'], df['profit']); plt.savefig('profit.png')
```

---

## 💻 6. Step 4: Building the Streamlit App
```python
import streamlit as st

st.title("📊 SusaLabs AI Data Analyst")

file = st.file_uploader("CSV file upload karein")
if file:
    df = pd.read_csv(file)
    st.write(df.head())
    
    question = st.text_input("Data ke baare mein kya janna hai?")
    if st.button("Analyze"):
        # Run the agent logic here
        response = agent.run(question)
        st.write(response)
        # If a chart was created, show it
        if os.path.exists("profit.png"):
            st.image("profit.png")
```

---

## ❌ 7. Failure Cases & Security (IMPORTANT)
- **Code Execution Risk:** AI can write `import os; os.system("rm -rf /")`. **Fix: Never run AI code on your main server! Use a Docker Container or a Sandboxed REPL (like E2B).**
- **Inaccurate Code:** AI forgot to handle "NULL" values, so the calculation is wrong. **Fix: In the system prompt, tell the agent: "Always check for NaNs before calculating."**
- **Large Dataset:** If the CSV is 10GB, the LLM can't see the whole file. **Fix: Only send the 'df.head()' and 'df.describe()' to the LLM so it knows the schema.**

---

## 🛡️ 8. 2026 Strategy: Tool-calling vs. Code Generation
- **Tool-calling:** The agent calls a function `calculate_sum(col)`. (Safer but less flexible).
- **Code Generation:** The agent writes raw Python. (Ultimate power but dangerous).
- **2026 Best Practice:** Use **Open Interpreter** (Open source code interpreter) inside a restricted sandbox.

---

## ✅ 9. Project Checklist
- [ ] CSV file successfully parsed.
- [ ] Agent can answer basic stats (mean, max, min).
- [ ] Agent can create and save a `.png` chart.
- [ ] Security sandbox implemented.
- [ ] UI is clean and shows the data table.

---

## 🚀 10. Future Improvements (Phase 2)
- **Multi-file Analysis:** Connect "Sales" and "Inventory" CSVs together.
- **Natural Language SQL:** Connect the agent to a **PostgreSQL** database.
- **Predictive Analytics:** Tell the agent to build a `scikit-learn` model to "Predict next month's sales."
