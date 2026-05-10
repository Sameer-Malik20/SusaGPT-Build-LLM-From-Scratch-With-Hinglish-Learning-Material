# 💻 Secure Coding Practices (General Security Guide)
> **Level:** Beginner → Expert | **Goal:** Master Input Validation, Error Handling, and Memory Safety

---

## 📋 Is Guide Se Kya Seekhoge

| Topic | Importance |
|-------|------------|
| 1. Input Validation | Sanitization and Blacklisting |
| 2. Memory Safety | Buffer Overflow prevention |
| 3. Safe Error Handling | Avoiding Data Leakage in Logs |
| 4. Secrets Management | Environment Variables, Vaults |
| 5. Third-party Library Security | Vulnerability Scanning |
| 6. Dependency management | Protecting npm/pip packages |

---

## 🏗️ 1. Input Validation: Rule #1

**Don't trust the user input.** User input ko treat karo as malicious by default.

- **Check Type:** Kya user ne number manga aur text bhej diya?
- **Check Length:** 10,000 words ka input memory crush kar sakta hai.
- **Whitelist vs Blacklist:** Sirf approved characters (Whitelist) allow karo, ghalat characters (Blacklist) filter out karo.

```python
# Unsafe input handling
user_input = request.form['name']

# Safe input logic
import re
def validate_name(name):
    if not re.match("^[a-zA-Z ]+$", name):
        raise ValueError("Invalid characters in name!")
    return name
```

---

## 🚨 2. Safe Error Handling

Bina soche samjhe `print(error)` production mein ghalat hai. Ismein sensitive data aur system internal structure (Stack trace) hacker ko dikh sakta hai.

**Vulnerable:**
`Internal Server Error: Connection string 'mongodb://admin:pass@db:27017' failed.`

**Secure:**
`Internal Server Error: Database connection failed. Please contact support [Code: 500-DB].` (Internal details log mein rakho, user ko generic message do).

---

## 🔒 3. Secrets Management (Secrets Logic)

GitHub mein hardcoded keys push karna sabse badi galti hai.

1. **Environment Variables:** Local machine/container mein store karein.
2. **Secret Managers:** Production mein AWS Secrets Manager ya HashiCorp Vault use karein.

**Gitleaks Logic:**
Tools use karein jo commits scan karein keys dhoondne ke liye.

---

## 📦 4. Dependency Security

Aapka 90% code library-based (PyTorch, Flask, Npm) hota hai. Agar library mein vulnerability hai, toh aapka code unsafe hai.

**Tools:**
- **Snyk:** Libraries scan karne ke liye.
- **GitHub Dependabot:** Security patches auto-update alert.

```bash
# Terminal audit check
# npm audit # Node users
# pip-audit # Python users
```

---

## 🧠 5. Logic Vulnerabilities

Kabhi-kabhi code technically sahi hai but logic ghalat hai.
**Example:** "Shopping cart mein item count negative ho sakta hai" -> `total = price * -5`. (Logic check zaroori hai!).

```python
def update_cart(quantity):
    if quantity < 0:
        raise ValueError("Logic Error: Quantity cannot be negative!")
    # Update logic
```

---

## 🛡️ 6. Hardening Production Apps

1. **Disable Unused Ports:** Sirf 80 aur 443 open rkho.
2. **Minimal Permissions:** App ko DB user "Read/Write" do, "Drop Table/Admin" nahi.
3. **Log Everything (Immutable):** Hacker logs delete na kar sake, logs third-party service pe bhej do.

---

## 🧪 Exercises — Secure Coding Scenarios!

### Challenge 1: The Crash Attack! ⭐⭐
**Scenario:** Aapne file upload feature banaya image upload ke liye. User ne 10GB ki file bhej di. 
Question: System crash kaise rokein?
<details><summary>Answer</summary>
**Input Validation (Size Check)**. Server side par content-length check karo aur specific size (e.g. 5MB) se upar file reject kar do early response system ke saath.
</details>

---

## 🔗 Resources
- [OWASP Secure Coding Practice Guide](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Snyk - Python Security Best Practices](https://snyk.io/blog/python-security-best-practices-cheat-sheet/)
- [The Tangled Web (Book)](https://nostarch.com/tangledweb)
