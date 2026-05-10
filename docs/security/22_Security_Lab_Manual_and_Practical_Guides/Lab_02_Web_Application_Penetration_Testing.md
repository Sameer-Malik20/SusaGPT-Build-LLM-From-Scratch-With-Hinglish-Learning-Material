# Lab 02: Web Application Penetration Testing

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **Web Pentesting** ka matlab hai "Websites ki kamzoriyan dhoondna." 

Is lab mein hum seekhenge ki kaise ek "Hacker's Browser" (Burp Suite) ka use karke website ke traffic ko "Beech mein rokna" (Intercept) aur badalna (Modify). Hum SQL Injection, XSS, aur Auth bypass jaise common attacks ko real-world scenarios mein try karenge. Yaad rakho: "Sirf website ko dekhne se hacking nahi hoti, website ko 'Chhedne' (Manipulate) se hacking hoti hai."

---

## 2. Deep Technical Setup
- **Target App**: **DVWA (Damn Vulnerable Web Application)** or **OWASP Juice Shop**.
- **Tools**:
    - **Burp Suite Community Edition** (Essential).
    - **Firefox** (with **FoxyProxy** extension).
    - **SQLMap** (for automated SQLi).
- **Environment**: Ensure the target app is running in Docker (see Lab 01).

---

## 3. Architecture Diagram
**The Interception Flow:**
```mermaid
graph LR
    Browser[Browser: Firefox] -- "Request" --> Burp[Burp Suite Proxy]
    Burp -- "Modified Request" --> Web[Vulnerable Website]
    Web -- "Response" --> Burp
    Burp -- "Final View" --> Browser
    Note over Burp: This is where we change the 'Price' or 'UserID'.
```

---

## 4. Real-world Lab Scenario
You are testing an E-commerce site. You find that when you buy an item, the browser sends a parameter `price=100`. You use Burp Suite to intercept that request and change it to `price=1` before it reaches the server. If the server accepts it, you've found a "Price Manipulation" bug.

---

## 5. Practical Execution Steps
### Phase 1: SQL Injection
1. Go to the SQL Injection page in DVWA.
2. Enter `' OR 1=1 #` in the User ID field.
3. Observe how the database returns EVERY user in the system.

### Phase 2: Cross-Site Scripting (XSS)
1. Go to the XSS (Stored) page.
2. Enter `<script>alert('Hacked')</script>` in the comment box.
3. Every person who views that page will now see a popup.

### Phase 3: Burp Suite Interception
1. Turn "Intercept ON" in Burp.
2. Submit a form in the browser.
3. Change the data inside Burp and click "Forward."

---

## 6. Failure Cases
- **Burp Certificate Issues**: If you can't see HTTPS traffic, you must download the "CA Certificate" from Burp and import it into your browser.
- **WAF Blocking**: If you get a "403 Forbidden," the app might have a simple firewall. Try to "Obfuscate" your attack.

---

## 7. Debugging and Investigation Guide
- **Browser DevTools (F12)**: Use the "Network" tab to see raw requests.
- **Burp 'Repeater'**: Use this to send the same request 100 times with small changes.

---

## 8. Tradeoffs
| Metric | Automated Scanning (ZAP) | Manual Pentesting (Burp) |
|---|---|---|
| Speed | High | Low |
| Accuracy | Medium (False positives) | Maximum |
| Depth | Shallow | Deep |

---

## 9. Security Best Practices
- **Parameterized Queries**: This is the #1 defense against SQL Injection.
- **Input Encoding**: Encoding `<` as `&lt;` to prevent XSS.

---

## 10. Production Hardening Techniques
- **Content Security Policy (CSP)**: A browser-level rule that tells the browser: "Only trust scripts from MY domain," which stops most XSS.

---

## 11. Monitoring and Logging Considerations
- **WAF Logs**: Practice reading logs to see how an SQLi attack looks to a defender (lots of quotes and semicolons in the URL).

---

## 12. Common Mistakes
- **Testing on 'Live' sites**: Never test on `google.com` or `facebook.com` without a Bug Bounty program.
- **Forgetting to 'Reset' the Lab**: Sometimes one attack breaks the database, making other attacks fail.

---

## 13. Compliance Implications
- **OWASP Top 10**: Your goal is to find at least 5 out of the top 10 vulnerabilities in your lab.

---

## 14. Interview Questions
1. What is the difference between Stored and Reflected XSS?
2. How do you identify a 'Blind' SQL Injection?
3. What is 'Burp Suite' and why is it called an 'Interception Proxy'?

---

## 15. Latest 2026 Security Patterns and Threats
- **GraphQL Injection**: Hacking modern APIs that use GraphQL instead of REST.
- **JWT (JSON Web Token) Attacks**: Changing the "Role" inside a login token to become an Admin.
- **AI-Native Web Attacks**: Using LLMs to generate 1,000 different ways to bypass a WAF.
