# 📐 Database Design Checklist: The Architect's Guide
> **Objective:** Ensure your database schema is robust, scalable, and follows industry best practices before writing a single line of code | **Language:** Hinglish | **Standard:** 2026 Expert Framework

---

## 🧭 1. Phase 1: Requirements Gathering
- [ ] **Data Entities identified?** Do you know all the "Nouns" (Users, Orders, Products)?
- [ ] **Relationships defined?** (One-to-One, One-to-Many, Many-to-Many).
- [ ] **Volume Estimation?** How many rows per day/month?
- [ ] **Read/Write Ratio?** Is the app more about reading data or writing data?

---

## 🧠 2. Phase 2: Schema Design (Normalization)
- [ ] **Primary Keys set?** Every table MUST have a unique primary key.
- [ ] **Normalization Level?** (Usually 3NF for Apps, 1NF/Denormalized for Analytics).
- [ ] **Data Types optimized?** (e.g., Don't use `TEXT` for a `BOOLEAN` status).
- [ ] **Foreign Keys defined?** Ensure data integrity between tables.
- [ ] **Naming Convention consistent?** (e.g., `user_id` vs `userid` — stick to one).

---

## ⚡ 3. Phase 3: Performance & Indexing
- [ ] **Initial Indexes identified?** Index columns used in `WHERE`, `JOIN`, and `ORDER BY`.
- [ ] **Composite Indexes planned?** For queries using multiple filters.
- [ ] **Avoid Over-indexing?** Don't index every single column.
- [ ] **Partitioning needed?** For tables expected to hit millions of rows.

---

## 🛡️ 4. Phase 4: Security & Privacy
- [ ] **PII identified?** (Emails, Phone numbers). Are they encrypted or masked?
- [ ] **Audit Columns added?** (`created_at`, `updated_at`, `created_by`).
- [ ] **Soft Deletes planned?** Use a `is_deleted` column instead of `DELETE` for critical data.
- [ ] **Role-based access?** Who has `SELECT`, `INSERT`, `DELETE` permissions?

---

## 🌍 5. Phase 5: Operations & Scalability
- [ ] **Backup Strategy ready?**
- [ ] **High Availability planned?** (Read Replicas, Multi-AZ).
- [ ] **Migration strategy ready?** How will you add columns later?
- [ ] **Monitoring metrics chosen?** (CPU, RAM, IOPS).

---

## ✅ 6. The Final "Red Flag" Test
- [ ] **Are there any NULL-heavy columns?** (Consider splitting the table).
- [ ] **Is there any "Magic String" redundancy?** (Use a lookup table or ENUM).
- [ ] **Can the DB survive a restart?** (Durability checks).
- [ ] **Is the documentation updated?** (ER Diagrams).

漫
---

## ⚠️ 7. Pro-Tip (2026 Standard)
"Hamesha ye socho ki agar kal 10x traffic aa gaya, toh aapka schema kahan tootega. Designing for success is better than fixing failures."
漫
