# 🗄️ DBMS & Data Engineering Lab: The Data Master

Data is gold, par agar query slow ho to wo kachra hai. Ye lab aapko database internals aur optimization ka mahir banayegi.

---

## 🛠️ Exercise 1: Query Optimization (EXPLAIN ANALYZE)
**Problem Statement:**
Aapke paas ek `Orders` table hai jisme 1 million rows hain. Ek query `SELECT * FROM Orders WHERE order_date > '2025-01-01' AND customer_id = 123` bohot slow hai.
1. Use `EXPLAIN ANALYZE` to see if it's doing a **Sequential Scan**.
2. **Indexing Strategy**: Ek composite index banao. Kya order of columns (`order_date, customer_id` vs `customer_id, order_date`) matter karta hai? Prove it.

---

## 🚀 Exercise 2: Transactions & Locking (Isolation Levels)
**Problem Statement:**
Simulate a "Double Spend" or "Race Condition" scenario where two threads try to deduct money from the same bank account.
1. Implement a transfer script with default isolation.
2. Observe the **Lost Update** problem.
3. Fix it using **SELECT FOR UPDATE** (Pessimistic Locking) or **Serializable** isolation level.

---

## 🏗️ Exercise 3: Database Sharding from Scratch
**Problem Statement:**
Socho aapka user data 1TB ho gaya hai. Ab aap use single machine par nahi rakh sakte.
1. Implement **Horizontal Sharding** (Manual) by creating 3 separate databases (`db_shard_1`, `db_shard_2`, `db_shard_3`).
2. Code likho jo `user_id % 3` use karke decide kare ki data kahan jayega.
3. Problem solve karo: "How to perform a cross-shard query?"

---

## 📦 Exercise 4: NoSQL vs SQL Modeling
**Problem Statement:**
Ek "Ecommerce Review System" design karo.
1. Case 1: **Postgres** mein relational schema banao (Normalization).
2. Case 2: **MongoDB** mein document schema banao (Denormalization).
3. Discussion: "When would you choose one over the other based on read/write patterns?"

---

## 📊 Exercise 5: CDC (Change Data Capture)
**Problem Statement:**
Aap chahte ho ki jaise hi user apna profile update kare, wo change search engine (Elasticsearch) mein chala jaye.
1. Database transaction logs read karo (using a tool like **Debezium** or simple webhooks).
2. Sync worker likho jo data transform karke downstream system mein bhej de.

---

## ❓ Interview Scenarios
1. "Explain B-Trees and why databases use them instead of Hash Maps for indexing."
2. "How does MVCC (Multi-Version Concurrency Control) work in Postgres?"
3. "What is the 'N+1 Query Problem' and how do you solve it at the DB level?"

---
*Data never sleeps. Start optimizing!*
