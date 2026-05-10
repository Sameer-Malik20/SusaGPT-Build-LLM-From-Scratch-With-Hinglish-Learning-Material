# Capstone 2: Cloud Infrastructure Hardening (Project 'Castle-Cloud')

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, ye project aapko "Cloud Security Architect" banayega. 

Ismein aapko koi website nahi banani, balki ek poora "Cloud Environment" (AWS ya Azure) banana hai jo itna secure ho ki hacker dekh kar hi ro de. Aap **Terraform** use karoge code likhne ke liye, aur woh code automatically ek VPC banayega, firewalls set karega, aur encryption on karega. Aapko "Cloud-native" security tools (jaise GuardDuty ya Sentinel) bhi set karne honge. Ye project dikhata hai ki aapko "Scale" par security manage karni aati hai.

---

## 2. Technical Project Requirements
- **Infrastructure as Code (IaC)**: Use **Terraform** or **AWS CDK**.
- **Network Isolation**: Create a multi-tier VPC (Public, Private, and Data subnets).
- **Identity**: Implement IAM Roles with "Least Privilege" (No permanent keys!).
- **Security Services**:
    - **Monitoring**: AWS GuardDuty or Azure Defender.
    - **Logging**: AWS CloudTrail + S3 (with Object Lock).
    - **Encryption**: KMS (Customer Managed Keys) for EBS and S3.
- **Compliance**: Auto-generate a report that shows your setup follows **CIS Benchmarks**.

---

## 3. Project Architecture Diagram
**The 'Castle-Cloud' VPC:**
```mermaid
graph TD
    IGW[Internet Gateway] --> ALB[Application Load Balancer]
    ALB -- "HTTPS only" --> Pub[Public Subnet: NAT Gateway]
    Pub --> Priv[Private Subnet: App Servers]
    Priv -- "Strict Port 5432" --> Data[Data Subnet: RDS Database]
    S3[S3 Bucket: Encrypted]
    Note over Priv,Data: All subnets have 'Flow Logs' enabled.
    Note over S3: Bucket has 'Public Access Blocked' at account level.
```

---

## 4. Phase-by-Phase Execution Guide
- **Phase 1: Networking**: Build the VPC with no public IPs for the servers.
- **Phase 2: Identity**: Create IAM Roles. Only allow the "App Server" to talk to the "S3 Bucket."
- **Phase 3: Hardening**: Turn on encryption for everything. Setup "Security Groups" that only allow port 443.
- **Phase 4: Monitoring**: Setup alerts. If someone logs in from a strange IP, send a Slack message.
- **Phase 5: Policy as Code**: Write **OPA (Rego)** rules to ensure nobody can accidentally make an S3 bucket public later.

---

## 5. Defensive Hardening Checklist
- [ ] Is there a 'Bastion Host' or 'AWS Client VPN' for admin access? (No open SSH!).
- [ ] Is CloudTrail enabled in ALL regions?
- [ ] Are S3 buckets encrypted with KMS?
- [ ] Are Security Groups using "Least Privilege" (No 0.0.0.0/0 on internal ports)?
- [ ] Is GuardDuty turned on and sending alerts?

---

## 6. Common Failure Points in this Project
- **NAT Gateway Cost**: Forgetting to turn off the NAT Gateway when not using it (It's expensive!).
- **Circular Dependencies**: Trying to make a security group depend on itself in Terraform.
- **Root Account Usage**: Using the AWS Root account instead of an IAM user. (Bad practice!).

---

## 7. Tools to Use
- **IaC**: Terraform.
- **Scanning**: **Checkov** or **TFSec** (Scans your Terraform code for bugs).
- **Cloud**: AWS (Free Tier) or Azure.
- **Audit**: **Prowler** (Scans your real cloud and gives a score).

---

| Layer | Traditional Cloud | 'Castle-Cloud' (Your Project) |
|---|---|---|
| **VPC** | Default VPC | **Custom Multi-Tier VPC** |
| **Access** | SSH open to world | **SSM Session Manager (No SSH)** |
| **Secrets** | Hardcoded in scripts | **AWS Secrets Manager** |
| **Logging** | Off / Default | **Aggregated in Locked S3** |

---

## 9. Security Best Practices for Cloud Capstones
- **Modular Terraform**: Don't put 1,000 lines in one file. Separate into `vpc.tf`, `iam.tf`, `db.tf`.
- **State File Security**: Encrypt your `terraform.tfstate` file in an S3 bucket with versioning.

---

## 10. Production Hardening Techniques
- **Service Control Policies (SCPs)**: A rule that says: "Even the Admin cannot delete the audit logs."
- **VPC Endpoints**: Communicating with S3/DynamoDB without using the public internet at all.

---

## 11. Monitoring and Logging Considerations
- **AWS Config**: Monitoring for "Configuration Drift" (e.g., if someone manually changes a firewall rule).
- **Billing Alarms**: The #1 security alert for cloud—getting notified if costs spike.

---

## 12. Deliverables for Portfolio
- **GitHub Repository**: Containing all your Terraform (.tf) files.
- **Prowler Report**: A PDF showing your cloud is 90%+ compliant with CIS standards.
- **Architecture Diagram**: A clean Mermaid or LucidChart diagram.

---

## 13. Compliance Context
- **CIS AWS Foundations Benchmark**: Your project should be built specifically to pass this benchmark. This is what real companies use.

---

## 14. Interview Talking Points
1. "I used **Infrastructure-as-Code** to ensure that my security settings are reproducible and auditable."
2. "I implemented a **Three-Tier Architecture** to completely isolate the database from the public internet."
3. "I utilized **AWS Secrets Manager** with automatic rotation to protect my database credentials."

---

## 15. Bonus: Advanced 2026 Features
- **Multi-Cloud Failover**: Building a project that can move from AWS to Azure automatically if one cloud is attacked.
- **Serverless WAF**: Using AWS WAF with "AI-Managed Rules" to block 2026-level bot attacks.
- **Zero-Trust with Verified Access**: Connecting to your private apps without a VPN using **AWS Verified Access**.
	
