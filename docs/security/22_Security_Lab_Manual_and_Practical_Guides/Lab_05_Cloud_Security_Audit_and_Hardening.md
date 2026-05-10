# Lab 05: Cloud Security Audit and Hardening

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **Cloud Security Audit** ka matlab hai "AWS/Azure/GCP ke ghar ki talashi lena." 

Cloud mein hacking "Software bugs" se kam aur "Galat Configuration" se zyada hoti hai. Ek khula hua S3 bucket ya ek purana IAM user poori company ko duba sakta hai. Is lab mein hum seekhenge ki kaise **Prowler** ya **ScoutSuite** jaise tools ka use karke apne cloud account ko scan karein aur dekhein ki kahan-kahan "Darwaze" khule hain. Hum "Best Practices" implement karenge taaki koi hacker hamare cloud ka bill $100,000 na bana de.

---

## 2. Deep Technical Setup
- **Account**: A "Free Tier" AWS account.
- **Tools**:
    - **Prowler**: The industry standard for AWS security auditing.
    - **Checkov**: For scanning "Terraform" or "CloudFormation" code.
    - **AWS CLI**: To interact with the account via terminal.
- **Environment**: Install Prowler on your Kali or Mac:
  ```bash
  pip install prowler
  prowler aws
  ```

---

## 3. Architecture Diagram
**The Cloud Audit Flow:**
```mermaid
graph LR
    Tool[Audit Tool: Prowler] -- "Read-Only API Calls" --> AWS[AWS Cloud]
    AWS -- "Resource Config" --> Tool
    Tool -- "Checks against 200+ Rules" --> Report[Security Report: HTML/CSV]
    Note over Report: Red = Critical (Public S3), Green = Good.
```

---

## 4. Real-world Lab Scenario
You are a Cloud Security Consultant. A client thinks their AWS account is "Fine." You run Prowler and find 5 IAM users without MFA, 2 S3 buckets that anyone can read, and an EC2 instance that has "Admin" permissions. You help them "Harden" the account.

---

## 5. Practical Execution Steps
### Phase 1: IAM Hardening
1. Go to IAM console.
2. Enable **MFA** for the Root user.
3. Find any user with `AdministratorAccess` and replace it with a specific policy (e.g., `AmazonS3FullAccess`).

### Phase 2: S3 Security
1. Run Prowler: `prowler aws --check s3_bucket_public_access`.
2. Find the public bucket.
3. Enable "Block all public access" in the S3 console.

### Phase 3: Infrastructure as Code (IaC) Scan
1. Create a simple `main.tf` file that creates an unencrypted S3 bucket.
2. Run `checkov -f main.tf`.
3. Fix the code by adding `server_side_encryption_configuration`.

---

## 6. Failure Cases
- **Permission Denied**: The IAM user you are using to run the audit doesn't have enough "Read" permissions. Use the `SecurityAudit` AWS policy.
- **Resource Limits**: If you have 10,000 resources, Prowler might take hours. Use `--check` to scan only one service at a time.

---

## 7. Debugging and Investigation Guide
- **AWS Trusted Advisor**: A built-in AWS tool that gives basic security advice.
- **CloudTrail**: The "CCTV" of AWS. Use it to see "Who" changed "What" and "When."

---

## 8. Tradeoffs
| Feature | Manual Audit (Console) | Automated Audit (Prowler) |
|---|---|---|
| Speed | Very Slow | Very Fast |
| Thoroughness | Low (Human error) | Maximum (250+ checks) |
| Learning | High (You see the buttons) | Low (It's a report) |

---

## 9. Security Best Practices
- **Least Privilege**: Only give the permissions needed for the job.
- **No Access Keys for Humans**: Use **AWS SSO** or **IAM Roles** instead of permanent `AccessKeyID` and `SecretAccessKey`.

---

## 10. Production Hardening Techniques
- **GuardDuty**: Enabling AWS's "Intrusion Detection" that uses AI to find bitcoin miners or hackers in your account.
- **SCP (Service Control Policies)**: A "Master Switch" that prevents anyone (even admins) from doing dangerous things like "Disabling Logging."

---

## 11. Monitoring and Logging Considerations
- **Config**: Enabling **AWS Config** to record every change to your infrastructure. If a bucket becomes public, Config will tell you exactly who did it.

---

## 12. Common Mistakes
- **Using the 'Root' account for daily work**: If your root account is hacked, it's "Game Over."
- **Leaving 'Default' Security Groups open**: Allowing Port 22 (SSH) or Port 3389 (RDP) to the whole world (`0.0.0.0/0`).

---

## 13. Compliance Implications
- **CIS Benchmarks**: Prowler specifically checks your cloud against the "CIS AWS Foundations Benchmark," which is the industry standard for cloud compliance.

---

## 14. Interview Questions
1. How do you find a public S3 bucket in a large AWS account?
2. What is the difference between an 'IAM User' and an 'IAM Role'?
3. What is 'Least Privilege' in the context of Cloud?

---

## 15. Latest 2026 Security Patterns and Threats
- **AI-Native Cloud Attacks**: Hackers using AI to find "Dangling DNS" or "Orphaned Resources" in your cloud that they can take over.
- **Serverless Malware**: Viruses that live inside Lambda functions and only "Wake up" when the function is called.
- **Multi-Cloud Drift**: Tools that ensure your security policy in AWS is exactly the same as your policy in Azure.
