# 🏭 LLM Pre-training Guide - From Scratch to Foundation Model
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** LLM ko scratch se pre-train kaise karein (Raw data se foundation model tak)

---

## 📋 Table of Contents: Pre-training Pipeline

| Stage | Topic | Key Concepts |
|-------|-------|--------------|
| **1. Data Collection** | Web Scraping & Corpus Building | Common Crawl, The Pile, RedPajama |
| **2. Data Cleaning** | Quality Filtering & Deduplication | Perplexity filtering, MinHash deduplication |
| **3. Tokenization** | Building Custom Tokenizers | BPE, SentencePiece, Vocabulary size selection |
| **4. Architecture Design** | Model Architecture Choices | Transformer variants, Parameter scaling laws |
| **5. Training Strategy** | Pre-training Objectives | Causal LM, Masked LM, Next Sentence Prediction |
| **6. Infrastructure** | Distributed Training Setup | FSDP, ZeRO, Multi-node training |
| **7. Evaluation** | Pre-training Metrics | Perplexity, Zero-shot evaluation |

---

## 1. 📊 Data Collection & Corpus Building

LLM ko pre-train karne ke liye bahut saara high-quality text data chahiye hota hai.

### A. Common Data Sources
- **Common Crawl:** Web crawl data (petabytes of text) - Internet ka saara content
- **The Pile:** Academic aur high-quality text corpus - Research papers, books
- **RedPajama:** Open-source reproduction of LLaMA dataset - LLaMA jaise dataset ka open version
- **BooksCorpus:** Fiction aur non-fiction books - Kahaniyan aur gyan ki books
- **Wikipedia:** Structured knowledge base - Organized knowledge base

### B. Data Quality Considerations
- **Domain diversity:** Technical, creative, conversational text ka mix hona chahiye
- **Language distribution:** Multiple languages ya single language focus
- **Temporal coverage:** Recent data ya historical data - Time period ka selection

---

## 2. 🧹 Data Cleaning Pipeline

Raw web data mein noise, duplicates, aur low-quality content hota hai.

### A. Quality Filtering
- **Perplexity filtering:** Too random ya too predictable text ko remove karna
- **Language detection:** Target language ke hisaab se filter karna
- **Content quality:** Spam, boilerplate, low-information text ko hata dena

### B. Deduplication Techniques
- **MinHash LSH:** Efficient near-duplicate detection - Similar documents dhundna
- **Exact deduplication:** Identical documents ko remove karna
- **Paragraph-level deduplication:** Document ke andar repeated content hata dena

---

## 3. 🔤 Tokenizer Training

Custom tokenizers domain-specific models ke liye bahut important hote hain.

### A. Tokenization Algorithms
- **Byte Pair Encoding (BPE):** LLMs ke liye sabse common
- **SentencePiece:** Language-agnostic tokenization - Kisi bhi language ke liye
- **WordPiece:** BERT models mein use hota hai

### B. Vocabulary Design
- **Size selection:** 32k-256k tokens (efficiency aur coverage ka balance)
- **Special tokens:** [CLS], [SEP], [MASK], [PAD] different tasks ke liye
- **Multilingual support:** Multiple languages ko efficiently handle karna

---

## 4. 🏗️ Model Architecture Design

Apne use case ke liye sahi architecture choose karna.

### A. Transformer Variants
- **Decoder-only:** GPT-style (causal attention) - Text generation ke liye
- **Encoder-only:** BERT-style (bidirectional attention) - Understanding ke liye  
- **Encoder-decoder:** T5-style (sequence-to-sequence) - Translation ke liye

### B. Scaling Laws
- **Chinchilla scaling:** Model size aur data ke beech optimal compute allocation
- **Parameter efficiency:** Apne compute budget ke hisaab se sweet spot dhundna
- **Architecture innovations:** Rotary embeddings, RMSNorm, SwiGLU - Modern improvements

---

## 5. 🎯 Pre-training Objectives

Different model types ke liye different objectives.

### A. Causal Language Modeling (CLM)
- **Used in:** GPT, LLaMA, Mistral
- **Objective:** Previous tokens dekh kar next token predict karna
- **Advantage:** Natural for text generation - Text banane ke liye perfect

### B. Masked Language Modeling (MLM)
- **Used in:** BERT, RoBERTa
- **Objective:** Context mein masked tokens ko predict karna
- **Advantage:** Better for understanding tasks - Samajhne ke liye behtar

### C. Next Sentence Prediction (NSP)
- **Used in:** BERT
- **Objective:** Predict if two sentences consecutive hain ya nahi
- **Modern approach:** Often skipped in favor of longer sequences

---

## 6. ⚙️ Training Infrastructure

Large models ko scale karna.

### A. Distributed Training Strategies
- **Data Parallelism:** Batch ko GPUs mein split karna
- **Model Parallelism:** Model ko GPUs mein split karna
- **Pipeline Parallelism:** Layers ko GPUs mein split karna
- **FSDP (Fully Sharded Data Parallel):** Large models ke liye modern standard

### B. Optimization Techniques
- **Mixed Precision:** FP16/BF16 training for memory efficiency
- **Gradient Accumulation:** Larger batch sizes simulate karna
- **Learning Rate Scheduling:** Cosine decay with warmup

---

## 7. 📈 Pre-training Evaluation

Training progress aur model quality ko monitor karna.

### A. Training Metrics
- **Perplexity:** Language modeling ka primary metric
- **Loss curves:** Convergence aur overfitting ko monitor karna
- **Gradient norms:** Training stability check karna

### B. Zero-shot Evaluation
- **MMLU:** Massive Multitask Language Understanding - Multiple tasks par test
- **HellaSwag:** Commonsense reasoning - Common sense check
- **TruthfulQA:** Truthfulness evaluation - Sachai test
- **GSM8K:** Mathematical reasoning - Maths solving test

---

## 🧪 Practice Exercises

### Exercise 1: Data Pipeline Design
1B parameter model ke liye data processing pipeline design karo:
- Data requirements estimate karo (Chinchilla scaling)
- Appropriate data sources choose karo
- Cleaning aur deduplication steps design karo

### Exercise 2: Architecture Selection
Decoder-only vs encoder-decoder architectures compare karo:
- Dono ke use cases
- Training efficiency considerations
- Inference performance differences

---

## 📚 Resources

### Essential Papers
- "Attention is All You Need" (Transformer)
- "Scaling Laws for Neural Language Models" (OpenAI)
- "Training Compute-Optimal Large Language Models" (Chinchilla)

### Tools & Libraries
- **Hugging Face Transformers:** Model implementations
- **Megatron-LM:** Large-scale training framework
- **DeepSpeed:** Optimization library
- **EleutherAI tools:** Open-source pre-training utilities

---

## 🏆 Checklist
- [ ] Data collection aur cleaning requirements samajh mein aaye
- [ ] Custom tokenizers train karne aata hai
- [ ] Appropriate model architecture choose kar sakte hain
- [ ] Different pre-training objectives samajh mein aaye
- [ ] Distributed training strategies familiar hain
- [ ] Pre-training progress evaluate kar sakte hain

> **Pro Tip:** Pre-training compute-intensive hai par foundational. Chhote models (100M-1B parameters) se start karo pipeline seekhne ke liye, phir scale up karo.