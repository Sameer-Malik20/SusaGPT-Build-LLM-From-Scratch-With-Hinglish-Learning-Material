# 🛠️ Project 2: Slow Query Optimization Lab
> **Objective:** Practice identifying, analyzing, and fixing performance bottlenecks in a large-scale database | **Difficulty:** Expert | **Target:** Backend & Database Engineers

---

## 🎯 1. The Challenge
Aapko ek "Slow Database" diya gaya hai jisme 1 Million users aur 10 Million orders hain. Kuch queries 5-10 seconds le rahi hain. Aapka kaam hai unhe $<100ms$ tak laana.

### The Setup (Postgres):
```sql
-- Create a large table
CREATE TABLE massive_orders (
    id SERIAL PRIMARY KEY,
    user_id INT,
    amount DECIMAL,
    order_date DATE,
    status TEXT
);

-- Seed 1 Million rows (Pseudo-code)
INSERT INTO massive_orders (user_id, amount, order_date, status)
SELECT 
    (random()*100000)::int, 
    (random()*1000)::decimal, 
    CURRENT_DATE - (random()*365)::int, 
    'completed'
FROM generate_series(1, 1000000);
```

---

## 🔍 2. The Task: Diagnose the Slow Query
Run this query:
```sql
EXPLAIN ANALYZE 
SELECT user_id, SUM(amount) 
FROM massive_orders 
WHERE order_date > '2024-01-01' 
GROUP BY user_id;
```

### Observation:
Check the output. You will likely see `Seq Scan on massive_orders`. This is the enemy!

---

## 🛠️ 3. Optimization Steps

### Step 1: Add the Right Index
```sql
CREATE INDEX idx_orders_date ON massive_orders(order_date);
```
Run `EXPLAIN ANALYZE` again. Is it faster?

### Step 2: Composite Index (Level Up)
What if the query also filters by `status`?
```sql
CREATE INDEX idx_orders_date_status ON massive_orders(order_date, status);
```

### Step 3: Covering Index (The Pro Move)
If we only need `user_id` and `amount`, we can "Include" them in the index.
```sql
CREATE INDEX idx_orders_covering ON massive_orders(order_date) INCLUDE (user_id, amount);
```
This should trigger an **Index Only Scan**.

---

## 📊 4. Measurement Table
| Step | Query Time (Initial) | Query Time (After) | Gain |
| :--- | :--- | :--- | :--- |
| **No Index** | 5200 ms | - | - |
| **Single Index** | - | 450 ms | $11x$ |
| **Covering Index**| - | 45 ms | $115x$ |

---

## ❌ 5. Troubleshooting (Common Traps)
- **Problem:** The DB is still doing a Seq Scan even after adding the index.
  - **Reason:** The statistics are old.
  - **Fix:** `ANALYZE massive_orders;`

---

## ✅ 6. Evaluation Criteria
- [ ] Successfully used `EXPLAIN ANALYZE` to find the bottleneck.
- [ ] Created a covering index to achieve an `Index Only Scan`.
- [ ] Reduced query time by at least $90\%$.
- [ ] Explained *why* the specific index was chosen.

漫
---

## 🚀 7. Bonus: The "Delete" Challenge
"Delete 500,000 rows from the table and then run `VACUUM`. Observe how the table size changes (or doesn't change) and explain why."
漫
