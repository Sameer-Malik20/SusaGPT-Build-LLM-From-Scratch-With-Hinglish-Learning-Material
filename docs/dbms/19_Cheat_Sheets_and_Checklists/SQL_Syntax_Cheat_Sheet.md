# 📝 SQL Syntax Cheat Sheet: The Developer's Handbook
> **Objective:** A high-speed reference for the most essential SQL commands, from basic CRUD to advanced analysis | **Language:** Hinglish | **Standard:** 2026 Expert Framework

---

## 🏗️ 1. Basic CRUD Operations
```sql
-- Create Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert
INSERT INTO users (name, email) VALUES ('Sameer', 'sameer@example.com');

-- Update
UPDATE users SET name = 'Sameer Malik' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
```

---

## 🔍 2. Advanced Filtering
```sql
-- Pattern Matching
SELECT * FROM users WHERE name LIKE 'S%'; -- Starts with S
SELECT * FROM users WHERE email ILIKE '%@gmail.com'; -- Case-insensitive

-- Ranges and Lists
SELECT * FROM orders WHERE amount BETWEEN 100 AND 500;
SELECT * FROM orders WHERE status IN ('shipped', 'delivered');

-- Handling NULLs
SELECT * FROM users WHERE phone IS NULL;
SELECT name, COALESCE(phone, 'No Phone') FROM users;
```

---

## 📊 3. Aggregation & Grouping
```sql
-- The Big Five
SELECT 
    COUNT(*) as total,
    SUM(amount) as revenue,
    AVG(amount) as avg_sale,
    MIN(amount) as min_sale,
    MAX(amount) as max_sale
FROM orders;

-- Grouping
SELECT category, SUM(amount) 
FROM products 
GROUP BY category 
HAVING SUM(amount) > 1000; -- Filter groups
```

---

## 🤝 4. Joins (Connecting Tables)
```sql
-- Inner Join (Intersection)
SELECT u.name, o.id 
FROM users u 
INNER JOIN orders o ON u.id = o.user_id;

-- Left Join (All users, even without orders)
SELECT u.name, o.id 
FROM users u 
LEFT JOIN orders o ON u.id = o.user_id;
```

---

## 🚀 5. Advanced Analysis (Window Functions)
```sql
-- Ranking
SELECT name, salary, 
    DENSE_RANK() OVER(ORDER BY salary DESC) as rank
FROM employees;

-- Running Total
SELECT date, amount,
    SUM(amount) OVER(ORDER BY date) as running_total
FROM sales;
```

---

## 🛠️ 6. Database Maintenance
```sql
-- Explain Plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = '...';

-- Add Index
CREATE INDEX idx_user_email ON users(email);

-- Transactions
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- OR ROLLBACK if something fails
```

---

## ✅ 7. The Golden Rules
- **Rule 1:** Always use `WHERE` in `UPDATE` and `DELETE`.
- **Rule 2:** `GROUP BY` must include all non-aggregated columns from `SELECT`.
- **Rule 3:** Use `JOIN` instead of subqueries for better performance.
- **Rule 4:** `HAVING` is for groups, `WHERE` is for rows.
- **Rule 5:** Always check `EXPLAIN ANALYZE` for slow queries.

漫
