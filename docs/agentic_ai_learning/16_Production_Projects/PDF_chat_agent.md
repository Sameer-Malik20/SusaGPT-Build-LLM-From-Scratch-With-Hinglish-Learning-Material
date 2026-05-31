# 📄 Project: PDF Chat Agent (Beginner)
> **Level:** Beginner | **Language:** Hinglish | **Goal:** Ek aisa production-grade RAG agent banayein jo users ko PDFs upload karne aur 99% accuracy ke sath questions puchne ki permission de.

---

## 🏗️ 1. Architecture
Hum ek **Classic RAG (Retrieval-Augmented Generation)** pipeline use karte hain.
- **Frontend:** File upload ke liye Streamlit / React.
- **Backend:** Processing ke liye FastAPI.
- **Ingestion:** PDF -> Text Chunks -> Vector Embeddings.
- **Storage:** FAISS (Local) ya Pinecone (Cloud).
- **Retrieval:** Semantic Search + LLM Refinement.

---

## 📂 2. Folder Structure
```text
pdf_chat_agent/
├── app/
│   ├── main.py          # FastAPI Gateway
│   ├── agent.py         # RAG Logic
│   ├── ingestion.py     # PDF to Vector
│   └── utils.py         # Helpers
├── data/                # Local PDF storage
├── vector_store/        # FAISS index files
├── requirements.txt
└── Dockerfile
```

---

## 💻 3. Full Code (Core Logic)
```python
# Hinglish Logic: PDF padho, chunks banao, aur vector DB mein dalo
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    
    db = FAISS.from_documents(chunks, OpenAIEmbeddings())
    db.save_local("vector_store")

def ask_question(query):
    db = FAISS.load_local("vector_store", OpenAIEmbeddings())
    docs = db.similarity_search(query)
    # response = llm.invoke(f"Context: {docs} \n Question: {query}")
    return "Answer from PDF"
```

---

## 🔍 4. Observability
- **LangSmith:** Har retrieval step ko trace karein taaki dekh sakein ki kaunsa chunk select hua hai.
- **Logging:** PDF upload failures aur search latency ko log karein.

---

## 📊 5. Evaluation
- **RAGAS:** Faithfulness (kya answer PDF mein hai?) aur Answer Relevancy ko measure karein.
- **Test Set:** Regression check karne ke liye har PDF ke liye 20 standard questions ka use karein.

---

## 🛡️ 6. Security
- **File Validation:** (Script execution ko rokne ke liye) sirf `.pdf` files hi allow karein.
- **Size Limit:** Denial of Service (DoS) attacks ko prevent karne ke liye max 10MB size limit rakhein.
- **PII Masking:** OpenAI ko bejne se pehle PDF se names/emails ko mask karein.

---

## 🚀 7. Deployment
- **Docker:** FastAPI app ko containerize karein.
- **Host:** Quick deployment ke liye Render / Fly.io ka use karein.

---

## 📈 8. Scaling
- **Horizontal Scaling:** PDF processing ke liye multiple workers run karein.
- **Vector DB:** 1000+ PDFs ko handle karne ke liye local FAISS se **Pinecone** par switch karein.

---

## 💰 9. Cost Optimization
- **Chunk Tuning:** Chote chunks query ke dauran kam tokens use karte hain.
- **Cache:** Identical questions ke answers ko cache karein.

---

## ⚠️ 10. Failure Handling
- **Malformed PDF:** Parsing errors ko catch karne ke liye try-except ka use karein aur user ko "PDF corrupt hai" batayein.
- **No Results:** Agar similarity score < 0.7 ho, toh user ko batayein "Info PDF mein nahi mili".

---
