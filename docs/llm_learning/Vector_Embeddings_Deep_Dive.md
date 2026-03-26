# 🔢 Vector Embeddings Deep Dive
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master Word2Vec, SBERT, cosine similarity

---

## 🧭 Core Concepts (Concept-First)

- Embedding Basics: Converting text to vectors
- Word2Vec: Skip-gram, CBOW
- Sentence Embeddings: SBERT
- Similarity Metrics: Cosine, Euclidean
- Practical Applications: Search, clustering

---

## 1. 📊 Embeddings Kya Hote Hain

Text ko numbers ki vector mein convert karna.

```python
import numpy as np
from sentence_transformers import SentenceTransformer

# Simple example
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "King",
    "Queen", 
    "Apple",
    "Orange"
]

embeddings = model.encode(sentences)

print(f"Embedding shape: {embeddings.shape}")  # (4, 384)

# Similarity check
from sklearn.metrics.pairwise import cosine_similarity

# King vs Queen - similar
sim_kq = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
# King vs Apple - different
sim_ka = cosine_similarity([embeddings[0]], [embeddings[2]])[0][0]

print(f"King-Queen similarity: {sim_kq:.3f}")
print(f"King-Apple similarity: {sim_ka:.3f}")
```

---

## 2. 🔤 Word2Vec — The Foundation

Word2Vec words ke context se embeddings banata hai.

### A. Skip-gram

```python
import torch
import torch.nn as nn

class SkipGram(nn.Module):
    """
    Skip-gram model: predict context from target word
    """
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()
        self.target_embedding = nn.Embedding(vocab_size, embedding_dim)
        self.context_embedding = nn.Embedding(vocab_size, embedding_dim)
    
    def forward(self, target, context):
        # Target word embedding
        target_emb = self.target_embedding(target)
        # Context word embedding
        context_emb = self.context_embedding(context)
        # Dot product (similarity)
        return torch.sum(target_emb * context_emb, dim=1)
    
    def get_embedding(self, word_idx):
        """Get embedding for a word"""
        return self.target_embedding(torch.tensor([word_idx]))

# Training data: (target, context) pairs
# "king" -> "royal", "throne", "crown"
```

### B. CBOW (Continuous Bag of Words)

```python
class CBOW(nn.Module):
    """
    CBOW model: predict target from context words
    """
    def __init__(self, vocab_size, embedding_dim, window_size):
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear = nn.Linear(embedding_dim, vocab_size)
    
    def forward(self, context_indices):
        # Get embeddings for context words
        emb = self.embeddings(context_indices)  # (batch, window, embed_dim)
        # Average
        avg_emb = torch.mean(emb, dim=1)
        # Predict
        return self.linear(avg_emb)
```

---

## 3. 🧠 Sentence-BERT (SBERT)

Sentence-level embeddings for semantic search.

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Encode sentences
sentences = [
    "The cat sits on the mat",
    "A dog is playing in the park",
    "A feline is resting on a rug",
    "The weather is nice today"
]

embeddings = model.encode(sentences)

# Find most similar
query = "A cat is sitting on a floor"
query_embedding = model.encode([query])

similarities = cosine_similarity([query_embedding[0]], embeddings)[0]
most_similar_idx = np.argmax(similarities)

print(f"Most similar: {sentences[most_similar_idx]}")
print(f"Similarity: {similarities[most_similar_idx]:.3f}")
```

---

## 4. 📐 Cosine Similarity

Most common similarity metric for embeddings.

```python
def cosine_similarity_manual(v1, v2):
    """Calculate cosine similarity"""
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product / (norm1 * norm2)

# Or with NumPy
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
print(f"Cosine similarity: {cos_sim:.3f}")  # 0.974

# Euclidean distance
euclidean_dist = np.linalg.norm(v1 - v2)
print(f"Euclidean distance: {euclidean_dist:.3f}")  # 5.196
```

---

## 5. 🗄️ Vector Databases

Efficient similarity search ke liye specialized databases.

### ChromaDB

```python
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize
client = chromadb.Client()
collection = client.create_collection("documents")

# Embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Add documents
docs = [
    "Python is a programming language",
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks"
]

embeddings = model.encode(docs).tolist()

collection.add(
    embeddings=embeddings,
    documents=docs,
    ids=["doc1", "doc2", "doc3"]
)

# Query
query = "What is Python?"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print(results['documents'])
```

### Pinecone

```python
import pinecone

# Initialize
pinecone.init(api_key="your-key", environment="us-west1")
index = pinecone.Index("my-index")

# Upsert vectors
vectors = [
    {"id": "vec1", "values": [0.1, 0.2, ...], "metadata": {"text": "..."}},
    {"id": "vec2", "values": [0.3, 0.4, ...], "metadata": {"text": "..."}}
]

index.upsert(vectors)

# Query
query_vector = [0.1, 0.2, ...]
results = index.query(vector=query_vector, top_k=5)
```

---

## 🧪 Exercises

### Exercise 1: Build Semantic Search
Simple document search system build karo.

### Exercise 2: Cluster Documents
K-means use karke documents cluster karo.

---

## ✅ Checklist

- [ ] Word2Vec working samjho
- [ ] SBERT vs Word2Vec difference explain kar sakte ho
- [ ] Cosine similarity calculate kar sakte ho
- [ ] Vector database use kar sakte ho
- [ ] Semantic search implement kar sakte ho