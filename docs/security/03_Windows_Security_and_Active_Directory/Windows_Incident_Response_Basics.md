# Windows Incident Response Basics: What to do when Hacked

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **Windows Incident Response (IR)** ka matlab hai "System hack hone ke baad ka Action Plan." 

Jab aapko lage ki system mein koi "Ghuspaithiya" (Intruder) hai, toh aapko panic nahi karna. Aapko "Saboot" (Evidence) collect karne hain bina unhe kharab kiye. Socho aap ek crime scene par ho—agar aapne galti se file delete kar di ya computer restart kar diya, toh hacker ke nishan (traces) mit sakte hain. Is module mein hum seekhenge ki kaise "RAM" se data nikalein aur kaise "Logs" check karke pata lagayein ki hacker kahan se aaya aur kya lekar gaya.

---

## 2. Deep Technical Explanation
- **The IR Process**: Preparation -> Identification -> Containment -> Eradication -> Recovery -> Lessons Learned.
- **Artifacts**: Pieces of evidence left behind (e.g., Registry keys, Prefetch files, Event logs).
- **Live Analysis vs. Dead Analysis**:
    - **Live**: Analyzing the system while it's running (checking RAM, active connections).
    - **Dead**: Shutting down and taking an image of the hard drive for offline analysis.
- **Volatile Data**: Data that is lost when the computer is turned off (RAM, network connections). Always collect this FIRST.

---

## 3. Attack Flow Diagrams
**The Investigation Loop:**
```mermaid
graph TD
    Alert[Security Alert: Unusual Admin Login] --> Identify[Identify: Which PC? Which Account?]
    Identify --> Volatile[Collect RAM & Network Connections]
    Volatile --> Analyze[Analyze: Find the Malware/Hacker traces]
    Analyze --> Contain[Contain: Disconnect from Network]
    Contain -- "Find more artifacts" --> Analyze
    Analyze --> Clean[Clean the system and Reset Passwords]
    Note over Volatile: Use 'FTK Imager' to dump RAM.
```

---

## 4. Real-world Attack Examples
- **Ransomware Discovery**: Finding a strange file `note.txt` on the desktop. The IR team checks the **MFT (Master File Table)** to see exactly when that file was created and which user did it.
- **Lateral Movement**: Seeing a user log in from PC-A to PC-B to PC-C. IR uses **Event ID 4624** (Login) to track the hacker's "Path" through the company.

---

## 5. Defensive Mitigation Strategies
- **Regular Backups**: The #1 defense against ransomware. If you have a clean backup, you can recover in hours.
- **Isolation**: Having a way to "Cut the cable" (digitally) for a specific PC so the virus doesn't spread.
- **Honeypots**: Creating a fake "Admin" account. If someone tries to log into it, you know for 100% certainty that you are being hacked.

---

## 6. Failure Cases
- **Over-writing Evidence**: Running an antivirus scan immediately. Antivirus might "Delete" the malware file, which was your #1 piece of evidence for analysis.
- **Restarting the PC**: This wipes the RAM, where the hacker's "Secret keys" and "Unsaved scripts" are often hidden.

---

## 7. Debugging and Investigation Guide
- **`tasklist /m`**: Seeing which DLLs are loaded into a process.
- **`netstat -naob`**: Seeing which program is talking to which IP address.
- **`Get-ScheduledTask`**: Checking if the hacker scheduled a "Virus" to run every day at 3 AM.
- **`Get-Service`**: Looking for strange new services.

---

## 8. Tradeoffs
| Method | Live Analysis | Memory Forensics (RAM Dump) |
|---|---|---|
| Speed | Fast | Slow |
| Detail | Medium | Maximum (See hidden malware) |
| Risk | High (Might alert hacker) | Low |

---

## 9. Security Best Practices
- **Write-Blockers**: Using a physical device to ensure that when you read a hard drive, you don't accidentally write any data to it (preserving the evidence).
- **Timeline Analysis**: Creating a master list of every event: "3:00 PM: File downloaded, 3:01 PM: Registry changed, 3:05 PM: Admin login."

---

## 10. Production Hardening Techniques
- **Sysmon**: Installing Sysmon *before* the hack happens so you have perfect logs when you need to investigate.
- **Centralized Log Server**: Ensuring logs are sent to a SIEM so the hacker can't delete them from the local PC.

---

## 11. Monitoring and Logging Considerations
- **PowerShell Transcription**: Capturing every command the hacker typed.
- **Prefetch Files**: Windows automatically records which programs were run recently. IR analysts check these to see what the hacker executed.

---

## 12. Common Mistakes
- **Assuming 'It's just a bug'**: Ignoring a strange error message that was actually the first sign of a hack.
- **Trusting the UI**: Hackers can hide processes from Task Manager. Always use command-line tools or external scanners.

---

## 13. Compliance Implications
- **GDPR / Data Breach Laws**: Many laws require you to report a hack within 72 hours. Fast IR is critical to meet these deadlines.

---

## 14. Interview Questions
1. What is the 'Order of Volatility'?
2. What is 'Lateral Movement' and how do you track it?
3. Why is it bad to restart a hacked computer immediately?

---

## 15. Latest 2026 Security Patterns and Threats
- **AI-Native IR Playbooks**: Using AI to automatically contain a hack in milliseconds (e.g., "AI sees ransomware behavior -> AI isolates the PC immediately").
- **Cloud Forensics**: Investigating a hack on a server that "Doesn't exist" (Serverless/Lambda), where you only have logs and no physical hard drive.
- **Memory-Only Malware**: Malware that never touches the disk. IR analysts now focus 100% on RAM analysis using tools like **Volatility 3**.
