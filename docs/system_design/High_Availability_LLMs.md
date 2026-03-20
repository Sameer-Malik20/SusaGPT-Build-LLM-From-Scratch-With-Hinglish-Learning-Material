# 🚥 High Availability & Fault Tolerance for LLMs
> **Level:** Beginner → Expert | **Goal:** Building AI Systems that Never Fail

---

## 📋 Is Guide Se Kya Seekhoge

| Topic | Importance |
|-------|------------|
| 1. High Availability (HA) | 99.9% Uptime logic |
| 2. Redundancy & Replication | Backup model servers |
| 3. Failover Logic (Fallback) | GPT-4 fail ho toh GPT-3.5 pe switch |
| 4. Health Checks & Auto-Healing | Kubernetes integration |
| 5. Monitoring & Observability | Drift and Latency alerts |
| 6. Disaster Recovery (DR) | Site-wide outage protection |

---

## 1. 🏗️ High Availability: What is 99.9%?

AI systems mein **HA (High Availability)** ka matlab hai ki aapka system single point of failure (SPOF) se bacha hua hai. 

- **Single point of failure:** Agar sirf ek GPU server hai aur wo crash ho jaye, toh poori app down ho jayegi.
- **Redundancy:** Kam se kam do GPU servers hone chahiye jo traffic ko share karein.

---

## 2. ⚖️ Load Balancing & Model Replicas

Production mein hum models ke multiple instances (Replicas) chalate hain.

```mermaid
graph TD
    User[👤 User] --> LB[⚖️ Load Balancer - HAProxy]
    LB --> V1[🎮 vLLM Instance 1 (GPU 1)]
    LB --> V2[🎮 vLLM Instance 2 (GPU 2)]
    LB --> V3[🎮 vLLM Instance 3 (GPU 3)]
    V1 -->|Unhealthy| LB(Stop Sending Traffic)
```

---

## 3. 🚨 Model Fallback Logic (The AI Backup)

Ek hi model pe depend karna risky hai (OpenAI/Anthropic APIs down ho sakti hain). Hum code mein **Fallback Chain** banate hain.

- **Primary:** GPT-4 (Best but slow/API-call).
- **Secondary:** local Llama-3-70B (Fallback if OpenAI is down).
- **Tertiary:** local Llama-3-8B (Emergency fallback).

```python
import openai

def get_ai_response(prompt):
    try:
        # GPT-4 attempt
        response = openai.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content
    except Exception as e:
        print(f"GPT-4 Down! Switching to Llama-3...")
        # Fallback to local vLLM API (Llama-3)
        return call_local_llama(prompt)
```

---

## 4. 🚒 Health Checks & Auto-Scaling

Inference server healthy hai ya nahi? Ye check karne ke liye hum dedicated **Health Endpoints** banate hain.

- **Liveness Probe:** Kya model process chal raha hai?
- **Readiness Probe:** Kya model weights load ho chuke hain (Ready for traffic)?

**Kubernetes Deployment Example snippet:**
```yaml
resources:
  limits:
    nvidia.com/gpu: 1
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 60
```

---

## 5. 📉 Monitoring AI Health: Observability

AI systems mein sirf 'Up' hona kafi nahi hai. Latency monitor karna zaroori hai.

1. **Slow Token Generation:** Agar TTFT (Time To First Token) 10 seconds se upar hai, toh ye "Unhealthy" account hona chahiye.
2. **GPU Memory Leak:** PyTorch ya vLLM memory leak par GPU restart karna auto-logic mein hona chahiye.

---

## 6. 🌍 Disaster Recovery (DR): Site-Wide Protection

Agar pura AWS ya Azure region down ho jaye, toh kya hoga? 

- **Multi-Region Support:** US-East aur US-West dono regions mein deployment rakho.
- **Backup Vector DB:** Vector store (knowledge) do alag locations pe synced ho (e.g. Pinecone multi-region).

---

## 🧪 Exercises — Fault Tolerance Challenges!

### Challenge 1: Fallback Chain Design ⭐⭐⭐
**Scenario:** Ek hospital AI app design kijiye. Doctors query bhejte hain patient reports ke liye. 
Question: Aap fallback logic kahan lagayenge (Code mein ya Load Balancer level par)? Kyu?
<details><summary>Answer</summary>
Fallback hamesha **Application code** (Gateway level) pe hona chahiye, kyu ki wahan zyada granular control hota hai (e.g. Token usage aur errors handle karne ka).
</details>

---

## 🔗 Resources
- [Google SRE Handbook (Availability Principles)](https://sre.google/sre-book/availability/)
- [Kubernetes AI Operator (KubeRay)](https://ray-project.github.io/kuberay/)
- [High Availability Architecture (AWS Whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/fault-tolerant-components/fault-tolerant-components.html)
