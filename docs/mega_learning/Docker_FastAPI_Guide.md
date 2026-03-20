# Filename: Docker_FastAPI_Guide.md

# Docker + FastAPI: AI Model Deployment (Complete Guide)

Production mein AI models ko containers mein pack karke deploy karna zaroori hai. Isse "Work on my machine" wali problems khatam ho jaati hain.

## 1. FastAPI: Modern API Framework
FastAPI fast hai aur async support deta hai. Isse AI models serve karna bahut efficient hota hai.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.post("/generate")
async def generate_text(req: ChatRequest):
    # Model inference logic yahan aayegi
    return {"response": f"AI response for: {req.prompt}"}
```

## 2. Docker: The Container Engine
Docker model ke code, libraries (PyTorch, Transformers), aur OS environment ko ek "Image" mein pack kar deta hai.
- **Image:** Blue print.
- **Container:** Running instance.
- **Dockerfile:** Instructions setup image ke liye.

## 3. Optimizing Dockerfile for AI
AI images badi (5GB+) ho sakti hain. Hum multi-stage builds ya optimized base images use karte hain.

```dockerfile
# Base Image (PyTorch with CUDA support)
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

# Working directory setup
WORKDIR /app

# Dependencies copy aur install karna (Caching optimized)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code copy
COPY main.py .

# API server port expose karna
EXPOSE 8000

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 4. docker-compose: Multiple Services ka Pura Setup
Jab aapko (FastAPI + vLLM + Redis) saath chalane hon, toh docker-compose kaam aata hai.

```yaml
version: '3'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - VLLM_URL=http://vllm_service:8080/v1
    depends_on:
      - vllm_service

  vllm_service:
    image: vllm/vllm-openai:latest
    command: --model facebook/opt-125m
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## 5. Health Checks aur Graceful Shutdown
AI model loading mein time leta hai (Weights load karna). Health checks ensure karte hain ki API tabhi start ho jab model ready ho.

```python
@app.get("/health")
def health_check():
    # Model weight loading status check logic
    return {"status": "healthy", "model_ready": True}
```

## 6. Mini Project: End-to-End AI Docker Setup
Is project mein hum:
1. Ek simple FastAPI application banayenge `main.py`.
2. `requirements.txt` mein (fastapi, uvicorn, transformers) dalenge.
3. optimized `Dockerfile` banakar model serve karenge container mein.
4. `docker-compose.yml` se pure backend stack ko ek saath boot karenge commands se:
   - `docker-compose up --build`
   - `curl -X POST http://localhost:8000/generate -d '{"prompt": "Hello AI"}'`
