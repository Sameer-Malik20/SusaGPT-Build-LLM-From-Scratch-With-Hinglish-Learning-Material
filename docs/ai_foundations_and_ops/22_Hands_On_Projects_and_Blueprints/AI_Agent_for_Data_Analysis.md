# 📈 Project: AI Agent for Data Analysis (PandasAgent)
> **Level:** Advanced | **Language:** Hinglish | **Goal:** Ek aisa AI agent build karein jo CSV file lekar user ke question ko samajh sake, Python code likh sake, use execute kar sake, aur charts show kar sake; jisme Code Interpreters, LangChain Agents, aur 2026 mein "Autonomous Analysts" banane ki strategies ko explore kiya gaya ho.

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
- **Code Execution Risk:** AI ye likh sakta hai `import os; os.system("rm -rf /")`. **Fix: Apne main server par AI code ko kabhi bhi run na karein! Docker Container ya kisi Sandboxed REPL (jaise E2B) ka use karein.**
- **Inaccurate Code:** AI "NULL" values ko handle karna bhool gaya, jisse calculation galat ho gayi. **Fix: System prompt mein agent ko batayein: "Always check for NaNs before calculating."**
- **Large Dataset:** Agar CSV 10GB ki hai, toh LLM poori file ko nahi dekh sakta. **Fix: LLM ko sirf 'df.head()' aur 'df.describe()' hi bhejein taaki use schema pata chal sake.**

---

## 🛡️ 8. 2026 Strategy: Tool-calling vs. Code Generation
- **Tool-calling:** Agent ek function `calculate_sum(col)` ko call karta hai. (Zyada safe par kam flexible).
- **Code Generation:** Agent raw Python code likhta hai. (Ultimate power par risky/dangerous).
- **2026 Best Practice:** Ek restricted sandbox ke andar **Open Interpreter** (Open source code interpreter) ka use karein.

---

## ✅ 9. Project Checklist
- [ ] CSV file successfully parse ho gayi ho.
- [ ] Agent basic stats (mean, max, min) ke answers de sakta ho.
- [ ] Agent ek `.png` chart create aur save kar sakta ho.
- [ ] Security sandbox implement kar diya gaya ho.
- [ ] UI clean ho aur data table show kar raha ho.

---

## 🚀 10. Future Improvements (Phase 2)
- **Multi-file Analysis:** "Sales" aur "Inventory" CSVs ko aapas mein connect karna.
- **Natural Language SQL:** Agent ko ek **PostgreSQL** database se connect karna.
- **Predictive Analytics:** Agent ko "Next month's sales ko predict karne" ke liye ek `scikit-learn` model build karne ke liye bolna.
