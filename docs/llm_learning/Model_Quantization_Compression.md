# 🗜️ Model Quantization & Compression — LLMs on Low VRAM (Optimization Mastery)
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master FP16, INT8, 4-bit, GGML/GGUF, EXL2, and AWQ.

---

## 📋 Table of Contents: Squeezing Billions of Parameters

| Method | Full Name | Compression | Quality Loss |
|--------|-----------|-------------|--------------|
| **1. FP16/BF16**| Half Precision | 2x | None |
| **2. INT8** | 8-bit Integer | 4x | Very Low |
| **3. NF4 / 4-bit**| 4-bit Normal Float | 8x | Observable |
| **4. AWQ** | Activations-aware | 8x | Minimum |
| **5. GGUF** | CPU-friendly | 4x-10x | Scalable |
| **6. EXL2** | ExLlama (GPU-only) | Fastest | Minimum |

---

## 1. 🔢 Precision: FP32 vs FP16 vs BF16

Computer numbers ko bits mein store karta hai.
- **FP32 (Full):** 32 bits (4 bytes) per parameter. 7B model = 28GB VRAM.
- **FP16 (Half):** 16 bits (2 bytes) per parameter. 7B model = 14GB VRAM. **Industry Standard for Training.**
- **BF16 (Brain Float):** Dynamic range zyada hota hai (Google design). Stable Training ke liye best.

---

## 2. 🛡️ Post-Training Quantization (PTQ)

Model banne ke baad uski "Precision" kam kar dena taki wo saste GPU mein chal sake.

### A. GPTQ (4-bit)
Weights ko mathematical formula se compress karte hain. Ye GPU par bohot fast chalta hai. 7B model ab 5.5GB VRAM khali lega.

### B. AWQ (Activation-aware Weight Quantization)
Ye dhyan rakhta hai ki "important" weights ko zyada bits milein aur "unimportant" ko kam. **Mistral/Llama models ke liye best precision per bit.**

---

## 3. 🖥️ CPU Inference (llama.cpp & GGUF)

Agar aapke paas GPU nahi hai, toh bhi aap LLM chala sakte ho.
- **GGUF (v3 Format):** Ye weights ko groups mein compress karta hai (q4_K_M, q5_0, etc.). 
- **llama.cpp:** Apple M-series chips aur standard CPUs ke liye optimized backend.

---

## 🚀 Tool Comparison: Kiska Quantization Best Hai?

| Backend | Format | Best For? |
|---------|--------|-----------|
| **AutoGPTQ** | `.safetensors` | General GPU serving. |
| **AutoAWQ** | `.safetensors` | High-quality 4-bit on GPU. |
| **llama.cpp** | `.gguf` | CPU / MacBook / Mobile. |
| **ExLlamaV2** | `.exl2` | Single GPU speed (Fastest tokens/sec). |

---

## 🏗️ Python Setup (AutoGPTQ/BitsAndBytes)

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 4-bit loading logic
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_quant_type="nf4" # Normal Float 4
)

# model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=quant_config)
```

---

## 🧪 Quick Test (Optimization Logic)

### Q1: Fine-tuning ke liye BF16 kyu use karein FP16 ki jagah?
**Answer:** FP16 mein numbers bohot bade ho jayein (Gradient Explosion) toh wo overflow ho jate hain (NaN values). BF16 is problem se bacha leti hai.

### Q2: Perplexity kya hai?
**Answer:** Quantization ke baad model ki galthi (Error) badh jati hai. Perplexity measure karti hai "How confused is the model?". Low Perplexity = Good Quantization.

---

## 🔗 Resources
- [The Case for 4-bit Quantization (Dettmers)](https://arxiv.org/abs/2211.10438)
- [AutoAWQ GitHub](https://github.com/casper-hansen/AutoAWQ)
- [llama.cpp ecosystem](https://github.com/ggerganov/llama.cpp)

---

## 🏆 Final Summary Checklist
- [ ] FP16 vs BF16 ka main difference bata sakte ho? (Hint: Range).
- [ ] BitsAndBytes (4-bit) se memory kitni bachti hai? (8x approx).
- [ ] CPU par model chalane ke liye kaunsa format chahiye? (GGUF).
- [ ] AWQ weights ko protect kyu karti hai? (Based on activations).

> **Expert Insight:** 4-bit quantization is nearly "Free" memory saving. Most users don't notice any quality drop compared to FP16, but memory 1/4th ho jati hai.
