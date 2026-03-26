# 🚦 API Rate Limiting Algorithms
> **Level:** Intermediate | **Language:** Hinglish | **Goal:** Master rate limiting

---

## 🧭 Core Concepts (Concept-First)

- Token Bucket
- Leaky Bucket
- Fixed Window
- Sliding Window

---

## 1. 🪣 Token Bucket

```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
    
    def consume(self, tokens=1):
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now

# Usage
bucket = TokenBucket(capacity=100, refill_rate=10)  # 10 tokens/sec
if bucket.consume():
    process_request()
else:
    return "Rate limited"
```

---

## 2. 💧 Leaky Bucket

```python
class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.level = 0
        self.leak_rate = leak_rate
        self.last_leak = time.time()
    
    def add(self):
        self._leak()
        if self.level < self.capacity:
            self.level += 1
            return True
        return False
    
    def _leak(self):
        now = time.time()
        elapsed = now - self.last_leak
        leaked = elapsed * self.leak_rate
        self.level = max(0, self.level - leaked)
        self.last_leak = now
```

---

## ✅ Checklist

- [ ] Token bucket implement kar sakte ho
- [ ] Rate limiting choose kar sakte ho