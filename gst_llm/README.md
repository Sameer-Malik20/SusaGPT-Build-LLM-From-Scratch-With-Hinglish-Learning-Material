# 🏛️ GST Tiny LLM — Production Ready

> **Ek domain-specific Tiny Language Model** jo sirf GST (Union Territory Tax Rate) notifications par trained hai.
> 2017–2025 ke 192 government PDFs se extract kiye gaye **1,76,722 words** par pretrain hua.
> **Laptop aur Mobile dono par chalta hai** — ONNX format se cross-platform support.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🧠 Architecture | Transformer (RoPE + GQA + SwiGLU) — LLaMA-style |
| 📦 Model Size | ~2–3M parameters, ~12 MB on disk |
| 🗜️ Quantized Size | ~3–4 MB (INT8 ONNX) — mobile ready |
| 📚 Training Data | 1,76,722 words from 192 GST PDFs (2017–2025) |
| 🌐 Cross-Platform | ONNX format — Windows, Linux, macOS, Android, iOS |
| ⚡ Speed | ~0.5–2s per answer on CPU |
| 🖥️ CLI | Single question, interactive chat, benchmark mode |
| 🔌 API | FastAPI REST server (port 8001) |
| 📊 Logging | Training logs saved to `artifacts/train_log.txt` |
| 💾 Checkpoints | Auto-saved every 10 epochs |

---

## 📁 Folder Structure

```
gst_llm/
│
├── cli.py                    ← 🖥️  Command-line interface (MAIN ENTRY)
├── train.py                  ← 🚀  Start pretraining
├── fine_tune.py              ← 🎯  Fine-tune on Q&A pairs
├── generate.py               ← 💬  Simple text generation
├── requirements.txt          ← 📦  All dependencies
├── README.md                 ← 📖  This file
│
├── data/
│   ├── corpus.txt            ← GST training corpus (176K words)
│   ├── qa_pairs.json         ← Q&A pairs for fine-tuning
│   └── preference_pairs.json ← RLHF alignment data
│
├── src/
│   ├── config.py             ← All model & training settings
│   ├── model.py              ← Transformer architecture
│   ├── tokenizer.py          ← BPE Tokenizer (8000 vocab)
│   ├── train.py              ← Training loop (with checkpoints + tqdm)
│   ├── fine_tune.py          ← QA fine-tuning loop
│   ├── generate.py           ← Inference engine
│   ├── evaluate.py           ← Perplexity evaluation
│   ├── rlhf.py               ← RLHF alignment
│   ├── quantize.py           ← PyTorch INT8 quantization
│   ├── export_onnx.py        ← 🌐 ONNX export for mobile/cross-platform
│   └── api.py                ← FastAPI REST server
│
└── artifacts/
    ├── models/
    │   ├── gst_llm_base.pt       ← Base pretrained model
    │   ├── gst_llm_finetuned.pt  ← Fine-tuned model (best for Q&A)
    │   ├── gst_llm.onnx          ← ONNX (cross-platform)
    │   └── gst_llm_quantized.onnx ← ONNX INT8 (mobile)
    ├── tokenizer/
    │   └── tokenizer.json        ← Trained BPE tokenizer
    ├── checkpoints/              ← Auto-saved every 10 epochs
    └── train_log.txt             ← Full training log
```

---

## ⚙️ Model Configuration

```python
MODEL_CONFIG = {
    "embed_dim"   : 128,    # Embedding dimension
    "num_heads"   : 4,      # Attention heads
    "num_kv_heads": 2,      # Key-Value heads (GQA)
    "num_layers"  : 4,      # Transformer blocks
    "max_len"     : 128,    # Context window (tokens)
    "dropout"     : 0.1,    # Regularization
}
# Estimated: ~2-3M parameters
```

---

## 🚀 Quick Start

### Step 0 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 1 — Train Base Model

```bash
cd c:\Projects\MyLLM\gst_llm
python train.py
```

- GST corpus padhega, BPE tokenizer build karega
- 50 epochs train karega (CPU par ~20-40 min)
- Checkpoint har 10 epochs par save hoga
- Best model save hoga: `artifacts/models/gst_llm_base.pt`

### Step 2 — Fine-Tune on Q&A

```bash
python fine_tune.py
```

- `data/qa_pairs.json` se QA pairs padhega
- Model ko direct Q&A behavior sikhata hai
- Saves: `artifacts/models/gst_llm_finetuned.pt`

### Step 3 — Export for Mobile/Cross-Platform

```bash
python src/export_onnx.py
```

- ONNX model export karega (sabhi platforms ke liye)
- INT8 quantized version bhi banayega (mobile ke liye)

---

## 🖥️ Usage Commands

### ✅ Single Question (Sabse Easy)

```bash
python cli.py --question "What is UTGST?"
python cli.py --question "GST rate for construction services?"
python cli.py --question "What is the rate for accommodation above Rs.2500 per day?"
```

### ✅ Interactive Mode (Chat-like)

```bash
python cli.py --interactive
```

```
Your question: What is Heading 9963?
Answer : Heading 9963 covers accommodation, food and beverage services...

Your question: GST rate for restaurants?
Answer : Restaurant without AC attracts 6% UTGST...

Your question: quit
```

### ✅ Benchmark Mode (10 Questions Test)

```bash
python cli.py --benchmark
```

Yeh 10 test questions chalayega aur `benchmark_results.json` save karega.

### ✅ Temperature Control

```bash
# More creative / diverse answers
python cli.py --question "..." --temperature 0.9

# More deterministic / factual answers
python cli.py --question "..." --temperature 0.3
```

### ✅ Force Base Model (Without Fine-tuning)

```bash
python cli.py --question "..." --base
```

### ✅ REST API Server

```bash
python -m uvicorn src.api:app --host 0.0.0.0 --port 8001 --reload
```

API docs: http://localhost:8001/docs

```bash
# cURL se query
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is UTGST rate for construction?"}'
```

---

## 📱 Mobile / Cross-Platform (ONNX)

ONNX model **kisi bhi platform par** chalega bina PyTorch ke:

```python
import onnxruntime as ort
import numpy as np

# Load ONNX model
session = ort.InferenceSession("artifacts/models/gst_llm_quantized.onnx")

# Inference
input_ids = np.array([[1, 23, 45, 67]], dtype=np.int64)   # tokenized input
logits = session.run(["logits"], {"input_ids": input_ids})[0]
next_token = logits[0, -1, :].argmax()
```

**Supported Platforms via ONNX Runtime:**
| Platform | How |
|---|---|
| Windows Laptop | `pip install onnxruntime` |
| Linux/Mac | `pip install onnxruntime` |
| Android | ONNX Runtime Android AAR |
| iOS | ONNX Runtime CocoaPod |
| Web Browser | ONNX Runtime Web (JavaScript) |
| Raspberry Pi | `pip install onnxruntime` (ARM build) |

---

## 📊 Training Details

| Setting | Value |
|---|---|
| Training corpus | 1,76,722 words (GST 2017–2025) |
| Tokenizer | BPE (Byte-Pair Encoding), vocab=8000 |
| Optimizer | AdamW (lr=3e-4, weight_decay=0.01) |
| Scheduler | Cosine decay with warmup |
| Batch size | 16 (effective 64 with accumulation) |
| Epochs | 50 (early stopping at patience=7) |
| Checkpointing | Every 10 epochs |
| Mixed precision | FP16 on CUDA, FP32 on CPU |

---

## ➕ Adding More QA Pairs (Better Accuracy)

`data/qa_pairs.json` mein add karo:

```json
[
  {
    "question": "What is the UTGST rate for IT services?",
    "answer": "Information Technology services under Heading 9983 attract 9% UTGST as per the rate schedule."
  },
  {
    "question": "Construction services ka GST rate kya hai?",
    "answer": "Heading 9954 ke under construction services par 9% UTGST lagta hai."
  }
]
```

Phir dobara fine-tune karo:
```bash
python fine_tune.py
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `No trained model found` | `python train.py` pehle chalao |
| `CUDA out of memory` | `config.py` mein `batch_size: 8` karo |
| `ModuleNotFoundError: tqdm` | `pip install tqdm` |
| `Model answers gibberish` | Fine-tuning karo: `python fine_tune.py` |
| ONNX export fails | `pip install onnx onnxruntime` |
| API not starting | Port 8001 already in use → change `API_CONFIG["port"]` |

---

## 🔄 Re-train with New PDFs

```bash
# 1. New PDFs add karo pdfs/ folder mein
# 2. Re-extract:
cd c:\Projects\MyLLM
python src/extract_pdfs.py

# 3. Corpus update karo:
copy data_extraction_for_llm\combined\all_corpus.txt gst_llm\data\corpus.txt

# 4. Re-train:
cd gst_llm
python train.py
```

---

*GST Tiny LLM — Built with ❤️ on 192 UTGST Rate Notifications (2017–2025)*
