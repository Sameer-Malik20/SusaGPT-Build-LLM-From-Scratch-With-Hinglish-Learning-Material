# 📚 RAG Interview Questions — From Retrieval to Reasoning
> **Goal:** Master the specific questions about RAG (Retrieval-Augmented Generation) architectures, vector databases, and evaluation.

---

## 🧭 1. Basics & Fundamentals
1. **"What is the difference between RAG and Fine-tuning?"**
   - *Hinglish Answer:* RAG "Open-book exam" hai (AI source dekh kar batata hai). Fine-tuning "Memorization" hai (AI dimaag mein knowledge store karta hai).
2. **"Explain the RAG Triad."**
   - *Hinglish Answer:* Context Relevance, Faithfulness (Groundedness), aur Answer Relevance.

---

## 🧠 2. Advanced Retrieval
3. **"What are Embeddings and how do they work?"**
   - *Hinglish Answer:* Text ko numbers (vectors) mein badalna taaki "Meaning" ke basis par search kiya ja sake.
4. **"Explain Hybrid Search (BM25 + Vector)."**
   - *Hinglish Answer:* Keyword matching (BM25) aur Semantic meaning (Vector) ka combination.
5. **"What is a Re-ranker and why is it used?"**
   - *Hinglish Answer:* Pehle 50 chunks dhoondho (Fast), fir unhe ek heavy model se re-order karo taaki best 3 upar aa jayein.

---

## 🧪 3. Evaluation & Metrics
6. **"How do you measure RAG performance without human labels?"**
   - *Hinglish Answer:* Using frameworks like **RAGAS** or **DeepEval** (LLM-as-a-Judge).
7. **"What is 'Hallucination' in RAG and how to detect it?"**
   - *Hinglish Answer:* Jab AI document se bahar ki baatein kare. Detect karne ke liye NLI (Natural Language Inference) use karte hain.

---

## 🏗️ 4. System Design & Scale
8. **"How do you handle PDF documents with tables in RAG?"**
   - *Hinglish Answer:* Using specialized parsers like **Unstructured.io** or converting tables into Markdown/JSON before embedding.
9. **"Which vector database would you choose for 1 billion documents?"**
   - *Hinglish Answer:* Pinecone (Managed), Milvus, or Qdrant (High performance at scale).
10. **"What is 'Semantic Chunking'?"**
    - *Hinglish Answer:* Fixed size ke bajaye "Topic change" hone par chunk break karna.

---

## 🚀 5. Advanced RAG Patterns
11. **"What is Agentic RAG?"**
    - *Hinglish Answer:* Jab agent decide karta hai ki use kab search karna hai, kitni baar karna hai, aur kya retrieved data kafi hai.
12. **"Explain Graph-RAG."**
    - *Hinglish Answer:* Knowledge graphs ka use karna entities ke beech relationships dhoondhne ke liye (High reasoning).

---

> **Expert Tip:** RAG interviews often focus on **Edge Cases**. Be ready to talk about "Low retrieval scores", "Noisy contexts", and "Conflicting documents".
