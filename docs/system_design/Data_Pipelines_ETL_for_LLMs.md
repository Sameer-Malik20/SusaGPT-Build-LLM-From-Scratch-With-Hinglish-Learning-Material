# 🛠️ Data Pipelines & ETL for LLMs — How to Ingest Billions of Tokens
> **Level:** Intermediate → Advanced | **Language:** Hinglish | **Goal:** Master Vectorization, Tokenization, Chunking, and Data Cleaning for RAG and Pre-training.

---

## 📋 Table of Contents: From Raw Data to Model Embeddings

| Stage | Process | Strategy |
|-------|---------|----------|
| **1. Extraction** | PDF / Web Scraping | Crawling and OCR (Tesseract / LayoutLM). |
| **2. Cleaning** | Redaction / Deduplication| PII delete karna aur duplicate data nikalna. |
| **3. Chunking** | Text Splitting | Fixed vs Semantic vs Recursive chunking. |
| **4. Vectorization**| Embedding Models | OpenAI (text-3), Hugging Face, Cohere. |
| **5. Storage** | Vector Databases | Pinecone, Weaviate, Milvus, Chroma. |
| **6. Automation** | Airflow / Dagster | Scheduled ETL DAGs. |

---

## 1. 📂 Extraction (The Dirty Work)

Raw data clean nahi hota. 
- **PDFs:** Text extract karte waqt headings aur tables ka layout bigad jata hai. **Solution:** `PyMuPDF` or `Unstructured.io`.
- **Web:** JavaScript pages ko scrape karna (Selenium/Playwright).
- **OCR:** Hath se likha hua ya scanned text ko image-to-text badalna.

---

## 2. 🧹 Cleaning: "Garbage In, Garbage Out"

Agar aapne model ko "password: admin" wale documents feedkiye, toh model wahi leak karega.
- **PII Redaction:** Credit cards, Emails, Ph. Numbers ko replace karna `[REDACTED]` se.
- **Deduplication:** Agar same paragraph 10 baar hai, toh embeddings mehngi padengi aur model biased ho jayega.

---

## 3. 🧩 Chunking: Word-to-Sentence-to-Block

Model ka 1 fixed length "Context window" hota hai. 
1. **Character Splitting:** Chota but context udd jata hai (Bech se word kat gaya).
2. **Fixed Token Splitting:** LLM tokenizer ke according chunks banana.
3. **Semantic Chunking:** Naya chunk tabhi banao jab "Topic" change ho jaye. (Best accuracy, but slow calculation).

---

## 🏗️ Python Example: Recursive Character Chunking (LangChain)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Chunking logic
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200, # 20% overlap context maintain karne ke liye
    separators=["\n\n", "\n", " ", ""]
)

# chunks = text_splitter.split_text(large_content)
```

---

## 🚀 Automation: Data Sync (The Pipeline)

Production mein data static nahi rehta (e.g. New company news).
- **Scheduled Sync:** Har 1 ghante mein AWS S3 se naya data check karo -> Clean karo -> Vector DB mein update (Upsert) karo.
- **Change Data Capture (CDC):** PostgreSQL mein row update hui toh turant Vector DB sync karo (Debezium / Kafka).

---

## 🧪 Quick Test (Data Engineer Check)

### Q1: Overlap kyu zaroori hai chunking mein?
**Answer:** Agar main "Messi plays for..." par chunk khatam kar doon, toh model ko pata nahi chalega ki "Who plays?" (Context lost). Overlap se pichla context naye chunk mein pass hota hai.

### Q2: Vector DB vs SQL?
**Answer:** SQL "Exact match" (WHERE id=1) ke liye hai. Vector DB "Meaningful match" (Find similar context) ke liye hai. In production, we use **Hybrid Search** (Dono ka mix).

---

## 🔗 Resources
- [Unstructured.io (Best for complex files)](https://unstructured.io/)
- [Pinecone Guide on Chunking](https://www.pinecone.io/learn/chunking-strategies/)
- [Ray Data (Scalable LLM data processing)](https://docs.ray.io/en/latest/data/data.html)

---

## 🏆 Final Summary Checklist
- [ ] PII redaction kyu mandatory hai? (Privacy compliance).
- [ ] Semantic chunking vs Fixed chunking ka trade-off bata sakte ho? (Cost vs Precision).
- [ ] Overlap ka kya benefit hai? (Context persistence).
- [ ] ETL pipeline automation kyu zaroori hai? (Stale data problem).

> **Data Mantra:** Your LLM is only as smart as your data. Spend 80% of your time on the pipeline, 20% on the model.
