# 🐳 Fullstack Docker Deployment - Complete Guide

> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master containerization for fullstack applications with Docker, Docker Compose, and multi-stage builds.

---

## 🧭 Core Concepts (Concept-First)

- Docker Basics: Images, containers, volumes
- Multi-stage Builds: Optimization, caching
- Docker Compose: Orchestration, networking
- Security: Non-root users, secrets
- CI/CD: GitHub Actions, deployment

---

## 📋 Complete Guide

### 1️⃣ Dockerfile for Node.js Backend

**Basic Dockerfile:**
```dockerfile
# Use specific version
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start application
CMD ["node", "server.js"]
```

**Optimized Multi-stage:**
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy built artifacts
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

# Switch to non-root user
USER nodejs

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### 2️⃣ Dockerfile for Next.js

**Next.js Dockerfile:**
```dockerfile
# Dependencies stage
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Builder stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Runner stage
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### 3️⃣ Docker Compose

**Development:**
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/myapp
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

**Production:**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
```

### 4️⃣ Docker Networking

**Custom Networks:**
```yaml
services:
  api:
    networks:
      - backend
      - frontend

  postgres:
    networks:
      - backend

  nginx:
    networks:
      - frontend

networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge
```

### 5️⃣ Docker Security

**Security Best Practices:**
```dockerfile
# Use specific version, not latest
FROM node:20.10.0-alpine3.19

# Don't run as root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set environment variables
ENV NODE_ENV=production \
    PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

# Read-only filesystem (where possible)
# Note: Not applicable for all apps
```

### 6️⃣ CI/CD with GitHub Actions

**Docker Build & Push:**
```yaml
name: Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
          
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: user/app:${{ github.sha }}
          cache-from: type=registry,ref=user/app:latest
          cache-to: type=inline
```

---

## 🎯 Best Practices Checklist

- [ ] Use specific base image versions
- [ ] Use multi-stage builds
- [ ] Run as non-root user
- [ ] Use .dockerignore
- [ ] Implement health checks
- [ ] Use volumes for development
- [ ] Use environment variables
- [ ] Optimize layer caching

---

## 🔗 Related Resources

- [Docker Documentation](https://docs.docker.com)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Docker](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

> 💡 **Tip:** Always use .dockerignore to exclude node_modules and build artifacts!