# 🛡️ Security Hardening Checklist: Protecting the Data
> **Objective:** Ensure your database is locked down and resistant to attacks, leaks, and unauthorized access | **Language:** Hinglish | **Standard:** 2026 Expert Framework

---

## 🧭 1. Phase 1: Network & Access
- [ ] **No Public IP.** Database should only be accessible within a Private VPC.
- [ ] **Firewall / Security Groups set?** Only allow specific IPs (e.g., Backend servers).
- [ ] **Default Port changed?** (Optional, but helps against automated bots).
- [ ] **SSH access disabled?** Don't allow direct login to the DB server.

---

## 🔑 2. Phase 2: Authentication & Authorization
- [ ] **Strong Passwords / IAM Roles.** Never use 'admin/admin'.
- [ ] **Principle of Least Privilege.** App should not have `DROP TABLE` or `GRANT` permissions.
- [ ] **Separate Users.** One user for the App, one for the Admin, one for the Data Scientist.
- [ ] **Enable MFA** (Multi-Factor Authentication) for admin access.

---

## 🔒 3. Phase 3: Encryption
- [ ] **Encryption at Rest.** (Disk encryption like AWS KMS).
- [ ] **Encryption in Transit.** (SSL/TLS required for all connections).
- [ ] **Field-level Encryption.** For sensitive data like Credit Cards or Passwords (use Hashes!).
- [ ] **Backup Encryption.** Ensure your backups are also encrypted.

---

## 🔍 4. Phase 4: Application Safety
- [ ] **Parameterized Queries.** Prevent SQL Injection 100%.
- [ ] **Sanitize Inputs.** Clean data before it hits the database.
- [ ] **Limit Result Sizes.** Don't allow a user to fetch 1 Million rows at once.
- [ ] **Log Auditing.** Track who accessed what data and when.

---

## 🔄 5. Phase 5: Operations & Compliance
- [ ] **Automated Patching enabled?** Stay up to date with security fixes.
- [ ] **Intrusion Detection.** Alert on unusual login attempts or massive data exports.
- [ ] **Regular Backups.** Test your recovery plan.
- [ ] **GDPR / Compliance checks.** Can you delete a user's data completely?

---

## ✅ 6. The "Hacker" Test
"Agar kisi ke paas mere backend server ka access aa gaya, toh kya wo pura database delete kar sakta hai? Agar haan, toh aapki security kamzor hai."
漫
---

## ⚠️ 7. Common Security Pitfalls
- **Hardcoding passwords in Git.**
- **Using 'Root' user for the web application.**
- **Leaving the 'Slow Query Log' public** (might leak sensitive data).
漫
