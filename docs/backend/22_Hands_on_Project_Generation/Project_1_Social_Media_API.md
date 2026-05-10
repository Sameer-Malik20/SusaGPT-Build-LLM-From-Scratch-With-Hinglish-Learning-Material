# 📱 Project 1: Advanced Social Media API
> **Objective:** Build a scalable, production-grade API for a Twitter/Threads clone | **Type:** Hands-on Project | **Standard:** 2026 Expert Framework

---

## 🧭 1. Project Vision
Is project mein hum sirf CRUD nahi banayenge. Hum handle karenge **Relationships**, **Feed Generation**, aur **Real-time Notifications**. Aap seekhenge ki kaise millions of posts aur followers ko efficiently manage kiya jata hai.

---

## 🛠️ 2. Tech Stack
- **Runtime:** Node.js (v20+)
- **Language:** TypeScript
- **Framework:** Express.js
- **Database:** PostgreSQL (with Prisma ORM)
- **Caching:** Redis (for session and feed)
- **Media:** Cloudinary (for image uploads)
- **Testing:** Jest + Supertest

---

## 🏗️ 3. Core Features & Requirements
### Phase 1: Auth & User Profile
- JWT-based Auth with Refresh Tokens.
- Profile management (Bio, Avatar, Cover Photo).
- Follow/Unfollow system (Self-referencing relationship).

### Phase 2: Post Management
- Create, Read, Update, Delete posts.
- Like/Unlike logic.
- Nested comments (Threaded conversations).

### Phase 3: The Feed (The Real Challenge)
- **Home Feed:** Show posts from people you follow (Optimized with Redis).
- **Infinite Scroll:** Pagination using `cursor-based` strategy.

### Phase 4: Real-time
- Notifications (X liked your post) via WebSockets (Socket.io).

---

## 📐 4. Database Schema (Prisma)
```prisma
model User {
  id        String   @id @default(uuid())
  username  String   @unique
  posts     Post[]
  followedBy User[]  @relation("UserFollows")
  following  User[]  @relation("UserFollows")
}

model Post {
  id        String   @id @default(uuid())
  content   String
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  likes     Like[]
}
```

---

## 💻 5. Implementation Roadmap
### Step 1: Initialize Project
```bash
npm init -y
npm install typescript ts-node express prisma @prisma/client
npx tsc --init
npx prisma init
```

### Step 2: Build the 'Follow' Logic
Ensure you prevent a user from following themselves and handle the "Mutual Follow" scenario.

### Step 3: Implement Feed Caching
When a user posts, push the post ID into the Redis lists of all their followers (Fan-out on write).

---

## ❌ 6. Failure Analysis (Common Pitfalls)
- **N+1 Query:** Fetching 10 posts and then running 10 separate queries to get the author's name. **Fix: Use Prisma's `include` or `select`.**
- **Circular Dependency:** Follower following followee.
- **Image Size:** Users uploading 10MB 4K photos. **Fix: Use Multer + Cloudinary transformation to resize to 800px on upload.**

---

## ✅ 7. Definition of Done
- All routes are protected by Auth middleware.
- API is documented using Swagger.
- 80%+ Test coverage for business logic.
- Environment variables are managed via `.env`.

---

## 📝 8. Interview Talking Points
- "How did you scale the home feed for a user following 5,000 people?"
- "Explain your strategy for handling image uploads without blocking the main thread."
- "Why did you choose PostgreSQL over MongoDB for a social app?"
漫
