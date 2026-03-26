# 📚 Git Complete Guide
> **Level:** Beginner → Intermediate | **Language:** Hinglish | **Goal:** Master Git version control

---

## 🧭 Core Concepts (Concept-First)

- Basic commands
- Branching & merging
- Remote workflows
- GitHub/GitLab

---

## 1. 🔰 Basic Commands

```bash
# Initialize repository
git init

# Clone repository
git clone <url>

# Add files
git add .
git add filename

# Commit
git commit -m "message"

# Check status
git status

# View history
git log
git log --oneline
```

---

## 2. 🌿 Branching

```bash
# Create branch
git branch feature-name

# Switch branch
git checkout feature-name
# or
git switch feature-name

# Create and switch
git checkout -b feature-name

# Delete branch
git branch -d feature-name
```

---

## 3. 🔀 Merging

```bash
# Merge branch
git merge feature-name

# Rebase
git rebase main

# Resolve conflicts
# Edit files, then:
git add .
git commit
```

---

## 4. ☁️ Remote Operations

```bash
# Add remote
git remote add origin <url>

# Push
git push origin main

# Pull
git pull origin main

# Fetch
git fetch origin
```

---

## ✅ Checklist

- [ ] Basic commands use kar sakte ho
- [ ] Branching manage kar sakte ho
- [ ] Merge aur rebase kar sakte ho
- [ ] Remote operations kar sakte ho