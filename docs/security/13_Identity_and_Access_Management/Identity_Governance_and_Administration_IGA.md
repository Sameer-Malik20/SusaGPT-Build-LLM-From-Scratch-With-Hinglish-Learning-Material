# Identity Governance and Administration (IGA): The Auditor's Lens

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **IGA** ka matlab hai "Identity ki Cleanliness" check karna. 

Socho aapki company mein 10,000 log hain. Kis ke paas kya access hai? Kya koi intern galti se "Finance" ke folders dekh raha hai? Kya koi employee jo 3 saal pehle "Sales" se "IT" mein gaya tha, uske paas abhi bhi sales ka access hai? **IGA** ek automated process hai jo har 3-6 mahine mein managers se puchta hai: "Kya is bande ko abhi bhi ye access chahiye?". Ise "Access Review" kehte hain. Bina IGA ke, company mein "Access ka Kachra" (Privilege Creep) jama ho jata hai.

---

## 2. Deep Technical Explanation
- **Core Components**:
    - **Identity Lifecycle Management**: Automated joiner, mover, leaver (JML) processes.
    - **Access Requests**: A "Self-service" portal where users can ask for permissions.
    - **Access Certification (Review)**: Periodic audits where managers confirm or revoke access.
    - **Segregation of Duties (SoD)**: Ensuring one person doesn't have too much power (e.g., the person who "Creates" a payment cannot "Approve" it).
    - **Policy Management**: Rules like "Nobody in HR can have access to Source Code."

---

## 3. Attack Flow Diagrams
**The 'Mover' Risk (Privilege Creep):**
```mermaid
graph TD
    S1[Start: Sales Dept] -- "Has Sales Access" --> S2[Move: Marketing Dept]
    S2 -- "Gets Marketing Access" --> S3[Wait: 2 Years]
    S3 -- "Now has Sales + Marketing + Everything else" --> Risk[Huge Attack Surface]
    Note over S3: IGA would have automatically removed 'Sales' access during the move.
```

---

## 4. Real-world Attack Examples
- **Internal Fraud**: An employee in a bank was able to create a fake customer account and "Approve" a loan for themselves because the bank didn't have **Segregation of Duties (SoD)** policies in their IGA system.
- **The 'Terminated' Admin**: An IT admin was fired but their account wasn't deleted for 48 hours. They used that time to log back in and delete 23 production servers. IGA "Leaver" processes should have killed the account in seconds.

---

## 5. Defensive Mitigation Strategies
- **Automated JML**: Connect your HR system (like Workday) directly to your IAM system. If someone is "Fired" in HR, they are "Deleted" in IT automatically.
- **Regular Access Reviews**: Make it a rule that every manager must review their team's access every 90 days.
- **Role-Based Access (RBAC)**: Don't give individual permissions. Give "Roles" (e.g., 'Marketing Lead'). If the role changes, the permissions change automatically.

---

## 6. Failure Cases
- **Certification Fatigue**: Managers get 500 emails and just click "Approve All" without reading, which makes the whole audit useless.
- **Shadow IT**: Employees using tools (like Trello or Dropbox) that are NOT connected to the central IGA system.

---

## 7. Debugging and Investigation Guide
- **Access Reports**: Generating a CSV of: "All users who have 'Admin' rights across all 50 apps."
- **SoD Violation Logs**: Searching for: "Users who have both 'Developer' and 'Production Deploy' rights."
- **SailPoint / Saviynt / Microsoft Entra ID Governance**: The top tools for IGA.

---

| Feature | Standard IAM | IGA (Governance) |
|---|---|---|
| Focus | "How to Login" | "Should they have access?" |
| Audience | Users | Managers / Auditors |
| Key Action | Authentication | Audit / Review |
| Automation | High (SSO/MFA) | Medium (Approvals/Workflows) |

---

## 9. Security Best Practices
- **Least Privilege Enforcement**: If a user hasn't used an app for 90 days, the IGA system should automatically "Ask" if they still need it, or just revoke it.
- **Risk-based Certification**: Review "High Risk" access (like Database Admin) every month, but "Low Risk" (like Zoom) once a year.

---

## 10. Production Hardening Techniques
- **Dynamic Roles**: Using "Tags" and "Attributes" (e.g., 'Project=Alpha') to automatically give and take access as projects change.
- **Closed-loop Remediation**: If an auditor clicks "Revoke," the IGA system must automatically talk to the app (via API) and delete the user—don't wait for a human to do it.

---

## 11. Monitoring and Logging Considerations
- **'SoD Violation' Alerts**: Immediate alert if a user is given two conflicting roles.
- **Overdue Reviews**: Alerting the Security Officer if a manager hasn't completed their quarterly access review.

---

## 12. Common Mistakes
- **Manual JML**: Doing everything via email and tickets. It's slow and always leaves "Orphaned" accounts behind.
- **Ignoring Non-human Accounts**: Not reviewing the access of "Bots" or "API keys."

---

## 13. Compliance Implications
- **SOX (Sarbanes-Oxley)**: Requires strict "Access Controls" for financial systems. Failing an IGA audit can lead to massive fines for public companies.
- **HIPAA**: Requires that access to health data be "Periodically reviewed."

---

## 14. Interview Questions
1. What is 'Segregation of Duties' (SoD)?
2. What happens during an 'Access Review'?
3. Explain the 'Joiner, Mover, Leaver' (JML) process.

---

## 15. Latest 2026 Security Patterns and Threats
- **AI-Native Governance**: AI that analyzes access patterns and says: "Sameer hasn't used his 'AWS' access for 6 months, should I remove it?" (Autonomous Identity).
- **Identity Analytics**: Using big data to find "Outliers"—users whose access is very different from their peers.
- **Just-in-Time Governance**: Moving away from "Fixed" roles to "On-demand" roles that only exist while you are working on a specific ticket.
	
