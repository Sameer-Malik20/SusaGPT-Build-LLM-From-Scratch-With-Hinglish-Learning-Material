# 🏛️ SusaGPT — Production Ready Tiny LLM

SusaGPT ek custom **Tiny Language Model** hai jo **SusaLabs** ke official dataset (Company info, AI services, custom software, CRM systems, and healthcare platforms) par trained hai. Yeh model fully self-contained, CPU-optimized aur edge-deployment ready hai.

---

## 📂 Production Folder Structure

Humne project ko ek clean industrial standard structure mein organize kiya hai:

```
susagpt/
├── data/
│   ├── data.txt                # SusaLabs pretraining corpus (573 lines)
│   ├── qa_pairs.json           # Fine-tuning QA pairs
│   └── preference_pairs.json   # RLHF preference pairs
├── src/                        # Core Model & Tokenizer implementation
│   ├── __init__.py
│   ├── config.py               # Hyperparameters and paths
│   ├── model.py                # PyTorch Transformer Architecture (RoPE, GQA, SwiGLU)
│   ├── tokenizer.py            # Custom Byte-level BPE Tokenizer
│   ├── generate.py             # Inference engine (Mirostat, Top-k, Top-p, KV cache)
│   └── api.py                  # FastAPI REST Server
├── scripts/                    # Runnable scripts for training/deployment
│   ├── train.py                # Pretraining entrypoint (Curriculum Learning)
│   ├── fine_tune.py            # Supervised Fine-Tuning (SFT)
│   ├── rlhf.py                 # RLHF-style alignment (Preference tuning)
│   ├── quantize.py             # PyTorch Dynamic INT8 Quantization
│   └── export_onnx.py          # ONNX graph export & ONNX INT8 Quantization
├── cli.py                      # Production CLI (Single Q, Interactive, Benchmark)
├── requirements.txt            # Python dependencies
└── README.md                   # Yeh documentation file
```

---

## 🛠️ Advanced Techniques & Real-World Model Mapping

Humne SusaGPT mein woh saare modern architecture patterns aur optimization techniques use kiye hain jo LLaMA, Gemma, aur GPT-4 jaise modern open/closed source models mein use hote hain.

Niche table mein in techniques, unka real-world mapping, and exact code files with line numbers ki details hain:

| Technique | Kis Model Mein Use Hota Hai | File Path | Code Line (Line Range) | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **Rotary Position Embeddings (RoPE)** | LLaMA 1/2/3, Mistral, Gemma, Qwen | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py) | **Line 27–40** (`RotaryEmbedding`) & **Line 49–54** (`apply_rotary_pos_emb`) | Absolute position embeddings (like Sinusoidal) ke bajaye relative distance sequence positions compute karne ke liye query/key pairs rotate karta hai. |
| **Grouped Query Attention (GQA)** | LLaMA 2 (70B), LLaMA 3, Mistral | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py) | **Line 66–153** (`SelfAttention` class init & forward) | Query heads ko split karta hai and Key/Value heads ko compress karta hai (KV repeat). Isse memory bandwidth aur cache requirements reduce hoti hain. |
| **SwiGLU Activation Function** | LLaMA, PaLM, Gemma | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py) | **Line 156–174** (`SwiGLUFeedForward`) | Standard ReLU ya GELU ke badle Swish (SiLU) gate activation function use karta hai jo linear projections ko multiply karke representational capacity badhata hai. |
| **RMSNorm** | LLaMA, Gemma, Mistral | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py) | **Line 14–24** (`RMSNorm`) | LayerNorm se faster normalizing technique jo bina mean calculation ke direct root-mean-square coordinate variance scale par normalize karti hai. |
| **LoRA (Low-Rank Adaptation)** | LLaMA 1/2/3, Gemma, GPT-4 (PEFT) | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py), [`susagpt/scripts/fine_tune.py`](file:///c:/Projects/MyLLM/susagpt/scripts/fine_tune.py), [`susagpt/scripts/rlhf.py`](file:///c:/Projects/MyLLM/susagpt/scripts/rlhf.py) | **model.py: Line 263-350**, **fine_tune.py: Line 275-285**, **rlhf.py: Line 105-110** | Base model parameters freeze karke attention (W_q, W_v) aur FFN (w1, w3) layers ke parallel low-rank (r=8) trainable matrices ($A$ aur $B$) use karta hai, jisse training parameters 90%+ reduce hote hain. Training ke baad weights merge ho jate hain zero inference latency ke liye. |
| **Byte-level BPE Tokenization** | GPT-2, GPT-3/4, LLaMA, Gemma | [`susagpt/src/tokenizer.py`](file:///c:/Projects/MyLLM/susagpt/src/tokenizer.py) | **Line 38–256** (`Tokenizer` class, `build_vocab`, `encode`, `decode`) | Character ya word level ke bajaye byte sequences par split karke merges training karta hai. Isse unknown tokens (`<UNK>`) handle nahi karne padte aur multilingual/code format support milta hai. |
| **Curriculum Learning** | GPT-4, LLaMA 3 | [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py) | **Line 72–106** (`split_into_curriculum_chunks` & `build_curriculum_text`) | Dataset mein simple and short sentences ko pehle, aur complex/punctuated sentences ko baad mein sort karke train karta hai, taaki model stable learn kare. |
| **RLHF-style Preference Tuning** | InstructGPT, ChatGPT, LLaMA 2/3-Chat | [`susagpt/scripts/rlhf.py`](file:///c:/Projects/MyLLM/susagpt/scripts/rlhf.py) | **Line 50–74** (`average_answer_logprob`) & **Line 134–138** (Pairwise loss sigmoid optimization) | chosen (pasandida) answer ki probability badhata hai aur rejected answer ki weightage kam karta hai using logits sigmoid gap loss. |
| **INT8 Dynamic Quantization** | LLaMA.cpp, PyTorch Mobile Deployments | [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py) | **Line 33–45** (`apply_dynamic_int8_quantization`) | Float32 weight tensors ko 8-bit integers mein convert karke CPU model footprints size ko 4x small aur fast compute-intensive banata hai. |
| **Mirostat Sampling** | LLaMA.cpp (local/edge devices engine) | [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py) | **Line 185–218** (`sample_with_mirostat`) | Next-token selection ke variance / surprise rate ko target parameter "tau" ke around dynamic control deta hai taaki loop repetitions ya generic generation avoid ho sake. |
| **ONNX Runtime Graph Export** | TensorRT, WebNN WebGPU Deployment, edge servers | [`susagpt/scripts/export_onnx.py`](file:///c:/Projects/MyLLM/susagpt/scripts/export_onnx.py) | **Line 56–78** (`export_onnx`) & **Line 80–100** (`quantize_onnx`) | PyTorch weights dependencies hatakar universal computation model output format export karta hai jo dynamic batch axis aur quantized engine optimization support karta hai. |

---

## 🚀 How to Run the Pipeline (Commands)

Aap in commands ko step-by-step terminal mein run karke model complete train aur deployment verify kar sakte hain:

### 1. Requirements Install Karein
```bash
pip install -r susagpt/requirements.txt
```

### 2. Base Model Training (Pretraining)
```bash
python susagpt/scripts/train.py
```
*Yeh SusaLabs core corpus `susagpt/data/data.txt` par curriculum pretraining shuru karega.*

### 3. Supervised Fine-Tuning (SFT)
```bash
python susagpt/scripts/fine_tune.py
```
*Yeh checkpoint load karke model ko QA pairs `susagpt/data/qa_pairs.json` ke corresponding direct response sikhayega.*

### 4. RLHF Alignment (Preference Tuning)
```bash
python susagpt/scripts/rlhf.py
```
*Yeh chosen vs rejected preference pair behavior sikhakar answer quality enhance karega.*

### 5. CPU Weight Quantization (PyTorch INT8)
```bash
python susagpt/scripts/quantize.py
```
*Trained model ko dynamic 8-bit integers compress target format `SusaGPT-int8.pt` mein save karega.*

### 6. ONNX Export aur Quantization (Mobile/Edge Deployment)
```bash
python susagpt/scripts/export_onnx.py
```
*Yeh full precision ONNX model (`SusaGPT.onnx`) aur quantized dynamic INT8 model (`SusaGPT_quantized.onnx`) generate karega.*

---

## 🤖 Production CLI Interface Usage

Humne ek advanced production-grade CLI built kiya hai jisse aap models benchmark aur test kar sakte hain:

### A. Ask a Single Question
```bash
python susagpt/cli.py --question "what does susalabs do"
```

### B. Interactive Chat Mode (type 'quit' to exit)
```bash
python susagpt/cli.py --interactive
```

### C. Run the Production 10-Question Benchmark
```bash
python susagpt/cli.py --benchmark
```
*Yeh benchmark model ko 10 different company queries par check karke execution timestamps analyze karega aur `benchmark_results.json` output file save karega.*

### D. Force Use Base Model (For comparing SFT/RLHF upgrades)
```bash
python susagpt/cli.py --question "what services does susalabs offer" --base
```
