# 🔗 tRPC Complete Guide
> **Level:** Intermediate | **Language:** Hinglish | **Goal:** Master type-safe APIs

---

## 🧭 Core Concepts (Concept-First)

- Type-safe APIs without boilerplate
- Server and client integration
- Next.js integration

---

## 1. 🚀 Setup

```typescript
// Server setup (server.ts)
import { initTRPC } from '@trpc/server';

const t = initTRPC.create();

export const router = t.router;
export const publicProcedure = t.procedure;

// Define router
export const appRouter = router({
  getUser: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(({ input }) => {
      return db.user.findUnique({ where: { id: input.id } });
    }),
  createUser: publicProcedure
    .input(z.object({ name: z.string(), email: z.string() }))
    .mutation(({ input }) => {
      return db.user.create({ data: input });
    }),
});

export type AppRouter = typeof appRouter;
```

---

## 2. 🎯 Client Usage

```typescript
// Client (Next.js)
import { createTRPCNext } from '@trpc/next';
import type { AppRouter } from '../server';

export const trpc = createTRPCNext<AppRouter>({
  config() {
    return {
      url: '/api/trpc',
    };
  },
});

// Use in component
import { trpc } from '../utils/trpc';

function UserList() {
  const { data, isLoading } = trpc.getUser.useQuery({ id: '1' });
  
  if (isLoading) return <div>Loading...</div>;
  return <div>{data?.name}</div>;
}
```

---

## ✅ Checklist

- [ ] tRPC setup kar sakte ho
- [ ] Type-safe API create kar sakte ho
- [ ] Client use kar sakte ho