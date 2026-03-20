# 🛠️ Free Security Tools & Bug Finding (Audit Guide)
> **Level:** Beginner → Expert | **Goal:** Master Vulnerability Scanning using Open-Source/Free Community Tools

---

## 📋 Is Guide Se Kya Seekhoge

| Category | Tool | Importance |
|----------|------|------------|
| 1. Dynamic Web Scan | OWASP ZAP (Free) | Finding XSS/SQLi in real-time |
| 2. Static Analysis (SAST) | Snyk (Free Tier), SonarCloud | Logic errors in code |
| 3. Secret Detection | Gitleaks (CLI) | Prevent API Keys leak |
| 4. Network Scanning | Nmap / Nessus Essentials | Open Ports detection |
| 5. Dependency Audit | npm audit, pip-audit | Vulnerable libraries check |
| 6. Intercepting Traffic | Burp Suite (Community) | Manual Pen Testing |

---

## 🏗️ 1. OWASP ZAP (ZED Attack Proxy)

ZAP ek **FREE** tool hai jo automated scanning deta hai web apps ki production/staging environments mein. 

- **Spidering:** Puri site ke pages dhundna automatically.
- **Active Scan:** XSS, SQLi, aur header missing vulnerabilities dhundna queries bhej kar.

```bash
# Terminal local ZAP docker run logic
# docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-full-scan.py -t http://domain.com
```

---

## 🔍 2. Snyk: Security for Developers

Snyk ka free tier code aur dependencies monitor karta hai GitHub/Gitlab integrations se.

- **Snyk Code:** AI-driven SAST jo code logic bugs find karta hai.
- **Snyk Open Source:** Pata chalata hai ki aapka `PyTorch` ya `Flask` version old kyu hai.

---

## 🕵️ 3. Gitleaks: Secrets Protection

Production mein sabse badi problem is "Keys pushed to Git". **Gitleaks** unhe turant scan kar leta hai.

```bash
# Command line check for all commits
# gitleaks detect --source . --verbose
```

---

## 📱 4. Burp Suite Community Edition

Professional pen-testers **Burp Suite** use karte hain "Middleman" bankar request modify karne ke liye.

- **Proxy:** Browser aur Server ke beech baithna.
- **Repeater:** Same request ko bar-bar bhejna parameter change karke.

---

## 🚀 5. Mastering Bug Finding Skills

Sirf tools chalana kaafi nahi hota. In "Skills" par focus karein:

1. **Payload Tinkering:** Parameter change karke error responses check karna. (Error messages internal secrets leak kar sakte hain).
2. **Path Traversal:** URL mein `../../etc/passwd` try karna.
3. **Logic Flaws:** Price parameter change karke order bvejhna.

---

## 🏗️ 6. Using MCP for Security Audits

**MCP (Model Context Protocol)** servers like `github-audit` ya `code-scanner` AI ko superpower dete hain scan karne ki.

- **Antigravity/Cursor Prompt:** "MCP github-audit tool use karke find karo ki hamare repository mein koi sensitive `id_rsa` file leaked toh nahi hai?"
- **Response:** AI files scan karke results batayega automated tools ke through.

---

## 🧪 Exercises — Find the Bug!

### Challenge 1: The Local Scan ⭐⭐
**Scenario:** Aapne Nmap chalaya aur `Port 8000` status "Open" dekha service `vLLM` ke liye bina login key ke. 
Question: Ye kitna bada security issue hai? Fix kya hoga?
<details><summary>Answer</summary>
**Critical Vulnerability**. Koi bhi aapka GPU misuse karke 1000$ ka bill generate kar sakta hai API hits se. Fix: Reverse Proxy (Nginx) lagao with **Auth Keys** ya VPC internal communication restrict karo. 
</details>

---

## 🔗 Resources
- [OWASP ZAP Download](https://www.zaproxy.org/download/)
- [Snyk Free Advisor](https://snyk.io/advisor/)
- [Burp Suite Training](https://portswigger.net/burp/communitydownload)
