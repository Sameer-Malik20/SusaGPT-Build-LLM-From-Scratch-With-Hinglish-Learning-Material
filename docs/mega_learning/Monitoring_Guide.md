# Filename: Monitoring_Guide.md

# ML Monitoring aur Observability: AI in Production (Complete Guide)

Production mein AI models kabhi bhi galat ho sakte hain (Data drift, model decay). Monitoring ensure karti hai ki humein waqt rehte pata chale.

## 1. Monitoring kyun zaroori hai?
Aapka model test data pe 90% accuracy deta hai, lekin real users ke saath 60% ho jaata hai. Ise **Production Performance Gap** kehte hain. Hamein latency (speed), throughput (batches), cost (API bills), aur quality (hallucinations) sab track karne hain.

## 2. Weights & Biases (W&B): The Standard
W&B model training ke waqt sabse bada aur popular dashboard deta hai. 
Isse hum loss curve, memory usage, aur graphs dekh sakte hain real-time mein.

```python
import wandb

# Initializing project
wandb.init(project="my_ai_model", config={"lr": 0.001, "epochs": 10})

# Metrics logging logic
for epoch in range(10):
    loss = 0.5 / (epoch + 1)
    wandb.log({"loss": loss, "epoch": epoch})

# End of training process
wandb.finish()
```

## 3. Training Monitoring: Charts & Alerts
Training ke waqt `wandb` ya `TensorBoard` use karke hum checkpoints save karte hain aur accuracy ko graph format mein monitor karte hain.

```python
from transformers import Trainer, TrainingArguments

# HuggingFace integration logic
# args = TrainingArguments(output_dir="./res", report_to="wandb")
# trainer = Trainer(model, args=args, ...)
```

## 4. LLM Output Monitoring: quality control
LLMs hallucinations (galat information) de sakte hain. Ise monitor karne ke liye hum prompt analytics use karte hain.
- **Latency:** Har token kitne time mein aa raha hai.
- **Cost:** Har request mein kitne tokens use ho rahe hain.

## 5. LangSmith: Debugging & Tracing AI Chains
LangChain ne LangSmith banaya hai traces dekhne ke liye. Ye batata hai ki aapke prompt ka kaunsa part model ne focus kiya.

```bash
# Terminal export logic
# export LANGCHAIN_TRACING_V2=true
# export LANGCHAIN_API_KEY=ls__... (From LangSmith website)
```

## 6. Prometheus + Grafana: System Monitoring
Jab model serving fast-scale pe ho, toh Prometheus API metrics (requests/sec, GPU temperature) collect karta hai aur Grafana dashboards banata hai.

```yaml
# Prometheus configuration snippet
# scrape_configs:
#   - job_name: 'vllm_api'
#     static_configs:
#       - targets: ['localhost:8000']
```

## 7. Alerting: Slack Pe Notification
Agar loss badh raha hai ya API down hai, toh auto-alerts (Slack/Discord) trigger ho sakte hain.

```python
# Alert trigger dummy logic
def check_performance(latency):
    if latency > 1000: # agar latency 1000ms+ hai
        # send_slack_notification("High Latency Alert!")
        pass
```

## 8. Cost Monitoring: Budget control
OpenAI ya Anthropic APIs use karte waqt billing limits set karna zaroori hai. Production mein API costs track karne ke liye logging wrapper banayein.

```python
import time

def track_cost_and_latency(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        # API call execute logic
        res = func(*args, **kwargs)
        duration = time.time() - start
        print(f"Time taken: {duration:.2f}s | Tokens used: {res.usage.total_tokens}")
        return res
    return wrapper
```
