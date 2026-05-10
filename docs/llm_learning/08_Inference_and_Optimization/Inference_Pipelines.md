# 🚀 LLM Deployment & Serving - Production Ready Systems
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** LLMs ko production mein deploy aur serve karne ki complete guide

---

## 📋 Table of Contents: Deployment Pipeline

| Stage | Focus | Key Technologies |
|-------|-------|------------------|
| **1. Model Preparation** | Optimization & Packaging | Quantization, ONNX, TorchScript |
| **2. Serving Infrastructure** | Inference Server Setup | vLLM, TGI, Triton Inference Server |
| **3. API Design** | Client Interfaces | REST, gRPC, WebSocket |
| **4. Scaling** | Load Handling | Kubernetes, Auto-scaling, Load Balancers |
| **5. Monitoring** | Performance Tracking | Prometheus, Grafana, OpenTelemetry |
| **6. Cost Optimization** | Resource Management | Spot instances, Model caching |

---

## 1. 🏗️ Model Preparation for Production

### A. Optimization Techniques

#### 1. **Quantization**
- **INT8 Quantization:** 4x memory reduction, minimal accuracy loss
- **FP8 Quantization:** New standard for inference efficiency
- **GPTQ/AWQ:** Post-training quantization for LLMs

#### 2. **Model Pruning**
- **Unstructured Pruning:** Individual weights remove karna
- **Structured Pruning:** Entire neurons/channels remove karna
- **Magnitude-based:** Smallest weights prune karna

#### 3. **Knowledge Distillation**
- Large teacher model se small student model train karna
- **Benefit:** 10x smaller model with similar performance

### B. Packaging Formats

#### 1. **ONNX (Open Neural Network Exchange)**
- Framework-agnostic model format
- **Advantage:** Multiple inference engines support karte hain

```python
import torch
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("gpt2")
dummy_input = torch.randint(0, 100, (1, 10))
torch.onnx.export(model, dummy_input, "model.onnx")
```

#### 2. **TorchScript**
- PyTorch models ko serializable format mein convert karna
- **Use case:** C++ deployment ke liye

#### 3. **TensorFlow SavedModel**
- TensorFlow models ka standard format
- **Advantage:** Versioning aur signatures support karta hai

---

## 2. ⚡ Inference Serving Engines

### A. vLLM (Virtual LLM)

#### Key Features:
- **PagedAttention:** Efficient KV cache management
- **Continuous Batching:** Dynamic request batching
- **High throughput:** 2-4x better than traditional serving

#### Deployment Example:
```bash
# Install vLLM
pip install vllm

# Start server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-chat-hf \
    --port 8000 \
    --tensor-parallel-size 2
```

### B. TGI (Text Generation Inference)

#### Key Features:
- **Hugging Face optimized:** Transformers library integration
- **Tensor Parallelism:** Multi-GPU support
- **Flash Attention:** Optimized attention computation

#### Docker Deployment:
```bash
docker run --gpus all \
    -p 8080:80 \
    -v /path/to/models:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Llama-2-7b-chat-hf \
    --num-shard 2
```

### C. Triton Inference Server

#### Key Features:
- **Multi-framework support:** PyTorch, TensorFlow, ONNX
- **Ensemble models:** Multiple models pipeline
- **Dynamic batching:** Automatic request batching

#### Configuration Example:
```yaml
name: "llama_7b"
platform: "pytorch_libtorch"
max_batch_size: 8
input [
  {
    name: "input_ids"
    data_type: TYPE_INT64
    dims: [ -1 ]
  }
]
output [
  {
    name: "output"
    data_type: TYPE_FP32
    dims: [ -1, 50257 ]
  }
]
```

---

## 3. 🔌 API Design Patterns

### A. REST API Design

#### OpenAI-compatible API:
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

@app.post("/v1/completions")
async def create_completion(request: CompletionRequest):
    # Model inference logic
    response = model.generate(request.prompt, 
                             max_tokens=request.max_tokens,
                             temperature=request.temperature)
    return {"choices": [{"text": response}]}
```

### B. gRPC for High Performance

#### Advantages:
- **Binary protocol:** Smaller payloads, faster serialization
- **Streaming support:** Bidirectional streaming
- **Language agnostic:** Multiple client languages

#### Protobuf Definition:
```protobuf
syntax = "proto3";

service LLMService {
  rpc Generate(GenerationRequest) returns (GenerationResponse);
  rpc StreamGenerate(stream GenerationRequest) returns (stream GenerationResponse);
}

message GenerationRequest {
  string prompt = 1;
  int32 max_tokens = 2;
  float temperature = 3;
}

message GenerationResponse {
  string text = 1;
  int32 tokens_generated = 2;
}
```

### C. WebSocket for Real-time Streaming

#### Implementation:
```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws/generate")
async def websocket_generate(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        prompt = data["prompt"]
        
        # Stream tokens one by one
        for token in model.stream_generate(prompt):
            await websocket.send_text(token)
```

---

## 4. 📈 Scaling Strategies

### A. Horizontal Scaling

#### 1. **Kubernetes Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-inference
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-inference
  template:
    metadata:
      labels:
        app: llm-inference
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
```

#### 2. **Auto-scaling Configuration**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-inference
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### B. Load Balancing

#### 1. **Round-robin Load Balancer**
- Simple distribution across instances
- **Limitation:** Doesn't consider instance load

#### 2. **Least Connections**
- New requests to least busy instance
- **Better for:** Variable request processing times

#### 3. **Intelligent Routing**
- Model-based routing (small models vs. large models)
- **Advanced:** Request characteristics ke hisaab se routing

---

## 5. 📊 Monitoring & Observability

### A. Key Metrics to Track

#### 1. **Performance Metrics**
- **Throughput:** Requests per second
- **Latency:** P50, P90, P99 response times
- **Token generation speed:** Tokens per second

#### 2. **Resource Metrics**
- **GPU Utilization:** Memory usage, compute utilization
- **CPU/Memory:** System resource usage
- **Network I/O:** Bandwidth consumption

#### 3. **Business Metrics**
- **Cost per request:** Inference cost calculation
- **Error rates:** Failed requests percentage
- **User satisfaction:** Response quality metrics

### B. Monitoring Stack

#### Prometheus Configuration:
```yaml
scrape_configs:
  - job_name: 'llm-inference'
    static_configs:
      - targets: ['llm-service:8000']
    metrics_path: '/metrics'
```

#### Grafana Dashboard:
- Real-time throughput visualization
- Latency distribution graphs
- Resource utilization heatmaps

### C. Distributed Tracing

#### OpenTelemetry Integration:
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

@app.post("/generate")
async def generate_text(request: GenerationRequest):
    with tracer.start_as_current_span("llm_inference"):
        # Inference logic
        return {"text": generated_text}
```

---

## 6. 💰 Cost Optimization Strategies

### A. Infrastructure Optimization

#### 1. **Spot Instances**
- 60-90% cost savings
- **Strategy:** Multiple availability zones, checkpointing

#### 2. **Autoscaling**
- Scale down during low traffic
- **Implementation:** Schedule-based scaling

#### 3. **Model Caching**
- Frequent requests ke responses cache karna
- **Implementation:** Redis or similar caching layer

### B. Model Optimization

#### 1. **Model Selection**
- Task ke hisaab se right-sized model choose karna
- **Rule of thumb:** Start small, scale up only if needed

#### 2. **Dynamic Batching**
- Batch size dynamically adjust karna based on load
- **Benefit:** Higher GPU utilization

#### 3. **Request Prioritization**
- High-priority requests ko preferential treatment
- **Implementation:** Multiple queues with different priorities

---

## 7. 🧪 Practical Deployment Exercise

### Exercise 1: Local vLLM Deployment
1. vLLM install karo aur test model load karo
2. OpenAI-compatible API server start karo
3. Python client se test requests send karo
4. Performance metrics collect karo

### Exercise 2: Kubernetes Deployment
1. Docker image build karo apne model ke saath
2. Kubernetes deployment YAML create karo
3. Service aur ingress configure karo
4. Load testing karo aur scaling observe karo

### Exercise 3: Monitoring Setup
1. Prometheus aur Grafana install karo
2. Custom metrics expose karo apne inference service se
3. Dashboard create karo key metrics ke liye
4. Alert rules configure karo for anomalies

---

## 📚 Resources

### Essential Tools
- **vLLM:** High-throughput LLM serving
- **Text Generation Inference (TGI):** Hugging Face optimized serving
- **Triton Inference Server:** NVIDIA's production inference server
- **Kubernetes:** Container orchestration
- **Prometheus/Grafana:** Monitoring stack

### Learning Resources
- **vLLM Documentation:** Official serving guide
- **Kubernetes for ML:** Production ML deployment patterns
- "Designing Data-Intensive Applications" (Book): Systems design principles

### Best Practices
- **Start simple:** Single instance deployment se start karo
- **Measure everything:** Comprehensive monitoring implement karo
- **Plan for failure:** Redundancy aur failover mechanisms design karo
- **Cost awareness:** Early stage se cost optimization consider karo

---

## 🏆 Checklist
- [ ] Model optimization techniques apply kar sakte hain
- [ ] vLLM/TGI inference server deploy kar sakte hain
- [ ] REST/gRPC APIs design aur implement kar sakte hain
- [ ] Kubernetes par LLM service deploy kar sakte hain
- [ ] Monitoring aur observability setup kar sakte hain
- [ ] Cost optimization strategies implement kar sakte hain
- [ ] Production deployment best practices jaante hain

> **Pro Tip:** Production deployment iterative process hai. Start with minimum viable deployment, measure performance, gather feedback, aur gradually improve karte raho.