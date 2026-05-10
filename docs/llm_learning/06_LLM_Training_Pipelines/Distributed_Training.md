# 🛳️ Distributed Training Deep Dive — Training Huge LLMs (Scaling Mastery)
> **Level:** Advanced → Expert | **Language:** Hinglish | **Goal:** Master DP, DDP, FSDP, Pipeline, and Tensor Parallelism.

---

## 📋 Table of Contents: Scaling AI Beyond One GPU

| Strategy | Full Name | How it Works? |
|----------|-----------|---------------|
| **1. DP** | Data Parallelism | Copy model on all GPUs, split data. |
| **2. DDP** | Distributed Data Par. | Efficient gradients sync (AllReduce). |
| **3. FSDP** | Fully Sharded Data Par. | Shard model, gradients, and optimizer. |
| **4. TP** | Tensor Parallelism | Split a single matrix multiplication. |
| **5. PP** | Pipeline Parallelism | Models layers split like an assembly line. |
| **6. ZeRO** | Zero Redundancy Opt. | DeepSpeed magic (Stage 1, 2, 3). |

---

## 1. 🚜 Data Parallelism (DP vs DDP)

Sabse simple strategy. Model chota hai par dataset bada hai.

### A. Data Parallelism (DP) - The Old Way
Ek GPU "Leader" banta hai, sabko model weights bhejta hai aur results collect karta hai.
- **Problem:** Leader GPU bottleneck ban jata hai (Slow).

### B. Distributed Data Parallelism (DDP) - The Industry Standard
Isme koi single leader nahi hota. Sab GPUs apne gradients calculate karte hain aur **All-Reduce** algorithm (Ring/Tree) se sync karte hain.
- **Use Case:** Jab model 1 GPU memory (e.g., 24GB or 80GB) mein fit ho raha ho.

---

## 2. 🧊 FSDP (Fully Sharded Data Parallelism): The Memory Saver

Agar model 70B parameters ka hai, toh wo 1 GPU (80GB A100) mein fit nahi hoga.
**FSDP** (Meta ki technique) model ke weights ko saare GPUs mein **"Shard"** (tod) deta hai.

1. **Model Sharding:** Har GPU ke paas model ka sirf ek part hota hai.
2. **On-the-fly Gathering:** Jab layer compute karni ho, tabhi baaki GPUs se part mangwao, compute karo, aur discard kar do.
- **Benefit:** 7B model ko hum 3-4 choti GPUs (12GB) par train kar sakte hain.

---

## 3. 🧩 Model Parallelism: TP & PP

Jab 1 single layer itni badi ho ki 1 GPU mein na aaye.

### A. Tensor Parallelism (TP)
Ek matrix multiplication (e.g., Attention head) ko bech se tod do. Half computation GPU-1 mein, half GPU-2 mein.
- **Fast Communication:** Sirf NVLink (NVIDIA server) par chalta hai kyunki bohot data transfer chahiye.

### B. Pipeline Parallelism (PP)
Layers ko divide kar do.
- GPU 1: Layers 1-10
- GPU 2: Layers 11-20
- **Problem (Bubble):** GPU 2 wait karega jab tak GPU 1 feed na kare. Ise "Micro-batches" se solve kiya jata hai.

---

## 🚀 DeepSpeed & ZeRO (Zero Redundancy Optimizer)

Microsoft ki **DeepSpeed** library ne LLM training ko revolutionize kiya. **ZeRO** 3 stages mein weights manage karta hai:
- **ZeRO-1:** Sirf Optimizer States shard karo.
- **ZeRO-2:** + Gradients shard karo.
- **ZeRO-3:** + Model weights shard karo (Full sharding).

---

## 📝 Practice Exercise (Decision Making)

### Scenario 1: Model size 7B, Data size 1TB, GPUs 8
**Decision:** DDP (Distributed Data Parallelism) use karo, kyunki 7B model 80GB/40GB GPU mein fit hota hai. Focus data speed par hona chahiye.

### Scenario 2: Model size 175B (GPT-3 level), GPUs 256
**Decision:** 3D Parallelism (TP + PP + DP) + DeepSpeed ZeRO-3. Sirf ek technique kaafi nahi hogi.

---

## 🏗️ Quick Setup (PyTorch logic)

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# Setup logic
# dist.init_process_group("nccl") # NVIDIA Collective Comm. Library
# model = model.to(rank)
# ddp_model = DDP(model, device_ids=[rank])
# sampler = DistributedSampler(dataset)
```

---

## 🔗 Resources
- [PyTorch DDP Tutorial](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- [DeepSpeed Official Docs](https://www.deepspeed.ai/)
- [Hugging Face Accelerate Library](https://huggingface.co/docs/accelerate/index)

---

## 🏆 Final Summary Checklist
- [ ] DDP vs DP ka fark explain kar sakte ho? (Hint: Ring All-Reduce).
- [ ] FSDP model sharding kaise karta hai?
- [ ] Tensor Parallelism kab use hota hai? (Huge layers).
- [ ] ZeRO Stage 3 kya save karta hai? (Full Memory).

> **Expert Tip:** Distributing training is as much about **Networking (NVLink/InfiniBand)** as it is about **GPU Compute**. Speed bottleneck aksar bandwidth hi hota hai.
