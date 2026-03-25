# 📊 LLM Evaluation & Benchmarks — Measuring AI Intelligence (Master Guide)
> **Level:** Intermediate → Advanced | **Language:** Hinglish | **Goal:** Master MMLU, HumanEval, HELM, RAGAS, and LLM-as-a-Judge.

---

## 📋 Table of Contents: How to Judge a Model?

| Type | Name | What it Measures? |
|------|------|-------------------|
| **1. Knowledge** | MMLU | Massive Multitask Language Understanding (57 topics). |
| **2. Code** | HumanEval / MBPP | Python programming and unit tests. |
| **3. Reasoning** | GSM8K / MATH | 8,000 Grade-school math word problems. |
| **4. Alignment** | MT-Bench | Model's ability to follow complex multi-turn commands. |
| **5. RAG** | RAGAS / TruLens | Faithfulness and Relevance in RAG systems. |
| **6. Automation** | LLM-as-a-Judge | GPT-4 judging a 7B model. |

---

## 1. 🌍 The Big Gold Standards (Benchmarks)

AI models ko comparing ke liye specific test sets hote hain.

### A. MMLU (Massive Multitask Language Understanding)
- **Top Topics:** Math, Law, Physics, Medicine.
- **Goal:** Model ki general intelligence (Knowledge) kitni hai?
- **GPT-4 score:** ~86.4%, **Llama-3-70B:** ~82%.

### B. HumanEval
OpenAI ka banaya hua dataset (164 coding problems). Unit tests pass karna hi goal hai.
- **Pass@1:** Pehle code attempt mein model kitne % sahi hai.

### C. GSM8K
Grade school math word problems. Ye model ki **"Logical Reasoning"** test karta hai.
- Isme models aksar Step-by-Step (Chain of Thought) solve karte hain.

---

## 2. 🛡️ Alignment & Chat (MT-Bench)

LLMs hamesha accurate nahi hote, par "Chat" mein helpful hone chahiye.
- **MT-Bench:** 80 multi-turn questions. User 1st question puchta hai, model jawab deta hai, phir 2nd question related to the first context.
- **Result Score:** 1 to 10 (Usually judged by GPT-4).

---

## 3. 🔍 RAG Evaluation (RAGAS Framework)

Retrieval Augmented Generation (RAG) ke liye special metrics hote hain:
1. **Faithfulness:** Kitna model ne actual retrieve kiye hue documents se answer kiya? (No Hallucinations).
2. **Relevance:** Kya answer prompt ke liye useful tha?
3. **Context Precision:** Kya sahi documents top par retrieve huye?

---

## 🚀 The Modern Way: LLM-as-a-Judge

Humans test cases check karne mein thak jate hain.
**Strategy:** Ek powerful model (e.g. GPT-4o-latest) judge banta hai aur hamare fine-tuned 7B/8B model ke answers ko 1-10 points deta hai.
- **Why?** Ye humans se fast hai aur accuracy lagbhag 80-90% humans ke level par milti hai.

---

## 🏗️ Python Tools for Eval

- **LM Evaluation Harness (EleutherAI):** Standard tool to run 200+ benchmarks in 1 command.
- **RAGAS:** For RAG pipeline evaluation.
- **Giskard:** For testing security and bias in AI models.

```bash
# Example command using LM-Eval Harness
# python main.py --model hf-causal --model_args pretrained=meta-llama/Llama-3-8b --tasks mmlu,gsm8k --device cuda:0
```

---

## 📝 Practice Exercise (Critical Thinking)

### Q1: Model A ka MMLU 85% hai par HumanEval 20%. Iska kya matlab hai?
**Answer:** Model ke paas bohot knowledge hai (Knowledge rich), par wo code likhne mein bilkul fattu (Bad) hai. Base model level par coding data kam tha.

### Q2: Hallucination kaise measure karein?
**Answer:** "TruthfulQA" benchmark use karo, jo aise questions puchta hai jinka answers insaan galat guess karte hain (False beliefs).

---

## 🔗 Resources
- [LM Evaluation Harness GitHub](https://github.com/EleutherAI/lm-evaluation-harness)
- [MT-Bench (LMSYS Chatbot Arena)](https://chat.lmsys.org/)
- [Stanford HELM (Holistic Evaluation of Language Models)](https://crfm.stanford.edu/helm/latest/)

---

## 🏆 Final Summary Checklist
- [ ] MMLU aur GSM8K mein kya fark hai? (Knowledge vs Logic).
- [ ] RAGAS ke metrics ka naam batao? (Faithfulness, Relevance, Context).
- [ ] LLM-as-a-Judge kyu useful hai? (Cheap, Fast, Reliable scaling).
- [ ] Pass@1 vs Pass@100 (Coding benchmarks level).

> **Expert Insight:** Benchmarks ko blind follow mat karo (Goodhart's Law). Kai baar models test sets par "Overfit" (Ratna) kar lete hain. Real-world output check karna hi असली (real) test hai.
