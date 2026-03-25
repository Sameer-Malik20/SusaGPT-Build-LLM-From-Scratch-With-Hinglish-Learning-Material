# 🐘 SQL Mastery — PostgreSQL Internals & Performance
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master Postgres, Transactions (ACID), Normalization, Joins, Triggers, Views, and WAL.

---

## 📋 Table of Contents: The SQL Engine

| Stage | Topic | What you'll learn? |
|-------|-------|--------------------|
| **1. Design** | Relational Data Modeling | 1NF, 2NF, 3NF Normalization. |
| **2. Engine** | PostgreSQL Internals | Heap, Pages, WAL (Write Ahead Log). |
| **3. Logic** | Transactions & Isolation | ACID properties deep dive (Dirty Reads). |
| **4. Performance**| JOINs, Subqueries & CTEs | Optimization of complex queries. |
| **5. Features** | Views, Triggers & Procedures | Database-side logic (Automation). |
| **6. Migration** | Schema Evolution | Naye tables bina downtime ke badalna. |

---

## 🏗️ 1. Relational Design: Normalization (1NF to 3NF)

Data duplicate na ho isliye hum use "Normalize" karte hain.
- **1NF:** Har column mein atomic values (No lists/arrays).
- **2NF:** Har non-major column primary key par dependent ho.
- **3NF:** Transitive dependency hatana. (e.g. `User -> Dept -> Manager`). Direct `User -> Manager` relation nahi hona chahiye.

---

## 🐘 2. PostgreSQL Engine: How it Stores Data?

Postgres data ko **Pages (8KB block)** mein store karta hai.
- **Heap File:** Jahan actual rows store hoti hain.
- **WAL (Write Ahead Log):** Sabse pehle transaction log file mein likha jata hai, phir heap mein. (Crash recovery logic).
- **VACUUM:** Jab row update hoti hai, purani row "Dead" ho jati hai. `VACUUM` use scan karke memory khali karta hai.

---

## 🛡️ 3. ACID Properties: Deep Dive

1. **Atomicity:** Poora transaction success (Commit) ya fail (Rollback).
2. **Consistency:** Schema rules (Unique, Foreign Key) hamesha follow honge.
3. **Isolation:** Do users ek saath table edit kar sakte hain (Isolation levels).
4. **Durability:** Data disk par permanent save hoga.

### Isolation Levels (Most Important for Scale):
- **Read Committed (Default):** Aap wahi data padhte ho jo dusre user ne commit kar diya ho. (No Dirty Reads).
- **Repeatable Read:** Transaction start hone ke waqt ka data waisa hi rahega.
- **Serializable:** Transactions line mein (one by one) lagenge. (Safest, but Slowest).

---

## 🚀 4. Performance: Advanced Querying

- **INNER JOIN vs LEFT JOIN:** Data missing ho toh NULL handling.
- **CTEs (WITH clause):** Query ko readable aur reusable banana.
- **Window Functions (OVER PARTITION BY):** Bina grouping ke aggregate calculations (Ranking/Summing).

```sql
-- Ranking users by score in each category
SELECT name, score, RANK() OVER (PARTITION BY category ORDER BY score DESC)
FROM users;
```

---

## 🏭 5. Views, Triggers & Procedures

- **Views:** Virtual tables for complex query aliases.
- **Materialized Views:** Query results ko disk par save karna for instant access (Dashboard reports).
- **Triggers:** Table update hone par automatically doosri action perform karna (Logging, auto-updating timestamps).

---

## 🛣️ 6. Database Migrations (The Production Way)

Downtime bina schema badalna:
- **Migration Scripts:** `Knex`, `Prisma`, or `Flyway`.
- **Backward Compatibility:** Pehle naya column add karo, phir code deploy karo, phir purana column delete karo (Phase-wise migration).

---

## 🧪 Quick Test — Senior SQL Architect Level!

### Q1: B-Tree index kab fail hota hai?
**Answer:** Jab cardinality bohot kam ho (e.g. Gender column: M/F). Index scanning se zyada fast full table scan ho sakta hai. Use Gin Index or Partial Index for large sets.

### Q2: Deadlocks kaise bachte hain?
**Answer:** Hamesha tables ko **same order** mein update karo. (User A: Tab1 -> Tab2, User B: Tab1 -> Tab2). Agar order alag hai (User B: Tab2 -> Tab1), toh deadlock lock ho jayega.

---

## 🏆 Final Summary Checklist
- [ ] Isolation levels ka selection clear hai?
- [ ] 3NF Normalization level follow kiya?
- [ ] Materialized views performance spikes handle karte hain?
- [ ] WAL logs crash recovery ke liye enabled hain?

> **SQL Tip:** Databases are the "Persistence Layer". Har logic DB mein likhna galat hai, par har DB design galat hona tabahi (disaster) hai. Model deep, query fast.
