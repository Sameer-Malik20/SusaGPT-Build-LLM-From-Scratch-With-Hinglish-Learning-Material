# 🗄️ SQL Beginner to Advanced
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Complete SQL mastery

---

## 🧭 Core Concepts (Concept-First)

- SELECT, WHERE, ORDER BY
- JOINs: INNER, LEFT, RIGHT, FULL
- Aggregations: GROUP BY, HAVING
- Subqueries & CTEs
- Window Functions

---

## 1. 🔍 Basic Queries

```sql
-- Select all
SELECT * FROM users;

-- Select specific columns
SELECT name, email FROM users;

-- WHERE clause
SELECT * FROM users WHERE age > 18;

-- ORDER BY
SELECT * FROM users ORDER BY name ASC;

-- LIMIT
SELECT * FROM users LIMIT 10;
```

---

## 2. 🔗 JOINs

```sql
-- INNER JOIN
SELECT u.name, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN
SELECT u.name, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Multiple JOINs
SELECT u.name, o.amount, p.name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id;
```

---

## 3. 📊 Aggregations

```sql
-- GROUP BY
SELECT status, COUNT(*) as count
FROM orders
GROUP BY status;

-- HAVING
SELECT status, COUNT(*) as count
FROM orders
GROUP BY status
HAVING COUNT(*) > 10;

-- Multiple aggregations
SELECT 
  status,
  COUNT(*) as total,
  SUM(amount) as total_amount,
  AVG(amount) as avg_amount
FROM orders
GROUP BY status;
```

---

## 4. 🎯 Window Functions

```sql
-- Running total
SELECT 
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) as running_total
FROM orders;

-- Rank
SELECT 
  name,
  salary,
  RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- Partition
SELECT 
  department,
  name,
  salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
```

---

## ✅ Checklist

- [ ] Basic queries likh sakte ho
- [ ] JOINs implement kar sakte ho
- [ ] Aggregations use kar sakte ho
- [ ] Window functions apply kar sakte ho