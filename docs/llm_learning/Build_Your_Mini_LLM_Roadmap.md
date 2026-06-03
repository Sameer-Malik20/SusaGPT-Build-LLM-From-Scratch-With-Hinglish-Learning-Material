# 🚀 Build Your Mini-LLM (10M): Step-by-Step Practical Blueprint

Yeh guide aapko batayegi ki [llm_learning](file:///c:/Projects/MyLLM/docs/llm_learning) folder ke kis document ko padhne se kaunsa concept clear hoga, aur aapko apne 10M Parameter LLM project ke liye kaunsi Python file code karni hogi. 

Isko is tarah se design kiya gaya hai ki **koi bhi beginner step-by-step padh kar aur code karke apna khud ka LLM scratch se bana sake**.

---

## 🏗️ Project Architecture Layout

Jab aap model banana shuru karenge, aapka repository structure kuch is tarah dikhega:
```text
my_mini_llm/
├── src/
│   ├── tokenizer.py      # BPE Tokenizer logic
│   ├── dataset.py        # PyTorch Dataset & DataLoader
│   ├── model.py          # Attention layers, MLP, Transformer blocks, LM Head
│   ├── train.py          # Training loop, optimizer, checkpointing
│   └── generate.py       # KV-Cache, Greedy/Top-p Sampling logic
├── data/
│   └── input.txt         # Dataset (e.g., TinyShakespeare)
└── run.py                # Single script to trigger training/generation
```

---

## 🗺️ Master Roadmap: Reading vs. Coding

Niche di gayi table ko follow karein. Pehle **Read** karein, uske baad related code write karein.

| Step | Target Component | folder/Files to Read 📖 | What you Code 💻 | Why this matters for Interview 🎙️ |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Project Setup & Data** | [00_Foundations_and_Roadmap/LLM_Engineering_Mindset.md](00_Foundations_and_Roadmap/LLM_Engineering_Mindset.md) | Setup project directories & download data (`data/input.txt`). | Engineering standards aur scale limits ki awareness. |
| **2** | **Tokenizer** | [05_NLP_Fundamentals_and_Tokenization/Tokenization.md](05_NLP_Fundamentals_and_Tokenization/Tokenization.md)<br>[05_NLP_Fundamentals_and_Tokenization/BPE_and_SentencePiece.md](05_NLP_Fundamentals_and_Tokenization/BPE_and_SentencePiece.md) | `src/tokenizer.py` (BPE vocabulary builder & encode/decode methods). | "How do tokenizers handle Out-of-Vocabulary (OOV) words?" |
| **3** | **Embeddings & Position** | [05_NLP_Fundamentals_and_Tokenization/Embeddings.md](05_NLP_Fundamentals_and_Tokenization/Embeddings.md)<br>[06_Transformer_Architecture_From_Scratch/Positional_Encoding.md](06_Transformer_Architecture_From_Scratch/Positional_Encoding.md)<br>[06_Transformer_Architecture_From_Scratch/RoPE_and_Rotary_Embeddings.md](06_Transformer_Architecture_From_Scratch/RoPE_and_Rotary_Embeddings.md) | `src/model.py`: Embeddings layer aur Rotary Position Embedding (RoPE) helper logic. | "Why RoPE is preferred over absolute positional encodings in Llama?" |
| **4** | **Attention Engine** | [06_Transformer_Architecture_From_Scratch/Self_Attention.md](06_Transformer_Architecture_From_Scratch/Self_Attention.md)<br>[06_Transformer_Architecture_From_Scratch/Multi_Head_Attention.md](06_Transformer_Architecture_From_Scratch/Multi_Head_Attention.md) | `src/model.py`: `CausalSelfAttention` class (Query, Key, Value calculations with causal masking). | "Why do we scale the dot product of Q and K by $\sqrt{d_k}$?" |
| **5** | **Transformer Block** | [06_Transformer_Architecture_From_Scratch/Residual_Connections_and_LayerNorm.md](06_Transformer_Architecture_From_Scratch/Residual_Connections_and_LayerNorm.md)<br>[06_Transformer_Architecture_From_Scratch/Encoder_vs_Decoder.md](06_Transformer_Architecture_From_Scratch/Encoder_vs_Decoder.md) | `src/model.py`: MLP layer (with SwiGLU), RMSNorm class, and assembling `TransformerBlock`. | "What is the benefit of RMSNorm over normal LayerNorm? What is Pre-LN vs Post-LN?" |
| **6** | **Model Assembly** | [07_Modern_LLMs_and_Scaling_Laws/SLM_Fundamentals.md](07_Modern_LLMs_and_Scaling_Laws/SLM_Fundamentals.md)<br>[07_Modern_LLMs_and_Scaling_Laws/Modern_LLMs_and_LLM_Scaling.md](07_Modern_LLMs_and_Scaling_Laws/Modern_LLMs_and_LLM_Scaling.md) | `src/model.py`: Core `Transformer` model configuration for **10M parameters**. | "How to compute the parameter count of a Transformer layer manually?" |
| **7** | **Data Loader** | [08_LLM_Training_and_Data_Engineering/Dataset_Preparation.md](08_LLM_Training_and_Data_Engineering/Dataset_Preparation.md) | `src/dataset.py`: PyTorch `Dataset` that fetches sequences of length `block_size` (context length). | "How is training data structured for next-token prediction task?" |
| **8** | **Training Loop** | [08_LLM_Training_and_Data_Engineering/Pretraining_Fundamentals.md](08_LLM_Training_and_Data_Engineering/Pretraining_Fundamentals.md)<br>[01_Mathematics_for_AI_and_LLMs/Optimization_Algorithms.md](01_Mathematics_for_AI_and_LLMs/Optimization_Algorithms.md) | `src/train.py`: Setups PyTorch training loop, AdamW optimizer, and cross-entropy loss function. | "Why is AdamW preferred over normal Adam? Explain gradient clipping." |
| **9** | **KV-Cached Generation** | [11_Inference_and_Optimization/KV_Cache.md](11_Inference_and_Optimization/KV_Cache.md)<br>[11_Inference_and_Optimization/Inference_Fundamentals.md](11_Inference_and_Optimization/Inference_Fundamentals.md) | `src/generate.py`: Text generation engine with KV-Cache optimization, Temperature, and Top-K/Top-P sampling. | "How does KV-cache reduce generation complexity from $O(N^2)$ to $O(N)$ per token?" |
| **10**| **Fine-Tuning** | [09_Fine_Tuning_and_Alignment/Fine_Tuning_Fundamentals.md](09_Fine_Tuning_and_Alignment/Fine_Tuning_Fundamentals.md)<br>[09_Fine_Tuning_and_Alignment/LoRA_and_QLoRA.md](09_Fine_Tuning_and_Alignment/LoRA_and_QLoRA.md) | Integrate LoRA layers in `src/model.py` for parameter-efficient parameter updates. | "Explain the math behind LoRA ($W + A \cdot B$). How does QLoRA save GPU RAM?" |

---

## 🛠️ Step-by-Step Implementation Guide

### Step 1: Data & Project Setup
* **Kya padhna hai**: [00_Foundations_and_Roadmap/LLM_Engineering_Mindset.md](00_Foundations_and_Roadmap/LLM_Engineering_Mindset.md)
* **Action**: Ek clean project folder banayein. Dataset ke liye **TinyShakespeare** raw text download karein:
  ```bash
  mkdir -p data src
  curl -o data/input.txt https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt
  ```

### Step 2: BPE Tokenizer Likhein
* **Kya padhna hai**: [05_NLP_Fundamentals_and_Tokenization/Tokenization.md](05_NLP_Fundamentals_and_Tokenization/Tokenization.md) aur [BPE_and_SentencePiece.md](05_NLP_Fundamentals_and_Tokenization/BPE_and_SentencePiece.md).
* **Action**: `src/tokenizer.py` file likhiye. 
  * Isme BPE (Byte Pair Encoding) ka logic coding kijiye jo character frequencies check karke top pairs merge karta hai aur raw text ko integers list (Token IDs) me translate karta hai.

### Step 3: Embeddings aur RoPE Code Karein
* **Kya padhna hai**: [06_Transformer_Architecture_From_Scratch/Positional_Encoding.md](06_Transformer_Architecture_From_Scratch/Positional_Encoding.md) aur [RoPE_and_Rotary_Embeddings.md](06_Transformer_Architecture_From_Scratch/RoPE_and_Rotary_Embeddings.md).
* **Action**: `src/model.py` shuru kijiye.
  * Token embeddings define kijiye.
  * Rotary Positional Embeddings (RoPE) ka function code kijiye jo vectors ko coordinate space me rotate karke context information extract karta hai.

### Step 4: Causal Multi-Head Attention Implement Karein
* **Kya padhna hai**: [06_Transformer_Architecture_From_Scratch/Self_Attention.md](06_Transformer_Architecture_From_Scratch/Self_Attention.md) aur [Multi_Head_Attention.md](06_Transformer_Architecture_From_Scratch/Multi_Head_Attention.md).
* **Action**: `src/model.py` me:
  * Linear project layers likhein Query (Q), Key (K), aur Value (V) ke liye.
  * Attention weight formula calculate kijiye: $\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V$ (Jahan $M$ mask tensor hai jo future tokens ko block karta hai).

### Step 5: Full Transformer Block Compile Karein
* **Kya padhna hai**: [06_Transformer_Architecture_From_Scratch/Residual_Connections_and_LayerNorm.md](06_Transformer_Architecture_From_Scratch/Residual_Connections_and_LayerNorm.md).
* **Action**: `src/model.py` me MLP block (SwiGLU) aur RMSNorm (Root Mean Square Normalization) likhein. Sabko wrap karke block banaiye:
  ```python
  x = x + self.attention(self.rmsnorm_1(x))
  x = x + self.mlp(self.rmsnorm_2(x))
  ```

### Step 6: 10M Parameter Configuration Config Karein
* **Kya padhna hai**: [07_Modern_LLMs_and_Scaling_Laws/SLM_Fundamentals.md](07_Modern_LLMs_and_Scaling_Laws/SLM_Fundamentals.md).
* **Action**: Target parameters control karne ke liye parameters optimize karein:
  ```python
  vocab_size = 50257  # Vocabulary Size
  n_embd = 288        # Embedding dimension
  n_layer = 6         # Blocks sequence count
  n_head = 6          # Attention heads count
  block_size = 256    # Max context window
  ```

### Step 7: Data Loader Build Karein
* **Kya padhna hai**: [08_LLM_Training_and_Data_Engineering/Dataset_Preparation.md](08_LLM_Training_and_Data_Engineering/Dataset_Preparation.md).
* **Action**: `src/dataset.py` me:
  * PyTorch `Dataset` class banaiye jo input file reads karke offsets create karegi.
  * Train dataset block size segment check karke features $X$ aur target shift label $Y$ generate karegi.

### Step 8: Optimizer aur Training Run setup karein
* **Kya padhna hai**: [08_LLM_Training_and_Data_Engineering/Pretraining_Fundamentals.md](08_LLM_Training_and_Data_Engineering/Pretraining_Fundamentals.md).
* **Action**: `src/train.py` build kijiye:
  * Loss calculate kijiye: `nn.CrossEntropyLoss()`.
  * Optimizers setup kijiye and validation curve checkpoints monitor kijiye.

### Step 9: Generation Engine with KV-Cache code karein
* **Kya padhna hai**: [11_Inference_and_Optimization/KV_Cache.md](11_Inference_and_Optimization/KV_Cache.md).
* **Action**: `src/generate.py` compile karein:
  * KV-cache matrix parameters optimize karein taaki decoding cycle linear cost scaling implement kare.

---

> [!TIP]
> **Pro-Tip for Interviews**: Jab aap is roadmap ko follow karke model code likhein, toh repository me modules likhte samay **[19_Interview_Preparation/LLM_Interview_Questions.md](19_Interview_Preparation/LLM_Interview_Questions.md)** ko open rakhein. Wahan bataye gaye interview scenarios ke answers ko code ke concepts se cross-verify karte chalein. Isse aapka theory aur practical ek dam strong ho jayega!
