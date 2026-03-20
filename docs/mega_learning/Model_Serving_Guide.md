# Filename: Model_Serving_Guide.md

# Model Serving (vLLM / TGI / Ollama): AI ko Production mein Kaise Layein? (Complete Guide)

AI models ko train karna alag cheez hai aur unhe server pe "High Speed" mein serve karna alag. Production environments mein humein latency kam aur throughput zyada chahiye hoti hai.

## 1. Model Serving: Local vs Production
Model serving ka matlab hai model ko ek API (FastAPI, REST) ke peeche rakhna taki koi user use request bhej sake (curl or app). 

## 2. vLLM — High-Efficiency Serving Framework
vLLM (Virtual Large Language Model) aaj ke time ka sabse fast open-source serving solution hai. Ye **PagedAttention** (operating system ke virtual memory logic ki tarah) use karke speed aur memory efficiency badhata hai.

```bash
# Installation logic
# pip install vllm
# nohup python -m vllm.entrypoints.openai.api_server --model facebook/opt-125m &
```

## 3. vLLM OpenAI-Compatible API Server
vLLM default mein OpenAI-compatible API deta hai, yani aapka model OpenAI ke base client se directly connect ho sakta hai.

```python
import openai

# OpenAI library vLLM server se connect ho rahi hai
client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

# prompt generation
# response = client.chat.completions.create(model="...", messages=[{"role": "user", "content": "..."}])
```

## 4. TGI (Text Generation Inference) — Hugging Face's Power
TGI Hugging Face ne banaya hai. Ye Rust-based core use karta hai aur production level inference ke liye optimized hai. Ise hamesha Docker container se chalana chahiye.

```bash
# Docker setup code
# docker run --gpus all --shm-size 1g -p 8080:80 \
# -v $PWD/data:/data ghcr.io/huggingface/text-generation-inference:2.0 \
# --model-id Llama-3-8B-Instruct
```

## 5. Ollama: Local AI at Your Fingertips
Ollama local usage ke liye (Mac/Linux/Windows) best hai. Ye models ko lightweight tarike se serve karta hai aur CLI base setup deta hai.

```bash
# Ollama simple command
# ollama run llama3
# ollama serve # To start background server
```

## 6. Continuous Batching: Speed ka Raaz
Pehle models line by line process hote the. **Continuous Batching** model ko allow karti hai ki wo naye requests ko bich mein add kar sake bina pichle outputs ke liye wait kiye. Isse machine poori tarah utilize hoti hai.

## 7. Quantization: Chhota aur Tez Model
Model weights (FP32) ko 4-bit (INT4) ya 8-bit mein convert karne ki process. 
- **AWQ (Activation-aware Weight Quantization):** Inference speed badhata hai.
- **GPTQ:** Post-training quantization.
- **LoRA/QLoRA:** Fine-tuning ke waqt memory save karne ke liye.

## 8. Benchmark Table: vLLM vs TGI vs Ollama
| Framework | Best for | Core Language | Support |
|-----------|----------|---------------|---------|
| **vLLM** | High Throughput | Python/CUDA | Multi-GPU |
| **TGI** | Enterprise Stability | Rust/Python | High Scale |
| **Ollama** | Local Use (Devs) | Go/C++ | Windows/Mac |

Project Exercise: Test a local Llama model with Ollama and benchmark response time (tokens per second).
