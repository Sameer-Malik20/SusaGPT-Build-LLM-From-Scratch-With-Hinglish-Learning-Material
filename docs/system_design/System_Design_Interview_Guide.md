# 🔍 System Design Interview Guide
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master system design interviews

---

## 🧭 Core Concepts (Concept-First)

- Scalability
- Load Balancing
- Caching
- Databases
- Design Patterns

---

## 1. 🎯 Design Twitter

```python
# Requirements
# - Post tweets
# - Timeline
# - Follow system

# Architecture
# - Write path: API -> Message Queue -> Fan-out Service -> DB
# - Read path: Cache -> Timeline Cache
# - Follows stored in separate service
```

---

## 2. 📱 Design WhatsApp

```python
# Requirements
# - 1-on-1 messaging
# - Groups
# - Online status

# Architecture
# - WebSocket for real-time
# - Message store
# - Presence service
# - Media storage
```

---

## 🧪 Common Questions

- Design YouTube
- Design Uber
- Design Netflix
- Design URL Shortener

---

## ✅ Checklist

- [ ] Requirements analyze kar sakte ho
- [ ] High-level design ban sakte ho
- [ ] Bottlenecks identify kar sakte ho