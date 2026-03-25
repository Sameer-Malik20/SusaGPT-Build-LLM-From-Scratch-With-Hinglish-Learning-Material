# 🐳 Docker & FastAPI: AI Deployment (Expert Guide)
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master FastAPI AI endpoints, Multi-stage Docker builds, and GPU orchestration

---

## 📋 Is Guide Se Kya Seekhoge

| Section | Topic | Why? |
|---------|-------|------|
| 1. FastAPI Internals | Dependency Injection, Async Handlers | High performance APIs |
| 2. AI endpoints Design | /generate, /embed, Metadata handling | Unified AI API |
| 3. Docker Foundations | Layers, Cache, Base images | Efficient packaging |
| 4. Multi-stage Docker | Build vs Runtime size optimization | Fast pulls |
| 5. Docker Compose & GPU | NVIDIA Container Toolkit | Multi-container orchestration |
| 6. Production Safety | Secrets, Health checks, Resource limits | Reliability |

---

## 1. ⚡ FastAPI for AI: Beyond Basics

Sirf `@app.get` se kaam nahi chalega. AI models memory aur compute intensive hote hain.

### A. Async Request Handling
AI model calls (like OpenAI or local vLLM) `io-bound` as well as `cpu-bound` ho sakti hain. `async def` allow karta hai multiple requests same time handle karna.

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI(title="SusaGPT API")

# Logic model config
class Query(BaseModel):
    prompt: str
    max_new_tokens: int = 120

@app.post("/generate")
async def generate(q: Query):
    # Simulated model call
    # response = await model_inference_engine(q.prompt)
    return {"status": "ok", "response": "Generated result"}
```

---

## 2. 📝 AI Endpoint Best Practices

AI API hamesha **Metadata** return karni chahiye (Tokens used, seed, finish reason).

```python
# Response Model Logic
@app.post("/v1/chat/completions")
async def chat_completion(q: Query):
    return {
        "id": "chat-svc-123",
        "object": "chat.completion",
        "choices": [{"message": {"content": "...", "role": "assistant"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 50, "total_tokens": 60}
    }
```

---

## 3. 📦 Docker for AI: Optimization is Key

AI images (PyTorch, CUDA) 10GB+ tak ho jati hain. Hamein optimized `Dockerfile` likhna chahiye.

### A. Good Dockerfile Blueprint
```dockerfile
# 1. Base Image selection (use specific runtime version)
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# 2. System Level dependencies
RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

# 3. Working Directory
WORKDIR /app

# 4. Cache optimized Dependency Installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Application Code
COPY . .

# 6. Runtime Config
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# 7. Start Command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 4. 🚀 Multi-stage Builds: Reduce Image Size

Multi-stage build mein hum "Build stage" mein sab libraries compile karte hain aur "Runtime stage" mein sirf use binary/package copy karte hain.

```dockerfile
# Stage 1: Build logic
FROM python:3.10-slim as builder
RUN pip install --user some-heavy-ai-library

# Stage 2: Final runtime logic
FROM python:3.10-slim
COPY --from=builder /root/.local /root/.local
# Runtime image size will be much smaller!
```

---

## 5. 🛠️ GPU Orchestration with Docker-Compose

Docker container default mein GPU ko "dekh" nahi sakta. Hum **nvidia-container-toolkit** use karte hain.

```yaml
version: '3.8'
services:
  vllm-server:
    image: vllm/vllm-openai
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1 # Number of GPUs to use
              capabilities: [gpu]
    command: --model facebook/opt-125m

  api-gateway:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - vllm-server
```

---

## 6. 🛡️ Production Readiness

1. **Health Checks:** Container tabhi healthy mark ho jab model load ho jaye.
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```
2. **Secrets Management:** `.env` files ya Docker Secrets use karein API keys ke liye.
3. **Resource Limits:** Docker ko 24GB RAM limit karein taki system crash na ho OOM ki wajah se.

---

## 🏗️ Mega Project: Containerized AI Chat Stack

Workflow:
1. Ek `FastAPI` app banayenge jo local model (Transformers) handle karegi.
2. `Redis` container add karenge chat history (Memory) store karne ke liye.
3. `docker-compose.yml` se pure stack ko run karenge.
4. Auto-restart policy apply karenge error handling ke liye.

---

## 🧪 Quick Test — Professional Level Check!

### Q1: Layer Cache logic
`COPY . .` command ko niche kyu rkhna chahiye `RUN pip install` se?
<details><summary>Answer</summary>
Docker layer caching use karta hai. Agar hum code change karein (jo `.` mein hai), toh Docker sab purane layers invalidate kar dega. Pip install agar pehle hai, toh bar-bar code change karne par dependencies dobara download nahi hongi (Space aur Time save).
</details>

### Q2: GPU Passthrough logic
Host system pe drivers installed nahi hain lekin Docker Image mein CUDA hai — Model Chalega?
<details><summary>Answer</summary>
**Nahi!** Host OS pe NVIDIA drivers installed aur running hone chahiye NVIDIA container runtime ke saath. Docker image physical hardware se driver level pe directly communicate nahi kar sakti bina Host drivers ke.
</details>

---

## 🔗 Resources
- [NVIDIA Container Toolkit Docs](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html)
- [FastAPI Best Practices (GitHub)](https://github.com/zhanymkanov/fastapi-best-practices)
- [Dockerizing AI Models Guide](https://docker.com/blog/how-to-dockerize-python-ai-ml-apps/)
