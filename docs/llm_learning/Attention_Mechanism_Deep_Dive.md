# 🔍 Attention Mechanism — Deep Dive
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master self-attention, masking, and KV cache

---

## 🧭 Core Concepts (Concept-First)

- Self-Attention: How tokens relate to each other
- Q, K, V: Query, Key, Value matrices
- Multi-Head Attention: Multiple attention heads
- Masking: Causal masks for generation
- KV Cache: Memory optimization for inference

---

## 1. 🎯 Self-Attention — The Core Mechanism

Self-attention ek token ko dusre tokens ke saath compare karta hai.

```python
import numpy as np

def softmax(x):
    """Softmax function"""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Scaled Dot-Product Attention
    Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
    
    Args:
        Q: Query shape (batch, heads, seq, d_k)
        K: Key shape (batch, heads, seq, d_k)
        V: Value shape (batch, heads, seq, d_v)
        mask: Optional mask shape (batch, heads, seq, seq)
    """
    d_k = Q.shape[-1]
    
    # Compute attention scores
    scores = np.matmul(Q, K.transpose(0, 1, 3, 2)) / np.sqrt(d_k)
    
    # Apply mask if provided
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    
    # Apply softmax
    attention_weights = softmax(scores)
    
    # Apply to values
    output = np.matmul(attention_weights, V)
    
    return output, attention_weights
```

---

## 2. 🔑 Q, K, V — Understanding the Trio

```python
class SelfAttention:
    """
    Self-Attention implementation
    """
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Linear projections for Q, K, V
        self.W_q = np.random.randn(d_model, d_model) * 0.01
        self.W_k = np.random.randn(d_model, d_model) * 0.01
        self.W_v = np.random.randn(d_model, d_model) * 0.01
        self.W_o = np.random.randn(d_model, d_model) * 0.01
    
    def split_heads(self, x):
        """Split d_model into num_heads"""
        batch_size, seq_len, d_model = x.shape
        x = x.reshape(batch_size, seq_len, self.num_heads, self.d_k)
        return x.transpose(0, 2, 1, 3)  # (batch, heads, seq, d_k)
    
    def forward(self, x):
        """
        Forward pass
        x: Input (batch, seq_len, d_model)
        """
        batch_size = x.shape[0]
        
        # Linear projections
        Q = np.matmul(x, self.W_q)
        K = np.matmul(x, self.W_k)
        V = np.matmul(x, self.W_v)
        
        # Split heads
        Q = self.split_heads(Q)
        K = self.split_heads(K)
        V = self.split_heads(V)
        
        # Scaled dot-product attention
        attention, weights = scaled_dot_product_attention(Q, K, V)
        
        # Merge heads
        attention = attention.transpose(0, 2, 1, 3).reshape(batch_size, -1, self.d_model)
        
        # Final linear
        output = np.matmul(attention, self.W_o)
        
        return output, weights

# Example usage
d_model = 512
num_heads = 8
seq_len = 10
batch_size = 32

x = np.random.randn(batch_size, seq_len, d_model)
attention = SelfAttention(d_model, num_heads)
output, weights = attention.forward(x)
print(f"Output shape: {output.shape}")  # (32, 10, 512)
```

---

## 3. 🎭 Multi-Head Attention

```python
class MultiHeadAttention:
    """
    Multi-Head Attention - Multiple attention functions in parallel
    """
    def __init__(self, d_model, num_heads):
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Create separate heads
        self.heads = [SelfAttention(d_model, 1) for _ in range(num_heads)]
        self.W_o = np.random.randn(d_model, d_model) * 0.01
    
    def forward(self, x):
        # Run each head
        head_outputs = []
        for head in self.heads:
            out, _ = head.forward(x)
            head_outputs.append(out)
        
        # Concatenate heads
        concat = np.concatenate(head_outputs, axis=-1)
        
        # Final projection
        output = np.matmul(concat, self.W_o)
        
        return output
```

---

## 4. 🚫 Masking — Preventing Information Leak

### A. Causal Mask (for decoder)

```python
def create_causal_mask(seq_len):
    """
    Create causal mask - prevent attending to future tokens
    """
    mask = np.triu(np.ones((seq_len, seq_len)), k=1)
    return mask.astype(np.float32)  # 1 where allowed, 0 where blocked

# Or in PyTorch
import torch

def create_causal_mask_pytorch(seq_len):
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
    mask = mask.masked_fill(mask == 1, float('-inf'))
    return mask
```

### B. Padding Mask

```python
def create_padding_mask(sequence, pad_token_id=0):
    """
    Create padding mask - ignore padding tokens
    """
    mask = (sequence != pad_token_id).astype(np.float32)
    return mask[:, np.newaxis, np.newaxis, :]  # (batch, 1, 1, seq)
```

### C. Combined Mask

```python
def create_combined_mask(seq_len):
    """Combine causal and padding masks"""
    causal = create_causal_mask(seq_len)
    # Both masks combined using minimum
    return causal
```

---

## 5. 💾 KV Cache — Memory Optimization

Inference ke samay KV cache use karke speed badhate hain.

```python
class KVCache:
    """
    Key-Value cache for efficient generation
    """
    def __init__(self):
        self.k_cache = None
        self.v_cache = None
    
    def update(self, k_new, v_new, position):
        """
        Update cache with new keys and values
        """
        if self.k_cache is None:
            self.k_cache = k_new
            self.v_cache = v_new
        else:
            # Append at correct position
            self.k_cache = np.concatenate([self.k_cache, k_new], axis=2)
            self.v_cache = np.concatenate([self.v_cache, v_new], axis=2)
        
        return self.k_cache, self.v_cache

# PyTorch implementation
class KVCachePyTorch:
    def __init__(self, max_batch_size, max_seq_len, num_heads, head_dim, device):
        self.k_cache = torch.zeros(max_batch_size, num_heads, max_seq_len, head_dim, device=device)
        self.v_cache = torch.zeros(max_batch_size, num_heads, max_seq_len, head_dim, device=device)
    
    def update(self, k_new, v_new, position):
        self.k_cache[:, :, position:position+k_new.shape[2], :] = k_new
        self.v_cache[:, :, position:position+v_new.shape[2], :] = v_new
        return self.k_cache[:, :, :position+k_new.shape[2], :], self.v_cache[:, :, :position+v_new.shape[2], :]
```

---

## 6. 📐 Attention Math — Deep Dive

### A. Matrix Multiplication View

```
QK^T = Scores (seq_len x seq_len)
Softmax(Scores) = Attention Weights (seq_len x seq_len)
Attention Weights @ V = Output (seq_len x d_model)
```

### B. Complexity Analysis

- **Time Complexity**: O(n² × d) where n = sequence length, d = dimension
- **Space Complexity**: O(n²) for attention matrix (can be optimized)

### C. Flash Attention

```python
# PyTorch Flash Attention (efficient)
import torch.nn.functional as F

def flash_attention(q, k, v, mask=None):
    """Flash Attention - memory efficient"""
    scale = 1.0 / np.sqrt(q.size(-1))
    attn = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
    return attn
```

---

## 🧪 Exercises

### Exercise 1: Implement Multi-Head Attention
Complete attention mechanism implement karo.

### Exercise 2: Analyze Attention Weights
Dekho attention weights kaise change hoti hain different positions par.

---

## ✅ Checklist

- [ ] Self-attention formula samjho
- [ ] Q, K, V ka role distinguish kar sakte ho
- [ ] Masking types implement kar sakte ho
- [ ] KV cache working samjho
- [ ] Attention complexity analyze kar sakte ho

> **Tip:** Attention is all you need — literally! It's the heart of transformers.