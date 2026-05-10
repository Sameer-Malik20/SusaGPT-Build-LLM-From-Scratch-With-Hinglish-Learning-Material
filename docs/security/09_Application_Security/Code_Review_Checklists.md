# Code Review Checklists: The Human Security Guard

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **Code Review** ka matlab hai "Doosre ki aankhon se check karwana." 

Jab hum apna code khud dekhte hain, toh humein apni galtiyan nahi dikhtin. Lekin jab koi doosra developer ya security engineer use dekhta hai, toh use turant "Security Holes" mil jate hain. Yeh module aapko ek "Checklist" dega—matlab woh sawal jo aapko har code review mein poochne chahiye: "Kya password leak ho raha hai?", "Kya user input check kiya?", "Kya session secure hai?".

---

## 2. Deep Technical Explanation
- **What is a Security Code Review?**: A manual or automated process of auditing source code for security flaws.
- **The Checklist Approach**: Ensuring that every piece of code meets a specific security baseline.
- **Key Focus Areas**:
    - **Authentication**: Is it required for sensitive actions?
    - **Authorization**: Is it checked on the *server-side*?
    - **Data Handling**: Is PII (Personal Info) encrypted?
    - **Error Handling**: Is sensitive info being leaked in logs?

---

## 3. Attack Flow Diagrams
**The 'Authorization Bypass' found in Review:**
```mermaid
graph TD
    D[Developer] -- "Writes code: 'deleteOrder(id)'" --> R[Reviewer]
    R -- "Question: Is the user the owner of the order?" --> D
    D -- "Realizes: No, anyone can delete any ID!" --> Fix[Fix: Adds ownership check]
    Fix -- "Security Restored" --> Prod[Production]
    Note over R: Without the reviewer, this would be a major BOLA vulnerability.
```

---

## 4. Real-world Attack Examples
- **BOLA (formerly IDOR)**: Many of the world's biggest breaches (like Uber or Instagram) were caused by a single missing line of code that checked "Who owns this data?". A good code review would have caught this in 2 minutes.
- **Hardcoded AWS Keys**: In 2019, a developer for a major bank pushed code to GitHub that had a hidden API key. The reviewer didn't catch it, and the bank was hacked.

---

## 5. Defensive Mitigation Strategies
- **Peer Review**: Every "Pull Request" must be reviewed by at least one other person.
- **Security Checklists**: Use a standard list like the **OWASP Code Review Guide**.
- **Checklist Automation**: Use tools that automatically comment on a PR if a dangerous function (like `eval()`) is used.

---

## 6. Failure Cases
- **Rubber Stamping**: Reviewers just clicking "Approve" without actually reading the code because they are in a hurry.
- **Too Many Changes**: A PR with 5,000 lines of code is impossible to review properly. (Keep PRs small!).

---

## 7. Debugging and Investigation Guide
- **GitHub 'Files Changed' Tab**: The main place to perform reviews.
- **SonarQube**: Automatically highlights "Security Hotspots" for the reviewer to focus on.
- **`git diff`**: Viewing changes in the command line.

---

| Feature | Automated Review (SAST) | Human Code Review |
|---|---|---|
| Speed | Very Fast | Slow |
| Logic Errors | Poor | Excellent |
| Configuration | Medium | Good |
| Context | None | High |

---

## 9. Security Best Practices
- **Focus on Logic**: Humans are better at finding "Business Logic" flaws (e.g., "A user can get a 100% discount if they enter a negative quantity").
- **Positive Culture**: Security reviews shouldn't be about "Blaming," but about "Learning."

---

## 10. Production Hardening Techniques
- **Mandatory Review Policies**: Configuring GitHub/GitLab to PREVENT merging unless a security-trained reviewer has approved.
- **Differential Reviews**: Only reviewing the *new* code, not the whole project, to save time.

---

## 11. Monitoring and Logging Considerations
- **Review Completion Time**: Monitoring if security reviews are taking 1 hour or 1 week.
- **Bugs Found in Review**: Tracking which developers are consistently making the same security mistakes so they can be trained.

---

## 12. Common Mistakes
- **Reviewing only the 'Backend'**: Forgetting that Frontend code (JavaScript) can also have security flaws like XSS or DOM-based injection.
- **Ignoring 3rd-party code**: Reviewing your code but not the libraries you added to `package.json`.

---

## 13. Compliance Implications
- **SOC2**: Specifically requires evidence of "Peer Reviews" for all changes to production systems.

---

## 14. Interview Questions
1. How do you find a 'BOLA' vulnerability in a code review?
2. What are the top 3 things you look for in a security code review?
3. Why is 'Human' review still necessary if we have 'Automated' scanners?

---

## 15. Latest 2026 Security Patterns and Threats
- **AI-Augmented Reviews**: AI that summarizes a PR and says: "This change touches the 'Payment' logic, please pay extra attention to lines 40-60."
- **Social Engineering in PRs**: Hackers trying to "Trick" a reviewer by hiding a malicious line inside a very large and boring code change.
- **Reviewer Fatigue Analytics**: Systems that alert if a reviewer is approving code too fast without actually reading it.
	
