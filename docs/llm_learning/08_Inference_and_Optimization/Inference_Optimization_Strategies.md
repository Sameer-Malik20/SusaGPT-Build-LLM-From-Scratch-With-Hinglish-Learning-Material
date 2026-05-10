# 🎲 Decoding Strategies — Mastery 2026
> **Level:** Expert | **Language:** Hinglish | **Goal:** Master Speculative Decoding, Grammar constraints, and advanced sampling.

---

## 🧭 Core Concepts (Expert-First)

2026 mein model sirf tokens generate nahi kar rahe, wo **Inference Optimized** hain.

- **Speculative Decoding:** 2x speedup using a small "Draft" model.
- **Grammar-Constrained Decoding:** Forcing JSON, SQL, or XML valid outputs.
- **Contrastive Decoding:** Penalizing "Dumb" model tendencies.
- **Logit Manipulation:** Using biases and penalties (Frequency vs Presence).
- **Beam Search vs Nucleus:** When to use search vs sampling.

---

## 🏎️ 1. Speculative Decoding (The 2026 Speed Standard)

Standard decoding slow hai kyunki har token ke liye bada model run hota hai.
- **Logic:** Ek chota model (e.g., Llama-1B) 5-10 tokens generate karta hai (Draft). Phir bada model (e.g., Llama-70B) unhe ek saath "Verify" karta hai.
- **Result:** Same output, but **2x to 3x faster** inference.

---

## 🏗️ 2. Grammar-Constrained Decoding

AI ko "Random" text ke bajaye strictly valid **JSON** ya **Code** generate karne par majboor karna.
- **Tools:** `Outlines`, `Guidance`, or `vLLM` logits processors.
- **How?** Tokenize karte waqt sirf un tokens ko allow karna jo grammar rules (Regex/GBNF) follow karte hain.

---

## 🔍 3. Contrastive Search & Decoding

Sirf "Best" token uthana repetitive ho sakta hai.
- **Contrastive Search:** Current token ko "Pichle tokens" se compare karna taaki model loop mein na phase.
- **Contrastive Decoding:** Large model (Expert) ke logits se Small model (Amateur) ke logits minus karna. Isse model ki "Generic" aur "Boring" baatein khatam ho jati hain.

---

## 🛠️ 4. Repetition Control (OpenAI Style)

- **Frequency Penalty:** Jo tokens baar-baar aa rahe hain unhe penalize karna. (Good for long articles).
- **Presence Penalty:** Ek token ke "Appear" hone par use penalize karna (Encourages new topics).

---

## 🎲 5. Sampling Refined (Top-P vs Top-K)

- **Top-K (Fixed):** Sirf Top 50 tokens se choose karna.
- **Top-P (Dynamic):** Itne tokens uthana jinka total probability mass 90% (0.9) ho. Ye better hai kyunki context ke hisaab se "Choice" expand ya contract hoti hai.

---

## 📝 2026 Interview Scenarios (Decoding)

### Q1: "JSON mode mein hallucination kaise rokein?"
**Ans:** Grammar-constrained decoding use karke. Logits processor sirf valid characters (like `{`, `"`, `:`) allow karega at specific positions based on the schema.

### Q2: "Temperature = 0 ka kya matlab hai?"
**Ans:** Ye technically "Greedy Decoding" ban jata hai. Model hamesha highest probability wala token choose karega, koi randomness nahi hogi. Best for Math/Code.

---

## 🏆 Project Integration: SusaGPT Inference
Aapke inference engine mein:
- [x] `Speculative Decoding` implemented for Llama-3-70B using a 1B drafter.
- [x] `Repetition Penalty` of 1.2 to keep conversations fresh.
- [x] `Guided Decoding` for structured output extraction.

> **Final Insight:** The difference between a "Stupid" AI and a "Smart" AI is often just the **Decoding Strategy**. Master the sampling, and you master the creativity of the model.