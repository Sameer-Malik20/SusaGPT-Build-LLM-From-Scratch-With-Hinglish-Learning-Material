# 📄 Project: PDF Chat Agent (Beginner)
> **Goal:** Build a production-grade RAG agent that allows users to upload PDFs and ask questions with 99% accuracy.

---

## 🏗️ 1. Architecture
We use a **Classic RAG (Retrieval-Augmented Generation)** pipeline.
- **Frontend:** Streamlit / React for file upload.
- **Backend:** FastAPI for processing.
- **Ingestion:** PDF -> Text Chunks -> Vector Embeddings.
- **Storage:** FAISS (Local) or Pinecone (Cloud).
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
- **LangSmith:** Trace every retrieval step to see which chunk was selected.
- **Logging:** Log PDF upload failures and search latency.

---

## 📊 5. Evaluation
- **RAGAS:** Measure Faithfulness (is the answer in the PDF?) and Answer Relevancy.
- **Test Set:** 20 standard questions for every PDF to check for regression.

---

## 🛡️ 6. Security
- **File Validation:** Only allow `.pdf` files (prevent script execution).
- **Size Limit:** Max 10MB to prevent Denial of Service (DoS) attacks.
- **PII Masking:** Mask names/emails in PDF before sending to OpenAI.

---

## 🚀 7. Deployment
- **Docker:** Containerize the FastAPI app.
- **Host:** Render / Fly.io for quick deployment.

---

## 📈 8. Scaling
- **Horizontal Scaling:** Run multiple workers for PDF processing.
- **Vector DB:** Switch from local FAISS to **Pinecone** for handling 1000+ PDFs.

---

## 💰 9. Cost Optimization
- **Chunk Tuning:** Smaller chunks use fewer tokens per query.
- **Cache:** Cache answers for identical questions.

---

## ⚠️ 10. Failure Handling
- **Malformed PDF:** Use try-except to catch parsing errors and tell the user "PDF is corrupt".
- **No Results:** If similarity score < 0.7, tell user "Info not found in PDF".

---
