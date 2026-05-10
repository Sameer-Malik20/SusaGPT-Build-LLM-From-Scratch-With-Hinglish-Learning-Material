# Kubernetes RBAC and Network Policies: Internal Lockdown

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **RBAC aur Network Policies** Kubernetes ke "Andarooni Taale" (Internal Locks) hain. 

- **RBAC (Role-Based Access Control)** decide karta hai ki "Kaun kya kar sakta hai" (e.g., Sameer sirf pods dekh sakta hai, lekin edit nahi kar sakta). 
- **Network Policies** decide karte hain ki "Kaun kisse baat kar sakta hai" (e.g., 'Frontend' pod sirf 'Backend' se baat kare, 'Database' se nahi).
By default, Kubernetes mein har pod doosre pod se baat kar sakta hai aur har kisi ke paas bahut saari permissions hoti hain. Yeh "Khula Maidan" hai hackers ke liye. In dono tools se hum K8s ko ek "High-Security Jail" mein badal dete hain.

---

## 2. Deep Technical Explanation
- **RBAC Components**:
    - **Role / ClusterRole**: Defines "Permissions" (Get, List, Create pods).
    - **Subject**: Who gets the permission (User, Group, or ServiceAccount).
    - **RoleBinding / ClusterRoleBinding**: Connects the "Who" to the "What."
- **Network Policies (L3/L4 Firewall)**:
    - Defines Ingress (Incoming) and Egress (Outgoing) rules for pods.
    - Uses "Labels" and "Selectors" to group pods.
    - Requires a **CNI Plugin** (like **Calico** or **Cilium**) to actually work.

---

## 3. Attack Flow Diagrams
**The 'Lateral Movement' Attack (Without Network Policies):**
```mermaid
graph LR
    H[Hacker] -- "Hacks 'Guestbook' Pod" --> G[Guestbook Pod]
    G -- "Network is OPEN" --> DB[Production Database Pod]
    G -- "Scans Internal Network" --> K[Kube-API Server]
    Note over G: Hacker can see everything inside the cluster because there is no 'Deewar' (Policy).
```

---

## 4. Real-world Attack Examples
- **Tiller (Helm v2) Attack**: Helm's old server (Tiller) had full cluster admin rights by default. Hackers found that any pod could talk to Tiller and tell it to: "Delete the whole cluster" or "Deploy a hacker-pod."
- **Default ServiceAccount Token Theft**: Hackers got into a pod, found the service account token in `/var/run/secrets/...`, and used it to become a Cluster Admin because the RBAC was too loose.

---

## 5. Defensive Mitigation Strategies
- **Principle of Least Privilege**: Never use `cluster-admin` for daily work. Create specific roles for specific tasks.
- **Default Deny All**: Create a Network Policy that blocks ALL traffic by default. Then, only allow the specific connections you need.
- **Namespace Isolation**: Use namespaces to separate "Dev," "Test," and "Prod," and use Network Policies to ensure they can't talk to each other.

---

## 6. Failure Cases
- **Missing CNI Support**: You create a Network Policy in AWS EKS, but you didn't install the "Network Policy Plugin." K8s says "OK," but the policy DOES NOT WORK. (Always test your policies!).
- **Wildcard Roles**: Creating a role with `resources: ["*"]` and `verbs: ["*"]`. This is basically giving root access.

---

## 7. Debugging and Investigation Guide
- **`kubectl auth can-i create pods`**: Checking if your current user has a specific permission.
- **`kubectl get netpol`**: Listing all network policies in a namespace.
- **`cilium monitor`**: A powerful tool to see every packet being blocked or allowed by your network policies in real-time.

---

| Feature | RBAC | Network Policy |
|---|---|---|
| Security Focus | Identity & API Access | Network Traffic (IP/Port) |
| Target | Users / ServiceAccounts | Pods |
| Enforced by | API Server | CNI Plugin (Calico/Cilium) |

---

## 9. Security Best Practices
- **No Automount Service Account Token**: Set `automountServiceAccountToken: false` in your pod spec if the pod doesn't need to talk to the K8s API.
- **Use 'ClusterRole' carefully**: Only use ClusterRole if the permission truly needs to be cluster-wide (like "List Nodes"). Otherwise, use a standard "Role."

---

## 10. Production Hardening Techniques
- **Cilium / eBPF**: Using Cilium for network policies because it works at the Kernel level and is much faster and more secure than old-school `iptables`.
- **Identity-based Network Policies**: Allowing traffic based on "Service Identity" rather than IP addresses.

---

## 11. Monitoring and Logging Considerations
- **Audit Logging for RBAC**: Recording every time someone tries to create a new "ClusterRoleBinding."
- **Dropped Packet Logs**: Seeing which pods are trying to talk to unauthorized destinations.

---

## 12. Common Mistakes
- **Confusing 'Role' and 'RoleBinding'**: Thinking that creating a "Role" gives someone access. You MUST bind it to a user!
- **Ignoring Egress**: Only protecting "Incoming" traffic but letting pods talk to any "Outgoing" IP (Malware often talks to a "C2" server).

---

## 13. Compliance Implications
- **PCI-DSS**: Specifically requires "Network Segmentation." Network Policies are the ONLY way to achieve this inside a K8s cluster.

---

## 14. Interview Questions
1. How do you find which users have 'Cluster-Admin' rights?
2. Why do you need a CNI for Network Policies to work?
3. What is the difference between a 'Role' and a 'ClusterRole'?

---

## 15. Latest 2026 Security Patterns and Threats
- **AI-Native Policy Generation**: Tools that watch your cluster for 24 hours and then "Generate" the perfect Network Policy and RBAC roles based on what actually happened.
- **Dynamic RBAC**: Giving users "Temporary" permissions that expire after 1 hour (Just-in-Time Access).
- **Service Mesh + NetPol**: Combining Istio's identity checks with Cilium's network checks for "Defense in Depth."
	
