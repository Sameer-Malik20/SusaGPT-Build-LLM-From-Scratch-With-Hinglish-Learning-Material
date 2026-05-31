# 💻 Project: Smart Coding Assistant (Beginner)
> **Level:** Beginner | **Language:** Hinglish | **Goal:** Ek aisa agent banayein jo natural language request leta hai aur Python code generate, explain, ya debug kar sakta hai.

---

## 🏗️ 1. Architecture
Hum ek **Code-Specialized Prompting** pattern use karte hain.
- **Model:** GPT-4o ya Claude 3.5 Sonnet (Coding ke liye best).
- **Workflow:** Request -> Schema Check -> Code Generation -> Explanation.
- **User Interface:** Ek simple CLI ya web code editor.

---

## 📂 2. Folder Structure
```text
coding_assistant/
├── src/
│   ├── generator.py     # Code generation logic
│   ├── debugger.py      # Error analysis logic
│   └── main.py          # CLI Interface
├── output/              # Saved .py files
├── tests/               # Unit tests for generated code
└── pyproject.toml
```

---

## 💻 3. Full Code (Core Logic)
```python
# Hinglish Logic: Sirf code mangne par LLM ko strict instruction do ki wo Markdown code block mein de
from langchain_openai import ChatOpenAI

def generate_code(request):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    system_msg = "You are an expert Python developer. Return ONLY valid python code."
    
    code_response = llm.invoke([
        ("system", system_msg),
        ("human", f"Write a script for: {request}")
    ])
    
    return code_response.content
```

---

## 🔍 4. Observability
- **Syntactic Validation:** generated code ko dikhane se pehle check karna ki kya wo actually valid Python code hai.
- **Latency Tracking:** Ek 100-line ka script generate karne mein kitna time lagta hai?

---

## 📊 5. Evaluation
- **Execution Test:** Kya code actually run hota hai?
- **Logic Score:** Kya ye user dwara requested specific problem ko solve karta hai?

---

## 🛡️ 6. Security
- **No Direct Execution:** Generated code ko apni host machine par automatically kabhi run na karein (`os.system('rm -rf /')` ka risk).
- **Input Sanitization:** "Code Injection" attacks ko prevent karein jahan user system info steal karne ki koshish karta hai.

---

## 🚀 7. Deployment
- **Web App:** FastAPI ka use karke microservice ke roop mein deploy karein.
- **CLI Tool:** Python library ke roop mein package karein (`pip install my-coding-agent`).

---

## 📈 8. Scaling
- **Model Switching:** Simple "Syntax check" ke liye chote models aur "Logic building" ke liye bade models ka use karein.
- **Caching:** Common code snippets (e.g., "SQL connection string") ko cache karein.

---

## 💰 9. Cost Optimization
- **Temperature=0:** Results ko deterministic rakhta hai aur "Random" token usage ko reduce karta hai.
- **Few-shot examples:** Long explanations ki need ko reduce karne ke liye prompt mein 2-3 code examples provide karein.

---

## ⚠️ 10. Failure Handling
- **Hallucinated Libraries:** Agar AI kisi aisi library ka use karta hai jo exist nahi karti, toh error show karein aur use "Sirf standard libraries use karne" ke liye kahein.
- **Syntax Error:** Agar code parse hone mein fail ho jata hai, toh self-correction ke liye error ko wapas AI ke paas bhejein.

---
