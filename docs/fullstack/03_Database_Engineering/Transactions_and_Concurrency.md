# Transactions and Concurrency: Complete Guide for Fullstack Engineers

## Hinglish Explanation (Beginner Level)

Bhai, transactions aur concurrency database ke非常重要的 concepts hain. Let me simple words mein explain kar deta hoon:

**Transaction** matlab ek group of operations jo ek saath complete honge ya completely fail honge. Jaise tum bank mein money transfer karte ho:
1. Tumhare account se paise deduct hote hain
2. Dusre account mein paise add hote hain
3. Agar kahi error aata hai toh sab rollback ho jata hai

**Concurrency** matlab ek saath bahut saare operations execute hona. Jaise ek restaurant mein ek waiter ek baar mein bahut saare tables serve karta hai - database bhi similarly ek saath bahut requests handle karta hai.

**ACID** properties ensure karti hain ki transactions reliable hain:
- **Atomicity**: Sab ya kuch nahi (All or nothing)
- **Consistency**: Data valid state mein rahe
- **Isolation**: Concurrent transactions ek dusre ko affect na karein
- **Durability**: Committed data safe rahe

## Deep Technical Explanation

Transactions and concurrency control are fundamental concepts that ensure data integrity in multi-user database environments.

### ACID Properties Deep Dive

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ACID Properties                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ATOMICITY                                                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  BEGIN TRANSACTION                                           │  │
│  │     │                                                         │  │
│  │     ▼                                                         │  │
│  │  ┌─────────┐                                                  │  │
│  │  │ Account │ Debit $100         ┌─────────┐                 │  │
│  │  │    A    │────────────────────│ Account │                 │  │
│  │  │         │   Credit $100      │    B    │                 │  │
│  │  └─────────┘◄────────────────────│         │                 │  │
│  │                                   └─────────┘                 │  │
│  │                                                               │  │
│  │  SUCCESS ────► COMMIT                                        │  │
│  │  FAIL ──────► ROLLBACK (all changes undone)                  │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CONSISTENCY                                                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  Constraint: Account balance >= 0                             │  │
│  │                                                               │  │
│  │  Before: Account A = $500                                    │  │
│  │                                                               │  │
│  │  Transaction: Transfer $600 to B                             │  │
│  │                                                               │  │
│  │  If balance would go negative:                                │  │
│  │     → ABORT (database enforces constraint)                    │  │
│  │     → Balance stays $500                                      │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ISOLATION (Levels)                                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  READ UNCOMMITTED: See uncommitted changes (dirty reads)     │  │
│  │  ┌────┐ T1: READ X ──────────────────────► X=100            │  │
│  │  │ T2 │ READ X ─────────────── WRITE X=200                  │  │
│  │  │    │ READ X (sees 200!) ── COMMIT                        │  │
│  │  └────┘ T1: READ X ───────────► X=200 (WRONG!)              │  │
│  │                                                               │  │
│  │  SERIALIZABLE: Equivalent to sequential execution           │  │
│  │  ┌────┐ T1: ████████████████████████████████                │  │
│  │  │ T2 │           ██████████████████████████████████        │  │
│  │  └────┘                (T2 waits for T1 to complete)         │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  DURABILITY                                                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  COMMIT ──────► Write to disk ──────► Durability guaranteed │  │
│  │                  (WAL/Redo Log)                                │  │
│  │                                                               │  │
│  │  Even if server crashes immediately after commit:            │  │
│  │     → Data is safe on disk                                   │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Transaction Isolation Levels

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Transaction Isolation Levels                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Level          │ Dirty Read │ Non-repeatable │ Phantom │ Lost Up │
│  ─────────────────────────────────────────────────────────────────│
│  READ UNCOMMIT  │     ✓     │       ✓        │    ✓   │    ✓    │
│  READ COMMITTED │     ✗     │       ✓        │    ✓   │    ✓    │
│  REPEATABLE READ│     ✗     │       ✗        │    ✓   │    ✓    │
│  SERIALIZABLE   │     ✗     │       ✗        │    ✗   │    ✗    │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  READ UNCOMMITTED                                                   │
│  - Sees uncommitted changes from other transactions                 │
│  - Fastest but least safe                                           │
│  - Use: Monitoring, logging where staleness acceptable              │
│                                                                      │
│  READ COMMITTED (PostgreSQL default)                                │
│  - Only sees committed changes                                      │
│  - Non-repeatable reads possible (same row different values)       │
│  - Use: Most applications                                           │
│                                                                      │
│  REPEATABLE READ (MySQL default)                                   │
│  - Snapshot taken at transaction start                              │
│  - Consistent reads throughout transaction                           │
│  - Phantom reads possible (new rows match WHERE clause)             │
│                                                                      │
│  SERIALIZABLE                                                       │
│  - Full isolation, equivalent to sequential execution               │
│  - Slowest, may cause serialization failures                        │
│  - Use: Critical financial operations                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Concurrency Control Mechanisms

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Concurrency Control Methods                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PESSIMISTIC LOCKING (Lock-based)                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                              │  │
│  │  SHARED LOCK (S)           EXCLUSIVE LOCK (X)                │  │
│  │  ┌─────────────────┐      ┌─────────────────────────┐      │  │
│  │  │ Multiple readers │      │ Single writer           │      │  │
│  │  │ can hold this    │      │ blocks others           │      │  │
│  │  │ lock             │      │ blocks S and X locks    │      │  │
│  │  └─────────────────┘      └─────────────────────────┘      │  │
│  │                                                              │  │
│  │  Compatibility Matrix:                                      │  │
│  │              S Lock     X Lock                               │  │
│  │  S Lock      ✓          ✗                                   │  │
│  │  X Lock      ✗          ✗                                   │  │
│  │                                                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  OPTIMISTIC LOCKING (MVCC-based)                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                              │  │
│  │  BEGIN                                                       │  │
│  │     version = SELECT version FROM items WHERE id = 1        │  │
│  │     UPDATE items SET ..., version = version + 1             │  │
│  │               WHERE id = 1 AND version = :version          │  │
│  │     IF rows_affected = 0 THEN                                │  │
│  │        ROLLBACK                                             │  │
│  │        REPEAT (conflict detected!)                          │  │
│  │     END                                                     │  │
│  │  COMMIT                                                      │  │
│  │                                                              │  │
│  │  Advantages: No locks, high concurrency                    │  │
│  │  Disadvantages: Retry on conflict                          │  │
│  │                                                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Architecture Diagram: PostgreSQL MVCC

```
┌─────────────────────────────────────────────────────────────────────┐
│              PostgreSQL MVCC (Multi-Version Concurrency Control)      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  TRANSACTION A (Read)              TRANSACTION B (Write)            │
│  ┌─────────────────────┐          ┌─────────────────────┐         │
│  │ BEGIN (snapshot A)   │          │ BEGIN               │         │
│  │ SELECT * FROM users  │          │ UPDATE users SET... │         │
│  │ ─────────────────────│          │ ────────────────────│         │
│  │ Sees: OLD data       │          │ Creates: NEW row    │         │
│  │ (before T2 changes)   │          │ (xmax = T2)         │         │
│  └─────────────────────┘          └──────────┬──────────┘         │
│                                               │                      │
│                                               ▼                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                         Heap (Data Pages)                        │ │
│  │                                                                  │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │ ROW (id=1)                                                │ │ │
│  │  │ ┌─────────────┬─────────────┬──────────────────────────┐ │ │ │
│  │  │ │ xmin: 100   │ xmax: 200   │ data: {name: "OLD"}      │ │ │ │
│  │  │ │ (created by │ (deleted by │                          │ │ │ │
│  │  │ │  T1)        │  T2)        │                          │ │ │ │
│  │  │ └─────────────┴─────────────┴──────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  │                                                                  │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │ ROW (id=1, NEW version)                                   │ │ │
│  │  │ ┌─────────────┬─────────────┬──────────────────────────┐ │ │ │
│  │  │ │ xmin: 200   │             │ data: {name: "NEW"}      │ │ │ │
│  │  │ │ (created by │             │                          │ │ │ │
│  │  │ │  T2)        │             │                          │ │ │ │
│  │  │ └─────────────┴─────────────┴──────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  Visibility Rules:                                                    │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Row is visible if:                                           │  │
│  │  1. xmin committed before snapshot's xmax                     │  │
│  │  2. xmax is NULL or not committed when snapshot taken         │  │
│  │  3. Transaction is not in progress                            │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  VACUUM Process:                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐               │  │
│  │  │ Dead Row │───►│  VACUUM  │───►│Free Space│               │  │
│  │  │ (old ver)│    │ marks as │    │ Map (FSM)│               │  │
│  │  └──────────┘    │ reusable │    └──────────┘               │  │
│  │                  └──────────┘                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Frontend + Backend Integration Examples

### PostgreSQL Transactions with Prisma

```typescript
// src/services/order.service.ts
import { PrismaClient, Prisma } from '@prisma/client';

const prisma = new PrismaClient();

// ============================================
// BASIC TRANSACTION
// ============================================

async function createOrderWithTransaction(
  customerId: string,
  items: Array<{ productId: string; quantity: number }>,
  shippingAddress: Address
) {
  // Serializable isolation for financial transactions
  return prisma.$transaction(async (tx) => {
    // 1. Verify customer exists and is active
    const customer = await tx.customer.findUnique({
      where: { id: customerId },
    });

    if (!customer || !customer.isActive) {
      throw new Error('Customer not found or inactive');
    }

    // 2. Lock and fetch products (FOR UPDATE prevents overselling)
    const productIds = items.map((i) => i.productId);
    const products = await tx.product.findMany({
      where: { id: { in: productIds } },
      // Simulate FOR UPDATE
      orderBy: { id: 'asc' }, // Consistent lock order prevents deadlocks
    });

    // Verify all products exist
    if (products.length !== productIds.length) {
      throw new Error('One or more products not found');
    }

    // 3. Validate stock and calculate total
    let totalAmount = 0;
    const orderItems: Array<{ productId: string; quantity: number; unitPrice: number }> = [];

    for (const item of items) {
      const product = products.find((p) => p.id === item.productId);
      if (!product) continue;

      if (product.stockQuantity < item.quantity) {
        throw new Error(
          `Insufficient stock for ${product.name}. Available: ${product.stockQuantity}`
        );
      }

      totalAmount += product.price * item.quantity;
      orderItems.push({
        productId: product.id,
        quantity: item.quantity,
        unitPrice: product.price,
      });
    }

    // 4. Deduct stock
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

    // 5. Create order
    const order = await tx.order.create({
      data: {
        orderNumber: await generateOrderNumber(tx),
        customerId,
        subtotal: totalAmount,
        tax: totalAmount * 0.18, // 18% GST
        shippingCost: shippingAddress.isInternational ? 500 : 0,
        total: totalAmount * 1.18 + (shippingAddress.isInternational ? 500 : 0),
        status: 'PENDING',
        shippingAddress: {
          create: {
            ...shippingAddress,
          },
        },
        items: {
          create: orderItems,
        },
      },
    });

    // 6. Create audit log
    await tx.auditLog.create({
      data: {
        entityType: 'Order',
        entityId: order.id,
        action: 'CREATE',
        userId: customerId,
        changes: { status: 'PENDING' },
      },
    });

    return order;
  }, {
    isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
    timeout: 30000,
  });
}

// ============================================
// TRANSFER FUNDS (Two-Phase Locking Pattern)
// ============================================

async function transferFunds(
  fromAccountId: string,
  toAccountId: string,
  amount: number
) {
  if (amount <= 0) {
    throw new Error('Amount must be positive');
  }

  return prisma.$transaction(async (tx) => {
    // Lock accounts in consistent order to prevent deadlocks
    const [firstId, secondId] = fromAccountId < toAccountId
      ? [fromAccountId, toAccountId]
      : [toAccountId, fromAccountId];

    // Fetch and lock accounts
    const accounts = await tx.account.findMany({
      where: { id: { in: [firstId, secondId] } },
      orderBy: { id: 'asc' },
    });

    const fromAccount = accounts.find((a) => a.id === fromAccountId)!;
    const toAccount = accounts.find((a) => a.id === toAccountId)!;

    // Validate sufficient balance
    if (fromAccount.balance < amount) {
      throw new Error('Insufficient funds');
    }

    // Debit from source
    const updatedFrom = await tx.account.update({
      where: { id: fromAccountId },
      data: { balance: { decrement: amount } },
    });

    // Credit to destination
    const updatedTo = await tx.account.update({
      where: { id: toAccountId },
      data: { balance: { increment: amount } },
    });

    // Create transaction records
    await tx.transactionRecord.createMany({
      data: [
        {
          accountId: fromAccountId,
          type: 'DEBIT',
          amount,
          balanceAfter: updatedFrom.balance,
          reference: `TRANSFER_TO:${toAccountId}`,
        },
        {
          accountId: toAccountId,
          type: 'CREDIT',
          amount,
          balanceAfter: updatedTo.balance,
          reference: `TRANSFER_FROM:${fromAccountId}`,
        },
      ],
    });

    return { from: updatedFrom, to: updatedTo };
  });
}

// ============================================
// OPTIMISTIC LOCKING
// ============================================

async function updateProductWithOptimisticLock(
  productId: string,
  price: number,
  expectedVersion: number
) {
  const result = await prisma.$transaction(async (tx) => {
    const product = await tx.product.findUnique({
      where: { id: productId },
    });

    if (!product) {
      throw new Error('Product not found');
    }

    // Check version
    if ((product as any).version !== expectedVersion) {
      throw new OptimisticLockError('Product has been modified by another user');
    }

    // Update with version increment
    return tx.product.update({
      where: { id: productId },
      data: {
        price,
        version: { increment: 1 },
      },
    });
  });

  return result;
}

class OptimisticLockError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'OptimisticLockError';
  }
}

// Retry logic for optimistic locking
async function updateProductWithRetry(
  productId: string,
  updateFn: (product: any) => any,
  maxRetries: number = 3
) {
  let retries = 0;

  while (retries < maxRetries) {
    try {
      const product = await prisma.product.findUnique({
        where: { id: productId },
      });

      const updatedData = updateFn(product);
      return await updateProductWithOptimisticLock(
        productId,
        updatedData.price,
        (product as any).version
      );
    } catch (error) {
      if (error instanceof OptimisticLockError) {
        retries++;
        if (retries >= maxRetries) {
          throw new Error('Update failed after maximum retries');
        }
        // Exponential backoff
        await new Promise((r) => setTimeout(r, 100 * Math.pow(2, retries)));
      } else {
        throw error;
      }
    }
  }
}
```

### MongoDB Transactions with Mongoose

```typescript
// src/services/order.service.ts
import mongoose, { ClientSession } from 'mongoose';

// ============================================
// MONGODB TRANSACTION
// ============================================

async function createOrderWithTransaction(
  customerId: string,
  items: Array<{ productId: string; quantity: number }>,
  shippingAddress: Address
): Promise<Order> {
  const session = await mongoose.startSession();
  
  try {
    session.startTransaction({
      readConcern: { level: 'snapshot' },
      writeConcern: { w: 'majority' },
    });

    // 1. Verify customer
    const customer = await Customer.findById(customerId).session(session);
    if (!customer) {
      throw new Error('Customer not found');
    }

    // 2. Fetch and validate products
    const productIds = items.map((i) => i.productId);
    const products = await Product.find({ _id: { $in: productIds } }).session(session);

    if (products.length !== productIds.length) {
      throw new Error('One or more products not found');
    }

    // 3. Calculate and validate
    let totalAmount = 0;
    const orderItems: any[] = [];

    for (const item of items) {
      const product = products.find(
        (p) => p._id.toString() === item.productId
      )!;

      if (product.stock < item.quantity) {
        throw new Error(`Insufficient stock for ${product.name}`);
      }

      const itemTotal = product.price * item.quantity;
      totalAmount += itemTotal;

      orderItems.push({
        productId: product._id,
        name: product.name,
        sku: product.sku,
        price: product.price,
        quantity: item.quantity,
        total: itemTotal,
      });

      // Deduct stock
      await Product.updateOne(
        { _id: product._id },
        { $inc: { stock: -item.quantity } }
      ).session(session);
    }

    // 4. Create order
    const order = new Order({
      orderNumber: await generateOrderNumber(),
      customerId,
      items: orderItems,
      subtotal: totalAmount,
      tax: totalAmount * 0.18,
      shippingCost: shippingAddress.isInternational ? 500 : 0,
      total: totalAmount * 1.18 + (shippingAddress.isInternational ? 500 : 0),
      status: 'pending',
      shippingAddress,
    });

    await order.save({ session });

    // 5. Create audit event
    await AuditLog.create(
      [
        {
          entityType: 'Order',
          entityId: order._id,
          action: 'CREATE',
          userId: customerId,
          data: { status: 'pending' },
        },
      ],
      { session }
    );

    // Commit transaction
    await session.commitTransaction();
    
    return order;
  } catch (error) {
    // Abort on any error
    await session.abortTransaction();
    throw error;
  } finally {
    session.endSession();
  }
}

// ============================================
// DISTRIBUTED LOCK WITH REDIS
// ============================================

import { redis } from '../config/redis';

class DistributedLock {
  private redis: typeof redis;
  private lockPrefix = 'lock:';
  private defaultTTL = 30000; // 30 seconds

  constructor(redisClient: typeof redis) {
    this.redis = redisClient;
  }

  async acquire(
    resourceId: string,
    ttl: number = this.defaultTTL
  ): Promise<string | null> {
    const lockKey = `${this.lockPrefix}${resourceId}`;
    const lockValue = `${Date.now()}-${Math.random().toString(36).substring(2)}`;

    // SET NX EX - atomic operation
    const acquired = await this.redis.set(lockKey, lockValue, 'EX', ttl, 'NX');

    if (acquired === 'OK') {
      return lockValue;
    }

    return null;
  }

  async release(resourceId: string, lockValue: string): Promise<boolean> {
    const lockKey = `${this.lockPrefix}${resourceId}`;

    // Lua script for atomic check-and-delete
    const script = `
      if redis.call("GET", KEYS[1]) == ARGV[1] then
        return redis.call("DEL", KEYS[1])
      else
        return 0
      end
    `;

    const result = await this.redis.eval(script, 1, lockKey, lockValue);
    return result === 1;
  }

  async extend(
    resourceId: string,
    lockValue: string,
    ttl: number
  ): Promise<boolean> {
    const lockKey = `${this.lockPrefix}${resourceId}`;

    const script = `
      if redis.call("GET", KEYS[1]) == ARGV[1] then
        return redis.call("EXPIRE", KEYS[1], ARGV[2])
      else
        return 0
      end
    `;

    const result = await this.redis.eval(script, 1, lockKey, lockValue, ttl);
    return result === 1;
  }
}

const distributedLock = new DistributedLock(redis);

// Usage with inventory management
async function reserveInventoryWithLock(
  productId: string,
  quantity: number,
  orderId: string
) {
  const lockValue = await distributedLock.acquire(`inventory:${productId}`, 30000);

  if (!lockValue) {
    throw new Error('Could not acquire inventory lock');
  }

  try {
    const session = await mongoose.startSession();
    session.startTransaction();

    const product = await Product.findById(productId).session(session);

    if (!product || product.stock < quantity) {
      throw new Error('Insufficient stock');
    }

    product.stock -= quantity;
    await product.save({ session });

    await InventoryReservation.create(
      [
        {
          productId,
          quantity,
          orderId,
          reservedAt: new Date(),
        },
      ],
      { session }
    );

    await session.commitTransaction();
    session.endSession();

    return product;
  } finally {
    await distributedLock.release(`inventory:${productId}`, lockValue);
  }
}
```

### API Routes with Transaction Handling

```typescript
// src/routes/order.routes.ts
import { Router, Request, Response, NextFunction } from 'express';
import { orderService } from '../services/order.service';
import { z } from 'zod';

const router = Router();

const createOrderSchema = z.object({
  customerId: z.string().uuid(),
  items: z.array(
    z.object({
      productId: z.string().uuid(),
      quantity: z.number().int().positive().max(100),
    })
  ).min(1).max(50),
  shippingAddress: z.object({
    name: z.string().min(1).max(200),
    phone: z.string().regex(/^\+?[1-9]\d{1,14}$/),
    line1: z.string().min(1).max(500),
    line2: z.string().max(500).optional(),
    city: z.string().min(1).max(100),
    state: z.string().min(1).max(100),
    postalCode: z.string().min(5).max(10),
    country: z.string().min(2).max(2),
    isInternational: z.boolean().default(false),
  }),
});

// Error handler wrapper
const asyncHandler = (fn: Function) =>
  (req: Request, res: Response, next: NextFunction) =>
    Promise.resolve(fn(req, res, next)).catch(next);

// POST /api/orders
router.post(
  '/',
  asyncHandler(async (req: Request, res: Response) => {
    const data = createOrderSchema.parse(req.body);

    try {
      const order = await orderService.createOrderWithTransaction(
        data.customerId,
        data.items,
        data.shippingAddress
      );

      res.status(201).json({
        success: true,
        data: order,
      });
    } catch (error) {
      if (error instanceof Error) {
        if (error.message.includes('Insufficient stock')) {
          return res.status(409).json({
            success: false,
            message: error.message,
            code: 'INSUFFICIENT_STOCK',
          });
        }

        if (error.message.includes('not found')) {
          return res.status(404).json({
            success: false,
            message: error.message,
            code: 'NOT_FOUND',
          });
        }
      }

      throw error;
    }
  })
);

// POST /api/orders/transfer
router.post(
  '/transfer',
  asyncHandler(async (req: Request, res: Response) => {
    const { fromAccountId, toAccountId, amount } = req.body;

    try {
      const result = await orderService.transferFunds(
        fromAccountId,
        toAccountId,
        amount
      );

      res.json({
        success: true,
        data: {
          fromBalance: result.from.balance,
          toBalance: result.to.balance,
        },
      });
    } catch (error) {
      if (error instanceof Error) {
        if (error.message === 'Insufficient funds') {
          return res.status(400).json({
            success: false,
            message: 'Insufficient funds for transfer',
            code: 'INSUFFICIENT_FUNDS',
          });
        }
      }

      throw error;
    }
  })
);
```

## Real-World Production Examples

### Example 1: Financial Transaction Processing

```sql
-- PostgreSQL: Financial transaction with proper isolation
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Lock accounts in deterministic order
SELECT * FROM accounts 
WHERE id IN ($from_id, $to_id) 
ORDER BY id 
FOR UPDATE;

-- Verify sufficient balance
SELECT balance FROM accounts WHERE id = $from_id FOR UPDATE;
-- If balance < amount, ROLLBACK

-- Debit
UPDATE accounts 
SET balance = balance - $amount, 
    updated_at = NOW() 
WHERE id = $from_id;

-- Credit
UPDATE accounts 
SET balance = balance + $amount, 
    updated_at = NOW() 
WHERE id = $to_id;

-- Create transaction records
INSERT INTO transactions (account_id, type, amount, balance_after, reference)
VALUES 
    ($from_id, 'DEBIT', $amount, (SELECT balance FROM accounts WHERE id = $from_id), $ref),
    ($to_id, 'CREDIT', $amount, (SELECT balance FROM accounts WHERE id = $to_id), $ref);

-- Create audit entry
INSERT INTO audit_log (entity_type, entity_id, action, changes)
VALUES ('Account', $from_id, 'TRANSFER', jsonb_build_object('to' => $to_id, 'amount' => $amount));

COMMIT;
```

### Example 2: Inventory Management with Deadlock Prevention

```typescript
// src/services/inventory.service.ts

class InventoryService {
  // Always acquire locks in consistent order to prevent deadlocks
  async reserveProducts(productIds: string[], quantities: number[]) {
    // Sort IDs to ensure consistent lock ordering
    const sorted = productIds
      .map((id, idx) => ({ id, quantity: quantities[idx] }))
      .sort((a, b) => a.id.localeCompare(b.id));

    return prisma.$transaction(async (tx) => {
      const reservations: any[] = [];

      for (const { id, quantity } of sorted) {
        // FOR UPDATE in consistent order
        const product = await tx.$queryRaw`
          SELECT id, stock, "lowStockThreshold", name
          FROM products
          WHERE id = ${id}
          FOR UPDATE
        `;

        if (!product[0] || product[0].stock < quantity) {
          throw new InsufficientStockError(
            product[0]?.name || 'Unknown',
            product[0]?.stock || 0,
            quantity
          );
        }

        // Deduct stock
        await tx.product.update({
          where: { id },
          data: { stock: { decrement: quantity } },
        });

        reservations.push({ productId: id, quantity });
      }

      // Create reservation record
      const reservation = await tx.inventoryReservation.create({
        data: {
          status: 'RESERVED',
          expiresAt: new Date(Date.now() + 30 * 60 * 1000), // 30 min expiry
          items: {
            create: reservations.map((r) => ({
              productId: r.productId,
              quantity: r.quantity,
            })),
          },
        },
      });

      return reservation;
    }, {
      isolationLevel: 'Serializable',
      timeout: 15000,
    });
  }

  // Compensating transaction for failed operations
  async releaseReservation(reservationId: string) {
    return prisma.$transaction(async (tx) => {
      const reservation = await tx.inventoryReservation.findUnique({
        where: { id: reservationId },
        include: { items: true },
      });

      if (!reservation) {
        throw new Error('Reservation not found');
      }

      if (reservation.status !== 'RESERVED') {
        throw new Error(`Cannot release reservation in ${reservation.status} status`);
      }

      // Restore stock
      for (const item of reservation.items) {
        await tx.product.update({
          where: { id: item.productId },
          data: { stock: { increment: item.quantity } },
        });
      }

      // Mark reservation as released
      await tx.inventoryReservation.update({
        where: { id: reservationId },
        data: { status: 'RELEASED' },
      });
    });
  }
}

class InsufficientStockError extends Error {
  constructor(
    public productName: string,
    public available: number,
    public requested: number
  ) {
    super(`Insufficient stock for ${productName}. Available: ${available}, Requested: ${requested}`);
    this.name = 'InsufficientStockError';
  }
}
```

### Example 3: Saga Pattern for Distributed Transactions

```typescript
// src/services/order.saga.ts

// Saga orchestrator for distributed order processing
interface OrderSagaStep {
  type: 'RESERVE_INVENTORY' | 'CHARGE_PAYMENT' | 'CREATE_ORDER' | 'SEND_NOTIFICATION';
  compensatable: boolean;
  execute: () => Promise<any>;
  compensate: () => Promise<void>;
}

class OrderSaga {
  private steps: OrderSagaStep[] = [];
  private completedSteps: any[] = [];

  addStep(step: OrderSagaStep): this {
    this.steps.push(step);
    return this;
  }

  async execute(): Promise<any> {
    const results: any[] = [];

    for (let i = 0; i < this.steps.length; i++) {
      const step = this.steps[i];

      try {
        const result = await step.execute();
        results.push(result);
        this.completedSteps.push({ step, result });
      } catch (error) {
        // Compensate completed steps in reverse order
        console.log(`Step ${i} failed: ${error.message}`);
        await this.compensate();

        throw new SagaExecutionError(
          `Order processing failed at step ${i} (${step.type})`,
          i,
          results
        );
      }
    }

    return results;
  }

  private async compensate(): Promise<void> {
    console.log('Starting compensation...');

    for (const { step, result } of [...this.completedSteps].reverse()) {
      if (step.compensatable) {
        try {
          console.log(`Compensating step: ${step.type}`);
          await step.compensate();
        } catch (compensationError) {
          // Log but continue
          console.error(`Compensation failed for ${step.type}:`, compensationError);
        }
      }
    }

    this.completedSteps = [];
  }
}

// Execute order saga
async function processOrder(orderData: CreateOrderInput): Promise<Order> {
  const saga = new OrderSaga()
    .addStep({
      type: 'RESERVE_INVENTORY',
      compensatable: true,
      execute: () => inventoryService.reserveProducts(
        orderData.items.map(i => i.productId),
        orderData.items.map(i => i.quantity)
      ),
      compensate: () => inventoryService.releaseReservation(
        /* reservation ID from execute */
      ),
    })
    .addStep({
      type: 'CHARGE_PAYMENT',
      compensatable: true,
      execute: () => paymentService.charge(orderData.paymentMethod, orderData.total),
      compensate: () => paymentService.refund(/* payment ID */),
    })
    .addStep({
      type: 'CREATE_ORDER',
      compensatable: false, // Final step - cannot compensate
      execute: () => orderService.create(orderData),
      compensate: async () => {}, // No-op
    })
    .addStep({
      type: 'SEND_NOTIFICATION',
      compensatable: false,
      execute: () => notificationService.sendOrderConfirmation(orderData.customerId),
      compensate: async () => {},
    });

  const [inventory, payment, order] = await saga.execute();
  return order;
}
```

## Failure Cases

### Case 1: Deadlock

**Problem**: Two transactions waiting for each other to release locks.

```sql
-- Session 1: Lock order A then B
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- Locks row 1
-- (Session 2 locks row 2 here)
SELECT * FROM accounts WHERE id = 2 FOR UPDATE;  -- Waits for row 2
-- Session 2: Lock order B then A
BEGIN;
SELECT * FROM accounts WHERE id = 2 FOR UPDATE;  -- Locks row 2
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- Waits for row 1
-- DEADLOCK DETECTED - one transaction aborted!

-- Solution: Always lock in consistent order
-- Option 1: By ID
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;

-- Option 2: Use advisory locks for complex scenarios
SELECT pg_advisory_xact_lock(12345); -- Transaction-scoped lock
```

### Case 2: Lost Updates (Race Condition)

**Problem**: Concurrent updates causing one to be lost.

```sql
-- T1: Read balance = $100
-- T2: Read balance = $100
-- T1: Write balance = $100 + $50 = $150
-- T2: Write balance = $100 + $25 = $125
-- Final balance = $125 (T1's update lost!)

-- Solution 1: Pessimistic Locking
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- T1 now holds lock, T2 waits
UPDATE accounts SET balance = 150 WHERE id = 1;
COMMIT;

-- Solution 2: Optimistic Locking with Version
UPDATE accounts 
SET balance = 150, version = version + 1 
WHERE id = 1 AND version = 5;
-- If rows affected = 0, another transaction updated it

-- Solution 3: Atomic Update
UPDATE accounts 
SET balance = balance + 50 
WHERE id = 1;
-- Atomic operation, no race condition
```

## Debugging Guide

### Detecting Lock Issues

```sql
-- Find blocking queries
SELECT 
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query,
    blocked.usename AS blocked_user,
    blocking.usename AS blocking_user
FROM pg_stat_activity AS blocked
JOIN pg_stat_activity AS blocking
    ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE blocked.state = 'active' AND blocking.state = 'active';

-- Find long-running transactions
SELECT 
    pid,
    state,
    query,
    query_start,
    NOW() - query_start AS duration,
    wait_event_type,
    wait_event
FROM pg_stat_activity
WHERE state != 'idle'
AND (NOW() - query_start) > interval '5 minutes'
ORDER BY query_start;

-- Find locks
SELECT 
    l.locktype,
    l.relation::regclass,
    l.mode,
    l.granted,
    l.pid,
    a.usename,
    a.query
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted
ORDER BY l.pid;

-- Kill blocking process
SELECT pg_cancel_backend(pid);  -- Graceful
SELECT pg_terminate_backend(pid); -- Forceful
```

### Transaction Diagnostics

```typescript
// Enable query logging in development
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});

// Custom logging for transactions
async function monitoredTransaction<T>(
  name: string,
  fn: (tx: any) => Promise<T>
): Promise<T> {
  const startTime = Date.now();
  console.log(`[TRANSACTION:${name}] Starting...`);

  try {
    const result = await prisma.$transaction(fn, {
      isolationLevel: 'Serializable',
    });

    const duration = Date.now() - startTime;
    console.log(`[TRANSACTION:${name}] Completed in ${duration}ms`);

    return result;
  } catch (error) {
    const duration = Date.now() - startTime;
    console.error(`[TRANSACTION:${name}] Failed after ${duration}ms:`, error);

    throw error;
  }
}

// Usage
const order = await monitoredTransaction('createOrder', async (tx) => {
  return tx.order.create({ data: orderData });
});
```

## Tradeoffs

### Isolation Levels vs Performance

| Level | Performance | Consistency | Concurrency |
|-------|------------|-------------|-------------|
| READ UNCOMMITTED | Highest | Lowest | Highest |
| READ COMMITTED | High | Moderate | High |
| REPEATABLE READ | Moderate | High | Moderate |
| SERIALIZABLE | Lowest | Highest | Lowest |

### Pessimistic vs Optimistic Locking

| Aspect | Pessimistic | Optimistic |
|--------|-----------|-----------|
| Locking | Acquire before access | Verify on update |
| Conflicts | Prevented | Detected after |
| Throughput | Lower | Higher |
| Latency | May wait for lock | No waiting |
| Retry | Not needed | Required |
| Best for | High contention | Low contention |
| Use case | Financial, inventory | User profiles, settings |

## Security Concerns

### Transaction-Level Security

```sql
-- Set security context
SET app.current_user_id = 'user-uuid';
SET app.current_tenant_id = 'tenant-uuid';

-- Use row-level security with context
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- Application sets context before each request
await prisma.$executeRaw`SET app.current_user_id = ${userId}`;
```

### Preventing SQL Injection in Transactions

```typescript
// BAD: SQL injection vulnerability
await prisma.$transaction(async (tx) => {
  await tx.$executeRawUnsafe(`DELETE FROM users WHERE id = ${userId}`);
});

// GOOD: Parameterized query
await prisma.$transaction(async (tx) => {
  await tx.$executeRaw`DELETE FROM users WHERE id = ${userId}`;
});
```

## Best Practices

### 1. Keep Transactions Short

```typescript
// BAD: Long transaction with network calls
await prisma.$transaction(async (tx) => {
  const user = await tx.user.findUnique({ where: { id } });
  
  // Network call in transaction - BAD!
  await fetch('https://api.example.com/validate');
  
  // Another network call - BAD!
  await sendEmail(user.email);
  
  await tx.user.update({ where: { id }, data: { status: 'active' } });
});

// GOOD: Short transaction
await prisma.$transaction(async (tx) => {
  await tx.user.update({ where: { id }, data: { status: 'active' } });
});

// Move network calls outside
const user = await prisma.user.findUnique({ where: { id } });
await sendEmail(user.email); // After transaction
```

### 2. Handle Transaction Timeouts

```typescript
// Set appropriate timeout
await prisma.$transaction(async (tx) => {
  // Complex transaction
}, {
  timeout: 10000, // 10 seconds
});
```

### 3. Always Use Appropriate Isolation Level

```typescript
// Financial operations need SERIALIZABLE
await prisma.$transaction(async (tx) => {
  // Money transfer
}, {
  isolationLevel: 'Serializable',
});

// Analytics can use READ COMMITTED
await prisma.$transaction(async (tx) => {
  // Read-heavy, non-critical
}, {
  isolationLevel: 'ReadCommitted',
});
```

## Common Mistakes

### Mistake 1: Not Using Transactions for Related Operations

```typescript
// BAD: Two separate operations
await prisma.order.create({ data: orderData });
await prisma.product.updateMany({
  where: { id: { in: itemIds } },
  data: { stock: { decrement: 1 } },
});
// If second fails, order exists but stock not updated!

// GOOD: Single transaction
await prisma.$transaction(async (tx) => {
  await tx.order.create({ data: orderData });
  await tx.product.updateMany({
    where: { id: { in: itemIds } },
    data: { stock: { decrement: 1 } },
  });
});
```

### Mistake 2: Swallowing Transaction Errors

```typescript
// BAD: Error swallowed
try {
  await prisma.$transaction(async (tx) => {
    await tx.order.create({ data });
  });
} catch (error) {
  console.log('Transaction failed'); // Generic handling
}

// GOOD: Proper error handling
try {
  await prisma.$transaction(async (tx) => {
    await tx.order.create({ data });
  });
} catch (error) {
  if (error.code === 'P40001') { // PostgreSQL serialization failure
    throw new ConflictError('Order was modified by another process');
  }
  throw error;
}
```

## Interview Questions

### Q1: What is the difference between pessimistic and optimistic locking?

**Answer**: Pessimistic locking acquires locks before accessing data, preventing conflicts. Optimistic locking allows access without locking but checks for conflicts before committing. Pessimistic is better for high contention, optimistic for low contention.

### Q2: Explain ACID properties

**Answer**: Atomicity ensures all-or-nothing execution. Consistency ensures database moves from valid state to valid state. Isolation ensures concurrent transactions don't interfere. Durability ensures committed data survives crashes.

### Q3: What is a deadlock? How to prevent?

**Answer**: Deadlock occurs when two or more transactions hold locks and wait for each other's locks in a circular dependency. Prevention: Always acquire locks in consistent order, use deadlock detection with automatic rollback, or use lock timeout.

### Q4: What is the difference between READ COMMITTED and SERIALIZABLE?

**Answer**: READ COMMITTED sees only committed data from other transactions but can see different values on re-read. SERIALIZABLE provides a consistent snapshot equivalent to sequential execution, preventing phantom reads and ensuring strict isolation.

### Q5: What is a savepoint in transactions?

**Answer**: Savepoints allow partial rollback within a transaction. You can set a savepoint, continue processing, and if needed, rollback to that savepoint instead of rolling back the entire transaction.

### Q6: What is the two-phase commit protocol?

**Answer**: Two-phase commit ensures distributed transactions commit or abort across multiple databases. Phase 1 (Prepare): Coordinator asks all participants to prepare. Phase 2 (Commit): If all prepared, coordinator sends commit; otherwise, rollback.

### Q7: What is the saga pattern?

**Answer**: Saga pattern handles distributed transactions by breaking them into local transactions with compensating actions. If a step fails, previous steps are compensated (rolled back) using their compensation logic.

## Latest 2026 Fullstack Engineering Patterns

### Pattern 1: Serverless Transaction with FaunaDB

```typescript
// FaunaDB - Transactional serverless database
import { Client, fql } from 'fauna';

const fauna = new Client({ secret: process.env.FAUNA_SECRET });

// All operations are automatically transactional
const result = await fauna.query(fql`
  Let(
    {
      customer: Get(Match(Index('customer_by_id'), ${customerId})),
      product: Get(Match(Index('product_by_id'), ${productId}))
    },
    If(
      And(
        Exists(Var('customer')),
        Exists(Var('product'))
      ),
      Create(Collection('orders'), {
        data: {
          customer: Select(['ref'], Var('customer')),
          product: Select(['ref'], Var('product')),
          status: 'pending',
          createdAt: Now()
        }
      }),
      Abort('Customer or product not found')
    )
  )
`);
```

### Pattern 2: Event Sourcing with CQRS

```typescript
// Event sourcing for audit trail
interface Event {
  id: string;
  aggregateId: string;
  type: string;
  payload: any;
  metadata: any;
  timestamp: Date;
  version: number;
}

class EventStore {
  async append(event: Omit<Event, 'id' | 'timestamp' | 'version'>): Promise<Event> {
    return this.db.transaction(async (tx) => {
      const lastEvent = await tx.events.findOne({
        where: { aggregateId: event.aggregateId },
        order: { version: 'desc' },
      });

      const newVersion = (lastEvent?.version || 0) + 1;
      const newEvent = await tx.events.create({
        ...event,
        version: newVersion,
        timestamp: new Date(),
      });

      return newEvent;
    });
  }

  async getStream(aggregateId: string): Promise<Event[]> {
    return this.db.events.findAll({
      where: { aggregateId },
      order: { version: 'asc' },
    });
  }

  async replay(aggregateId: string): Promise<any> {
    const events = await this.getStream(aggregateId);
    return events.reduce((state, event) => {
      return this.applyEvent(state, event);
    }, this.getInitialState());
  }
}
```

This comprehensive guide covers transactions and concurrency from basics to advanced production patterns. Practice these concepts and always consider the tradeoffs when implementing transactions in your fullstack applications.
