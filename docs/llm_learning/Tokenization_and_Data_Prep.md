# 🔤 Tokenization & Data Preparation — The Fuel of LLMs
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master Byte-Pair Encoding (BPE), Tokenizers, Data Deduplication, and Quality Filtering.

---

## 📋 Table of Contents: From Raw Data to Tokens

| Pillar | Topic | Why? |
|--------|-------|------|
| **1. The Split**| Word vs Char vs Subword | Context vs Vocabulary size tradeoff. |
| **2. BPE Engine**| Byte-Pair Encoding (BPE) | How GPT-4 tokenizes "Indivisible". |
| **3. Variants** | WordPiece vs Unigram | BERT and T5 styles of tokenization. |
| **4. Cleaning** | Quality Filtering & Deduplication| "Garbage In, Garbage Out". |
| **5. Encoding** | Specials Tokens [CLS], [SEP]| How models understand start and end. |
| **6. Tools** | Tiktoken & SentencePiece | The industry-standard libraries. |

---

## 🏗️ 1. Why Subword Tokenization? (The Choice)

- **Word Level:** Bohot bada vocabulary size (Millions of words), Unknown words (OOV) handle nahi hote.
- **Char Level:** Vocabulary bohot choti (256 bytes) par sentence bohot lamba (Computation heavy).
- **Subword Level (Best):** Words ko components mein todna (e.g. `Lower -> Low + er`). All words covered with ~50k to 100k vocabulary.

---

## 🌀 2. BPE (Byte-Pair Encoding): The GPT Way

BPE sabse popular algorithm hai.
1. Har char ko pehle count karo.
2. Sabse frequent "Pair" ko ek naya symbol banao.
3. Tab tak merge karo jab tak vocabulary target complete na ho jaye.

> 💡 **Byte-level BPE (Llama/GPT-4):** Ye unicode bytes par kaam karta hai, isliye koi unknown word (OOV) kabhi nahi aata.

---

## 🧹 3. Data Cleaning (Pre-training magic)

Data is the boss. Piles of data (Common Crawl) ko clean kaise karte hain?
- **Language Identification:** Sirf wahi language rakho jo training ke liye chahiye.
- **Quality Scorer:** Bahar ke ads, gibberish, ya bad quality content (e.g. `asdfasdf`) identify karke remove karna.
- **Deduplication:** MinHash ya Fuzzy matching se duplicate paragraphs hatana (Avoid model overfitting).
- **Purity:** Personal names, addresses (PII) filter karna safely.

---

## 🚀 4. Tokenizer Libraries Comparison

| Tokenizer | Used In | Efficiency |
|-----------|---------|------------|
| **Tiktoken** | OpenAI GPT-4 | Extremely fast (Rust based). |
| **SentencePiece**| Llama series | Language agnostic (Google). |
| **FastTokenizers**| Hugging Face | Multi-threaded performance. |

---

## 🧪 Quick Test — LLM Data Engineer!

### Q1: "Tokenization is essentially lossy?"
**Answer:** Technically, yes. Agar tokenizer "Hindi" aur "Mandarin" words ko sahi se nahi todta (unbalanced), toh model unhe samajhne mein zyada compute power (tokens) kharch karega.

### Q2: WordPiece vs BPE?
- **BPE:** Max frequent pair merge karta hai (Frequency based).
- **WordPiece:** Likelihood of the language model increase karne ke liye merge karta hai (Probability based).

---

## 🏆 Final Summary Checklist
- [ ] BPE algorithm flow clear hai?
- [ ] Deduplication models kyu train karte hain? (Overfitting).
- [ ] Tokenizer vocab size vs Context window tradeoff.
- [ ] Special tokens ([BOS], [EOS], [PAD]) usage.

> **Data Tip:** A bad tokenizer can ruin a 100 Billion parameter model. Always check your "Tokens per Word" score.
