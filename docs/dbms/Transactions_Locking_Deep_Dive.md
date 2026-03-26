# 🔒 Transactions & Locking Deep Dive
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master transactions and concurrency

---

## 🧭 Core Concepts (Concept-First)

- ACID Properties
- Isolation Levels
- Locking Mechanisms
- Deadlock Prevention

---

## 1. 🛡️ ACID Properties

```sql
-- Atomicity: All or nothing
BEGIN;
INSERT INTO accounts (id, balance) VALUES (1, 100);
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
UPDATE accounts SET balance = balance + 50 WHERE id = 2;
COMMIT;  -- All succeed together

-- If any fails, ROLLBACK
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
-- Error here
ROLLBACK;  -- All changes undone
```

---

## 2. 📊 Isolation Levels

```sql
-- Read Uncommitted (dirty reads possible)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- Read Committed (default in PostgreSQL)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Repeatable Read
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Serializable (highest protection)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

---

## 3. 🔒 Locking

```sql
-- Explicit locking
BEGIN;
LOCK TABLE users IN EXCLUSIVE MODE;
-- Do operations
COMMIT;

-- Row-level lock
SELECT * FROM users WHERE id = 1 FOR UPDATE;
```

---

## ✅ Checklist

- [ ] ACID properties samjho
- [ ] Isolation levels compare kar sakte ho
- [ ] Locking implement kar sakte ho