# LLM Interview Preparation (2026 Edition)

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, LLM interviews ab sirf "Prompt Engineering" ke baare mein nahi rahe. Interviewer ab yeh dekhna chahta hai ki kya tum model ki "Internal Working" samajhte ho ya nahi.

Interview mein woh tumse Transformer ke andar ka math pooch sakta hai, ya yeh ki "H100 GPU par model train karte waqt agar loss NaN ho jaye toh kya karoge?". Is guide mein humne woh saare sawal cover kiye hain jo ek senior AI Engineer role ke liye zaroori hain. Taiyari aisi honi chahiye ki interviewer ko lage ki tumne sirf API nahi chalayi, balki model ko "Feel" kiya hai.

---

## 2. Deep Technical Interview Topics
1.  **Transformer Architecture**: Multi-head attention, self-attention, cross-attention, positional encoding (RoPE vs Sinusoidal), LayerNorm vs RMSNorm.
2.  **Training Pipelines**: Pre-training objectives, tokenization strategies (BPE), dataset curation, catastrophic forgetting.
3.  **Fine-tuning & Alignment**: SFT, RLHF, DPO, PPO, LoRA, QLoRA.
4.  **Inference Optimization**: Quantization (bitsandbytes, GGUF, EXL2), KV Cache, Paged Attention (vLLM), Speculative Decoding.
5.  **RAG & Retrieval**: Vector databases, hybrid search, reranking, GraphRAG, Agentic RAG.
6.  **Agentic Systems**: Tool use, planning (ReAct), multi-agent orchestration, memory management.

---

## 3. Mathematical Questions (Whiteboard)
- Derive the time complexity of Self-Attention $O(N^2 d)$.
- Explain the significance of the $\sqrt{d_k}$ denominator in Scaled Dot-Product Attention.
- What is the difference between Cross-Entropy and KL Divergence in the context of DPO?
- How does RoPE (Rotary Positional Embedding) use rotation matrices to maintain relative distance?

---

## 4. Architecture Design Scenario
**Question**: "Design a RAG system for a legal firm that needs to query 1 million 100-page PDF documents with extremely high accuracy and low latency."
**Key points to cover**:
- Chunking strategy (Semantic chunking).
- Embedding model selection.
- Hierarchical indexing.
- Cross-encoder reranking.
- Caching layer (Semantic cache).
- Human-in-the-loop for edge cases.

---

## 5. Coding Challenge Example
"Implement a simple multi-head attention head in PyTorch without using `nn.MultiheadAttention`."
(Refer to `03_Transformers_From_Scratch/Building_GPT_From_Scratch.md` for solution).

---

## 6. Failure Analysis Questions
- "Your model is hallucinating specific dates in a financial report. How do you fix it without re-training?" (Answer: RAG with citations, prompt engineering with 'I don't know' instructions, or constrained decoding).
- "The model's throughput dropped by 50% after moving to a new GPU. What do you check?" (Answer: CUDA version, Flash Attention compatibility, VRAM fragmentation).

---

## 7. Tradeoff Discussions
- **Parameter Count vs. Context Length**: Larger models reason better but have smaller context limits on same hardware.
- **RAG vs. Fine-tuning**: RAG for dynamic/private data; Fine-tuning for style/format/domain-specific language.
- **Quantization vs. Accuracy**: 4-bit vs 8-bit tradeoffs in reasoning capability.

---

## 8. Debugging Scenarios
- "Training loss is flat for 5000 steps. Debug."
- "The model is repeating the same sentence in a loop. Why?"
- "The agent is stuck in an infinite tool-calling loop. How to break it?"

---

## 9. Best Practices in Interviews
- **Be Practical**: Don't just give theoretical answers. Mention specific libraries (vLLM, Unsloth, LangGraph).
- **Cost Awareness**: Always mention how your design saves GPU costs.
- **Security First**: Mention prompt injection and PII protection in every design question.

---

## 10. Latest 2026 Patterns to Mention
- **In-Context Learning (ICL) scaling**.
- **Self-Improving models (o1-style)**.
- **Small Language Models (SLMs) for production edge cases**.

---

## 11. Mock Interview: The 15-Minute Technical Drill
1. What is the KV Cache and why is it $O(N)$?
2. Explain LoRA's rank $r$ and how it affects training.
3. How does vLLM solve VRAM fragmentation?
4. What is the 'Lost in the Middle' problem in long context?
5. Difference between Hard vs Soft prompt tuning.
6. When would you use DPO instead of RLHF?
7. Explain 'Chain of Thought' prompting intuition.
8. How to evaluate a RAG system using RAGAS?
9. What is 'Semantic Chunking'?
10. How to prevent Prompt Injection?
11. Explain 'Flash Attention' VRAM saving logic.
12. Why is 'Next Token Prediction' a good proxy for reasoning?
13. What is the 'Chinchilla scaling law'?
14. How to host a 70B model on two 40GB A100s?
15. What are 'mixture of experts' (MoE) routing layers?
