# 🔀 Consistent Hashing
> **Level:** Intermediate | **Language:** Hinglish | **Goal:** Master consistent hashing

---

## 🧭 Core Concepts (Concept-First)

- Hash Ring
- Virtual Nodes
- Data Distribution

---

## 1. 🎯 Basic Implementation

```python
import hashlib

class ConsistentHash:
    def __init__(self, nodes=None, virtual_nodes=100):
        self.ring = {}
        self.sorted_keys = []
        self.virtual_nodes = virtual_nodes
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node):
        for i in range(self.virtual_nodes):
            hash_key = self._hash(f"{node}-{i}")
            self.ring[hash_key] = node
        
        self.sorted_keys = sorted(self.ring.keys())
    
    def remove_node(self, node):
        for i in range(self.virtual_nodes):
            hash_key = self._hash(f"{node}-{i}")
            del self.ring[hash_key]
        
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key):
        hash_key = self._hash(key)
        
        # Binary search for first node >= hash_key
        for i, key in enumerate(self.sorted_keys):
            if key >= hash_key:
                return self.ring[key]
        
        # Wrap around to first node
        return self.ring[self.sorted_keys[0]]
```

---

## ✅ Checklist

- [ ] Consistent hashing samjho
- [ ] Implementation kar sakte ho