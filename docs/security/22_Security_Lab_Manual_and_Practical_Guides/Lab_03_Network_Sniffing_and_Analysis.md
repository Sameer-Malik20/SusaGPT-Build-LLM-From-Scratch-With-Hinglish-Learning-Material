# Lab 03: Network Sniffing and Analysis

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **Network Sniffing** ka matlab hai "Hawa mein udte data ko pakadna." 

Jab aap internet use karte ho, toh data "Packets" ki shakal mein travel karta hai. Agar woh data encrypted nahi hai (jaise HTTP ya FTP), toh koi bhi use "Sniff" karke aapke passwords aur messages dekh sakta hai. Is lab mein hum seekhenge ki kaise **Wireshark** ka use karke network traffic ko analyze karein aur kaise **ArpSpoofing** karke "Man-in-the-Middle" (MITM) attack perform karein. Yeh lab aapko dikhayegi ki "Encryption" kyun itni zaruri hai.

---

## 2. Deep Technical Setup
- **Tools**:
    - **Wireshark**: The world's most popular network protocol analyzer.
    - **Ettercap** or **Bettercap**: For MITM and ARP Spoofing.
    - **Nmap**: For scanning the network.
- **Environment**: You need at least two VMs (e.g., Kali and a Windows/Ubuntu target) on the same "Host-Only" or "NAT Network."

---

## 3. Architecture Diagram
**The MITM Attack:**
```mermaid
graph LR
    User[Victim PC] -- "Data" --> Hacker[Hacker's PC]
    Hacker -- "Forwarded Data" --> Router[Router/Gateway]
    Note over Hacker: Hacker tells Victim: 'I am the Router'.
    Note over Hacker: Hacker tells Router: 'I am the Victim'.
```

---

## 4. Real-world Lab Scenario
Imagine you are at a public Airport Wi-Fi. Someone is logging into an old website that uses `http://` (not https). You use your Kali laptop to intercept their traffic and see their username and password in plain text on your screen.

---

## 5. Practical Execution Steps
### Phase 1: Network Scanning
1. Find your network range: `ip a`.
2. Scan for targets: `nmap -sn 10.0.2.0/24`.

### Phase 2: Sniffing with Wireshark
1. Open Wireshark and select your interface (`eth0`).
2. Click "Start."
3. Filter for `http` or `dns` or `tcp`.
4. Right-click a packet and select "Follow -> TCP Stream" to see the conversation.

### Phase 3: ARP Spoofing (Bettercap)
1. Run Bettercap: `sudo bettercap -iface eth0`.
2. Start discovery: `net.probe on`.
3. Start spoofing: `set arp.spoof.targets 10.0.2.5; arp.spoof on`.
4. Now all traffic from `.5` will pass through your Kali VM.

---

## 6. Failure Cases
- **Switched Networks**: Modern switches are smart; they don't send everyone's data to everyone. You *must* use ARP Spoofing to force the data to your PC.
- **Encrypted Traffic (HTTPS)**: You will see the packets, but they will look like "Garbage" (Encrypted). You won't be able to see passwords unless you use a "SSL Strip" attack.

---

## 7. Debugging and Investigation Guide
- **`arp -a`**: Run this on the victim machine. If the MAC address of the Gateway matches the MAC of the Hacker, the victim is being spoofed.
- **Packet Color Coding**: In Wireshark, "Black" packets usually mean errors or resets. "Green" is usually HTTP.

---

## 8. Tradeoffs
| Feature | Hub (Old) | Switch (Modern) |
|---|---|---|
| Security | Low (Anyone can sniff) | High (Data sent to destination only) |
| Performance | Low | High |
| Sniffing Ease | Extremely Easy | Hard (Needs Spoofing) |

---

## 9. Security Best Practices
- **Use HTTPS/TLS**: Encrypt the data so sniffing is useless.
- **Static ARP**: Telling your computer: "This is the ONLY MAC address I trust for the Router."
- **VPN**: Encrypting all your traffic in a tunnel so the local Wi-Fi hacker can't see anything.

---

## 10. Production Hardening Techniques
- **Dynamic ARP Inspection (DAI)**: A feature on Cisco/managed switches that automatically blocks ARP Spoofing attempts.
- **Port Security**: Only allowing specific devices to plug into specific network ports.

---

## 11. Monitoring and Logging Considerations
- **IDS Alerts**: Most IDS (like Snort) will trigger an "ARP Spoofing Detected" alert if they see someone trying to take over the gateway.

---

## 12. Common Mistakes
- **Sniffing on your Home Wi-Fi**: This is safe, but don't do it on your neighbor's Wi-Fi!
- **Overloading the Network**: If you spoof a busy server, your Kali VM might crash because it can't handle all that traffic.

---

## 13. Compliance Implications
- **PCI-DSS**: Requires that all "Cardholder Data" be encrypted over public networks. Sniffing is the test used to prove if this is working.

---

## 14. Interview Questions
1. What is 'ARP Spoofing' and how does it work?
2. How do you find a password in a Wireshark PCAP file?
3. What is the difference between 'Promiscuous Mode' and 'Monitor Mode'?

---

## 15. Latest 2026 Security Patterns and Threats
- **DoH (DNS over HTTPS)**: Hackers can't even see which websites you are visiting anymore because DNS queries are now encrypted.
- **TLS 1.3**: The latest version of TLS which makes it almost impossible to "Decrypt" traffic even if you have the server's private key (Forward Secrecy).
- **Wi-Fi 7 Security**: New features that make "Evil Twin" and "De-authentication" attacks much harder.
