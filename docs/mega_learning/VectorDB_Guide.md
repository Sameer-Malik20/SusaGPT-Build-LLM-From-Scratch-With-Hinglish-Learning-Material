# Filename: VectorDB_Guide.md

# Vector Databases: Multi-Dimensional AI Storage (Complete Guide)

Vector Databases AI models (RAG - Retrieval Augmented Generation) ke liye "Memory" ki tarah hain. Jab model ke paas context kam hota hai, tab Vector DB use karke info fetch hoti hai.

## 1. Vector Embeddings: Text to Numbers
Model text ko nahi samajhta, wo numbers ke patterns samajhta hai. 
**Embedding:** Ek text string ko constant length vector (list of numbers) mein convert karna.

```python
from sentence_transformers import SentenceTransformer

# Simple Embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
sentence = "AI is changing the world!"
embedding = model.encode(sentence)
print(f"Vector dim: {len(embedding)}") # usually 384, 768 or 1536
```

## 2. Similarity Search: Match Kaise?
Vector databases cosine similarity (distance) ya dot product check karte hain queries aur stored vectors ke beech.

## 3. ChromaDB: Open Source & Local
ChromaDB local setup ke liye sabse best hai aur beginners ke liye easy interface deta hai.

```python
import chromadb

# Chrome setup
client = chromadb.Client()
collection = client.create_collection(name="my_documents")

# Add documents
collection.add(
    documents=["PyTorch is great.", "Vector DBs are useful."],
    metadatas=[{"source": "pytorch"}, {"source": "vectordb"}],
    ids=["id1", "id2"]
)

# Query Documents
results = collection.query(
    query_texts=["Tell me about PyTorch"],
    n_results=1
)
print(results['documents'])
```

## 4. Pinecone: Enterprise Cloud Vector DB
Agar aapko cloud-native vector store chahiye, toh Pinecone best choice hai. Ye million level datasets ko fast query kar sakta hai.

```python
# Pinecone code overview
from pinecone import Pinecone, ServerlessSpec

# pc = Pinecone(api_key="your_key")
# index = pc.Index("my_index")
# index.upsert(vectors=[("id-1", [0.1, 0.2, ...], {"topic": "ai"})])
# index.query(vector=[...], top_k=2)
```

## 5. FAISS: Meta's Fast Similarity Search
FAISS (Facebook AI Similarity Search) tab use hota hai jab millions ya billions vectors process karne hon local servers pe efficiently.

```python
import faiss
import numpy as np

# Random data simulation
dimension = 64
nb = 10000 
xb = np.random.random((nb, dimension)).astype('float32')

# Index build
index = faiss.IndexFlatL2(dimension)
index.add(xb)

# Search
xq = np.random.random((1, dimension)).astype('float32') # 1 query
D, I = index.search(xq, k=4) # search top-4
print(f"Top matches indices: {I}")
```

## 6. Weaviate: Schema-Based & Advanced
Weaviate ek vector database hai jo images, audio, video aur text sab handle karta hai meta-data filter ke saath.

## 7. Comparison Table: Kon Sa Use Karein?
| Feature | ChromaDB | Pinecone | FAISS | Weaviate |
|---------|----------|----------|-------|----------|
| **Setup** | Local (Python) | Managed Cloud | Local Library | Container (Docker) |
| **Speed** | Medium | Very Fast | Ultimate (C++) | Fast |
| **Ease** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 8. Mini Project: PDF to Vector Store
Project Logic:
1. `PyPDFLoader` (LangChain) se PDF read kiya.
2. `RecursiveCharacterTextSplitter` se chunks banaye.
3. Chunks ko embed kiya (HuggingFaceEmbeddings).
4. `ChromaDB` mein store kiya aur similarity search kiya.
