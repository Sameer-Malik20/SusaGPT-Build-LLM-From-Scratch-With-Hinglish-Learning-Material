# 🎯 Mixture of Experts (MoE) — Complete Guide
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master MoE architecture, routing, and implementation

---

## 🧭 Core Concepts (Concept-First)

- MoE Basics: What is mixture of experts
- Gating Mechanism: How experts are selected
- Sparse MoE: Efficient expert activation
- Implementation: Practical code examples

---

## 1. 🔍 MoE Kya Hai

MoE ek architecture hai jahan multiple "experts" hote hain aur gating mechanism decide karta hai kaunsa expert use karna hai.

```python
import numpy as np

class MixtureOfExperts:
    """
    Basic MoE implementation
    """
    def __init__(self, input_dim, num_experts, expert_dim):
        self.num_experts = num_experts
        self.experts = []
        
        # Create multiple expert networks
        for _ in range(num_experts):
            expert = {
                'w1': np.random.randn(input_dim, expert_dim) * 0.01,
                'b1': np.zeros(expert_dim),
                'w2': np.random.randn(expert_dim, input_dim) * 0.01,
                'b2': np.zeros(input_dim)
            }
            self.experts.append(expert)
        
        # Gating network
        self.gate_w = np.random.randn(input_dim, num_experts) * 0.01
        self.gate_b = np.zeros(num_experts)
    
    def forward(self, x):
        """
        Forward pass through MoE
        """
        # Compute gating weights
        gate_logits = np.dot(x, self.gate_w) + self.gate_b
        gate_weights = self.softmax(gate_logits)
        
        # Get expert outputs
        expert_outputs = []
        for expert in self.experts:
            # Simple feedforward
            h = np.maximum(0, np.dot(x, expert['w1']) + expert['b1'])
            out = np.dot(h, expert['w2']) + expert['b2']
            expert_outputs.append(out)
        
        # Weighted combination
        output = np.zeros_like(x)
        for i, w in enumerate(gate_weights[0]):
            output += w * expert_outputs[i]
        
        return output, gate_weights
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
```

---

## 2. 🎛️ Gating Mechanism

Kaunsa expert activate karna hai ye decide karta hai.

### A. Soft Gating

```python
def soft_gating(x, experts, gate):
    """Soft gating - weighted combination of all experts"""
    output = np.zeros_like(x)
    for i, expert in enumerate(experts):
        output += gate[i] * expert(x)
    return output
```

### B. Hard Gating (Top-K)

```python
def hard_gating(x, experts, k=2):
    """
    Hard gating - activate only top-k experts
    Mixtral style approach
    """
    # Get gate values
    gate_values = np.array([expert(x) for expert in experts])
    
    # Get top-k indices
    top_k_idx = np.argsort(gate_values)[-k:]
    
    # Create sparse gate (only top-k non-zero)
    gate = np.zeros(len(experts))
    gate[top_k_idx] = 1.0 / k
    
    # Weighted combination
    output = np.zeros_like(x)
    for i in top_k_idx:
        output += (1.0/k) * experts[i](x)
    
    return output
```

---

## 3. ⚡ Sparse MoE — Efficient Implementation

```python
class SparseMoE:
    """
    Sparse MoE - only activate top-k experts
    Similar to Mixtral/GPT-4 architecture
    """
    def __init__(self, hidden_dim, num_experts=8, top_k=2):
        self.hidden_dim = hidden_dim
        self.num_experts = num_experts
        self.top_k = top_k
        
        # Initialize experts
        self.experts = [
            ExpertLayer(hidden_dim) for _ in range(num_experts)
        ]
        
        # Gating network
        self.gate = nn.Linear(hidden_dim, num_experts, bias=False)
    
    def forward(self, x):
        """
        Forward pass with sparse activation
        """
        # Get gate logits
        gate_logits = self.gate(x)  # (batch, seq, num_experts)
        
        # Top-k selection
        top_k_logits, top_k_idx = torch.topk(gate_logits, self.top_k, dim=-1)
        
        # Apply softmax to top-k only
        top_k_weights = torch.softmax(top_k_logits, dim=-1)
        
        # Initialize output
        output = torch.zeros_like(x)
        
        # Process top-k experts
        for i in range(self.top_k):
            expert_idx = top_k_idx[:, :, i]
            weight = top_k_weights[:, :, i]
            
            # Get expert output (only for selected expert)
            expert_output = self.experts[expert_idx](x)
            
            # Weighted sum
            output += weight.unsqueeze(-1) * expert_output
        
        return output
```

---

## 4. 📊 MoE vs Dense Models

| Aspect | Dense Model | MoE Model |
|--------|-------------|-----------|
| Parameters | All active | Only some active |
| Computation | O(d²) | O(d² × k) where k << d |
| Memory | Large | Very large (all params) |
| Inference | Consistent | Variable (depends on routing) |
| Training | Stable | Can be unstable |

### Memory Requirements

```python
# Dense: 70B parameters
# MoE: 70B total, but only ~12B active per token
# This makes MoE faster at inference but larger for storage
```

---

## 🧪 Exercises

### Exercise 1: Implement Basic MoE
Simple MoE with 4 experts implement karo.

### Exercise 2: Compare Performance
Dense vs MoE performance compare karo.

---

## ✅ Checklist

- [ ] MoE architecture samjho
- [ ] Gating mechanisms distinguish kar sakte ho
- [ ] Sparse vs dense compare kar sakte ho
- [ ] MoE implementation kar sakte ho

> **Tip:** MoE is how GPT-4 achieves massive scale with reasonable inference cost!