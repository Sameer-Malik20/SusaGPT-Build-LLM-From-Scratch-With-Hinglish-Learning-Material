# 🛡️ Security Audit Lab: Hardening Your Fortress

Bhai, secure code likhna sirf "Best Practice" nahi hai, ye survival skill hai. Ye exercises aapko ek security engineer ki tarah threat detect karna sikhayengi.

---

## 🛠️ Exercise 1: OWASP Top 10 Hunt
**Problem Statement:**
Aapko ek purani Node.js app mili hai. Find and fix:
1. **SQL Injection**: Find raw string concatenation in queries and replace with **Parametrized Queries**.
2. **XSS (Cross-Site Scripting)**: Sanitize user inputs using libraries like `dompurify`.
3. **IDOR (Insecure Direct Object Reference)**: Ensure users can't access `/api/orders/999` if they don't own it.

---

## 🚀 Exercise 2: Auth Hardening (2FA/MFA)
**Problem Statement:**
Simple login/password is not enough.
1. Implement **TOTP (Time-based One-Time Password)** using `speakeasy` or `otplib`.
2. QR Code generate karo jise Google Authenticator scan kar sake.
3. "Recovery Codes" generating mechanism likho.

---

## 🏗️ Exercise 3: Secrets Management
**Problem Statement:**
Aapke code mein API Keys aur Database passwords hardcoded hain.
1. Move all secrets to `.env` files (gitignore them!).
2. Implement **AWS Secrets Manager** or **HashiCorp Vault** for a production environment.
3. Code likho jo "Rotating Secrets" ko handle kar sake bina app restart kiye.

---

## 📦 Exercise 4: Network Security (TLS/SSL & CORS)
**Problem Statement:**
Aapki app insecure connection par chal rahi hai.
1. Local development mein **Self-signed Certificates** (mkcert) use karke HTTPS enable karo.
2. CORS policy configure karo jo sirf specific trusted domains ko allow kare.
3. **Helmet.js** middleware use karke secure headers set karo (HSTS, No-Sniff, etc.).

---

## 📊 Exercise 5: AI & LLM Security Lab
**Problem Statement:**
Aapka AI Chatbot vulnerable hai.
1. **Prompt Injection**: Ek aisa prompt banao jo system prompt ko "Ignore" karwa de. Phir use block karne ke liye "Guardrails" likho.
2. **Data Leakage**: Ensure karo ki LLM kabhi bhi "System Internal API Keys" user ko na bataye.
3. **Rate Limiting**: AI inference bohot costly hai. Implement inference rate limits per user.

---

## ❓ Interview Scenarios
1. "Explain the difference between Symmetric and Asymmetric Encryption."
2. "What is a 'Zero-Day Vulnerability' and how does an organization respond to it?"
3. "How would you secure a multi-tenant database to prevent data bleeding between customers?"

---
*Stay paranoid, stay secure!*
