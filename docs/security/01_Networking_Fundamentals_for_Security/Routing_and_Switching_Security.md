# Routing and Switching Security: Hardening the Network Core

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **Routing aur Switching** network ki "Roads aur Intersections" hain. 

**Switch** aapki building ki "Gali" hai jo devices ko connect karti hai. **Router** woh "Highway" hai jo ek building ko doosri building se (ya internet se) connect karta hai. Agar roads hi secure nahi hain, toh koi bhi hacker aapke data ke beech mein aa sakta hai. Is module mein hum seekhenge ki kaise switches ke "Ports" ko lock karein aur routers ko "Galat rasta" (Fake routes) dikhane se bachayein.

---

## 2. Deep Technical Explanation
- **Switch Security (L2)**:
    - **Port Security**: Limiting the number of MAC addresses allowed on a single port.
    - **VLANs**: Logically separating users (e.g., Guest Wi-Fi vs. Admin servers).
    - **BPDU Guard**: Preventing someone from plugging in their own switch to take over the network.
- **Router Security (L3)**:
    - **ACLs (Access Control Lists)**: Rules that allow or block traffic based on IP.
    - **Routing Protocol Auth**: Requiring a password before a router accepts a new "Path" from another router (OSPF/BGP).
    - **uRPF**: Checking if a packet is coming from a "Fake" source IP.

---

## 3. Attack Flow Diagrams
**The 'MAC Flooding' Attack on a Switch:**
```mermaid
graph TD
    H[Hacker] -- "Sends 10,000 Fake MACs" --> S[Switch]
    S -- "MAC Table Full" --> Fail[Fails to 'Hub' Mode]
    Fail -- "Broadcasts ALL data to ALL ports" --> H
    Note over H: Hacker can now sniff everyone's traffic.
```

---

## 4. Real-world Attack Examples
- **BGP Hijacking**: A router tells the whole internet: "I am the fastest way to YouTube." All YouTube traffic goes to the hacker's router before reaching the real site.
- **VLAN Hopping**: A hacker on the "Guest" network uses a special packet trick to "Jump" into the "Internal/Server" network.

---

## 5. Defensive Mitigation Strategies
- **Dynamic ARP Inspection (DAI)**: Stopping hackers from pretending to be the router.
- **Control Plane Policing (CoPP)**: Protecting the router's "Brain" from being overwhelmed by a DDoS attack.
- **SSH instead of Telnet**: Never manage your router using unencrypted Telnet.

---

## 6. Failure Cases
- **Default Passwords**: Many routers are hacked because they still use `admin/admin`.
- **Unused Ports**: Leaving empty desks with active network ports that anyone can plug into.

---

## 7. Debugging and Investigation Guide
- **`show mac address-table`**: Seeing who is connected to the switch.
- **`show ip route`**: Checking the router's current "Map" of the network.
- **`tracert` / `traceroute`**: Seeing the path a packet takes to reach its destination.

---

## 8. Tradeoffs
| Feature | VLAN Segmentation | Physical Separation |
|---|---|---|
| Security | High | Maximum |
| Cost | Low (Same switch) | High (Separate hardware) |
| Flexibility | High | Low |

---

## 9. Security Best Practices
- **Disabled Unused Ports**: If a port isn't being used, turn it off!
- **Native VLAN Hardening**: Don't use "VLAN 1" for anything important.

---

## 10. Production Hardening Techniques
- **802.1X Auth**: Requiring a username and password before a port even "Turns on" for a laptop.
- **Management Plane Isolation**: Having a separate network (Out-of-Band) just for managing routers and switches.

---

## 11. Monitoring and Logging Considerations
- **SNMP Traps**: Getting an instant alert if a switch port goes down or if someone tries to log in 10 times.
- **Syslog**: Sending all router logs to a central server (SIEM).

---

## 12. Common Mistakes
- **Assuming 'VLAN = Firewall'**: A VLAN separates traffic, but a router can still connect them. You need a firewall or ACLs between VLANs.
- **Ignoring Console Ports**: Forgetting that someone can plug a cable directly into the physical router if the room isn't locked.

---

## 13. Compliance Implications
- **ISO 27001**: Requires that "Network segregation" be implemented to protect sensitive data.

---

## 14. Interview Questions
1. What is 'Port Security' and how do you configure it?
2. What is the difference between a Router and a Layer 3 Switch?
3. How do you prevent 'VLAN Hopping'?

---

## 15. Latest 2026 Security Patterns and Threats
- **AI-Native Routing**: Routers that use AI to "Detect" a BGP hijack in milliseconds and automatically reroute traffic.
- **SD-WAN Security**: Using software-defined networking to encrypt and secure connections across different branches and the cloud.
- **Infrastructure as Code (IaC) for Networks**: Using **Terraform** or **Ansible** to build and secure 100 switches in 5 minutes with zero human error.
