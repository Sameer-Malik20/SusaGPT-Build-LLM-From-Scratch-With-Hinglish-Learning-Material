# 🛠️ Project 4: Vector Search with Python
> **Objective:** Build a semantic search engine using Python and a Vector Database (Chroma/Pinecone) to search through documents by "Meaning" instead of "Keywords" | **Difficulty:** Intermediate | **Target:** AI & Software Engineers

---

## 🎯 1. The Challenge
Aapko ek "Smart FAQ" search engine banana hai. Agar user puche "How can I pay?", toh use "Payment Methods" wala document milna chahiye, bhale hi "Pay" word exactly wahan na ho.

### Tools:
- Python 3.10+
- `chromadb` (Local Vector DB)
- `sentence-transformers` (For Embeddings)

---

## 💻 2. Implementation Steps

### Step 1: Install Dependencies
```bash
pip install chromadb sentence-transformers
```

### Step 2: The Search Script (`search.py`)
```python
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Initialize DB and Embedding Model
client = chromadb.Client()
collection = client.create_collection(name="faq_collection")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Add Documents
documents = [
    "We accept credit cards, debit cards, and UPI.",
    "Shipping usually takes 3 to 5 business days.",
    "You can return items within 30 days of purchase."
]
ids = ["id1", "id2", "id3"]

# Convert text to vectors (Embeddings)
embeddings = model.encode(documents).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=ids
)

# 3. Perform Semantic Search
query = "How to send money for orders?"
query_vector = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_vector,
    n_results=1
)

print(f"Query: {query}")
print(f"Top Result: {results['documents'][0][0]}")
```

---

## ⚡ 3. Advanced Tasks (Level Up)
1. **Metadata Filtering:** Add metadata like `category: "shipping"` to the documents and filter your search by category.
2. **Hybrid Search:** Combine this vector search with a standard SQL `LIKE` search and see which one is more accurate.
3. **LLM Integration:** Connect this to an LLM (like GPT-4) to create a "RAG" (Retrieval-Augmented Generation) system that answers questions based on the retrieved document.

---

## 🌍 4. Real-World Vision
Ye vahi technology hai jo **ChatGPT** use karta hai aapke documents "yaad" rakhne ke liye. Isse hum "Image Search", "Music Recommendation", aur "Semantic Document Search" bana sakte hain.

---

## ❌ 5. Troubleshooting (Common Traps)
- **Problem:** Search results are irrelevant.
  - **Reason:** The embedding model is too small or not trained for this specific language.
  - **Fix:** Try a larger model like `all-mpnet-base-v2`.
- **Problem:** DB is slow.
  - **Fix:** Use an **HNSW** index (built-in in Chroma) for faster searching.

---

## ✅ 6. Evaluation Criteria
- [ ] Successfully converted text to vectors using an embedding model.
- [ ] Stored and queried vectors in ChromaDB.
- [ ] Achieved accurate "Semantic" results for different queries.
- [ ] Understood the difference between "Keyword" and "Vector" search.

漫
---

## 🚀 7. Bonus: The "Image" Challenge
"Instead of text, can you use a model like CLIP to store images and search for 'Sunset' to find photos of sunsets? Give it a try!"
漫
