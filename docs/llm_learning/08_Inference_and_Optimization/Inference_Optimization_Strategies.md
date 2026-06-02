# 🎲 Decoding Strategies — Mastery 2026
> **Level:** Expert | **Language:** Hinglish | **Goal:** Speculative Decoding, Grammar constraints, aur advanced sampling ko master karna.

---

## 🧭 Core Concepts (Expert-First)

2026 mein model sirf tokens generate nahi kar rahe, wo **Inference Optimized** hain.

- **Speculative Decoding:** Chhote "Draft" model ke saath 2x speedup.
- **Grammar-Constrained Decoding:** JSON, SQL, ya XML valid outputs force karna.
- **Contrastive Decoding:** "Dumb" model tendencies ko penalize karna.
- **Logit Manipulation:** Biases aur penalties use karna (Frequency vs Presence).
- **Beam Search vs Nucleus:** Search vs sampling kab use karna hai.

---

## 🏎️ 1. Speculative Decoding (The 2026 Speed Standard)

Standard decoding slow hai kyunki har token ke liye bada model run hota hai.
- **Logic:** Ek chota model (e.g., Llama-1B) 5-10 tokens generate karta hai (Draft). Phir bada model (e.g., Llama-70B) unhe ek saath "Verify" karta hai.
- **Result:** Same output, lekin **2x to 3x tez** inference.

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

- **Frequency Penalty:** Jo tokens baar-baar aa rahe hain unhe penalize karna. (Long articles ke liye accha hai).
- **Presence Penalty:** Ek token ke "Appear" hone par use penalize karna (Naye topics encourage karta hai).

---

## 🎲 5. Sampling Refined (Top-P vs Top-K)

- **Top-K (Fixed):** Sirf Top 50 tokens se choose karna.
- **Top-P (Dynamic):** Itne tokens uthana jinka total probability mass 90% (0.9) ho. Ye better hai kyunki context ke hisaab se "Choice" expand ya contract hoti hai.

---

## 📝 2026 Interview Scenarios (Decoding)

### Q1: "JSON mode mein hallucination kaise rokein?"
**Ans:** Grammar-constrained decoding use karke. Logits processor sirf valid characters (jaise `{`, `"`, `:`) allow karega specific positions par, schema ke hisaab se.

### Q2: "Temperature = 0 ka kya matlab hai?"
**Ans:** Ye technically "Greedy Decoding" ban jata hai. Model hamesha highest probability wala token choose karega, koi randomness nahi hogi. Math/Code ke liye best hai.

---

## 🏆 Project Integration: SusaGPT Inference
Aapke inference engine mein:
- [x] `Speculative Decoding` Llama-3-70B ke liye 1B drafter ke saath implement kiya gaya hai.
- [x] `Repetition Penalty` 1.2 ka hai taaki conversations fresh rahe.
- [x] `Guided Decoding` structured output extraction ke liye.

> **Final Insight:** "Stupid" AI aur "Smart" AI ke beech ka farq aksar sirf **Decoding Strategy** hota hai. Sampling ko master karo, aur aap model ki creativity ko master karoge.