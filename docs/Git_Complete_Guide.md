# 📚 Git Mastery — The Ultimate Version Control Guide (2026)
> **Level:** Expert | **Language:** Hinglish | **Goal:** Master Git Internals, Advanced Workflows, and Recovery Strategies.

---

## 🧭 Core Concepts (Expert-First)

2026 mein Git sirf code save karne ke liye nahi hai, ye **Collaboration Engine** hai.

- **The Three Stages:** Working Directory, Staging Area, and Local Repo.
- **Branching Strategies:** Git Flow vs GitHub Flow vs Trunk-based development.
- **Advanced Operations:** Rebase, Cherry-pick, and Interactive Rebase.
- **Git LFS (Large File Storage):** Managing AI models and datasets.
- **Recovery Mastery:** `git reflog`—how to never lose a commit.

---

## 🏗️ 1. The Architecture of Git

Git data ko "Snapshots" ki tarah store karta hai, diffs ki tarah nahi.
- **BLOB:** File content.
- **TREE:** Directory structure.
- **COMMIT:** Snapshot of the tree with metadata.

---

## 🌿 2. Branching & Merging (Professional)

### A. Merge vs Rebase
- **Merge:** Branch ki history preserve karta hai (Extra merge commit banta hai).
- **Rebase:** History ko linear banata hai (Cleaner, but "Re-writes history"—don't use on public branches).

### B. Interactive Rebase (`git rebase -i`)
Apne pichle commits ko "Squash" (combine), "Reword" (message change), ya "Drop" (delete) karna.

```bash
# Combine last 3 commits into one
git rebase -i HEAD~3
```

---

## 🚀 3. Advanced Tools: Stash, Cherry-pick, and Hooks

### A. Stash
Jab aap beech kaam mein branch switch karna chahte ho:
```bash
git stash       # Save current work
git stash pop   # Bring it back later
```

### B. Cherry-pick
Ek specific commit ko doosri branch se uthakar apni branch par lana.
```bash
git cherry-pick <commit-hash>
```

### C. Git Hooks
Automation before commit.
- `pre-commit`: Model linting aur unit tests auto-run karna.

---

## 🐘 4. Git LFS: Large File Storage

AI models (100MB+) standard Git mein slow hote hain.
- **Logic:** Actual file S3/Cloud par rehti hai, Git mein sirf "Pointer" file hoti hai.
- **Setup:** `git lfs install` -> `git lfs track "*.safetensors"`

---

## 🚑 5. Fixing Mistakes (The Life Savers)

1. **`git commit --amend`:** Pichle commit ka message ya files update karna.
2. **`git reset --soft`:** Commit hatana lekin code change rehne dena.
3. **`git reset --hard`:** Sab kuch delete karke pichle commit par wapas jana.
4. **`git reflog`:** Git ki poori history (even deleted branches) dekhna. **Mastery tip:** Jab tak aapka code commit ho chuka hai, `reflog` use use wapas la sakta hai.

---

## 📝 2026 Interview Scenarios (Git)

### Q1: "Merge Conflict kaise resolve karein?"
**Ans:** Merge conflict tab hota hai jab do branches mein same line modify ho. Hum manual collision resolve karke `git add` aur `git commit` karte hain. Pro tip: Always `rebase main` before merging to catch conflicts early.

### Q2: "Forking vs Branching?"
**Ans:** 
- **Branching:** Same repository ke andar alag paths.
- **Forking:** Repository ki complete copy apne account mein banana (Standard for Open Source).

---

## 🏆 Project Integration: SusaGPT Workflow
Aapke repository mein:
- [x] Use `Feature Branch` workflow for every new task.
- [x] Use `Git LFS` for any model checkpoints.
- [x] Regular `git tag` for version releases (v1.0, v1.1).

> **Final Insight:** Git is a time machine. If you know how to navigate its history, you can never fail. Master the `reflog`, and you become fearless.