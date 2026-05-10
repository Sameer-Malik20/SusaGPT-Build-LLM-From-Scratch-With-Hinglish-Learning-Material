# 🏗️ System Design Scenarios: Architecting at Scale

Bhai, ye senior roles ke liye sabse important section hai. Yahan "Code" se zyada "Architecture" matter karta hai.

---

## 🛠️ Scenario 1: Design a Global URL Shortener (TinyURL)
**Requirements:**
1. Generate unique short aliases for long URLs.
2. Handle 10,000 requests per second.
3. High availability and low latency globally.

**Tasks:**
1. **Estimation**: Storage kitna chahiye 5 saal ke liye?
2. **Architecture**: Draw the diagram (Load Balancer -> App Servers -> Cache -> DB).
3. **Deep Dive**: ID generate karne ke liye kya use karoge? (Base62, Snowflake, or DB Auto-increment?)

---

## 🚀 Scenario 2: Design a Real-Time Notification System (WhatsApp/FB)
**Requirements:**
1. Support Push, SMS, and Email notifications.
2. Priority queues (OTPs must be delivered in < 2 seconds).
3. Deduplication (Ek user ko do baar notification mat bhejo).

**Tasks:**
1. **Message Bus**: Kafka vs RabbitMQ choice justify karo.
2. **Scaling**: Notification workers ko kaise scale karoge?
3. **Failure**: Agar SMS provider down hai to kya hoga?

---

## 📦 Scenario 3: Design a Scalable Video Streaming Platform (Netflix)
**Requirements:**
1. Support millions of concurrent viewers.
2. Adaptive Bitrate Streaming (Low data par low quality, high par 4K).
3. Global distribution of content.

**Tasks:**
1. **CDN Strategy**: Content ko edge par kaise rakhoge?
2. **Encoding Pipeline**: Video upload hone ke baad kya process hota hai?
3. **Database**: User watch history ke liye kaunsa DB best hai? (Cassandra or SQL?)

---

## 📊 Scenario 4: Design a Rate Limiter
**Requirements:**
1. Protect your APIs from DDoS attacks.
2. Support "Tiered" limits (Free vs Paid users).
3. Distributed system support (Multiple nodes sharing the limit).

**Tasks:**
1. **Algorithm**: Token Bucket vs Leaky Bucket vs Sliding Window Log.
2. **Storage**: Redis use karne ka logic samjhao.
3. **Location**: Rate limiter ko API Gateway par rakhna chahiye ya separate service?

---

## 🏗️ Scenario 5: Designing for "AI Scale" (Vector Search)
**Requirements:**
1. 100 Million vectors store karne hain.
2. Sub-second retrieval for similarity search.
3. High write throughput for new documents.

**Tasks:**
1. **Vector DB Choice**: Pinecone vs Milvus vs pgvector.
2. **Indexing**: HNSW vs IVF indexing patterns compare karo.
3. **Hybrid Search**: Semantic search aur Keyword search ko kaise combine karoge?

---

## ❓ Interview Scenarios
1. "How do you handle 'Hot Keys' in a distributed cache like Redis?"
2. "Explain the 'Circuit Breaker' pattern and why it is critical for microservices."
3. "What are the tradeoffs between 'Strict Consistency' and 'Eventual Consistency'?"

---
*Ready to lead? Think big, design bigger!*
