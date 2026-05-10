# 🔑 API Security & Authentication (Security Guide)
> **Level:** Beginner → Expert | **Goal:** Master AI Endpoints Security, JWT, OAuth, and Rate Limiting
## 🧭 Core Concepts (Concept-First)
+- API Security Fundamentals: Protecting AI endpoints from unauthorized access and abuse
+- Authentication Methods: API keys, JWT tokens, OAuth2 flows for secure access
+- Rate Limiting & Throttling: Preventing DoS attacks and managing resource usage
+- CORS & Security Headers: Browser-side protections for AI web applications
+- Practical Security Exercises: Hands-on challenges for authentication and authorization
---

## 📋 Is Guide Se Kya Seekhoge

| Topic | Importance |
|-------|------------|
| 1. API Keys Management | Protecting model access |
| 2. JWT (JSON Web Tokens) | Stateless authentication |
| 3. OAuth2 Flow | Third-party login (Google/Github) |
| 4. Rate Limiting AI APIs | DoS protection logic |
| 5. CORS & Headers Security | Browser-side safety |
| 6. Exercises & Challenges | Attack identification |

---

## 1. 🛡️ API Key Strategy: The First Line

AI APIs (vLLM, OpenAI, Anthropic) expensive hoti hain, isliye keys chori hone par aapka bank account khali ho sakta hai.

- **Environment Variables (.env):** Kabhi bhi code mein keys mat likho (`hardcode`).
- **Rotation:** Har month keys change (rotate) karne ka logic rkho.
- **Leaked Key Check:** GitHub Actions lagao jo keys push hone se pehle check karein (e.g. `TruffleHog`).

---

## 2. 🔑 JWT (JSON Web Tokens) for AI Services

User login ke liye JWT best hai kyu ki ye "Stateless" hai (Server ko databases check nahi karne padte har request pe).

- **Header:** Algorithm (HS256).
- **Payload:** User ID + Expiry Time (`exp`).
- **Signature:** Hash of (header + payload + secret).

```python
import jwt
import datetime

SECRET_KEY = "super-secret-key"

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

---

## 3. 🚦 AI Rate Limiting: Protecting GPUs

GPUs expensive aur limited hote hain. Ek user agar 10,000 queries second mein bhej dega (DoS attack), toh server crash ho jayega.

- **Limit by IP:** Har IP address ko 5 requests per minute allow karo.
- **Limit by Token:** 10,000 tokens per hour per user.

```python
from fastapi import FastAPI, Request, HTTPException
import time

app = FastAPI()
rates = {} # Store user last request time logic

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    user_ip = request.client.host
    now = time.time()
    if user_ip in rates and now - rates[user_ip] < 5: # 5 second gap
        raise HTTPException(status_code=429, detail="Too Many Requests")
    rates[user_ip] = now
    return await call_next(request)
```

---

## 🌍 4. CORS (Cross-Origin Resource Sharing)

Agar aapka frontend `mysite.com` hai aur backend `api.ai-site.com`, toh browsers traffic block karenge bina CORS allow kiye. 

**Security Tip:** Sirf apni domain (`mysite.com`) allow karein, `*` (All domains) allow karna unsafe hai AI production mein.

---

## 5. 🏗️ Secure Headers for AI Apps

Web browsers ko secure rakhne ke liye common headers:
- **Strict-Transport-Security (HSTS):** Hamesha HTTPS use karo.
- **X-Content-Type-Options:** No MIME sniffing.
- **X-Frame-Options:** No Clickjacking (Frame block).

---

## 🧪 Exercises — Authentication Challenge!

### Challenge 1: The Token Expiry Question ⭐⭐
**Scenario:** Aapne JWT expiry set ki hai 10 years (long life). 
Question: Ye security risk kyu hai?
<details><summary>Answer</summary>
Kyuki agar user ka token chori (leak) ho jata hai, toh hacker 10 saal tak aapki AI API free mein use kar sakta hai. Tokens hamesha **Short-lived** (1-24 hours) hone chahiye session refresh logic ke saath.
</details>

---

## 🔗 Resources
- [JWT.io Debugger](https://jwt.io/)
- [OAuth 2.0 Simplified Guide](https://aaronparecki.com/oauth-2-simplified/)
- [FastAPI Security Tutorial](https://fastapi.theloop.io/tutorial/security/)
