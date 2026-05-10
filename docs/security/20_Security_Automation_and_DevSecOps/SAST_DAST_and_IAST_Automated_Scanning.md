# SAST, DAST, and IAST: The Automated Scanner Trio

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **SAST, DAST, aur IAST** code ko check karne ke teen alag "Nazariye" (Perspectives) hain. 

- **SAST (Static)**: Ye code ko "Bina chalaaye" (Inside-Out) check karta hai. Jaise ek doctor aapka X-ray dekh kar bataye ki "Haddi tooti hai." Ye developer ke laptop par hi bugs pakad leta hai.
- **DAST (Dynamic)**: Ye app ko "Chala kar" (Outside-In) check karta hai. Jaise ek hacker website par "Goliyan" (Malicious requests) chala kar dekhe ki kya hota hai. Ye app ke deploy hone ke baad bugs dhoondta hai.
- **IAST (Interactive)**: Ye dono ka mix hai. Ye app ke "Andar" baithta hai jab woh chal rahi hoti hai. 

---

## 2. Deep Technical Explanation
- **SAST (Static Application Security Testing)**:
    - Analyzes Source Code, Bytecode, or Binaries.
    - Finds: Buffer overflows, SQL injection patterns, Hardcoded keys.
    - Pros: Finds bugs early, shows the exact line of code.
- **DAST (Dynamic Application Security Testing)**:
    - Attacks the running application (Web, API).
    - Finds: Cross-Site Scripting (XSS), Insecure Headers, Server Misconfigurations.
    - Pros: No false positives (if it hits, it's real), tests the whole system (DB + Server + Code).
- **IAST (Interactive Application Security Testing)**:
    - Uses an "Agent" inside the app runtime.
    - Combines code analysis with live traffic data.

---

## 3. Attack Flow Diagrams
**The 'Scanning' Timeline:**
```mermaid
graph LR
    Code[1. Writing Code] -- "SAST Scan" --> Build[2. Building App]
    Build -- "SCA Scan (Libraries)" --> Test[3. Testing Environment]
    Test -- "DAST / IAST Scan" --> Deploy[4. Production]
    Note over Code,Build: SAST is fast and finds 'Typo' level security bugs.
    Note over Test: DAST finds 'Real-world' hacking holes.
```

---

## 4. Real-world Attack Examples
- **The 'Hardcoded Key' Disaster (SAST win)**: A developer put their AWS secret key in a comment in the code. A SAST scanner found it in 2 seconds and blocked the commit. Without SAST, that key would be on GitHub in minutes.
- **The 'Hidden Admin' Page (DAST win)**: A developer created a secret page `/admin_test` for debugging. They forgot to delete it. SAST didn't see it because the code looked "Normal." But a DAST scanner "Crawled" the website, found the link, and realized it had no password.

---

## 5. Defensive Mitigation Strategies
- **Pipeline Integration**: Put SAST in your "Pre-commit" or "Pull Request" stage. Put DAST in your "Staging/UAT" stage.
- **Triage False Positives**: Scanners are often "Too sensitive." An engineer must review the results and say "This is not a real bug" so the developers don't get annoyed.
- **Open Source Tools**: Use **SonarQube** (SAST) and **OWASP ZAP** (DAST) to start for free.

---

## 6. Failure Cases
- **DAST can be 'Destructive'**: If you run a DAST scanner on a production database, it might try to "Delete" users or "Submit" 10,000 fake orders. (Only run DAST in a test environment!).
- **SAST 'Blindness'**: SAST can't find bugs in "Third-party" APIs or "Server settings" because it only looks at your code.

---

## 7. Debugging and Investigation Guide
- **SonarLint**: An IDE plugin that shows you SAST bugs *while you type*. (Like a security spell-checker).
- **ZAP Desktop**: A tool where you can "Record" yourself using the app, and then tell ZAP: "Now attack every button I just clicked."
- **Semgrep**: A modern, super-fast SAST tool that uses simple patterns to find bugs.

---

| Feature | SAST | DAST | IAST |
|---|---|---|---|
| Knowledge | White Box (Full access) | Black Box (No access) | Glass Box (Agent inside) |
| Phase | Development | Test / Staging | Test / Staging |
| Speed | Fast | Slow | Medium |
| Finds | Code Bugs | Infrastructure / Logic | **The Best of Both** |

---

## 9. Security Best Practices
- **Fix 'Criticals' First**: Don't try to fix 500 "Info" alerts. Fix the 5 "Critical" SQL Injections first.
- **Standardize Rules**: Use the **OWASP Top 10** as your base rulebook for all scanners.

---

## 10. Production Hardening Techniques
- **Security as Code**: Write your own custom SAST rules (e.g., "In our company, never use the 'md5' function").
- **Dynamic DAST**: Configuring your DAST scanner to log in as different users (Admin, User, Guest) to see if a "User" can see an "Admin" page.

---

## 11. Monitoring and Logging Considerations
- **Vulnerability Density**: Tracking: "How many security bugs per 1,000 lines of code do we have?".
- **Scanner Coverage**: Are we scanning ALL our apps, or only the "Main" website?

---

## 12. Common Mistakes
- **Only using SAST**: Thinking that because the code is clean, the website is safe. (Firewall and Server bugs are still there!).
- **Ignoring the Results**: Running the scanner but never looking at the 50-page PDF report it generates.

---

## 13. Compliance Implications
- **PCI-DSS Requirement 6.3.2**: Specifically requires that you review code for common vulnerabilities. SAST is the standard way to prove you are doing this.

---

## 14. Interview Questions
1. What is the main difference between SAST and DAST?
2. Why is 'False Positive' a major problem in automated scanning?
3. What is 'IAST' and why is it becoming popular?

---

## 15. Latest 2026 Security Patterns and Threats
- **AI-Powered Scanning**: Scanners that use LLMs to "Understand" the context of a bug, reducing false positives by 90%.
- **Infrastructure SAST**: Scanning your Terraform and Kubernetes files as if they were "Code" (using tools like **KICS**).
- **API-First DAST**: Specialized scanners that only attack JSON/REST APIs (using tools like **StackHawk**).
	
