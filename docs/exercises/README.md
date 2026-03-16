# 🎮 Interactive Exercises — Yahan Code Run Karo!

> **Ye folder saare topics ke interactive Python demos rakhta hai.**
> **Markdown me code padhne ke baad wahan khud run karo aur dekho!**

---

## 🚀 Ek Command Se Sab Kuch:

```bash
# Ye ek command sab kuch shuru kar deta hai!
python docs/exercises/run_me.py
```

---

## 📦 Individual Scripts

| Script | Topics | Run Command |
|--------|--------|-------------|
| `run_me.py` | 🏠 Main launcher (sab ek jagah) | `python docs/exercises/run_me.py` |
| `tokenizer_demo.py` | BPE algorithm, Byte encoding | `python docs/exercises/tokenizer_demo.py` |
| `architecture_demo.py` | Attention, GQA, SwiGLU, RMSNorm, RoPE | `python docs/exercises/architecture_demo.py` |
| `training_demo.py` | Loss, AdamW, Gradient Clipping, LR Scheduler | `python docs/exercises/training_demo.py` |
| `sampling_demo.py` | Top-K, Top-P, KV Cache, Repetition Penalty | `python docs/exercises/sampling_demo.py` |
| `evaluation_demo.py` | BLEU Score, Perplexity | `python docs/exercises/evaluation_demo.py` |
| `ai_agents_demo.py` | AI Agents, Weather Agent, Research Agent | `python docs/exercises/ai_agents_demo.py` |
| `agentic_ai_demo.py` | Agentic AI, Competitor Research, Reflection | `python docs/exercises/agentic_ai_demo.py` |
| `mcp_demo.py` | MCP Server, Tools, Interactive Client | `python docs/exercises/mcp_demo.py` |

---

## 🔗 MD File → Demo Mapping

| MD File | Corresponding Demo |
|---------|-------------------|
| `docs/susagpt/SusaGPT_Diagram_Guide.md` | `tokenizer_demo.py`, `sampling_demo.py` |
| `docs/susagpt/SusaGPT_Architecture.md` | `architecture_demo.py` |
| `docs/susagpt/SusaGPT_Skills.md` | `training_demo.py`, `evaluation_demo.py` |
| `docs/ai/AI_Agents_Guide.md` | `ai_agents_demo.py` |
| `docs/ai/Agentic_AI_Guide.md` | `agentic_ai_demo.py` |
| `docs/ai/MCP_Guide.md` | `mcp_demo.py` |
| `README.md` | `run_me.py` (all topics) |

---

## ⚙️ System Requirements

| Script | Requirements |
|--------|-------------|
| `tokenizer_demo.py` | ✅ No extra — only Python stdlib |
| `architecture_demo.py` | 🔶 PyTorch (`pip install torch`) |
| `training_demo.py` | 🔶 PyTorch for demos 1-3; stdlib for 4-6 |
| `sampling_demo.py` | 🔶 PyTorch for demos 1,2,4; stdlib for 3,5 |
| `evaluation_demo.py` | ✅ No extra — only math, re |
| `ai_agents_demo.py` | ✅ No extra |
| `agentic_ai_demo.py` | ✅ No extra |
| `mcp_demo.py` | ✅ No extra |

---

## 🧩 Har Demo Me Kya Milega?

```
Har demo me ye hota hai:
  📊 Live Visualizations (text-based)
  🎮 Interactive Inputs (aap khud parameters set karo)
  ✏️  Exercises (khud solve karo)
  📝 MCQ Test (answers check ho jaate hain)
  ⭐ Score tracking
```

---

## 💡 Tips

- **PyTorch demos**: `architecture_demo.py` aur training demos ke liye pytorch chahiye
- **Without PyTorch**: MCQ tests aur kuch demos bina torch ke bhi chalte hain
- **Windows me**: `python` command use karo, `python3` nahi
- **Keyboard shortcuts**: Kisi bhi demo me `Ctrl+C` se exit kar sakte ho
