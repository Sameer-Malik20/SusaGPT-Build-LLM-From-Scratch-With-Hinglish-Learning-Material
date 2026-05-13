# SQL and PostgreSQL: Complete Guide for Fullstack Engineers

## Hinglish Explanation (Beginner Level)

Bhai, let me tell you SQL aur PostgreSQL kya hota hai simple words mein:

**SQL (Structured Query Language)** - Ye ek language hai jisme hum database se baat karte hain. Jaise Hindi bolne ke liye Hindi zaroori hai, database se baat karne ke liye SQL zaroori hai. CRUD operations (Create, Read, Update, Delete) sab ismein hote hain.

**PostgreSQL** - Ye ek database management system (DBMS) hai jo SQL ko support karta hai. Imagine karo ek bada filing cabinet hai jisme tum records store karte ho. PostgreSQL wo cabinet ka organizer hai jo sabkuch systematic rakhta hai.

Yeh combination ek powerful duo hai - SQL wo rulebook hai aur PostgreSQL implementation. Modern web apps jaise Instagram, Spotify, Netflix PostgreSQL use karte hain.

```sql
-- Basic SQL commands jo har developer ko aani chahiye
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data insert karna
INSERT INTO users (name, email) VALUES ('Rahul', 'rahul@example.com');

-- Data read karna
SELECT * FROM users WHERE name = 'Rahul';

-- Data update karna
UPDATE users SET email = 'newemail@example.com' WHERE id = 1;

-- Data delete karna
DELETE FROM users WHERE id = 1;
```

## Deep Technical Explanation

PostgreSQL ek open-source, object-relational database management system (ORDBMS) hai jo ACID compliance, MVCC (Multi-Version Concurrency Control), dan complex data types support karta hai.

### PostgreSQL Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Instance                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Client    │  │   Client    │  │   Client (psql)     │  │
│  │  (Node.js)  │  │  (Python)   │  │   (CLI)             │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │            │
│         └────────────────┼─────────────────────┘            │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │    PostgreSQL Server  │                       │
│              │    (Postmaster)       │                       │
│              │    Port: 5432         │                       │
│              └───────────┬───────────┘                       │
│                          ▼                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Shared Buffers                      │  │
│  │    (Memory pool for table/index data - typically      │  │
│  │     25% of available RAM)                             │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│    ┌─────────────────────┼─────────────────────┐            │
│    ▼                     ▼                     ▼            │
│ ┌──────────┐      ┌──────────┐         ┌──────────┐       │
│ │ WAL Files │      │  System  │         │   Temp   │       │
│ │(Write-Ahead│    │ Catalogs │         │   Files  │       │
│ │ Logging)  │      │ (pg_*)   │         │          │       │
│ └──────────┘      └──────────┘         └──────────┘       │
│                          │                                   │
│    ┌─────────────────────┼─────────────────────┐            │
│    ▼                     ▼                     ▼            │
│ ┌────────┐         ┌────────┐           ┌────────┐        │
│ │ tables │         │ indexes │           │ views  │        │
│ │  .dat  │         │  .index │           │        │        │
│ └────────┘         └────────┘           └────────┘        │
│                          │                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Data Directory                      │  │
│  │    /var/lib/postgresql/data (Linux)                   │  │
│  │    C:\Program Files\PostgreSQL\data (Windows)         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### MVCC (Multi-Version Concurrency Control)

PostgreSQL readers ko writers ko block nahi karta - yeh MVCC se possible hota hai:

```
Transaction A (Read)                    Transaction B (Write)
      │                                        │
      │  BEGIN;                                │  BEGIN;
      │  SELECT * FROM users                  │  UPDATE users SET...
      │       │                               │       │
      │       ▼                               │       ▼
      │  ┌─────────────────────────────────┐   │
      │  │ Visibility Check:               │   │  New row version created
      │  │ - xmin < snapshot.xmin?         │   │  with xmax = Transaction B
      │  │ - xmax != committed?            │   │
      │  │ - Not in updating transaction?   │   │
      │  └─────────────────────────────────┘   │
      │       │                               │
      │  Sees OLD data (consistent)            │  COMMIT;
      │       │                               │
      │  COMMIT;                               │
```

### Advanced PostgreSQL Features

```sql
-- Window Functions
SELECT 
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;

-- Common Table Expression (CTE) with Recursion
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e
    INNER JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree;

-- JSON/JSONB Operations (PostgreSQL-specific)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_data JSONB
);

INSERT INTO events (event_data) VALUES 
    ('{"type": "click", "user_id": 123, "metadata": {"page": "/home"}}');

-- Query JSONB efficiently
SELECT * FROM events 
WHERE event_data @> '{"type": "click"}'
AND event_data -> 'metadata' ->> 'page' = '/home';

-- Full-Text Search
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR;
UPDATE articles SET search_vector = to_tsvector('english', title || ' ' || content);

SELECT title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql & tutorial')
WHERE search_vector @@ query
ORDER BY rank DESC;
```

## Architecture Diagram: Fullstack Integration

```
┌────────────────────────────────────────────────────────────────────┐
│                        Frontend (React/Next.js)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ React Query  │  │ Apollo Client│  │    Form Components       │ │
│  │ (TanStack)   │  │ (GraphQL)    │  │ (Zod + React Hook Form)  │ │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘ │
└─────────┼─────────────────┼───────────────────────┼───────────────┘
          │                 │                       │
          ▼                 ▼                       ▼
┌────────────────────────────────────────────────────────────────────┐
│                     API Layer (Node.js/Express)                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      Route Handlers                            │  │
│  │  POST /api/users    GET /api/users    PUT /api/users/:id      │  │
│  └─────────────────────────┬────────────────────────────────────┘  │
│                            │                                         │
│  ┌─────────────────────────▼────────────────────────────────────┐  │
│  │                  Business Logic Layer                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │  │
│  │  │ Validation  │  │ Auth Checks │  │ Rate Limiting       │   │  │
│  │  │ (Zod/Joi)   │  │ (JWT/Perm)  │  │ (express-rate-limit)│   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘   │  │
│  └─────────────────────────┬────────────────────────────────────┘  │
└────────────────────────────┼───────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                   ORM / Database Driver Layer                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │ Prisma           │  │ Drizzle ORM      │  │ TypeORM          │  │
│  │ - Schema-first   │  │ - Type-safe SQL  │  │ - Active Record │  │
│  │ - Migration CLI  │  │ - Lightweight    │  │ - migrations     │  │
│  │ - Type inference │  │ - Edge ready    │  │                 │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  │
└───────────┼──────────────────────┼─────────────────────┼────────────┘
            │                      │                     │
            ▼                      ▼                     ▼
┌────────────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │  │
│  │  │ Connection│  │ Query   │  │Storage  │  │ Replication     │ │  │
│  │  │ Pooler   │  │ Engine  │  │ Engine  │  │ Manager         │ │  │
│  │  │ (PgBouncer│  │         │  │         │  │ (Streaming Rep) │ │  │
│  │  │  /PgPool)│  │         │  │         │  │                 │ │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Frontend + Backend Integration Examples

### Backend Setup with Prisma (Node.js)

```typescript
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@index([published])
}

// Database service layer
// src/services/database.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

// src/services/user.service.ts
export class UserService {
  async createUser(data: { email: string; name?: string }) {
    return prisma.user.create({
      data,
      select: { id: true, email: true, name: true, createdAt: true },
    });
  }

  async getUserByEmail(email: string) {
    return prisma.user.findUnique({
      where: { email },
      include: {
        posts: {
          where: { published: true },
          select: { id: true, title: true },
        },
      },
    });
  }

  async getUsersWithPagination(page: number, limit: number) {
    const skip = (page - 1) * limit;
    
    const [users, total] = await Promise.all([
      prisma.user.findMany({
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      prisma.user.count(),
    ]);

    return {
      users,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };
  }

  async updateUser(id: number, data: Partial<{ email: string; name: string }>) {
    return prisma.user.update({
      where: { id },
      data,
    });
  }

  async deleteUser(id: number) {
    return prisma.user.delete({
      where: { id },
    });
  }

  async searchUsers(query: string) {
    return prisma.user.findMany({
      where: {
        OR: [
          { name: { contains: query, mode: 'insensitive' } },
          { email: { contains: query, mode: 'insensitive' } },
        ],
      },
    });
  }
}

export const userService = new UserService();
```

### API Routes (Express)

```typescript
// src/routes/user.routes.ts
import { Router } from 'express';
import { userService } from '../services/user.service';
import { z } from 'zod';

const router = Router();

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).optional(),
});

const updateUserSchema = z.object({
  email: z.string().email().optional(),
  name: z.string().min(1).optional(),
});

// POST /api/users - Create user
router.post('/', async (req, res) => {
  try {
    const data = createUserSchema.parse(req.body);
    const user = await userService.createUser(data);
    res.status(201).json({ success: true, data: user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, errors: error.errors });
    } else {
      console.error('Create user error:', error);
      res.status(500).json({ success: false, message: 'Internal server error' });
    }
  }
});

// GET /api/users - List users with pagination
router.get('/', async (req, res) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const limit = Math.min(parseInt(req.query.limit as string) || 10, 100);
    
    const result = await userService.getUsersWithPagination(page, limit);
    res.json({ success: true, ...result });
  } catch (error) {
    console.error('List users error:', error);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

// GET /api/users/:email - Get user by email
router.get('/:email', async (req, res) => {
  try {
    const user = await userService.getUserByEmail(req.params.email);
    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }
    res.json({ success: true, data: user });
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

// PUT /api/users/:id - Update user
router.put('/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const data = updateUserSchema.parse(req.body);
    const user = await userService.updateUser(id, data);
    res.json({ success: true, data: user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, errors: error.errors });
    } else {
      console.error('Update user error:', error);
      res.status(500).json({ success: false, message: 'Internal server error' });
    }
  }
});

// DELETE /api/users/:id - Delete user
router.delete('/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    await userService.deleteUser(id);
    res.status(204).send();
  } catch (error) {
    console.error('Delete user error:', error);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

export default router;
```

### Frontend Integration (React + React Query)

```typescript
// src/api/users.ts
import { apiClient } from './client';

export interface User {
  id: number;
  email: string;
  name: string | null;
  createdAt: string;
}

export interface CreateUserInput {
  email: string;
  name?: string;
}

export interface UpdateUserInput {
  email?: string;
  name?: string;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export const userApi = {
  create: async (data: CreateUserInput): Promise<User> => {
    const response = await apiClient.post<User>('/api/users', data);
    return response.data;
  },

  list: async (page: number = 1, limit: number = 10): Promise<PaginatedResponse<User>> => {
    const response = await apiClient.get<PaginatedResponse<User>>('/api/users', {
      params: { page, limit },
    });
    return response.data;
  },

  getByEmail: async (email: string): Promise<User> => {
    const response = await apiClient.get<User>(`/api/users/${encodeURIComponent(email)}`);
    return response.data;
  },

  update: async (id: number, data: UpdateUserInput): Promise<User> => {
    const response = await apiClient.put<User>(`/api/users/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/users/${id}`);
  },
};

// src/hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi, CreateUserInput, UpdateUserInput } from '../api/users';

export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (page: number, limit: number) => [...userKeys.lists(), { page, limit }] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (email: string) => [...userKeys.details(), email] as const,
};

export function useUsers(page: number = 1, limit: number = 10) {
  return useQuery({
    queryKey: userKeys.list(page, limit),
    queryFn: () => userApi.list(page, limit),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useUser(email: string) {
  return useQuery({
    queryKey: userKeys.detail(email),
    queryFn: () => userApi.getByEmail(email),
    enabled: !!email,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserInput) => userApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateUserInput }) =>
      userApi.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      queryClient.invalidateQueries({ queryKey: userKeys.details() });
    },
  });
}

export function useDeleteUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => userApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

// src/components/UserList.tsx
import { useState } from 'react';
import { useUsers, useDeleteUser } from '../hooks/useUsers';

export function UserList() {
  const [page, setPage] = useState(1);
  const { data, isLoading, isError, error } = useUsers(page, 10);
  const deleteUser = useDeleteUser();

  if (isLoading) return <div>Loading users...</div>;
  if (isError) return <div>Error: {(error as Error).message}</div>;

  return (
    <div>
      <h2>Users ({data?.pagination.total})</h2>
      
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Name</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data?.data.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.email}</td>
              <td>{user.name || '-'}</td>
              <td>{new Date(user.createdAt).toLocaleDateString()}</td>
              <td>
                <button
                  onClick={() => deleteUser.mutate(user.id)}
                  disabled={deleteUser.isPending}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div>
        <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>
          Previous
        </button>
        <span>Page {page} of {data?.pagination.totalPages}</span>
        <button 
          disabled={page === data?.pagination.totalPages} 
          onClick={() => setPage(p => p + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

## Real-World Production Examples

### Example 1: E-commerce Order Processing System

```sql
-- Production schema for e-commerce
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(500) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    category_id UUID REFERENCES categories(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    status VARCHAR(50) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    shipping_address JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Critical indexes for production
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id) WHERE is_active = true;
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Partial index for pending orders
CREATE INDEX idx_orders_pending ON orders(created_at DESC) 
WHERE status = 'pending';

-- Covering index for common query
CREATE INDEX idx_products_search ON products(category_id, is_active) 
INCLUDE (id, name, price);
```

```typescript
// Order processing with transaction
async function createOrder(
  customerId: string,
  items: Array<{ productId: string; quantity: number }>,
  shippingAddress: Address
) {
  return prisma.$transaction(async (tx) => {
    // 1. Validate customer exists
    const customer = await tx.customer.findUnique({
      where: { id: customerId },
    });
    
    if (!customer) {
      throw new Error('Customer not found');
    }

    // 2. Validate and lock products (FOR UPDATE prevents overselling)
    const productIds = items.map(i => i.productId);
    const products = await tx.product.findMany({
      where: { id: { in: productIds } },
    });

    if (products.length !== productIds.length) {
      throw new Error('Some products not found');
    }

    // Check stock availability
    for (const item of items) {
      const product = products.find(p => p.id === item.productId)!;
      if (product.stockQuantity < item.quantity) {
        throw new Error(`Insufficient stock for ${product.name}`);
      }
    }

    // 3. Calculate total
    let totalAmount = 0;
    for (const item of items) {
      const product = products.find(p => p.id === item.productId)!;
      totalAmount += product.price * item.quantity;
    }

    // 4. Create order
    const order = await tx.order.create({
      data: {
        customerId,
        status: 'pending',
        totalAmount,
        shippingAddress: shippingAddress as any,
        items: {
          create: items.map(item => {
            const product = products.find(p => p.id === item.productId)!;
            return {
              productId: item.productId,
              quantity: item.quantity,
              unitPrice: product.price,
            };
          }),
        },
      },
    });

    // 5. Deduct stock
    for (const item of items) {
      await tx.product.update({
        where: { id: item.productId },
        data: {
          stockQuantity: {
            decrement: item.quantity,
          },
        },
      });
    }

    return order;
  }, {
    isolationLevel: 'Serializable', // Highest isolation for financial transactions
    timeout: 30000,
  });
}
```

### Example 2: Real-time Analytics Dashboard

```sql
-- Analytics event tracking schema
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    user_id UUID,
    session_id VARCHAR(255) NOT NULL,
    device_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Partitioning by month for better performance
CREATE TABLE analytics_events_partitioned (
    LIKE analytics_events INCLUDING ALL
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE analytics_events_2026_01 
    PARTITION OF analytics_events_partitioned
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

-- Hyper table for TimescaleDB (time-series optimization)
CREATE TABLE metrics (
    time        TIMESTAMPTZ NOT NULL,
    metric_name TEXT NOT NULL,
    value       DOUBLE PRECISION,
    tags        JSONB
);

SELECT create_hypertable('metrics', 'time');

-- Materialized view for pre-aggregated reports
CREATE MATERIALIZED VIEW hourly_metrics AS
SELECT 
    time_bucket('1 hour', created_at) AS hour,
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM analytics_events
GROUP BY 1, 2;

CREATE UNIQUE INDEX ON hourly_metrics(hour, event_type);

-- Refresh materialized view periodically
CREATE OR REPLACE FUNCTION refresh_hourly_metrics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY hourly_metrics;
END;
$$ LANGUAGE plpgsql;
```

## Failure Cases

### Case 1: Deadlock in Concurrent Updates

**Problem**: Two transactions waiting for each other to release locks.

```sql
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Locks row 1
-- Session 2
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 2;  -- Locks row 2
-- Session 1
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Waits for row 2
-- Session 2
UPDATE accounts SET balance = balance + 100 WHERE id = 1;  -- DEADLOCK!
```

**Solution**:
```sql
-- Always update in consistent order
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Use advisory locks for complex operations
SELECT pg_advisory_xact_lock(12345);  -- Lock with transaction scope
```

### Case 2: Connection Pool Exhaustion

**Problem**: Too many connections cause "too many connections" error.

```typescript
// BAD: Creating new Prisma instance per request
export async function handler(req, res) {
  const prisma = new PrismaClient();  // Creates new connection!
  const users = await prisma.user.findMany();
  await prisma.$disconnect();
}

// GOOD: Reuse global instance
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL + '?connection_limit=5&pool_timeout=10',
    },
  },
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

### Case 3: N+1 Query Problem

**Problem**: Loading related data causes excessive queries.

```sql
-- BAD: 1 query for posts + N queries for each author's profile
-- SELECT * FROM posts LIMIT 100;
-- SELECT * FROM users WHERE id = 1;
-- SELECT * FROM users WHERE id = 2;
-- ... 99 more queries!
```

```typescript
// GOOD: Use include or select for eager loading
const posts = await prisma.post.findMany({
  take: 100,
  include: {
    author: {
      select: { id: true, name: true, avatar: true },
    },
    comments: {
      include: {
        author: { select: { name: true } },
      },
    },
  },
});
// This executes only 1 query with JOINs!
```

## Debugging Guide

### Using EXPLAIN ANALYZE

```sql
-- Analyze query execution plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT 
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.customer_id
WHERE u.created_at > '2025-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC
LIMIT 20;

-- Output example:
-- Hash Join  (cost=1000.00..5000.00 rows=500 width=100)
--              (actual time=10.5..150.3 rows=50 loops=1)
--   Buffers: shared hit=200 read=150
--   ->  Seq Scan on users  (cost=0..1000.00 rows=50000 width=50)
--         Filter: (created_at > '2025-01-01')
--         Rows Removed by Filter: 45000
```

### Key Metrics to Watch

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Connection Usage | < 50% | 50-80% | > 80% |
| Query Duration (p95) | < 100ms | 100-500ms | > 500ms |
| Cache Hit Ratio | > 95% | 80-95% | < 80% |
| Lock Wait Time | < 10ms | 10-100ms | > 100ms |
| Replication Lag | < 1s | 1-10s | > 10s |

### PostgreSQL System Views

```sql
-- Current running queries
SELECT 
    pid,
    usename,
    application_name,
    state,
    query,
    query_start,
    NOW() - query_start as duration
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Long-running queries
SELECT 
    pid,
    now() - query_start AS duration,
    state,
    query
FROM pg_stat_activity
WHERE (now() - query_start) > interval '5 minutes'
AND state = 'active';

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Table bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Kill long-running query
SELECT pg_cancel_backend(pid);  -- Graceful
SELECT pg_terminate_backend(pid);  -- Forceful
```

## Tradeoffs

### PostgreSQL vs MongoDB

| Aspect | PostgreSQL | MongoDB |
|--------|------------|---------|
| Data Model | Relational | Document |
| Schema | Fixed | Flexible |
| Transactions | ACID (always) | ACID (multi-doc, since v4) |
| Joins | Native | Manual/lookup |
| Scaling | Vertical | Horizontal (sharding) |
| Best For | Financial, transactional | Content, logs, catalogs |

### When to Use PostgreSQL

1. **Financial transactions** - Money transfers need ACID guarantees
2. **Complex relationships** - Users -> Orders -> Products -> Categories
3. **Data integrity** - Foreign keys prevent orphan records
4. **Reporting** - Aggregations, window functions, CTEs
5. **Geospatial** - PostGIS extension for GIS data

### When to Use MongoDB

1. **Rapid prototyping** - Schema changes without migrations
2. **Hierarchical data** - Comments nested in posts
3. **Large documents** - Single document > 16MB
4. **Flexible schemas** - Different fields per record

## Security Concerns

### SQL Injection Prevention

```typescript
// BAD: Never interpolate user input directly!
const query = `SELECT * FROM users WHERE email = '${req.body.email}'`;

// GOOD: Use parameterized queries
const result = await prisma.user.findUnique({
  where: { email: req.body.email },
});

// GOOD: If raw query needed, always use parameterized values
const result = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = ${email}
`;
```

### Row-Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Users can only see their own orders
CREATE POLICY user_orders ON orders
    FOR SELECT
    USING (customer_id = current_user_id());

-- Users can only update their own orders
CREATE POLICY user_orders_update ON orders
    FOR UPDATE
    USING (customer_id = current_user_id())
    WITH CHECK (customer_id = current_user_id());

-- Set current user context
SET app.current_user_id = 'user-uuid-here';
```

### Connection Security

```bash
# SSL mode configuration
DATABASE_URL="postgresql://user:pass@host:5432/db?sslmode=require"

# pg_hba.conf - Trust local, require cert for remote
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             0.0.0.0/0               scram-sha-256
hostssl all             all             0.0.0.0/0               verify-full
```

## Performance Optimization

### Indexing Strategies

```sql
-- Composite index (order matters!)
-- Query: WHERE status = 'active' AND created_at > '2025-01-01'
-- Best: (status, created_at) not (created_at, status)

CREATE INDEX idx_composite ON orders(status, created_at DESC);

-- Partial index - smaller, faster
CREATE INDEX idx_pending ON orders(created_at)
WHERE status = 'pending';

-- Expression index
CREATE INDEX idx_email_lower ON users(LOWER(email));

-- Covering index (INCLUDE avoids table access)
CREATE INDEX idx_covering ON orders(customer_id)
INCLUDE (status, total_amount, created_at);
```

### Query Optimization

```sql
-- Avoid SELECT * in production
-- BAD
SELECT * FROM orders WHERE id = 1;

-- GOOD
SELECT id, status, total_amount, created_at 
FROM orders WHERE id = 1;

-- Use EXISTS instead of IN for subqueries
-- BAD (loads all matching IDs into memory)
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);

-- GOOD (stops at first match)
SELECT * FROM users WHERE EXISTS (
    SELECT 1 FROM orders WHERE orders.user_id = users.id
);

-- Batch operations instead of individual updates
-- BAD
UPDATE products SET stock = stock - 1 WHERE id = 1;
UPDATE products SET stock = stock - 1 WHERE id = 2;

-- GOOD
UPDATE products AS p SET stock = p.stock - v.qty
FROM (VALUES (1, 1), (2, 1)) AS v(id, qty)
WHERE p.id = v.id;
```

### Connection Pool Configuration

```typescript
// Prisma connection pool
const connectionString = process.env.DATABASE_URL || '';
const url = new URL(connectionString);

// Recommended pool size: CPU cores * 2 + effective spindle count
const poolSize = process.env.NODE_ENV === 'production' 
    ? 20 
    : 5;

url.searchParams.set('connection_limit', String(poolSize));
url.searchParams.set('pool_timeout', '10');
url.searchParams.set('statement_timeout', '30000');

export const prisma = new PrismaClient({
  datasources: { db: { url: url.toString() } },
});
```

## Scaling Challenges

### Read Replicas

```
┌─────────────────────────────────────────────────────────────┐
│                        Application                           │
│                   (Connection Router)                        │
│              Route writes to primary, reads to replicas     │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│   Primary     │◄──────────│   Replica 1   │
│  (Writes)     │  Replicate│   (Reads)     │
│               │           │               │
│  10.0.0.1     │           │  10.0.0.2     │
└───────────────┘           └───────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │   Replica 2   │
                            │   (Reads)     │
                            │  10.0.0.3     │
                            └───────────────┘
```

```typescript
// Multi-database setup with Prisma
// prisma-primary.ts
export const primaryDb = new PrismaClient({
  datasources: { db: { url: process.env.DATABASE_PRIMARY_URL } },
});

// prisma-replica.ts
export const replicaDb = new PrismaClient({
  datasources: { db: { url: process.env.DATABASE_REPLICA_URL } },
});

// Auto-route based on operation type
export const db = {
  async create(data: any) {
    return primaryDb.user.create({ data });
  },
  
  async findMany(args?: any) {
    // Read operations go to replica
    return replicaDb.user.findMany(args);
  },
  
  async findUnique(args: any) {
    return replicaDb.user.findUnique(args);
  },
  
  async update(args: any) {
    return primaryDb.user.update(args);
  },
};
```

### Partitioning for Large Tables

```sql
-- Range partitioning by date
CREATE TABLE events (
    id BIGSERIAL,
    event_type VARCHAR(100),
    event_data JSONB,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Create partitions for each month
CREATE TABLE events_2026_q1 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

CREATE TABLE events_2026_q2 PARTITION OF events
    FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');

-- Automatic partition creation function
CREATE OR REPLACE FUNCTION create_monthly_partition()
RETURNS void AS $$
DECLARE
    start_date DATE;
    end_date DATE;
    partition_name TEXT;
BEGIN
    start_date := date_trunc('month', NOW())::date;
    end_date := (date_trunc('month', NOW()) + INTERVAL '1 month')::date;
    partition_name := 'events_' || to_char(start_date, 'YYYY_MM');
    
    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF events 
         FOR VALUES FROM (%L) TO (%L)',
        partition_name, start_date, end_date
    );
END;
$$ LANGUAGE plpgsql;
```

## Best Practices

### 1. Always Use Transactions for Related Operations

```typescript
async function transferFunds(fromId: string, toId: string, amount: number) {
  return prisma.$transaction(async (tx) => {
    const fromAccount = await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });
    
    if (fromAccount.balance < 0) {
      throw new Error('Insufficient funds');
    }
    
    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });
    
    await tx.transactionLog.create({
      data: { fromId, toId, amount, type: 'TRANSFER' },
    });
  });
}
```

### 2. Use Soft Deletes for Audit Trail

```typescript
// Add deletedAt field
model User {
  id        Int       @id @default(autoincrement())
  email     String    @unique
  deletedAt DateTime?  // Soft delete timestamp
  // ...
}

// Query only active records
prisma.user.findMany({
  where: { deletedAt: null },
});

// For critical data, use separate archive table
```

### 3. Validate at Database Level

```sql
-- Always use constraints
ALTER TABLE products ADD CONSTRAINT positive_price 
    CHECK (price >= 0);

ALTER TABLE order_items ADD CONSTRAINT positive_quantity 
    CHECK (quantity > 0);

-- Use enums for fixed values
CREATE TYPE order_status AS ENUM (
    'pending', 'confirmed', 'processing', 
    'shipped', 'delivered', 'cancelled'
);

ALTER TABLE orders ALTER COLUMN status TYPE order_status;
```

### 4. Regular Maintenance

```sql
-- Analyze tables (update statistics)
ANALYZE;

-- Vacuum to reclaim space and clean dead tuples
VACUUM (VERBOSE, ANALYZE) orders;

-- Reindex to improve performance
REINDEX TABLE CONCURRENTLY orders;

-- Check for bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    n_dead_tup,
    n_live_tup,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
```

## Common Mistakes

### Mistake 1: Not Using UUIDs for Distributed Systems

```sql
-- BAD: Serial IDs can have conflicts
CREATE TABLE users (id SERIAL PRIMARY KEY);

-- GOOD: UUIDs are globally unique
CREATE TABLE users (id UUID PRIMARY KEY DEFAULT gen_random_uuid());

-- In Prisma
model User {
  id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
}
```

### Mistake 2: Ignoring Timezone Handling

```sql
-- BAD: Store without timezone
created_at TIMESTAMP  -- No timezone info

-- GOOD: Always use TIMESTAMPTZ
created_at TIMESTAMPTZ DEFAULT NOW()  -- With timezone

-- In application code
const now = new Date(); // Already in UTC
await prisma.user.create({ data: { createdAt: now } });

// Always convert to UTC before storage
const utcDate = new Date().toISOString();
```

### Mistake 3: Not Setting Appropriate Timeouts

```typescript
// BAD: No timeout
const result = await prisma.$queryRaw`SELECT * FROM huge_table`;

// GOOD: Always set timeouts
await prisma.$queryRaw`SELECT * FROM huge_table`.catch(e => {
  if (e.code === '57014') {  // Query cancelled
    throw new Error('Query timeout');
  }
});

// Set statement_timeout in connection
url.searchParams.set('statement_timeout', '5000'); // 5 seconds
```

## Interview Questions

### Q1: Explain the difference between PRIMARY KEY and UNIQUE constraint

**Answer**: 
- PRIMARY KEY: One per table, auto-implies NOT NULL, creates clustered index
- UNIQUE: Multiple allowed, allows one NULL (or multiple NULLs in PostgreSQL), creates non-clustered index

### Q2: What is MVCC in PostgreSQL?

**Answer**: Multi-Version Concurrency Control allows concurrent transactions without blocking each other. Each transaction sees a consistent snapshot of the database at a point in time. Writers don't block readers and vice versa. Dead tuples are cleaned up by VACUUM.

### Q3: Explain ACID properties

**Answer**:
- **Atomicity**: All operations in a transaction succeed or all fail
- **Consistency**: Database moves from one valid state to another
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Committed data survives crashes

### Q4: What is a dead tuple?

**Answer**: When a row is updated or deleted, PostgreSQL marks the old version as dead. These occupy space until VACUUM cleans them up. Excessive dead tuples indicate need for VACUUM.

### Q5: How would you optimize a slow query?

**Answer**:
1. Use EXPLAIN ANALYZE to see execution plan
2. Check for missing indexes
3. Look for sequential scans on large tables
4. Verify statistics are up to date (ANALYZE)
5. Consider query rewrite
6. Check for proper index column order
7. Review connection pool settings

### Q6: What is the difference between DELETE, TRUNCATE, and DROP?

**Answer**:
- DELETE: Removes rows one by one, triggers triggers, can be rolled back, slow on large tables
- TRUNCATE: Removes all rows quickly, doesn't trigger triggers, resets sequences, cannot be rolled back in same way
- DROP: Removes entire table including structure, cannot be recovered

### Q7: Explain partial index and when to use it

**Answer**: A partial index includes only rows that satisfy a condition. Useful when queries consistently filter on a specific condition (e.g., active orders), making the index smaller and faster.

## Latest 2026 Fullstack Engineering Patterns

### Pattern 1: Edge Database with Global Distribution

```typescript
// Using Turso (LibSQL) or PlanetScale for edge deployment
import { createClient } from '@libsql/client';

const db = createClient({
  url: process.env.TURSO_DATABASE_URL,
  authToken: process.env.TURSO_AUTH_TOKEN,
});

// Serverless-compatible query
export async function getUser(id: string) {
  const result = await db.execute({
    sql: 'SELECT * FROM users WHERE id = ?',
    args: [id],
  });
  return result.rows[0];
}
```

### Pattern 2: Real-time Subscriptions with Prisma

```typescript
// Prisma Accelerate for global caching and real-time
import { PrismaClient } from '@prisma/client';
import { withAccelerate } from '@prisma/extension-accelerate';

const prisma = new PrismaClient().$extends(withAccelerate());

// Real-time subscription
export function subscribeToOrders(userId: string) {
  return prisma.order.findMany({
    where: { customerId: userId },
    cursor: { id: 'last_seen_id' },
    take: 10,
    // Accelerate handles caching and real-time updates
  });
}
```

### Pattern 3: Multi-tenant Database per Tenant

```typescript
// Per-tenant database for enterprise customers
class TenantDatabaseManager {
  private connections: Map<string, PrismaClient> = new Map();
  
  async getTenantDb(tenantId: string): Promise<PrismaClient> {
    if (this.connections.has(tenantId)) {
      return this.connections.get(tenantId)!;
    }
    
    const config = await this.getTenantConfig(tenantId);
    const db = new PrismaClient({
      datasources: {
        db: { url: config.databaseUrl },
      },
    });
    
    this.connections.set(tenantId, db);
    return db;
  }
  
  async createTenant(tenantId: string, plan: string) {
    // Provision new database
    const dbUrl = await provisionDatabase(tenantId, plan);
    await this.saveTenantConfig(tenantId, dbUrl);
  }
}
```

### Pattern 4: Event Sourcing with PostgreSQL

```sql
-- Event store table
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    metadata JSONB,
    version INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(aggregate_id, version)
);

-- Projections for read models
CREATE TABLE account_balances (
    account_id UUID PRIMARY KEY,
    balance DECIMAL(19, 4) DEFAULT 0,
    version INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Handle events
CREATE OR REPLACE FUNCTION handle_money_deposited()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE account_balances 
    SET balance = balance + (NEW.event_data->>'amount')::DECIMAL,
        version = version + 1,
        updated_at = NOW()
    WHERE account_id = NEW.aggregate_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Pattern 5: AI-Powered Query Optimization

```typescript
// Using AI to suggest indexes based on query patterns
import { Prisma } from '@prisma/client';

class QueryAnalyzer {
  async suggestIndexes(queries: string[]) {
    const response = await fetch('/api/ai/analyze-queries', {
      method: 'POST',
      body: JSON.stringify({ queries }),
    });
    
    const suggestions = await response.json();
    
    // Apply recommended indexes
    for (const suggestion of suggestions.indexes) {
      await prisma.$executeRaw`
        CREATE INDEX CONCURRENTLY IF NOT EXISTS ${Prisma.raw(suggestion.name)}
        ON ${Prisma.raw(suggestion.table)} (${Prisma.join(suggestion.columns)})
      `;
    }
  }
}
```

### Pattern 6: Zero-Downtime Schema Migrations

```typescript
// Migration strategy for production
// Step 1: Add nullable column (no downtime)
await prisma.$executeRaw`
  ALTER TABLE users ADD COLUMN phone VARCHAR(20)
`;

// Step 2: Backfill data
await prisma.$executeRaw`
  UPDATE users SET phone = 'unknown' WHERE phone IS NULL
`;

// Step 3: Add NOT NULL constraint
await prisma.$executeRaw`
  ALTER TABLE users ALTER COLUMN phone SET NOT NULL
`;

// Step 4: Add default (if needed)
await prisma.$executeRaw`
  ALTER TABLE users ALTER COLUMN phone SET DEFAULT 'unknown'
`;
```

This comprehensive guide covers SQL and PostgreSQL from basics to advanced production patterns. Practice these concepts and always consider the tradeoffs when choosing database solutions for your fullstack applications.
