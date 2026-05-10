# Word Embeddings: Giving Meaning to Numbers

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, computer sirf numbers samajhta hai, words nahi. Toh hum "Apple" ko computer ko kaise samjhayein? 

**Word Embeddings** ka matlab hai har word ko ek "Vector" (lambhi list of numbers) dena. Par yeh random numbers nahi hote. Inhe aise design kiya jata hai ki jo words "Meaning" mein paas hain (jaise 'King' aur 'Queen'), unke vectors bhi math ki duniya mein paas honge. Socho ki pura language ek 3D space mein map hai, jahan har word ki apni ek location hai.

---

## 2. Deep Technical Explanation
Word embeddings are dense, low-dimensional vector representations of words in a continuous vector space.
- **Static Embeddings**: Word2Vec (Skip-gram/CBOW) and GloVe. A word has the same vector regardless of context (e.g., 'bank' in 'river bank' vs 'bank account').
- **Contextual Embeddings**: BERT, GPT. The vector for 'bank' changes based on the surrounding words.
- **Cosine Similarity**: The primary metric to measure how "similar" two embeddings are.

---

## 3. Mathematical Intuition
Word2Vec skip-gram objective: Maximize the probability of context words $w_{c}$ given a center word $w_{t}$:
$$J(\theta) = \prod_{t=1}^T \prod_{-m \leq j \leq m, j \neq 0} P(w_{t+j} | w_t; \theta)$$
This creates the famous relationship:
$$\text{Vector("King")} - \text{Vector("Man")} + \text{Vector("Woman")} \approx \text{Vector("Queen")}$$

---

## 4. Architecture Diagrams
```mermaid
graph TD
    Word[Word: King] --> Input[One-hot Vector]
    Input --> Hidden[Embedding Layer: Weights W]
    Hidden --> Vector[Dense Vector: [0.12, -0.5, 0.8...]]
    
    subgraph "Vector Space"
        K[King] --- Q[Queen]
        M[Man] --- W[Woman]
    end
```

---

## 5. Production-ready Examples
Using `Gensim` to explore embeddings:

```python
import gensim.downloader as api

# Load pre-trained GloVe vectors
model = api.load("glove-wiki-gigaword-100")

# Find most similar words
print(model.most_similar("india"))
# Output: [('pakistan', 0.83), ('delhi', 0.77), ('indian', 0.76)...]

# Math with words
result = model.most_similar(positive=['woman', 'king'], negative=['man'])
print(result[0]) # Output: ('queen', 0.76)
```

---

## 6. Real-world Use Cases
- **Recommendation Systems**: Finding products similar to what you bought.
- **Semantic Search**: Searching for "Smartphones" and getting results for "iPhone" and "Android".

---

## 7. Failure Cases
- **Polysemy (Static)**: Static embeddings can't handle multiple meanings of the same word.
- **Out of Vocabulary (OOV)**: If a word wasn't in the training set, the model has no vector for it. (Solved by Subword tokenization).

---

## 8. Debugging Guide
1. **Visualization**: Use T-SNE or UMAP to project high-dimensional vectors to 2D and see if clusters make sense.
2. **Norm Check**: If vector norms are too small, they might not carry enough signal.

---

## 9. Tradeoffs
| Feature | Static (Word2Vec) | Contextual (BERT) |
|---|---|---|
| Speed | Extremely Fast | Slow |
| Context | No | Yes |
| Memory | Low | High |

---

## 10. Security Concerns
- **Bias**: Embeddings often reflect societal biases (e.g., associating 'doctor' more with 'man' than 'woman').

---

## 11. Scaling Challenges
- **Large Vocab**: Storing an embedding for every word in English takes several GBs of VRAM.

---

## 12. Cost Considerations
- **Storage**: Vector databases (Pinecone, Milvus) charge based on the number of embeddings and their dimensions.

---

## 13. Best Practices
- Use **Pre-trained embeddings** for small tasks.
- For LLMs, always use **Learned Embeddings** that update during training.

---

## 14. Interview Questions
1. How does Cosine Similarity differ from Euclidean Distance?
2. Explain the intuition behind the Skip-gram model in Word2Vec.

---

## 15. Latest 2026 Patterns
- **Multimodal Embeddings**: CLIP style embeddings where "an image of a cat" and the word "cat" point to the same location in vector space.
