# 🗄️ Fullstack Database Patterns - Complete Guide

> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master database integration with ORMs, migrations, and patterns for fullstack applications.

---

## 🧭 Core Concepts (Concept-First)

- ORM Fundamentals: Prisma, Drizzle, Sequelize
- Schema Design: Migrations, relations, indexes
- Query Optimization: N+1 prevention, pagination
- Real-time Data: WebSockets, subscriptions
- Vector Databases: AI embeddings, similarity search

---

## 📋 Complete Guide

### 1️⃣ Prisma - Modern ORM

**Setup:**
```bash
npm install prisma --save-dev
npx prisma init
```

**Schema:**
```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(uuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]
  createdAt DateTime @default(now())
}

model Tag {
  id    String @id @default(uuid())
  name  String @unique
  posts Post[]
}
```

**Basic Operations:**
```typescript
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

// Create
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
    posts: {
      create: {
        title: 'Hello World',
        content: 'My first post'
      }
    }
  }
})

// Read with relations
const users = await prisma.user.findMany({
  include: {
    posts: {
      where: { published: true }
    }
  }
})

// Update
const updated = await prisma.user.update({
  where: { id: userId },
  data: { name: 'New Name' }
})

// Delete
await prisma.post.delete({
  where: { id: postId }
})
```

### 2️⃣ Drizzle - Lightweight ORM

**Setup:**
```bash
npm install drizzle-orm postgres
npm install drizzle-kit --save-dev
```

**Schema:**
```typescript
import { pgTable, text, timestamp, uuid, boolean } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow()
})

export const posts = pgTable('posts', {
  id: uuid('id').defaultRandom().primaryKey(),
  title: text('title').notNull(),
  content: text('content'),
  published: boolean('published').default(false),
  authorId: uuid('author_id').references(() => users.id)
})
```

**Queries:**
```typescript
import { eq, desc } from 'drizzle-orm'

// Select
const allUsers = await db.select().from(users)

// Insert
await db.insert(users).values({
  email: 'bob@example.com',
  name: 'Bob'
})

// Update
await db.update(users)
  .set({ name: 'Updated Name' })
  .where(eq(users.id, userId))

// Delete
await db.delete(users).where(eq(users.id, userId))
```

### 3️⃣ Migrations

**Prisma Migrations:**
```bash
# Create migration
npx prisma migrate dev --name init

# Apply migration
npx prisma migrate deploy

# Reset database
npx prisma migrate reset

# Generate after schema change
npx prisma generate
```

**Drizzle Migrations:**
```bash
# Push changes
npx drizzle-kit push:pg

# Create migration
npx drizzle-kit migrate

# Pull from database
npx drizzle-kit introspect:pg
```

### 4️⃣ Query Optimization

**N+1 Problem:**
```typescript
// Bad - N+1 queries
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({
    where: { authorId: user.id }
  })
}

// Good - Single query with include
const users = await prisma.user.findMany({
  include: {
    posts: true
  }
})

// Good - Select specific fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    posts: {
      select: {
        title: true
      }
    }
  }
})
```

**Pagination:**
```typescript
// Offset-based
const page = 1
const limit = 10
const posts = await prisma.post.findMany({
  skip: (page - 1) * limit,
  take: limit,
  orderBy: { createdAt: 'desc' }
})

// Cursor-based (better for large datasets)
const cursor = lastPostId
const posts = await prisma.post.findMany({
  take: 10,
  skip: cursor ? 1 : 0,
  cursor: cursor ? { id: cursor } : undefined,
  orderBy: { createdAt: 'desc' }
})
```

### 5️⃣ Real-time with Database

**PostgreSQL LISTEN/NOTIFY:**
```typescript
// Server - Emit notification
await prisma.$executeRaw`
  NOTIFY new_post, '${JSON.stringify(post)}'
`

// Server - Listen
prisma.$on('query', e => {
  console.log(e.query)
})

// With pg
import { Client } from 'pg'
const client = new Client()
await client.connect()
await client.query('LISTEN new_post')

client.on('notification', (msg) => {
  console.log('New post:', msg.payload)
})
```

### 6️⃣ Vector Databases for AI

**Pgvector Setup:**
```prisma
model Document {
  id        String   @id @default(uuid())
  content   String
  embedding Unsupported("vector(1536)")
  createdAt DateTime @default(now())
}
```

**Similarity Search:**
```typescript
import { sql } from 'drizzle-orm'

// Find similar documents
const similarDocs = await db.select()
  .from(documents)
  .orderBy(sql`embedding <=> ${queryEmbedding}::vector`)
  .limit(5)
```

---

## 🎯 Best Practices Checklist

- [ ] Use proper indexes for query optimization
- [ ] Implement connection pooling
- [ ] Use pagination for large datasets
- [ ] Handle migrations properly
- [ ] Use proper error handling
- [ ] Implement soft deletes where needed

---

## 🔗 Related Resources

- [Prisma Documentation](https://www.prisma.io/docs)
- [Drizzle ORM](https://orm.drizzle.team)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

> 💡 **Tip:** Drizzle Prisma se lightweight hai aur TypeScript ke saath behtar kaam karta hai!