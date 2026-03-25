# 🐳 Infrastructure & Microservices — Docker, K8s, and Scaling
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master Dockerization, Kubernetes, Serverless, Microservices, and Cloud Infrastructure (AWS/GCP).

---

## 📋 Table of Contents: The Cloud Engine

| Layer | Topic | Significant? |
|-------|-------|--------------|
| **1. Container**| Docker & Images | "Build Once, Run Anywhere" (Box management). |
| **2. Orchestration**| Kubernetes (K8s) | 1000 containers ko auto-manage karna. |
| **3. Serverless**| AWS Lambda / GCP Functions| Bina server manage kiye code run karna. |
| **4. Patterns** | Microservices Design | Service-to-Service communication. |
| **5. Network** | Nginx, Load Balancers, VPC | Traffic ko sahi jagah pe bhejná. |
| **6. CI/CD Pipeline**| GitHub Actions / GitLab | Automatic Testing to Cloud Deployment. |

---

## 🏗️ 1. Docker: Isolation & Consistency

Aapka code aapke laptop par chal raha hai, par server par nahi? **Docker is the solution.**
- **Dockerfile:** Recipe banaye "OS + Node.js + Code + Dependencies".
- **Docker Image:** Immutable template jise hum cloud par upload karte hain.
- **Docker Compose:** Multiple containers (Backend, Frontend, Redis, DB) ko ek saath run karna.

---

## ☸️ 2. Kubernetes (K8s): The Conductor

Docker containers ko cluster par distribute karna.
- **Pods:** Kubernetes ki sabse choti unit (Container runtime).
- **Service:** Pods ko external world (User) se connect karna.
- **Auto-Scaling:** Agar traffic badhe, toh apne aap 2 se 100 pods bana dena (HPA - Horizontal Pod Autoscaler).

---

## ⚡ 3. Serverless: No Server Management

"Serverless" ka matlab server nahi hona nahi hai, balki aapko "Manage" nahi karna parta.
- **AWS Lambda:** Sirf 1 function run karna (e.g. Image resize, Email send).
- **Pricing:** Sirf "Execution time" ke paise dena. (0 traffic = $0 cost).

---

## 🌐 4. Microservices: The Architecture of Giants

Bade systems (Netflix, Amazon) ek bade monolith (Ek hi code repo) mein nahi hote.
- **Decoupling:** Auth service fail hui toh Payment service chalti rehne chahiye.
- **Internal Talk:** HTTP API, gRPC, ya Messaging (RabbitMQ / Kafka) use karna asynchronous communication ke liye.

---

## 📡 5. Networking & Security: VPC & Nginx

- **VPC (Virtual Private Cloud):** Apne database ko public internet se chhupana (Private Subnet).
- **Reverse Proxy (Nginx):** Frontend requests ko port 80/443 se backend port 3000 par bhejná.
- **SSL/TLS (HTTPS):** Data ko encrypt karna using Certificates (Let's Encrypt).

---

## 🚀 6. CI/CD: Automated Deployment

Har bar manually `git push` ke baad `ssh` karke `npm start` mat karo (Old school!).
- **GitHub Actions:** Code push -> Build -> Tests -> Docker Image Build -> Cloud Deploy. (Automatically in 2 minutes!).

```yaml
# GitHub Action logic
# jobs:
#   build:
#     - run: docker build -t backend:latest .
#     - run: aws ecs update-service --service backend
```

---

## 🧪 Quick Test — Senior DevOps / Backend Level!

### Q1: Monolith vs Microservices?
**Answer:** Monolith sasta aur fast development ke liye (Startups). Microservices scaling aur different teams (multi-language/different DBs) ke liye best hain (Enterprise).

### Q2: Why Docker over VM (Virtual Machines)?
**Answer:** VMs mein poora OS (Windows/Linux) copy hota hai (Slow & Heavy). Docker sirf libraries aur process isolated rakhta hai (Fast & Lightweight).

---

## 🏆 Final Summary Checklist
- [ ] Dockerfiles are minimal (Using Alpine images)?
- [ ] Microservice boundaries clearly defined (DDD Pattern)?
- [ ] Serverless for sporadic tasks (Events)?
- [ ] Load balancer setup for high traffic?

> **Infra Tip:** Automation is the key. Hard-coded IPs are the enemy. Use DNS and Service Discovery.
