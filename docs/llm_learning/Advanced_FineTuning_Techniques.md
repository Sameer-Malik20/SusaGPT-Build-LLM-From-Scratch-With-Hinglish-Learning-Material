# 🎛️ Advanced Fine-tuning Techniques - LoRA, QLoRA & PEFT Mastery
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** LLMs ke liye parameter-efficient fine-tuning methods master karna
## 🧭 Core Concepts (Concept-First)
+- Parameter-Efficient Fine-tuning: Why full fine-tuning is impractical for large models
+- LoRA Mechanics: Low-rank decomposition, adapter matrices, and targeted weight updates
+- QLoRA Innovation: 4-bit quantization combined with LoRA for memory efficiency
+- PEFT Framework: Unified interface for various parameter-efficient methods
+- Practical Applications: Resource-constrained fine-tuning, adapter composition, merging strategies
---

## 📋 Table of Contents: PEFT Methods

| Method | Parameters Updated | Memory Usage | Use Case |
|--------|-------------------|--------------|----------|
| **Full Fine-tuning** | 100% | Very High | Jab aapke paas abundant compute aur data ho |
| **LoRA** | 0.1-1% | Low | Limited resources mein task adaptation |
| **QLoRA** | 0.1-1% | Very Low | Consumer hardware par fine-tuning |
| **Prefix Tuning** | < 1% | Low | Prompt-based adaptation |
| **Adapter Layers** | 1-5% | Medium | Modular task adaptation |

---

## 1. 🔍 The Problem: Kyun Full Fine-tuning Nahi?

Large models (7B+ parameters) ko fine-tune karne ke liye chahiye:
- **Massive GPU memory:** 7B model in FP16 = ~14GB (sirf weights ke liye)
- **Gradient storage:** Additional 14GB for gradients
- **Optimizer states:** AdamW needs 2x parameters = 28GB
- **Total:** ~56GB for 7B model (consumer GPUs par impossible)

**Solution:** Sirf chhota subset of parameters update karo!

---

## 2. 🎯 LoRA (Low-Rank Adaptation)

### A. Core Idea
Saare weights $W$ update karne ki jagah, low-rank decomposition add karo:
$W' = W + BA$
jahaan:
- $B \in \mathbb{R}^{d \times r}$ (low-rank matrix)
- $A \in \mathbb{R}^{r \times k}$ (low-rank matrix)
- $r \ll d, k$ (rank chhota hota hai, e.g., 4, 8, 16)

### B. Implementation Details
- **Applied to:** Query, Key, Value, aur Output projections in attention layers
- **Rank selection:** Typically 4, 8, ya 16 (higher = more capacity)
- **Alpha parameter:** Learned weights ke liye scaling factor
- **Dropout:** Optional for regularization

### C. Code Example (PyTorch-like)
```python
class LoRALayer(nn.Module):
    def __init__(self, in_dim, out_dim, rank=8, alpha=16):
        super().__init__()
        self.rank = rank
        self.alpha = alpha
        self.A = nn.Parameter(torch.randn(in_dim, rank) * 0.02)
        self.B = nn.Parameter(torch.zeros(rank, out_dim))
        
    def forward(self, x, original_weight):
        # x shape: (batch, seq_len, in_dim)
        lora_update = (x @ self.A) @ self.B  # (batch, seq_len, out_dim)
        scaled_update = lora_update * (self.alpha / self.rank)
        return x @ original_weight.T + scaled_update
```

### D. Advantages
- **Memory efficient:** Sirf chhote matrices A aur B store karo
- **Modular:** LoRA adapters ko add/remove kar sakte hain base model change kiye bina
- **Composable:** Multiple adapters ko merge ya switch kar sakte hain

---

## 3. 💎 QLoRA (Quantized LoRA)

### A. The Innovation
QLoRA combine karta hai:
1. **4-bit quantization** of base model (NF4 format)
2. **Paged Optimizers** memory spikes handle karne ke liye
3. **Double quantization** of quantization constants

### B. Memory Savings
| Component | Full FT (16-bit) | LoRA (16-bit) | QLoRA (4-bit) |
|-----------|------------------|---------------|---------------|
| Model weights | 14GB | 14GB | **3.5GB** |
| Gradients | 14GB | 0.1GB | 0.1GB |
| Optimizer states | 28GB | 0.2GB | 0.2GB |
| **Total** | **56GB** | **14.3GB** | **3.8GB** |

### C. Implementation with bitsandbytes
```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config
)

# Add LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
```

---

## 4. 🧩 PEFT (Parameter-Efficient Fine-tuning) Library

Hugging Face ka PEFT library sabhi methods ke liye unified interface provide karta hai.

### A. Supported Methods
- **LoRA:** Low-Rank Adaptation
- **Prefix Tuning:** Learnable prompt embeddings
- **P-Tuning:** Prompt tuning with continuous prompts
- **Adapter Layers:** Small bottleneck layers
- **IA3:** Infused Adapter by Inhibiting and Amplifying Inner Activations

### B. Training Workflow
```python
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForSequenceClassification

# 1. Load base model
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")

# 2. Configure PEFT
peft_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    target_modules=["query", "value"]
)

# 3. Wrap model
model = get_peft_model(model, peft_config)

# 4. Train (sirf LoRA parameters update honge)
training_args = TrainingArguments(output_dir="./results")
trainer = Trainer(model=model, args=training_args, ...)
trainer.train()
```

---

## 5. 📊 Comparison & Selection Guide

### Kab Kaunsi Method Use Karein?

| Scenario | Recommended Method | Kyun |
|----------|-------------------|-----|
| **Single consumer GPU (8-12GB)** | QLoRA | Maximum memory savings |
| **Multiple GPUs, abundant memory** | LoRA | Simpler, no quantization overhead |
| **Need to switch between tasks quickly** | LoRA adapters | Easy adapter swapping |
| **Very limited data (< 100 examples)** | Prefix Tuning | Less prone to overfitting |
| **Production deployment** | Merged LoRA | Single model, no overhead |

### Performance Trade-offs
- **Accuracy:** Full FT ≥ LoRA > QLoRA (chhota gap, typically < 1%)
- **Training speed:** LoRA/QLoRA 2-3x faster than full FT
- **Inference latency:** Merged LoRA = base model, unmerged has small overhead

---

## 6. 🧪 Practical Exercises

### Exercise 1: Llama-2 ko QLoRA se Fine-tune Karna
1. bitsandbytes aur PEFT ke saath environment setup karo
2. Llama-2-7b ko 4-bit precision mein load karo
3. Instruction following ke liye LoRA configure karo
4. Alpaca dataset par train karo
5. Instruction-following benchmarks par evaluate karo

### Exercise 2: Adapter Composition
1. Alag-alag LoRA adapters train karo:
   - Code generation (CodeAlpaca par)
   - Math reasoning (GSM8K par)
   - Creative writing (WritingPrompts par)
2. Inference time par adapter switching implement karo
3. Multi-task fine-tuned model se compare karo

---

## 7. 📈 Advanced Topics

### A. LoRA for Different Architectures
- **Vision Transformers:** MLP layers par apply karo
- **Multimodal models:** Har modality ke liye alag adapters
- **Speech models:** Temporal adaptation patterns

### B. Optimization Techniques
- **Gradient Checkpointing:** Compute ke badle memory trade
- **Flash Attention:** Faster attention computation
- **Gradient Accumulation:** Effective larger batch sizes

### C. Adapter Merging & Arithmetic
- **Task arithmetic:** Adapter weights ko add/subtract karna
- **Adapter fusion:** Multiple adapters ka weighted combination
- **Sparse adaptation:** Sirf most important parameters update karna

---

## 📚 Resources

### Essential Papers
- "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al.)
- "QLoRA: Efficient Finetuning of Quantized LLMs" (Dettmers et al.)
- "PEFT: State-of-the-art Parameter-Efficient Fine-tuning methods" (Mangrulkar et al.)

### Libraries & Tools
- **PEFT Library:** Hugging Face ka official PEFT implementation
- **bitsandbytes:** 8-bit aur 4-bit quantization
- **Axolotl:** Easy fine-tuning framework
- **Unsloth:** Consumer hardware ke liye optimized fine-tuning

---

## 🏆 Checklist
- [ ] Samajh mein aaya kyun full fine-tuning impractical hai large models ke liye
- [ ] LoRA scratch se implement kar sakte hain
- [ ] Jaante hain QLoRA memory usage kaise reduce karta hai
- [ ] PEFT library use kar ke fine-tuning kar sakte hain
- [ ] Different PEFT methods ke trade-offs samajh mein aaye
- [ ] Diye gaye scenario ke liye appropriate method choose kar sakte hain

> **Pro Tip:** Experimentation ke liye hamesha QLoRA se start karo. Jab approach validate ho jaye, tab production ke liye LoRA consider karo agar quantization overhead concern hai.