# 🛡️ Web Security OWASP Top 10 (Security Guide)
> **Level:** Beginner → Expert | **Goal:** Protect Web Apps from Professional Attacks (XSS, SQLi, CSRF)

---

## 📋 Is Guide Se Kya Seekhoge

| Topic | Importance |
|-------|------------|
| 1. SQL Injection (SQLi) | Protecting Databases |
| 2. Cross-Site Scripting (XSS) | Protecting Frontend/Browsers |
| 3. Cross-Site Request Forgery (CSRF) | Protecting Sessions |
| 4. Insecure Direct Object Refs (IDOR) | Protecting Data Access |
| 5. Security Misconfigurations | Hardening Servers |
| 6. Exercises & Challenges | Attack identification |

---

## 1. 💉 SQL Injection (SQLi)

Jab user input bina sanitize kiye SQL query mein dal diya jata hai, toh hacker database se data nikal sakta hai.

**Vulnerable Code:**
```python
# Unsafe logic
query = f"SELECT * FROM users WHERE username = '{user_input}'"
# User input: "admin' OR '1'='1"
```

**Secure Code (Parameterized Queries):**
```python
# Safe logic using Prepared Statements
cursor.execute("SELECT * FROM users WHERE username = %s", (user_input,))
```

---

## 🏗️ 2. Cross-Site Scripting (XSS)

Hacker user ke browser mein malicious JavaScript chalata hai.

1. **Stored XSS:** Comment box mein script save kar dena jo har user ko dikhe.
2. **Reflected XSS:** URL mein script bhej kar link share karna.

**Protection:** Hamesha user input ko **Escape/Sanitize** karein render karne se pehle.
```html
<!-- Input: <script>alert(1)</script> logic -->
<!-- Escaped: &lt;script&gt;alert(1)&lt;/script&gt; -->
```

---

## 🔄 3. CSRF (Cross-Site Request Forgery)

Hacker user ko aisi website pe le jata hai jahan se unka browser automatic authentic request bhej deta hai aapki app par (e.g. Email change or Transfer money).

**Solution:** **CSRF Tokens** (ek hidden unique field for each request) use karein verification ke liye.

---

## 🔒 4. IDOR (Insecure Direct Object Reference)

Jab user URL change karke dusre user ka data dekh le.
- **Attack:** `mysite.com/profile/101` -> `mysite.com/profile/102` (Without permission check).

**Fix:** Har request par Authorization check (RBAC - Role Based Access Control) karein. 

---

## 🏢 5. Security Hardening Checklist

1. **HTTPS Only (HSTS):** No unencrypted traffic allowed.
2. **Content Security Policy (CSP):** Browser ko batana ki script kahan se load ho sakti hai.
3. **No Defaults:** Purane default passwords (admin/admin) change karein service install hone par.
4. **Regular Patching:** Libraries hamesha updated rakho.

---

## 🧪 Exercises — Cyber Attack Challenges!

### Challenge 1: Identify the Fix! ⭐⭐
**Scenario:** Aapne notice kiya ki users URL mein `?id=101` ki jagan `?id=102` dalkar dusre ka password dekh rahe hain. 
Question: Ye kaunsa attack hai aur iska fix kya hoga?
<details><summary>Answer</summary>
Ye **IDOR** (Insecure Direct Object Reference) attack hai. Iska fix ye hai ki backend par check karo ki kya logged-in user ke paas Permission hai ID 102 dekhne ki session checking ke through.
</details>

---

## 🔗 Resources
- [OWASP Top 10 Project (Official)](https://owasp.org/www-project-top-10/)
- [PortSwigger Security Academy (Free Labs)](https://portswigger.net/web-security)
- [Hacker101 (Learn Hacking Concepts)](https://www.hacker101.com/)
