# ⚡ Performance Tuning Checklist: Debugging Slowness
> **Objective:** A step-by-step troubleshooting guide to identify and fix database performance bottlenecks in production | **Language:** Hinglish | **Standard:** 2026 Expert Framework

---

## 🧭 1. Step 1: Identify the Culprit
- [ ] **Check Slow Query Log.** Find the top 5 slowest queries.
- [ ] **Run `EXPLAIN ANALYZE`.** Is it doing a `Seq Scan` (Table Scan)?
- [ ] **Check Resource Utilization.** Is CPU > 90%? Is RAM full?
- [ ] **Check Locks.** Are queries waiting for other transactions to finish?

---

## 🔍 2. Step 2: Query Optimization
- [ ] **Add missing indexes.** (The #1 fix for $80\%$ of issues).
- [ ] **Use Composite Indexes.** For queries with multiple `AND` filters.
- [ ] **Avoid `SELECT *`.** Only fetch the columns you actually need.
- [ ] **Remove `LIKE '%keyword%'`.** Use Full-Text Search or Vector Search instead.
- [ ] **Simplify Joins.** Can you break a 10-table join into 2 smaller queries?

---

## 🧠 3. Step 3: Database & Engine Tuning
- [ ] **Increase Buffer Pool.** (MySQL `innodb_buffer_pool_size` or Postgres `shared_buffers`).
- [ ] **Tune `work_mem`.** Prevent sorting from spilling to disk.
- [ ] **Update Statistics.** Run `ANALYZE` (Postgres) or `OPTIMIZE` (MySQL).
- [ ] **Check for Bloat.** Run `VACUUM` to reclaim space from deleted rows.

---

## 🔌 4. Step 4: Connection & Network Tuning
- [ ] **Use Connection Pooling.** (PgBouncer, HikariCP, or RDS Proxy).
- [ ] **Check Network Latency.** Is the DB far away from the App server?
- [ ] **Increase Connection Limits.** But keep an eye on RAM usage.

---

## 🏗️ 5. Step 5: Architecture & Scaling
- [ ] **Add Read Replicas.** Move heavy `SELECT` queries to a secondary node.
- [ ] **Implement Caching.** Use **Redis** for frequently accessed "Hot" data.
- [ ] **Sharding needed?** Split the data across multiple servers.
- [ ] **Upgrade Hardware.** (Vertical Scaling) More CPU/RAM/IOPS.

---

## ✅ 6. The "Golden Rule" of Tuning
"Change only ONE thing at a time. Measure performance, and then decide if you need the second change."
漫
---

## ⚠️ 7. Diagnostic Checklist (Immediate Action)
| Symptom | Probable Cause | Fix |
| :--- | :--- | :--- |
| **Random spikes in latency** | Checkpoint / Vacuum | Adjust checkpoint interval. |
| **Queries slow only for 1 user** | Locking issue | Find the long-running transaction blocking others. |
| **High Disk I/O** | Missing index | Check for `Seq Scan` in `EXPLAIN`. |
漫
