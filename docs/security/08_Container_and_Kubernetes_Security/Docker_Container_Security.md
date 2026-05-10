# 🐳 Docker & Container Security
> **Level:** Intermediate | **Language:** Hinglish | **Goal:** Secure Docker deployments

---

## 🧭 Core Concepts (Concept-First)

- Image Security: Scanning, minimal base
- Runtime Security: Non-root users, capabilities
- Network Security: Isolation
- Secrets Management

---

## 1. 🖼️ Secure Images

```dockerfile
# Use minimal base
FROM node:20-alpine

# Non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy files
COPY --chown=nodejs:nodejs . .

# Switch to non-root
USER nodejs

CMD ["node", "server.js"]
```

---

## 2. 🔒 Security Best Practices

```dockerfile
# Don't expose secrets in image
# Use build args for sensitive values

# Multi-stage build for minimal image
FROM node:20-alpine AS builder
COPY . .
RUN npm run build

FROM node:20-alpine
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
```

---

## 3. 🛡️ Docker Security Commands

```bash
# Scan images
docker scout cves myimage:latest

# Run container securely
docker run --read-only --tmpfs /tmp myimage

# Drop capabilities
docker run --cap-drop ALL --cap-drop NET_BIND_SERVICE myimage

# Limit resources
docker run --memory=512m --cpus=1.0 myimage
```

---

## ✅ Checklist

- [ ] Secure Dockerfile likh sakte ho
- [ ] Container securely run kar sakte ho
- [ ] Image scan kar sakte ho