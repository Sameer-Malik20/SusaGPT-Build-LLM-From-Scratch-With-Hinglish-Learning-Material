# 🛠️ Lab: Point-in-Time Recovery (PITR)
> **Objective:** Practice the advanced technique of restoring a database to a specific second in the past to recover from accidental data deletion or corruption | **Difficulty:** Expert | **Language:** Hinglish | **Standard:** 2026 Expert Framework

---

## 🎯 1. The Scenario
Aapke ek developer ne galti se production database mein `DELETE FROM customers;` chala diya (Oops!).
- **Time of incident:** 10:45:30 AM
- **Last Full Backup:** Aaj subah 2:00 AM
- **The Goal:** Database ko 10:45:29 AM ki state mein wapas lana (The second before the disaster).

---

## 🧠 2. The Logic: How PITR works
PITR depends on two things:
1. **The Base Backup:** A full copy of the DB from the past.
2. **Transaction Logs (WAL/Binlog):** A record of every change since that backup.

**The Process:** 
1. Restore the 2 AM backup.
2. "Replay" the logs one by one.
3. Tell the database to **STOP** exactly at 10:45:29 AM.

---

## 💻 3. Step-by-Step Implementation (PostgreSQL)

### Step 1: Pre-requisites (Check your config)
Ensure your database is generating logs.
```sql
-- postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /path/to/archive/%f'
```

### Step 2: Restore the Base Backup
Stop the database and replace the data directory with your 2 AM backup.
```bash
pg_ctl stop
rm -rf /var/lib/postgresql/data/*
cp -R /path/to/backups/2am_backup/* /var/lib/postgresql/data/
```

### Step 3: Configure Recovery
Create a file to tell Postgres how far to go.
```bash
# For Postgres 12+
touch /var/lib/postgresql/data/recovery.signal
```
Add these lines to `postgresql.conf`:
```sql
restore_command = 'cp /path/to/archive/%f %p'
recovery_target_time = '2026-05-10 10:45:29'
recovery_target_action = 'promote'
```

### Step 4: Start and Verify
```bash
pg_ctl start
# Check the logs to see if it reached the target time
# Verify that the 'customers' table has data!
```

---

## 🏗️ 4. Visualizing the Timeline
```mermaid
graph LR
    B[2 AM Backup] --> L1[Log: 3 AM]
    L1 --> L2[Log: 6 AM]
    L2 --> L3[Log: 10 AM]
    L3 --> T[TARGET: 10:45:29 AM]
    T --> X[DISASTER: 10:45:30 AM]
    style X fill:#f00,color:#fff
    style T fill:#0f0,color:#fff
```

---

## ❌ 5. Troubleshooting (Common Traps)
- **Problem:** Database starts but doesn't restore data.
  - **Reason:** Missing a log file in the middle of the chain. If one 1-minute log is missing, you can't go past that time.
- **Problem:** Recovery target not reached.
  - **Reason:** Timezone mismatch. Always use **UTC** for backups and recovery targets.

---

## ✅ 6. Evaluation Criteria
- [ ] Successfully restored the base backup.
- [ ] Correctly configured the `restore_command`.
- [ ] Database stopped at the exact target time.
- [ ] Confirmed data integrity after recovery.

漫
---

## 🚀 7. Bonus: The "Integrity" Challenge
"Can you perform PITR while the database is still running for other users? (Hint: Use a separate 'Recovery Instance'). Explain the pros and cons."
漫
