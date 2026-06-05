# 📚 LLM Data Extraction Guide — Hinglish Edition

> **Yeh README kya hai?**
> Yeh file sirf is project ke liye nahi hai. Yeh ek **complete reference document** hai jo batata hai ki:
> - PDFs se data kaise nikala jata hai
> - Millions of documents aur websites se data kaise collect karte hain
> - Kaun sa format kab use karna chahiye
> - LLM banate waqt data dene mein kaun-kaun si complexities aati hain
> - Kya-kya dhyan rakhna hota hai jab hum ek LLM ko train karte hain

---

## 📁 Is Project Ka Folder Structure

```
data_extraction_for_llm/
│
├── raw/                        ← Har PDF ka alag .txt file (year ke hisab se)
│   ├── 2017/
│   │   ├── 11-2017_UTGST_Rate.txt
│   │   └── ...
│   ├── 2018/ ... 2025/
│
├── jsonl/                      ← Best format for LLM Training — year-wise
│   ├── 2017.jsonl
│   ├── 2018.jsonl
│   └── ...
│
├── combined/                   ← Poora merged dataset ek jagah
│   ├── all_corpus.txt          ← Ek badi text file (chhote LLMs ke liye)
│   └── all_corpus.jsonl        ← Ek bada JSONL (bade LLMs + RAG ke liye)
│
├── stats/
│   └── extraction_stats.json   ← Kitne docs, words, tables, errors — sab yahan
│
└── README.md                   ← Yeh file
```

---

## ⚙️ Yeh Extraction Kaise Kaam Karta Hai

### Step 1 — PDF Parsing (PyMuPDF / fitz)

Hum **PyMuPDF** (`fitz`) use karte hain kyunki yeh:
- PDF ke text ko **reading order** (upar se neeche, left to right) mein extract karta hai.
- **Tables automatically detect** kar leta hai `page.find_tables()` se.
- Image blocks ko text blocks se alag karta hai.

> ⚠️ **Scanned PDFs (images):** Agar PDF scan ki hui image hai (searchable nahi), toh PyMuPDF blank text dega. Iske liye neeche **OCR section** padho.

### Step 2 — Tables ka Markdown mein Convert Karna

GST notifications mein sabse important data tables mein hota hai — jaise tax rates, HS codes, service descriptions. Agar inhe raw text ki tarah extract karo, toh columns ka relation kho jaata hai aur LLM galat facts seekhta hai.

**Solution:** Har table ko **Markdown table format** mein convert karo:

```
| Sl. No. | Chapter / Heading       | Description                   | Rate (%) |
|---------|-------------------------|-------------------------------|----------|
| 3       | Heading 9954            | Construction Services         | 9        |
```

Isse LLM seekhta hai: *"Heading 9954 construction services = 9% rate"* — bilkul sahi.

### Step 3 — Noise Cleaning (Gandgi Hatana)

| Gandgi Ka Type | Example | Kya Karte Hain |
|---|---|---|
| Page numbers | `1`, `2`, `14` | **Delete** |
| Gazette headers | `[TO BE PUBLISHED IN GAZETTE...]` | **Delete** |
| File numbers | `F. No. 354/17/2017-TRU` | **Delete** |
| Bare URLs | `www.cbic.gov.in` | **Delete** |
| Extra blank lines | 3+ consecutive newlines | **Collapse** |
| Multiple spaces | `"tax  rate"` | **Single space** |

### Step 4 — Metadata Add Karna

Har document ke saath rich metadata JSONL mein save hoti hai:

```json
{
  "id": "a1b2c3d4e5f6",
  "source_file": "Union Territory Tax (Rate)/2017/11-2017_UTGST_Rate.pdf",
  "category": "Union Territory Tax (Rate)",
  "year": "2017",
  "filename": "11-2017_UTGST_Rate.pdf",
  "notification": "11",
  "language": "en",
  "pages": 14,
  "tables_found": 23,
  "word_count": 8412,
  "text": "Government of India\nMinistry of Finance...\n\n| Sl. No. | ..."
}
```

Yeh metadata LLM ko context deta hai ki woh kya padh raha hai — isse hallucination kum hoti hai.

---

## 📦 KAUN SA FORMAT KAB USE KARO — Complete Guide

Yeh sabse important question hai. Format choose karna data size, language, aur use case par depend karta hai.

### Format Comparison Table

| Format | File Extension | Best For | Kab Use Karo |
|--------|---------------|----------|--------------|
| **Plain Text** | `.txt` | Chhote LLMs, simple pretraining | Jab data sirf paragraphs ho, koi metadata nahi chahiye |
| **JSON Lines** | `.jsonl` | Large LLMs, HuggingFace, RAG | Jab metadata chahiye + streaming processing |
| **Apache Parquet** | `.parquet` | Petabyte-scale datasets, Apache Spark | Jab millions of documents hon aur fast columnar queries chahiye hon |
| **CSV** | `.csv` | Simple tabular data | Jab sirf structured tables ho — text training ke liye avoid karo |
| **WebDataset (TAR shards)** | `.tar` | GPU streaming during training | Jab data itna bada ho ki disk I/O bottleneck ban jaye |
| **Pre-tokenized Binary** | `.bin` / `.npy` | Final training phase | Jab tokenization already ho chuki ho aur GPUs ko seedha integers feed karne ho |
| **HuggingFace Dataset** | Arrow format | HuggingFace Trainer / transformers | Jab `datasets` library use kar rahe ho |

### Practical Rules:

```
Data < 1 GB      → Plain TXT ya JSONL (simple, kaam chal jaata hai)
Data 1GB–100GB   → JSONL ya Parquet (metadata + efficient reads)
Data > 100GB     → Parquet + WebDataset shards (distributed processing)
Final Training   → Pre-tokenized Binary .bin files (maximum GPU speed)
RAG System       → JSONL → Vector DB index (ChromaDB, FAISS, Pinecone)
```

---

## 🌐 MILLIONS OF DOCUMENTS / WEBSITES SE DATA KAISE EXTRACT KAREIN

Yeh section batata hai ki Gemini, ChatGPT, Claude jaise models ne apna data kaise collect kiya — aur tum apne LLM ke liye kaise kar sakte ho.

### Phase 1 — Data Sources (Data Kahan Se Aata Hai)

```
┌─────────────────────────────────────────────────────┐
│              DATA SOURCES                           │
├─────────────────┬───────────────────────────────────┤
│ Open Datasets   │ Common Crawl, Wikipedia, OpenWebText│
│                 │ C4, The Pile, RedPajama, ROOTS      │
├─────────────────┼───────────────────────────────────┤
│ Websites        │ Web Scraping (Scrapy, Playwright)   │
│                 │ APIs (News API, Reddit API, etc.)   │
├─────────────────┼───────────────────────────────────┤
│ Documents       │ PDFs, Word, Excel (PyMuPDF, docx)  │
│                 │ Government portals, Legal databases │
├─────────────────┼───────────────────────────────────┤
│ Books           │ Project Gutenberg, OpenLibrary      │
├─────────────────┼───────────────────────────────────┤
│ Code            │ GitHub (via GH Archive, BigQuery)  │
└─────────────────┴───────────────────────────────────┘
```

### Phase 2 — Large Scale Web Scraping

Lakhon websites se data scrape karne ke liye:

```python
# Scrapy — distributed web crawler
pip install scrapy

# Spider example
import scrapy

class GSTSpider(scrapy.Spider):
    name = "gst_spider"
    start_urls = ["https://cbic-gst.gov.in/notifications.html"]

    def parse(self, response):
        for link in response.css("a[href$='.pdf']::attr(href)").getall():
            yield scrapy.Request(url=link, callback=self.save_pdf)

    def save_pdf(self, response):
        filename = response.url.split("/")[-1]
        with open(f"pdfs/{filename}", "wb") as f:
            f.write(response.body)
```

**Large scale ke liye tools:**
- **Scrapy** + **Scrapy-Redis** — distributed crawling (multiple machines)
- **Playwright** — JavaScript-heavy sites ke liye (React, Angular pages)
- **Common Crawl** — already crawled 400TB+ internet data — seedha download karo
- **WARC files** — web archive format jo Common Crawl use karta hai

### Phase 3 — Distributed Processing (Spark / Ray)

Jab documents crores mein hon:

```python
# Apache Spark se lakhs of PDFs parallel process karo
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("LLMDataPipeline").getOrCreate()

# Distribute PDF paths across cluster
pdf_paths = spark.sparkContext.parallelize(all_pdf_files)

# Process each PDF on different machine in parallel
def extract_one(path):
    import fitz
    doc = fitz.open(path)
    return " ".join([page.get_text() for page in doc])

texts = pdf_paths.map(extract_one).collect()
```

### Phase 4 — Deduplication (Duplicates Hatana)

Millions of documents mein bahut saare duplicates hote hain. Agar duplicates rahe, LLM usi cheez ko baar baar memorize karta hai.

```python
# MinHash LSH — near-duplicate detection
pip install datasketch

from datasketch import MinHash, MinHashLSH

lsh = MinHashLSH(threshold=0.85, num_perm=128)

def get_minhash(text):
    m = MinHash(num_perm=128)
    for word in text.lower().split():
        m.update(word.encode("utf-8"))
    return m

# Add documents
for i, text in enumerate(all_texts):
    mh = get_minhash(text)
    try:
        lsh.insert(f"doc_{i}", mh)
    except ValueError:
        pass  # duplicate found — skip
```

### Phase 5 — Data Cleaning Pipeline

```
RAW DATA
   │
   ▼
[Language Detection]  ← FastText ya langdetect se
   │
   ▼
[Quality Filters]     ← Word count, punctuation ratio, perplexity score
   │
   ▼
[Deduplication]       ← MinHash LSH (near-duplicates hatao)
   │
   ▼
[PII Redaction]       ← Emails, phone numbers, Aadhaar numbers mask karo
   │
   ▼
[Format Conversion]   ← .txt → .jsonl → Parquet → Pre-tokenized .bin
   │
   ▼
LLM TRAINING
```

### Phase 6 — Tokenization aur Binary Conversion

Final step mein text ko integers mein convert karo:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Text → tokens
tokens = tokenizer.encode("GST rate for construction is 9 percent")
# Output: [38, 2257, 2494, 329, 5103, 318, 860, 1411]

# Save as binary numpy array for fast GPU loading
import numpy as np
arr = np.array(tokens, dtype=np.uint16)
arr.tofile("data/corpus.bin")
```

---

## 🚀 Is Project Ka Extraction Kaise Run Karein

### Prerequisites

```bash
pip install pymupdf pandas tabulate
```

### Run the Pipeline

```bash
# Project root se (c:\Projects\MyLLM)
python src/extract_pdfs.py
```

Script yeh karega:
1. `pdfs/` ke andar sab subdirectories scan karega.
2. Har `.pdf` file se text + tables extract karega.
3. `data_extraction_for_llm/` mein outputs save karega.
4. Live progress print karega.
5. `stats/extraction_stats.json` mein summary likhega.

---

## 🌐 Multi-Language Support (Hindi, Urdu, English)

### Language Detection

Script mein lightweight language detector built-in hai:

| Script | Unicode Range | Language Tag |
|---|---|---|
| Arabic / Urdu script | U+0600–U+06FF | `ur` |
| Devanagari (Hindi) | U+0900–U+097F | `hi` |
| Latin (English) | Default | `en` |

**Better accuracy ke liye `langdetect` install karo:**
```bash
pip install langdetect
```

`src/extract_pdfs.py` mein `detect_language_hint()` function replace karo:
```python
from langdetect import detect
def detect_language_hint(text):
    try:
        return detect(text[:500])
    except Exception:
        return "unknown"
```

### Urdu / RTL PDFs (Scanned)

Urdu PDFs aksar scanned images hoti hain. PyMuPDF empty dega. EasyOCR use karo:

```bash
pip install easyocr
```

```python
import easyocr
reader = easyocr.Reader(['ur', 'en'])
results = reader.readtext('urdu_scan.pdf')
```

### Hindi PDFs (Devanagari)

```bash
pip install easyocr
```

```python
reader = easyocr.Reader(['hi', 'en'])
```

---

## 🧹 Scanned / Image-based PDFs ke liye OCR

Agar `extraction_stats.json` mein `skipped_empty > 0` ho, toh woh PDFs scanned images hain.

### OCR Fallback Setup:

```bash
pip install pytesseract pillow pymupdf
# Tesseract binary bhi install karo:
# https://github.com/UB-Mannheim/tesseract/wiki (Windows installer)
```

```python
import fitz
import pytesseract
from PIL import Image
import io

def ocr_pdf_page(page):
    """Image-only PDF pages ke liye OCR fallback."""
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img, lang="eng+hin+urd")
```

---

## 🤖 LLM Ko Data Dene Ki POORI COMPLEXITIES — Jo Dhyan Rakhna Hota Hai

Yeh sabse important section hai. Sirf data collect karna kaafi nahi — data **kaise dete hain** uspar hi model ki quality depend karti hai.

---

### ⚠️ COMPLEXITY 1 — Data Imbalance (Kuch Data Zyada, Kuch Kum)

**Problem:** Agar 2017 ke 50 documents hain aur 2025 ke sirf 8, toh model 2017 ka data zyada seekhega aur 2025 ka almost bhool jaega.

**Solution:**
```python
# Weighted sampling — har year ka equal representation
import random

year_data = {
    "2017": docs_2017,   # 50 docs
    "2025": docs_2025,   # 8 docs
}

# Upsample 2025 data
balanced = []
for year, docs in year_data.items():
    # Har year se max 30 docs
    balanced.extend(random.choices(docs, k=30))
```

---

### ⚠️ COMPLEXITY 2 — Context Length vs. Document Length

**Problem:** Agar ek PDF 50 pages ka hai aur LLM ka context window sirf 512 tokens hai, toh poora document ek saath dena possible nahi.

**Solution — Chunking (Documents ko chhote pieces mein todna):**

```python
def chunk_document(text, chunk_size=400, overlap=50):
    """
    Document ko overlapping chunks mein todo.
    Overlap isliye ki context break na ho sentence boundary par.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
    return chunks

# Example
chunks = chunk_document(long_document_text, chunk_size=400, overlap=50)
```

**Context window guidelines:**
| Model Size | Recommended Context | Chunk Size |
|---|---|---|
| Small (< 10M params) | 128–256 tokens | 100–200 words |
| Medium (10M–100M) | 512–1024 tokens | 400–800 words |
| Large (1B+) | 2048–8192 tokens | 1600–6000 words |

---

### ⚠️ COMPLEXITY 3 — Data Quality vs. Quantity

**Problem:** LLMs ke liye "zyada data" hamesha better nahi hota. 1 million garbage documents se behtar hai 100K clean documents.

**Quality filters jo lagane chahiye:**

```python
def is_quality_document(text):
    words = text.split()

    # 1. Too short — barely any content
    if len(words) < 50:
        return False

    # 2. Too many repeated words — spam ya template content
    unique_ratio = len(set(words)) / len(words)
    if unique_ratio < 0.3:
        return False

    # 3. Too many numbers/special chars — likely garbage/encoded data
    alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)
    if alpha_ratio < 0.5:
        return False

    # 4. Too many ALL CAPS words — header spam
    caps_words = sum(1 for w in words if w.isupper() and len(w) > 2)
    if caps_words / len(words) > 0.4:
        return False

    return True
```

---

### ⚠️ COMPLEXITY 4 — Hallucination Prevention (Model Ka Jhoot Bolna)

**LLM kyun hallucinate karta hai?**

1. **Contradictory data:** Ek document keh raha hai rate 9% hai, doosra 12%. Model dono seekh leta hai aur randomly kuch bhi bolta hai.
2. **Training data mein specific facts nahi hain:** Model guess karta hai.
3. **Table data wrong extract hua:** Row-column relation kho gaya, model galat mapping seekhta hai.

**Hallucination kum karne ke liye:**

```
✅ Tables → Markdown format mein convert karo (is project mein yeh hota hai)
✅ Contradictory documents remove karo ya explicitly mark karo
✅ Har document ke saath source + year metadata do
✅ RAG (Retrieval Augmented Generation) use karo —
   model training mein guess nahi karega, database se fetch karega
✅ Formatting consistent rakho — ek hi cheez agar 5 tarike se likhi hai,
   model confuse ho jaata hai
```

---

### ⚠️ COMPLEXITY 5 — Tokenizer Mismatch

**Problem:** Agar aapka data Hindi/Urdu mein hai lekin tokenizer sirf English ke liye train hua hai, toh ek Hindi word = 10+ tokens ho jaata hai. Isse:
- Context window waste hota hai
- Model Hindi badly represent karta hai

**Solution:**
```python
from transformers import AutoTokenizer

# Check karo ki tokenizer Hindi ko kaise encode karta hai
tokenizer = AutoTokenizer.from_pretrained("gpt2")  # English only
hindi_text = "GST दर निर्माण सेवाओं के लिए 9 प्रतिशत है"
tokens = tokenizer.encode(hindi_text)
print(len(tokens))  # 40+ tokens — bahut zyada!

# Better: Use a multilingual tokenizer
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-bert")
tokens = tokenizer.encode(hindi_text)
print(len(tokens))  # ~10 tokens — much better!
```

---

### ⚠️ COMPLEXITY 6 — Data Leakage (Test Data Training Mein Aa Jaana)

**Problem:** Agar jo documents test set mein hain woh training set mein bhi hain, toh model ki accuracy falsely high dikhti hai.

```python
import hashlib

def get_doc_hash(text):
    return hashlib.md5(text[:500].encode()).hexdigest()

# Sab hashes collect karo
all_hashes = set()
train_docs, test_docs = [], []

for doc in all_documents:
    h = get_doc_hash(doc["text"])
    if h in all_hashes:
        continue  # duplicate — skip
    all_hashes.add(h)
    # 90/10 split
    if len(train_docs) / max(len(test_docs), 1) < 9:
        train_docs.append(doc)
    else:
        test_docs.append(doc)
```

---

### ⚠️ COMPLEXITY 7 — PII (Personal Information) Exposure

**Problem:** Government notifications mein sometimes officer names, addresses, phone numbers hote hain. Agar LLM training data mein yeh rahe, model inhe generate kar sakta hai.

```python
import re

def redact_pii(text):
    # Phone numbers
    text = re.sub(r'\b[6-9]\d{9}\b', '[PHONE]', text)
    # Email addresses
    text = re.sub(r'\b[\w.]+@[\w.]+\.\w+\b', '[EMAIL]', text)
    # Aadhaar numbers
    text = re.sub(r'\b\d{4}\s\d{4}\s\d{4}\b', '[AADHAAR]', text)
    # PAN numbers
    text = re.sub(r'\b[A-Z]{5}\d{4}[A-Z]\b', '[PAN]', text)
    return text
```

---

### ⚠️ COMPLEXITY 8 — Domain Shift (Training Data aur Real World Ka Mismatch)

**Problem:** Agar model sirf 2017–2019 ke GST documents par train hua hai, toh 2024 ke amendments ke baare mein yeh galat answers dega — kyunki us waqt ke rules change ho chuke hain.

**Solution:**
```
1. Training data mein timestamp/year metadata rakho (is project mein rakhi hai)
2. Model ko explicitly date-aware banao ("As of 2024, the rate is...")
3. RAG system use karo — model latest documents se real-time fetch karega
4. Periodically model ko newer data ke saath fine-tune karo
```

---

### ⚠️ COMPLEXITY 9 — Curriculum Learning (Easy se Hard Data Order)

**Problem:** Agar pahle se bahut complex sentences aaye, model early training mein confuse ho jaata hai aur slow seekhta hai.

**Solution (is project ki `train.py` mein pehle se hai):**

```python
def difficulty_score(text):
    """Chhota = easy, bada = hard"""
    words = text.split()
    punctuation = sum(1 for c in text if not c.isalnum() and not c.isspace())
    return len(words) + punctuation * 0.5

# Sort: easy documents pehle, hard baad mein
sorted_docs = sorted(all_docs, key=lambda d: difficulty_score(d["text"]))
```

---

### ⚠️ COMPLEXITY 10 — GPU Memory aur Batch Size Balance

**Problem:** Agar batch size bahut bada ho, GPU OOM (Out of Memory) error deta hai. Bahut chhota ho toh training unstable hoti hai.

```python
# Gradient Accumulation — small batch ka effect large batch jesa
REAL_BATCH_SIZE = 32   # Chahiye tha
BATCH_SIZE = 4         # GPU mein itna hi fit hota hai
ACCUMULATION_STEPS = REAL_BATCH_SIZE // BATCH_SIZE  # = 8

# Har 8 mini-batches ke baad optimizer step lena
for i, batch in enumerate(dataloader):
    loss = model(batch) / ACCUMULATION_STEPS
    loss.backward()

    if (i + 1) % ACCUMULATION_STEPS == 0:
        optimizer.step()
        optimizer.zero_grad()
```

---

## 📊 Data Quality Checklist (Training Se Pehle)

Training start karne se pehle yeh verify karo:

- [ ] `extraction_stats.json` mein 0 ya minimal errors hain.
- [ ] Kuch `.txt` files manually khol ke padhe — tables readable hain.
- [ ] `all_corpus.jsonl` mein har line valid JSON hai.
- [ ] Word count > 50,000 minimum (basic LLM ke liye).
- [ ] Duplicate documents < 5% hain.
- [ ] Language tags sahi hain (`en`, `hi`, `ur`).
- [ ] Koi sensitive PII (phone, Aadhaar, email) nahi hai.
- [ ] Data mein contradictory facts nahi hain.

---

## 📦 LLM Training Mein Data Kaise Dena Hai

### Option A — Chhote LLM ke liye (Is Project — SusaGPT)

```bash
# Extracted data ko existing data.txt mein add karo
type data_extraction_for_llm\combined\all_corpus.txt >> data\data.txt

# Training run karo
python train.py
```

### Option B — HuggingFace Trainer ke saath

```python
import json
from datasets import Dataset

docs = []
with open("data_extraction_for_llm/combined/all_corpus.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        docs.append(json.loads(line))

dataset = Dataset.from_list(docs)
dataset.save_to_disk("hf_dataset/gst_corpus")
```

### Option C — RAG System (Hallucination-Free Q&A)

```bash
pip install chromadb sentence-transformers
```

```python
import chromadb
from sentence_transformers import SentenceTransformer
import json

client = chromadb.Client()
collection = client.create_collection("gst_notifications")
model = SentenceTransformer("all-MiniLM-L6-v2")

docs, ids, metas = [], [], []
with open("data_extraction_for_llm/combined/all_corpus.jsonl") as f:
    for line in f:
        doc = json.loads(line)
        docs.append(doc["text"][:2000])
        ids.append(doc["id"])
        metas.append({"year": doc["year"], "source": doc["source_file"]})

embeddings = model.encode(docs).tolist()
collection.add(documents=docs, ids=ids, embeddings=embeddings, metadatas=metas)

# Query
results = collection.query(
    query_texts=["Construction services ka GST rate kya hai?"],
    n_results=5
)
```

---

## 🛠️ Common Errors aur Fix

| Error | Cause | Fix |
|---|---|---|
| `No text extracted` | Scanned/image PDF | OCR fallback use karo (neeche dekho) |
| `Table looks garbled` | Complex merged cells | `df.fillna("")` lagao before markdown |
| `Unicode errors` | Non-UTF8 PDF | `fitz.open(..., filetype="pdf")` use karo |
| `ModuleNotFoundError: tabulate` | Not installed | `pip install tabulate` |
| `GPU OOM` | Batch too large | Batch size aadha karo, accumulation double karo |
| `Model hallucinating` | Contradictory data | Deduplication + RAG use karo |
| `Training loss not decreasing` | Learning rate wrong | `3e-4` se start karo, cosine decay use karo |
| `Hindi badly represented` | Wrong tokenizer | Multilingual tokenizer use karo |

---

*Banaya gaya: SusaGPT LLM Pipeline — `src/extract_pdfs.py`*
*Agar naye PDFs aaye toh dobara run karo: `python src/extract_pdfs.py`*
