# 🔤 Tokenization Complete Guide
> **Level:** Beginner → Intermediate | **Language:** Hinglish | **Goal:** Master BPE, WordPiece, SentencePiece

---

## 🧭 Core Concepts (Concept-First)

- Tokenization Basics: Why we need tokens
- BPE (Byte Pair Encoding): Simple and effective
- WordPiece: Used in BERT
- SentencePiece: Unigram, for any language

---

## 1. 📊 Tokenization Kya Hai

Text ko small pieces (tokens) mein divide karna.

```python
# Simple character-level tokenization
text = "hello world"
tokens = list(text)
print(tokens)  # ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']

# Word-level
words = text.split()
print(words)  # ['hello', 'world']
```

---

## 2. 🔄 BPE (Byte Pair Encoding)

Most popular tokenization for LLMs.

```python
from collections import Counter, defaultdict

class BPETokenizer:
    """
    Simple BPE implementation
    """
    def __init__(self):
        self.vocab = {}
        self.merges = []
    
    def get_frequencies(self, text):
        """Get character frequencies"""
        return Counter(text)
    
    def get_pair_frequencies(self, text):
        """Get adjacent pair frequencies"""
        pairs = defaultdict(int)
        for i in range(len(text) - 1):
            pair = text[i:i+2]
            pairs[pair] += 1
        return pairs
    
    def train(self, text, num_merges=100):
        """Train BPE"""
        # Initialize with characters
        vocab = set(text)
        
        for _ in range(num_merges):
            pairs = self.get_pair_frequencies(text)
            if not pairs:
                break
            
            # Find most common pair
            best_pair = max(pairs, key=pairs.get)
            
            # Merge
            text = text.replace(best_pair, best_pair[0])
            vocab.add(best_pair)
            self.merges.append(best_pair)
        
        self.vocab = vocab
    
    def tokenize(self, text):
        """Tokenize new text"""
        tokens = list(text)
        for merge in self.merges:
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and tokens[i] + tokens[i+1] == merge:
                    new_tokens.append(merge)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        return tokens
```

---

## 3. 🎯 SentencePiece

Google's unigram-based tokenizer, language-agnostic.

```python
import sentencepiece as spm

# Train SentencePiece
spm.SentencePieceTrainer.train(
    input='data.txt',
    model_prefix='m',
    vocab_size=8000,
    character_coverage=1.0,
    model_type='unigram'
)

# Load and use
sp = spm.SentencePieceProcessor()
sp.load('m.model')

# Encode
ids = sp.encode('Hello world')
print(ids)  # [x, x, x, x, x]

# Decode
text = sp.decode(ids)
print(text)  # Hello world
```

---

## 4. 🌍 Multilingual Tokenization

Challenges with different languages.

```python
# English: ~1 token = 4 chars
# Chinese: ~1 token = 1-2 chars
# Hindi: ~1 token = 2-3 chars

texts = [
    "Hello world",  # English
    "你好世界",       # Chinese  
    "नमस्ते विश्व",   # Hindi
]

for text in texts:
    tokens = sp.encode(text)
    print(f"{text}: {len(tokens)} tokens")
```

---

## 🧪 Exercises

### Exercise 1: Train BPE
Custom corpus par BPE train karo.

### Exercise 2: Compare Tokenizers
BPE vs WordPiece vs SentencePiece compare karo.

---

## ✅ Checklist

- [ ] BPE working samjho
- [ ] SentencePiece use kar sakte ho
- [ ] Multilingual challenges understand kar sakte ho
- [ ] Tokenizer train kar sakte ho