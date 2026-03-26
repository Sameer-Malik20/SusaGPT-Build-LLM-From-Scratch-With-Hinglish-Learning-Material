# 🎲 Decoding Strategies — Complete Guide
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master greedy, beam, top-k, top-p, temperature

---

## 🧭 Core Concepts (Concept-First)

- Greedy Search: Always pick the best token
- Beam Search: Explore multiple paths
- Top-K Sampling: Random from top k tokens
- Top-P (Nucleus): Dynamic threshold sampling
- Temperature: Control randomness

---

## 1. 🎯 Greedy Search — The Simplest

Hamesha highest probability wala token pick karta hai.

```python
import numpy as np
import torch

def greedy_decode(model, input_ids, max_length=50):
    """
    Greedy decoding - always pick highest probability
    """
    model.eval()
    generated = input_ids.clone()
    
    for _ in range(max_length):
        # Get logits
        with torch.no_grad():
            outputs = model(generated)
            logits = outputs.logits[:, -1, :]  # Last token logits
        
        # Greedy: pick highest probability
        next_token = torch.argmax(logits, dim=-1)
        
        # Append to sequence
        generated = torch.cat([generated, next_token.unsqueeze(0)], dim=1)
        
        # Stop if EOS
        if next_token.item() == tokenizer.eos_id:
            break
    
    return generated
```

---

## 2. 🔱 Beam Search — Explore Multiple Paths

Multiple promising paths explore karta hai.

```python
def beam_search(model, input_ids, num_beams=5, max_length=50, length_penalty=0.6):
    """
    Beam search - keep top 'num_beams' candidates
    """
    model.eval()
    
    # Initialize with input
    beams = [(input_ids, 0.0)]  # (sequence, score)
    completed = []
    
    for step in range(max_length):
        all_candidates = []
        
        for seq, score in beams:
            # Get logits
            with torch.no_grad():
                outputs = model(seq)
                logits = outputs.logits[:, -1, :]
            
            # Get top k tokens
            topk_logits, topk_indices = torch.topk(logits, num_beams)
            
            # Apply length penalty
            seq_len = seq.shape[1]
            normalized_score = score + (topk_logits[0].numpy() / (seq_len ** length_penalty))
            
            # Create new candidates
            for i in range(num_beams):
                new_seq = torch.cat([seq, topk_indices[0, i:i+1].unsqueeze(0)], dim=1)
                all_candidates.append((new_seq, normalized_score[i]))
        
        # Select top beams
        all_candidates.sort(key=lambda x: x[1], reverse=True)
        beams = all_candidates[:num_beams]
        
        # Check for completed sequences
        new_beams = []
        for seq, score in beams:
            if seq[0, -1].item() == tokenizer.eos_id:
                completed.append((seq, score))
            else:
                new_beams.append((seq, score))
        
        beams = new_beams
        if not beams:
            break
    
    # Return best completed sequence
    if completed:
        completed.sort(key=lambda x: x[1], reverse=True)
        return completed[0][0]
    
    return beams[0][0] if beams else input_ids
```

---

## 3. 🎲 Top-K Sampling — Controlled Randomness

Top-K tokens se random sample lena.

```python
def top_k_sample(logits, k=50, temperature=1.0):
    """
    Top-K sampling
    - First filter to top k tokens
    - Then sample from them
    """
    # Apply temperature
    logits = logits / temperature
    
    # Convert to probabilities
    probs = torch.softmax(logits, dim=-1)
    
    # Get top k
    top_k_probs, top_k_indices = torch.topk(probs, k)
    
    # Sample from top k
    sampled_idx = torch.multinomial(top_k_probs, num_samples=1)
    next_token = top_k_indices[0, sampled_idx[0]]
    
    return next_token.item()

def top_k_decode(model, input_ids, k=50, temperature=1.0, max_length=50):
    """Top-K decoding"""
    model.eval()
    generated = input_ids.clone()
    
    for _ in range(max_length):
        with torch.no_grad():
            outputs = model(generated)
            logits = outputs.logits[:, -1, :].squeeze()
        
        next_token = top_k_sample(logits, k=k, temperature=temperature)
        
        generated = torch.cat([generated, torch.tensor([[next_token]])], dim=1)
        
        if next_token == tokenizer.eos_id:
            break
    
    return generated
```

---

## 4. 📊 Top-P (Nucleus) Sampling — Dynamic Selection

Probability mass ke top-p portion se sample lena.

```python
def top_p_sample(logits, p=0.9, temperature=1.0):
    """
    Top-P (Nucleus) sampling
    - Sort by probability descending
    - Keep adding until cumulative >= p
    - Sample from that set
    """
    # Apply temperature
    logits = logits / temperature
    
    # Convert to probabilities
    probs = torch.softmax(logits, dim=-1)
    
    # Sort by probability
    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    
    # Calculate cumulative probability
    cumsum_probs = torch.cumsum(sorted_probs, dim=-1)
    
    # Find cutoff where cumsum >= p
    cutoff_idx = torch.where(cumsum_probs >= p)[0]
    cutoff = cutoff_idx[0].item() + 1 if len(cutoff_idx) > 0 else len(sorted_probs)
    
    # Keep only top-p tokens
    top_p_probs = sorted_probs[:cutoff]
    top_p_indices = sorted_indices[:cutoff]
    
    # Re-normalize
    top_p_probs = top_p_probs / top_p_probs.sum()
    
    # Sample
    sampled_idx = torch.multinomial(top_p_probs, num_samples=1)
    next_token = top_p_indices[sampled_idx[0]]
    
    return next_token.item()

def top_p_decode(model, input_ids, p=0.9, temperature=1.0, max_length=50):
    """Top-P decoding"""
    model.eval()
    generated = input_ids.clone()
    
    for _ in range(max_length):
        with torch.no_grad():
            outputs = model(generated)
            logits = outputs.logits[:, -1, :].squeeze()
        
        next_token = top_p_sample(logits, p=p, temperature=temperature)
        
        generated = torch.cat([generated, torch.tensor([[next_token]])], dim=1)
        
        if next_token == tokenizer.eos_id:
            break
    
    return generated
```

---

## 5. 🌡️ Temperature — Randomness Control

Temperature controls probability distribution ki sharpness.

```python
def apply_temperature(logits, temperature):
    """
    Temperature scaling
    - temp > 1: More random, flatter distribution
    - temp < 1: Less random, sharper distribution
    - temp = 1: Original distribution
    """
    return logits / temperature

# Comparison
# Temperature = 0.5 (more deterministic)
# Temperature = 1.0 (normal)
# Temperature = 2.0 (more creative/random)
```

---

## 6. 🔄 Combined Strategy — Production Approach

Modern models usually multiple strategies combine karte hain.

```python
def generate_with_strategy(
    model,
    input_ids,
    strategy='top_p',
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    max_length=100,
    repetition_penalty=1.2
):
    """
    Combined generation strategy
    """
    model.eval()
    generated = input_ids.clone()
    
    for _ in range(max_length):
        with torch.no_grad():
            outputs = model(generated)
            logits = outputs.logits[:, -1, :].squeeze()
        
        # Apply repetition penalty
        for token_id in set(generated[0].tolist()):
            logits[token_id] /= repetition_penalty
        
        # Apply temperature
        logits = logits / temperature
        
        # Apply strategy
        if strategy == 'greedy':
            next_token = torch.argmax(logits).item()
        elif strategy == 'top_k':
            probs = torch.softmax(logits, dim=-1)
            topk = torch.topk(probs, top_k)
            next_token = topk.indices[torch.multinomial(topk.values, 1)].item()
        elif strategy == 'top_p':
            probs = torch.softmax(logits, dim=-1)
            sorted_probs, sorted_indices = torch.sort(probs, descending=True)
            cumsum = torch.cumsum(sorted_probs, dim=-1)
            cutoff = (cumsum >= top_p).nonzero()[0].item() + 1
            top_p_probs = sorted_probs[:cutoff]
            top_p_indices = sorted_indices[:cutoff]
            top_p_probs = top_p_probs / top_p_probs.sum()
            sampled = torch.multinomial(top_p_probs, 1)
            next_token = top_p_indices[sampled].item()
        else:
            next_token = torch.argmax(logits).item()
        
        generated = torch.cat([generated, torch.tensor([[next_token]])], dim=1)
        
        if next_token == tokenizer.eos_id:
            break
    
    return generated
```

---

## 📊 Strategy Comparison

| Strategy | Creativity | Quality | Speed |
|----------|-----------|---------|-------|
| Greedy | ❌ Low | ⚠️ Can be repetitive | ✅ Fastest |
| Beam | ⚠️ Medium | ✅ Good | ✅ Fast |
| Top-K | ✅ Medium | ✅ Good | ⚠️ Medium |
| Top-P | ✅ High | ✅ Best for creative | ⚠️ Medium |
| Temperature | Variable | Variable | ✅ Fast |

---

## 🧪 Exercises

### Exercise 1: Compare Strategies
Same input par different strategies run karke output compare karo.

### Exercise 2: Tune Parameters
Temperature, top-k, top-p vary karke quality analyze karo.

---

## ✅ Checklist

- [ ] Greedy vs Beam search difference samjho
- [ ] Top-K vs Top-P compare kar sakte ho
- [ ] Temperature ka effect explain kar sakte ho
- [ ] Production-ready generation implement kar sakte ho
- [ ] Repetition penalty implement kar sakte ho

> **Tip:** For code generation, use lower temperature. For creative writing, use higher!