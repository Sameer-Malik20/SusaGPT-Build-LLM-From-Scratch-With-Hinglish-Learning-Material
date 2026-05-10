# ⚙️ Backend Engineering Lab: Production-Grade Systems

Bhai, backend engineering sirf "API banana" nahi hai, ye "Scalability and Reliability" ka khel hai. Ye exercises aapko ek senior backend engineer ki tarah sochne par majboor karengi.

---

## 🛠️ Exercise 1: The Event-Loop Detective
**Problem Statement:**
Ek aisa API endpoint likho jo server ko block kar deta hai (CPU intensive). 
1. `node --inspect` use karke find karo ki event loop kahan block ho raha hai.
2. Isse fix karne ke liye **Worker Threads** use karo.

---

## 🚀 Exercise 2: Scalable Auth & Sessions
**Problem Statement:**
Ek authentication system banao jo **JWT** aur **Redis** use kare.
1. Implement "Refresh Tokens" with rotation.
2. Token ko blacklisting (logout) karne ke liye Redis use karo.
3. Middleware likho jo "Rate Limiting" kare per-user base par.

---

## 📦 Exercise 3: File Processing Pipeline
**Problem Statement:**
Ek service banao jahan users 100MB ki CSV file upload karein.
1. File ko **Streams** use karke read karo (Pura memory mein mat load karo!).
2. Har row ko validate karke ek database mein save karo.
3. User ko "Processing Started" response turant do aur email baad mein (Async).

---

## 🔗 Exercise 4: gRPC vs REST
**Problem Statement:**
Do microservices ke beech communication setup karo.
1. Implement a `User` service and an `Order` service.
2. Pehle **REST (JSON)** use karo communication ke liye.
3. Phir use **gRPC (Protobuf)** mein convert karo aur benchmark karo (latency and payload size).

---

## 🏗️ Exercise 5: Database Scaling (Read/Write Split)
**Problem Statement:**
Postgres database setup karo with 1 Master and 2 Read Replicas.
1. Middleware likho jo automatic `GET` requests ko replica par aur `POST/PUT` requests ko master par bheje.
2. "Replication Lag" handle karne ka ek plan banao.

---

## ❓ Interview Scenarios
1. "How do you handle 'Thundering Herd' problem in a caching layer?"
2. "Why would you choose RabbitMQ over Kafka for a simple email notification system?"
3. "Explain the difference between 'Deep Health Checks' and 'Shallow Health Checks' in Kubernetes."

---
*Ready to scale? Open your terminal and start building!*
