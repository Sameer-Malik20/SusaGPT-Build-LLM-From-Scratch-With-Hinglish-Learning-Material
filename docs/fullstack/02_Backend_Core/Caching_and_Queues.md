# Caching and Message Queues - Performance & Reliability

Bhai, caching aur queues fullstack development mein performance aur reliability ke liye bahut important hain. Agar tum samajh loge ki kab aur kaise inka use karna hai, toh tumhara application bahut fast aur scalable ban jayega. Chalo detail mein cover karte hain!

---

## 1. Beginner-Friendly Hinglish Explanation

### Caching Kya Hai?

Soch ki tu apne **fridge** mein khaana rakhta hai:
- Jab tu hungry hota hai, pehle fridge check karta hai
- Agar khaana hai, turant le leta hai (fast!)
- Agar nahi hai, toh market jaake laata hai (slow)

Backend mein bhi aise hi hai:
- **Cache** = Fridge (fast memory)
- **Database** = Market (slow but has everything)
- Jab data chahiye, pehle cache check karo
- Agar nahi hai, database se lao aur cache mein store karo

### Message Queue Kya Hai?

Soch ek **restaurant kitchen** mein:
- Order aata hai → Counter pe rakha → Chef ko diya → Chef kaam karta hai → Ready hua → Server deliver karta hai

Message queue bhi aise hi kaam karta hai:
- **Producer** = Counter (order create karta hai)
- **Queue** = Order list (order store hota hai)
- **Consumer** = Chef (order process karta hai)
- **Result** = Prepared food

Benefits:
- Chef simultaneously bahut orders handle kar sakta hai
- Agar chef busy hai, orders queue mein wait karte hain
- Agar chef chala gaya (crash), orders secure hain (koi food waste nahi)

### Caching Ke Types

| Type | Jaise | Use Case |
|------|-------|----------|
| **In-Memory** | Fridge (ghar ke andar) | Session data, hot data |
| **Distributed Cache** | Fridge with roommates (shared) | Multi-server caching |
| **CDN** | Nearby grocery store | Static files, images |
| **Database Cache** | Chef's prep station | Query results |
| **Application Cache** | Your brain (memory) | Computed results |

### Queues Ke Types

| Type | Example | Use Case |
|------|---------|----------|
| **Message Queue** | RabbitMQ, SQS | Background jobs |
| **Task Queue** | Celery, BullMQ | Scheduled tasks |
| **Event Bus** | Kafka | Event streaming |
| **Pub/Sub** | Redis Pub/Sub | Real-time updates |

---

## 2. Deep Technical Explanation

### Caching Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CACHING ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                       CLIENT LAYER                           │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │                   BROWSER CACHE                      │   │   │
│  │  │  - LocalStorage, SessionStorage                      │   │   │
│  │  │  - Service Worker Cache                              │   │   │
│  │  │  - HTTP Cache Headers (Cache-Control, ETag)          │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                       CDN LAYER                              │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐               │   │
│  │  │ Cloudflare│  │   AWS     │  │   Vercel  │               │   │
│  │  │  /Fastly  │  │   Cloud   │  │   Edge    │               │   │
│  │  │           │  │   Front   │  │   Cache   │               │   │
│  │  └───────────┘  └───────────┘  └───────────┘               │   │
│  │  - Static Assets (JS, CSS, Images)                         │   │
│  │  - API Response Caching                                    │   │
│  │  - Edge Locations Worldwide                                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    APPLICATION LAYER                         │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │               IN-MEMORY CACHE (L1)                   │    │   │
│  │  │         ┌───────────┐  ┌───────────┐              │    │   │
│  │  │         │   Node    │  │   LRU     │              │    │   │
│  │  │         │  process  │  │   Cache   │              │    │   │
│  │  │         └───────────┘  └───────────┘              │    │   │
│  │  │   - Fastest access (< 1ms)                       │    │   │
│  │  │   - Per-process (not shared)                      │    │   │
│  │  │   - Lost on restart                               │    │   │
│  │  └─────────────────────────────────────────────────────┘    │   │
│  │                              │                              │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │               DISTRIBUTED CACHE (L2)                │    │   │
│  │  │         ┌───────────────────────────────────┐      │    │   │
│  │  │         │            REDIS                  │      │    │   │
│  │  │         │   ┌─────────┐  ┌─────────┐        │      │    │   │
│  │  │         │   │  Cache  │  │ Session │        │      │    │   │
│  │  │         │   │  Store  │  │  Store  │        │      │    │   │
│  │  │         │   └─────────┘  └─────────┘        │      │    │   │
│  │  │         │   ┌─────────┐  ┌─────────┐        │      │    │   │
│  │  │         │   │ Rate    │  │  Pub/   │        │      │    │   │
│  │  │         │   │ Limit   │  │  Sub    │        │      │    │   │
│  │  │         │   └─────────┘  └─────────┘        │      │    │   │
│  │  │         └───────────────────────────────────┘      │    │   │
│  │  │   - Sub-millisecond access                           │    │   │
│  │  │   - Shared across all processes                       │    │   │
│  │  │   - Persistent with RDB/AOF                          │    │   │
│  │  └─────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                       DATABASE LAYER                        │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │                 DATABASE CACHE                       │    │   │
│  │  │   ┌────────────────────────────────────────────┐    │    │   │
│  │  │   │  Query Cache | Row Cache | Buffer Pool    │    │    │   │
│  │  │   └────────────────────────────────────────────┘    │    │   │
│  │  └─────────────────────────────────────────────────────┘    │   │
│  │                              │                              │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │                    DATABASE                          │    │   │
│  │  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │    │   │
│  │  │   │ PostgreSQL │  │   MongoDB   │  │  Cassandra  │ │    │   │
│  │  │   │             │  │             │  │             │ │    │   │
│  │  │   └─────────────┘  └─────────────┘  └─────────────┘ │    │   │
│  │  └─────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Message Queue Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      MESSAGE QUEUE ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    MESSAGE QUEUE PATTERNS                    │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │                    POINT-TO-POINT                    │    │   │
│  │  │                                                      │    │   │
│  │  │    Producer ─────> [Queue] ─────> Consumer          │    │   │
│  │  │                     (FIFO)                           │    │   │
│  │  │                                                      │    │   │
│  │  │   - One consumer processes each message             │    │   │
│  │  │   - Message deleted after processing                │    │   │
│  │  │   - Examples: SQS, RabbitMQ, BullMQ                 │    │   │
│  │  └─────────────────────────────────────────────────────┘    │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │                      PUB/SUB                          │    │   │
│  │  │                                                      │    │   │
│  │  │    Publisher ─────> [Topic] ─────> Subscriber 1      │    │   │
│  │  │                             ├──────> Subscriber 2     │    │   │
│  │  │                             ├──────> Subscriber 3     │    │   │
│  │  │                                                      │    │   │
│  │  │   - Multiple consumers receive same message         │    │   │
│  │  │   - Message persists until consumed                  │    │   │
│  │  │   - Examples: Kafka, Redis Pub/Sub                   │    │   │
│  │  └─────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    QUEUE COMPONENTS                           │   │
│  │                                                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │   │
│  │  │  Message     │  │   Queue      │  │   Consumer       │   │   │
│  │  │  Producer    │  │   Broker     │  │   Worker Pool   │   │   │
│  │  │              │  │              │  │                  │   │   │
│  │  │ - API Server │  │ - RabbitMQ   │  │ - Background     │   │   │
│  │  │ - Any service│  │ - Redis      │  │   workers        │   │   │
│  │  │ - IoT device │  │ - Kafka      │  │ - Multiple       │   │   │
│  │  │ - Cron job   │  │ - SQS        │  │   instances      │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘   │   │
│  │                              │                               │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │                    MESSAGE FORMAT                     │   │   │
│  │  │   {                                                    │   │   │
│  │  │     "id": "uuid",                                     │   │   │
│  │  │     "type": "order.created",                          │   │   │
│  │  │     "payload": { ... },                               │   │   │
│  │  │     "timestamp": "ISO8601",                           │   │   │
│  │  │     "headers": { "correlationId": "..." }            │   │   │
│  │  │   }                                                    │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Redis Caching Implementation

### Complete Redis Caching Strategy

```javascript
// File: caching/redisClient.js
const Redis = require('ioredis');
const { promisify } = require('util');

// Redis connection with retry
const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: process.env.REDIS_PORT || 6379,
  password: process.env.REDIS_PASSWORD,
  retryStrategy: (times) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  },
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: true,
});

redis.on('error', (err) => console.error('Redis error:', err));
redis.on('connect', () => console.log('Redis connected'));
redis.on('reconnecting', () => console.log('Redis reconnecting...'));

// Promisify methods
const redisGet = promisify(redis.get).bind(redis);
const redisSet = promisify(redis.set).bind(redis);
const redisDel = promisify(redis.del).bind(redis);

// File: caching/cacheManager.js
class CacheManager {
  constructor(redis) {
    this.redis = redis;
    this.defaultTTL = 3600; // 1 hour
  }

  // Cache-aside pattern
  async getOrSet(key, fetchFn, ttl = this.defaultTTL) {
    // Try to get from cache
    const cached = await this.redis.get(key);
    if (cached) {
      console.log(`Cache hit: ${key}`);
      return JSON.parse(cached);
    }

    // Fetch from source
    console.log(`Cache miss: ${key}`);
    const data = await fetchFn();

    // Store in cache
    if (data !== null && data !== undefined) {
      await this.redis.setex(key, ttl, JSON.stringify(data));
    }

    return data;
  }

  // Multi-get for efficiency
  async getMany(keys) {
    if (keys.length === 0) return {};

    const pipeline = this.redis.pipeline();
    keys.forEach(key => pipeline.get(key));
    const results = await pipeline.exec();

    const data = {};
    keys.forEach((key, index) => {
      const [err, value] = results[index];
      data[key] = err ? null : JSON.parse(value);
    });

    return data;
  }

  // Write-through cache
  async set(key, value, ttl = this.defaultTTL) {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  // Write-behind (lazy)
  async invalidate(key) {
    await this.redis.del(key);
  }

  // Invalidate by pattern
  async invalidatePattern(pattern) {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
    return keys.length;
  }

  // Cache with locking (prevent thundering herd)
  async getOrSetWithLock(key, fetchFn, ttl = this.defaultTTL, lockTTL = 10) {
    const lockKey = `lock:${key}`;

    // Try to get cached value
    const cached = await this.redis.get(key);
    if (cached) return JSON.parse(cached);

    // Try to acquire lock
    const lock = await this.redis.set(lockKey, '1', 'EX', lockTTL, 'NX');
    
    if (lock === 'OK') {
      try {
        // Fetch and cache
        const data = await fetchFn();
        await this.redis.setex(key, ttl, JSON.stringify(data));
        return data;
      } finally {
        // Release lock
        await this.redis.del(lockKey);
      }
    } else {
      // Wait and retry
      await new Promise(resolve => setTimeout(resolve, 100));
      return this.getOrSet(key, fetchFn, ttl);
    }
  }
}

module.exports = { CacheManager, redis };
```

### Cache Patterns Implementation

```javascript
// File: caching/patterns.js

// Pattern 1: Cache-Aside (Lazy Loading)
class CacheAsidePattern {
  async getUser(userId) {
    const cacheKey = `user:${userId}`;
    
    // 1. Check cache
    const cached = await redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // 2. Cache miss - fetch from DB
    const user = await prisma.user.findUnique({ where: { id: userId } });

    // 3. Store in cache
    if (user) {
      await redis.setex(cacheKey, 3600, JSON.stringify(user));
    }

    return user;
  }

  async updateUser(userId, data) {
    // 1. Update database
    const user = await prisma.user.update({
      where: { id: userId },
      data,
    });

    // 2. Invalidate cache
    await redis.del(`user:${userId}`);

    return user;
  }
}

// Pattern 2: Write-Through Cache
class WriteThroughCache {
  async createUser(data) {
    // 1. Write to database
    const user = await prisma.user.create({ data });

    // 2. Write to cache immediately
    await redis.setex(`user:${user.id}`, 3600, JSON.stringify(user));

    return user;
  }

  async updateUser(userId, data) {
    // 1. Write to database
    const user = await prisma.user.update({
      where: { id: userId },
      data,
    });

    // 2. Update cache
    await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));

    return user;
  }
}

// Pattern 3: Read-Through Cache
class ReadThroughCache {
  async getProduct(productId) {
    const cacheKey = `product:${productId}`;
    
    const cached = await redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // Database fetch is abstracted
    const product = await this.fetchProductFromDB(productId);
    
    await redis.setex(cacheKey, 7200, JSON.stringify(product));
    return product;
  }

  async fetchProductFromDB(productId) {
    // Simulated DB fetch
    return prisma.product.findUnique({ where: { id: productId } });
  }
}

// Pattern 4: Cache Tags (for invalidation)
class TaggedCache {
  async set(key, value, tags, ttl = 3600) {
    const pipeline = this.redis.pipeline();
    
    // Set the value
    pipeline.setex(key, ttl, JSON.stringify(value));
    
    // Add to tag sets
    for (const tag of tags) {
      pipeline.sadd(`tag:${tag}`, key);
      pipeline.expire(`tag:${tag}`, ttl + 60);
    }
    
    await pipeline.exec();
  }

  async invalidateTag(tag) {
    // Get all keys with this tag
    const keys = await this.redis.smembers(`tag:${tag}`);
    
    if (keys.length > 0) {
      // Delete all keys
      await this.redis.del(...keys);
      // Delete the tag
      await this.redis.del(`tag:${tag}`);
    }
  }
}

// Pattern 5: LRU Cache (in-memory + Redis)
class TwoLevelCache {
  constructor(redis, maxSize = 1000) {
    this.redis = redis;
    this.l1 = new Map(); // In-memory LRU
    this.maxSize = maxSize;
  }

  async get(key) {
    // L1 check (fastest)
    if (this.l1.has(key)) {
      const value = this.l1.get(key);
      // Move to end (most recently used)
      this.l1.delete(key);
      this.l1.set(key, value);
      return value;
    }

    // L2 check (Redis)
    const value = await this.redis.get(key);
    if (value) {
      const parsed = JSON.parse(value);
      // Promote to L1
      this.promoteToL1(key, parsed);
      return parsed;
    }

    return null;
  }

  async set(key, value, ttl = 3600) {
    // Set in L2 (Redis)
    await this.redis.setex(key, ttl, JSON.stringify(value));
    
    // Set in L1
    this.promoteToL1(key, value);
  }

  promoteToL1(key, value) {
    // Evict if necessary
    if (this.l1.size >= this.maxSize) {
      // Remove least recently used (first item)
      const firstKey = this.l1.keys().next().value;
      this.l1.delete(firstKey);
    }
    this.l1.set(key, value);
  }
}

module.exports = {
  CacheAsidePattern,
  WriteThroughCache,
  ReadThroughCache,
  TaggedCache,
  TwoLevelCache,
};
```

---

## 4. Message Queue Implementation

### BullMQ Implementation

```javascript
// File: queues/bullmqSetup.js
const { Queue, Worker, QueueEvents, Job } = require('bullmq');
const IORedis = require('ioredis');

// Redis connection for BullMQ
const connection = new IORedis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  maxRetriesPerRequest: null,
});

// Email Queue
const emailQueue = new Queue('emails', { connection });

// Order Processing Queue
const orderQueue = new Queue('orders', { connection });

// File Processing Queue
const fileQueue = new Queue('files', { connection });

// Queue Events for monitoring
const emailQueueEvents = new QueueEvents('emails', { connection });
const orderQueueEvents = new QueueEvents('orders', { connection });

// Monitor events
emailQueueEvents.on('completed', ({ jobId }) => {
  console.log(`Email job ${jobId} completed`);
});

emailQueueEvents.on('failed', ({ jobId, failedReason }) => {
  console.error(`Email job ${jobId} failed: ${failedReason}`);
});

// File: queues/emailWorker.js
const emailWorker = new Worker(
  'emails',
  async (job) => {
    console.log(`Processing email job ${job.id}`);
    
    const { to, subject, template, data } = job.data;
    
    switch (template) {
      case 'welcome':
        await sendWelcomeEmail(to, data);
        break;
      case 'order-confirmation':
        await sendOrderConfirmation(to, data);
        break;
      case 'password-reset':
        await sendPasswordReset(to, data);
        break;
      default:
        await sendGenericEmail(to, subject, data);
    }
    
    return { sent: true, to, template };
  },
  {
    connection,
    concurrency: 5, // Process 5 emails simultaneously
    limiter: {
      max: 100,
      duration: 60000, // Max 100 per minute
    },
  }
);

// Configure retry strategy
emailWorker.on('failed', async (job, err) => {
  console.error(`Email job ${job.id} failed with error: ${err.message}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  await emailWorker.close();
  await emailQueueEvents.close();
});

// File: queues/orderWorker.js
const orderWorker = new Worker(
  'orders',
  async (job) => {
    console.log(`Processing order job ${job.id}`);
    
    const { orderId, userId, items } = job.data;
    
    try {
      // Step 1: Validate order
      await validateOrder(orderId);
      
      // Step 2: Reserve inventory
      await reserveInventory(items);
      
      // Step 3: Process payment
      const payment = await processPayment(orderId);
      
      // Step 4: Update order status
      await updateOrderStatus(orderId, 'CONFIRMED', { paymentId: payment.id });
      
      // Step 5: Send confirmation email (add to email queue)
      await emailQueue.add('send-confirmation', {
        to: await getUserEmail(userId),
        template: 'order-confirmation',
        data: { orderId },
      });
      
      return { success: true, orderId, paymentId: payment.id };
    } catch (error) {
      // Compensating transactions
      await handleOrderFailure(orderId, error);
      throw error;
    }
  },
  {
    connection,
    concurrency: 10,
    removeOnComplete: { count: 100 }, // Keep last 100 completed
    removeOnFail: { count: 500 }, // Keep last 500 failed
  }
);

// Job options
const emailJobOptions = {
  attempts: 3,
  backoff: {
    type: 'exponential',
    delay: 2000, // 2s, 4s, 8s
  },
  removeOnComplete: true,
  removeOnFail: false, // Keep for debugging
};

// File: queues/producer.js
class QueueProducer {
  constructor() {
    this.emailQueue = new Queue('emails', { connection });
    this.orderQueue = new Queue('orders', { connection });
    this.fileQueue = new Queue('files', { connection });
  }

  async sendEmail(to, subject, template, data, options = {}) {
    return this.emailQueue.add(
      `email-${template}`,
      { to, subject, template, data, createdAt: new Date().toISOString() },
      {
        ...emailJobOptions,
        ...options,
        jobId: options.jobId || `email-${to}-${Date.now()}`,
      }
    );
  }

  async createOrder(orderData) {
    const job = await this.orderQueue.add(
      'process-order',
      {
        ...orderData,
        createdAt: new Date().toISOString(),
      },
      {
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 1000,
        },
        removeOnComplete: 100,
        removeOnFail: 500,
      }
    );
    
    return job.id;
  }

  async processFile(fileId, type) {
    return this.fileQueue.add(
      'process-file',
      { fileId, type, createdAt: new Date().toISOString() },
      {
        attempts: 5,
        backoff: {
          type: 'exponential',
          delay: 1000,
        },
        priority: type === 'thumbnail' ? 1 : 5, // Thumbnail gets priority
      }
    );
  }

  // Bulk add
  async sendBulkEmails(emails) {
    const jobs = emails.map((email, index) => ({
      name: `email-${email.template}-${index}`,
      data: { ...email, createdAt: new Date().toISOString() },
      opts: emailJobOptions,
    }));
    
    return this.emailQueue.addBulk(jobs);
  }
}

module.exports = { QueueProducer, emailQueue, orderQueue };
```

### Kafka Implementation

```javascript
// File: queues/kafkaSetup.js
const { Kafka, Partitioners } = require('kafkajs');

// Kafka client
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: [
    process.env.KAFKA_BROKER_1 || 'localhost:9092',
    process.env.KAFKA_BROKER_2 || 'localhost:9093',
  ],
  retry: {
    initialRetryTime: 100,
    retries: 8,
  },
});

// Producers
const producer = kafka.producer({
  createPartitioner: Partitioners.DefaultPartitioner,
  allowAutoTopicCreation: true,
});

const admin = kafka.admin();

// File: queues/kafkaProducer.js
class KafkaEventProducer {
  constructor() {
    this.producer = kafka.producer();
  }

  async connect() {
    await this.producer.connect();
    console.log('Kafka producer connected');
  }

  async disconnect() {
    await this.producer.disconnect();
  }

  async publishEvent(topic, eventType, payload, options = {}) {
    const message = {
      key: options.key || payload.id || String(Date.now()),
      value: JSON.stringify({
        id: this.generateUUID(),
        type: eventType,
        payload,
        timestamp: new Date().toISOString(),
        version: '1.0',
        ...options.headers && { headers: options.headers },
      }),
      headers: {
        'correlation-id': options.correlationId || this.generateUUID(),
        'event-type': eventType,
      },
    };

    await this.producer.send({
      topic,
      messages: [message],
    });

    return message.key;
  }

  // User events
  async publishUserCreated(user) {
    return this.publishEvent('user-events', 'user.created', user, {
      key: user.id,
    });
  }

  async publishUserUpdated(user) {
    return this.publishEvent('user-events', 'user.updated', user, {
      key: user.id,
    });
  }

  // Order events
  async publishOrderCreated(order) {
    return this.publishEvent('order-events', 'order.created', order, {
      key: order.userId, // Partition by user
    });
  }

  async publishOrderStatusChanged(orderId, status, previousStatus) {
    return this.publishEvent('order-events', 'order.status_changed', {
      orderId,
      status,
      previousStatus,
    }, {
      key: orderId,
    });
  }

  // Payment events
  async publishPaymentCompleted(payment) {
    return this.publishEvent('payment-events', 'payment.completed', payment, {
      key: payment.orderId,
    });
  }

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}

// File: queues/kafkaConsumer.js
class KafkaEventConsumer {
  constructor(groupId) {
    this.consumer = kafka.consumer({ groupId });
    this.subscriptions = new Map();
  }

  async connect() {
    await this.consumer.connect();
    console.log(`Kafka consumer connected (group: ${this.consumer.groupId})`);
  }

  async subscribe(topic, handler) {
    await this.consumer.subscribe({ topic, fromBeginning: false });
    
    if (!this.subscriptions.has(topic)) {
      this.subscriptions.set(topic, []);
    }
    this.subscriptions.get(topic).push(handler);
  }

  async start() {
    await this.consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const value = JSON.parse(message.value.toString());
        
        console.log({
          topic,
          partition,
          offset: message.offset,
          key: message.key?.toString(),
          value,
        });

        const handlers = this.subscriptions.get(topic) || [];
        for (const handler of handlers) {
          try {
            await handler(value, { topic, partition, offset: message.offset });
          } catch (error) {
            console.error(`Handler error for topic ${topic}:`, error);
          }
        }
      },
    });
  }

  async disconnect() {
    await this.consumer.disconnect();
  }
}

// Usage
async function setupKafkaConsumers() {
  const consumer = new KafkaEventConsumer('order-processing-group');

  await consumer.connect();

  // Subscribe to order events
  await consumer.subscribe('order-events', async (event) => {
    switch (event.type) {
      case 'order.created':
        await handleNewOrder(event.payload);
        break;
      case 'order.status_changed':
        await handleOrderStatusChange(event.payload);
        break;
    }
  });

  // Subscribe to payment events
  await consumer.subscribe('payment-events', async (event) => {
    switch (event.type) {
      case 'payment.completed':
        await handlePaymentCompleted(event.payload);
        break;
    }
  });

  await consumer.start();
}

module.exports = { KafkaEventProducer, KafkaEventConsumer, kafka };
```

---

## 5. Frontend Integration

### Caching on Frontend

```typescript
// File: client/src/api/cachedApiClient.ts
import axios, { AxiosInstance, AxiosError } from 'axios';

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
}

class CachedApiClient {
  private client: AxiosInstance;
  private cache: Map<string, CacheEntry<any>>;
  private cacheTtl: number;

  constructor(baseURL: string, cacheTtl = 60000) {
    this.client = axios.create({ baseURL, timeout: 30000 });
    this.cache = new Map();
    this.cacheTtl = cacheTtl;
  }

  // Check if cache is valid
  private isCacheValid(key: string): boolean {
    const entry = this.cache.get(key);
    if (!entry) return false;
    return Date.now() - entry.timestamp < entry.ttl;
  }

  // Get from cache
  private getFromCache<T>(key: string): T | null {
    if (this.isCacheValid(key)) {
      return this.cache.get(key)!.data;
    }
    return null;
  }

  // Set to cache
  private setCache<T>(key: string, data: T, ttl?: number): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl: ttl || this.cacheTtl,
    });
  }

  // Invalidate cache
  invalidate(key: string): void {
    this.cache.delete(key);
  }

  invalidatePattern(pattern: string): void {
    const regex = new RegExp(pattern.replace('*', '.*'));
    for (const key of this.cache.keys()) {
      if (regex.test(key)) {
        this.cache.delete(key);
      }
    }
  }

  // GET with caching
  async get<T>(url: string, params?: any, options?: { cache?: boolean; ttl?: number; forceRefresh?: boolean }) {
    const cacheKey = `${url}:${JSON.stringify(params || {})}`;
    
    if (!options?.forceRefresh) {
      const cached = this.getFromCache<T>(cacheKey);
      if (cached) return cached;
    }

    const response = await this.client.get<T>(url, { params });
    
    if (options?.cache !== false) {
      this.setCache(cacheKey, response.data, options?.ttl);
    }

    return response.data;
  }

  // POST (invalidates related cache)
  async post<T>(url: string, data?: any) {
    const response = await this.client.post<T>(url, data);
    // Invalidate list caches
    this.invalidatePattern(url.split('/')[1] + '/*');
    return response.data;
  }
}

// Create instances
export const userApiClient = new CachedApiClient('/api/users', 60000); // 1 minute
export const productApiClient = new CachedApiClient('/api/products', 300000); // 5 minutes
export const orderApiClient = new CachedApiClient('/api/orders', 10000); // 10 seconds
```

### Service Worker Caching

```javascript
// File: client/public/sw.js
const CACHE_NAME = 'v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/static/js/main.js',
  '/static/css/main.css',
];

const API_CACHE = 'api-cache-v1';

// Install event - cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // API requests - network first, cache fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Clone and cache successful GET responses
          if (request.method === 'GET' && response.status === 200) {
            const responseClone = response.clone();
            caches.open(API_CACHE).then((cache) => {
              cache.put(request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // Return cached response if network fails
          return caches.match(request);
        })
    );
    return;
  }

  // Static assets - cache first, network fallback
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        // Update cache in background
        fetch(request).then((response) => {
          if (response.status === 200) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, response);
            });
          }
        });
        return cachedResponse;
      }
      return fetch(request);
    })
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME && name !== API_CACHE)
          .map((name) => caches.delete(name))
      );
    })
  );
});

// Background sync for offline form submissions
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-orders') {
    event.waitUntil(syncOrders());
  }
});

async function syncOrders() {
  const db = await openDatabase();
  const orders = await db.getAll('pendingOrders');
  
  for (const order of orders) {
    try {
      await fetch('/api/orders', {
        method: 'POST',
        body: JSON.stringify(order),
        headers: { 'Content-Type': 'application/json' },
      });
      await db.delete('pendingOrders', order.id);
    } catch (error) {
      console.error('Sync failed:', error);
    }
  }
}
```

---

## 6. Real-World Production Examples

### E-commerce Caching Strategy

```javascript
// File: production/ecommerceCaching.js
const ecommerceCachingStrategy = {
  // Homepage - Cache heavily, refresh occasionally
  homepage: {
    ttl: 300, // 5 minutes
    strategy: 'stale-while-revalidate',
    content: ['featuredProducts', 'categories', 'promotions', 'banners'],
  },

  // Product listing - Cache with filters
  productListing: {
    ttl: 60, // 1 minute
    strategy: 'cache-aside',
    varyBy: ['category', 'sort', 'page'],
    keys: ['product:list:{category}:{sort}:{page}'],
  },

  // Product detail - Cache heavily
  productDetail: {
    ttl: 3600, // 1 hour
    strategy: 'cache-aside',
    keys: ['product:{id}'],
    tags: ['product', 'category:{categoryId}', 'brand:{brandId}'],
  },

  // User-specific data - Don't cache!
  userData: {
    cache: false,
    strategy: 'no-store',
    content: ['cart', 'wishlist', 'orders', 'profile'],
  },

  // Session data - Short TTL
  session: {
    ttl: 1800, // 30 minutes
    strategy: 'write-through',
    storage: 'redis',
  },

  // Search results - Cache with search hash
  search: {
    ttl: 60,
    strategy: 'cache-aside',
    keys: ['search:{hash}'],
  },
};

// Full-page caching with Redis
const fullPageCache = {
  async getCachedPage(key) {
    return this.redis.get(`page:${key}`);
  },

  async setCachedPage(key, html, ttl = 300) {
    // Compress before caching
    const compressed = zlib.gzipSync(html);
    await this.redis.setex(`page:${key}`, ttl, compressed);
  },

  async invalidatePage(pattern) {
    const keys = await this.redis.keys(`page:${pattern}`);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  },
};
```

### Real-time Notification System

```javascript
// File: production/notificationSystem.js
const notificationSystem = {
  // Notification types
  types: {
    order: {
      queue: 'order-notifications',
      channels: ['email', 'sms', 'push'],
      priority: 'high',
    },
    message: {
      queue: 'message-notifications',
      channels: ['websocket', 'push'],
      priority: 'high',
    },
    marketing: {
      queue: 'marketing-notifications',
      channels: ['email'],
      priority: 'low',
    },
  },

  // Processing pipeline
  async processNotification(notification) {
    const config = this.types[notification.type];
    
    // Add to appropriate queue
    const job = await notificationQueue.add(
      config.queue,
      notification,
      {
        priority: config.priority === 'high' ? 1 : 10,
        attempts: 3,
        backoff: { type: 'exponential', delay: 1000 },
      }
    );

    return job.id;
  },

  // Worker processes each channel
  async sendEmail(notification) {
    // Template rendering
    const html = await renderTemplate(notification.template, notification.data);
    
    // Send via email service
    await emailService.send({
      to: notification.user.email,
      subject: notification.subject,
      html,
    });

    // Track in analytics
    await analytics.track('notification_sent', {
      type: 'email',
      notificationId: notification.id,
    });
  },

  async sendPush(notification) {
    // Get user's device tokens
    const tokens = await getUserDeviceTokens(notification.userId);
    
    for (const token of tokens) {
      await pushService.send(token, {
        title: notification.title,
        body: notification.body,
        data: notification.data,
      });
    }
  },
};
```

---

## 7. Debugging Guide

### Redis Debugging

```javascript
// File: debugging/redisDebug.js
const redisDebug = {
  // Monitor all commands (use sparingly in production)
  async monitor() {
    const monitor = await this.redis.monitor();
    monitor.on('message', (command) => {
      console.log('Command:', command);
    });
    return monitor;
  },

  // Get slow queries
  async getSlowLog() {
    return this.redis.slowlog('get', 10);
  },

  // Memory analysis
  async memoryStats() {
    return this.redis.memory('stats');
  },

  // Key analysis
  async analyzeKeys(pattern = '*') {
    const keys = await this.redis.keys(pattern);
    const analysis = {
      total: keys.length,
      byType: {},
      bySize: {},
    };

    for (const key of keys.slice(0, 100)) { // Sample first 100
      const type = await this.redis.type(key);
      analysis.byType[type] = (analysis.byType[type] || 0) + 1;
      
      if (type === 'string') {
        const len = await this.redis.strlen(key);
        analysis.bySize[key] = len;
      }
    }

    return analysis;
  },

  // Connection info
  async getConnectionInfo() {
    return this.redis.info('clients');
  },
};

// Cache hit/miss monitoring
const cacheMetrics = {
  hits: 0,
  misses: 0,

  recordHit() {
    this.hits++;
    this.reportMetrics();
  },

  recordMiss() {
    this.misses++;
    this.reportMetrics();
  },

  getHitRate() {
    const total = this.hits + this.misses;
    return total > 0 ? (this.hits / total) * 100 : 0;
  },

  reportMetrics() {
    console.log({
      hits: this.hits,
      misses: this.misses,
      hitRate: this.getHitRate().toFixed(2) + '%',
    });
  },
};
```

### Queue Debugging

```javascript
// File: debugging/queueDebug.js
const queueDebug = {
  // BullMQ queue inspection
  async inspectQueue(queueName) {
    const queue = new Queue(queueName, { connection });
    
    const [waiting, active, completed, failed, delayed] = await Promise.all([
      queue.getWaiting(),
      queue.getActive(),
      queue.getCompleted(),
      queue.getFailed(),
      queue.getDelayed(),
    ]);

    return {
      name: queueName,
      waiting: waiting.length,
      active: active.length,
      completed: completed.length,
      failed: failed.length,
      delayed: delayed.length,
    };
  },

  // Get job details
  async getJobDetails(queueName, jobId) {
    const queue = new Queue(queueName, { connection });
    const job = await queue.getJob(jobId);
    
    if (!job) return null;

    return {
      id: job.id,
      name: job.name,
      status: await job.getState(),
      progress: job.progress,
      attempts: job.attemptsMade,
      data: job.data,
      result: job.returnvalue,
      failedReason: job.failedReason,
      timestamps: {
        created: job.timestamp,
        started: job.processedOn,
        finished: job.finishedOn,
      },
    };
  },

  // Retry failed jobs
  async retryFailedJobs(queueName) {
    const queue = new Queue(queueName, { connection });
    const failed = await queue.getFailed();
    
    for (const job of failed) {
      await job.retry();
    }

    return { retried: failed.length };
  },

  // Clean old jobs
  async cleanQueue(queueName, olderThan = 86400000) {
    const queue = new Queue(queueName, { connection });
    
    const [failed, completed] = await Promise.all([
      queue.clean(olderThan, 100, 'failed'),
      queue.clean(olderThan, 100, 'completed'),
    ]);

    return { failed, completed };
  },
};
```

---

## 8. Tradeoffs

### Caching Tradeoffs

| Cache Type | Pros | Cons |
|------------|------|------|
| **In-Memory** | Fastest (< 1ms) | Lost on restart, not shared |
| **Redis** | Shared, persistent | Network latency |
| **CDN** | Global distribution | Stale data risk |
| **Database Cache** | Transparent | Complex invalidation |

### Queue Tradeoffs

| Queue Type | Pros | Cons |
|------------|------|------|
| **Redis** | Simple, fast | No persistence option |
| **RabbitMQ** | Rich features, ACK | Complex setup |
| **Kafka** | High throughput, persistence | Complex, latency |
| **SQS** | Fully managed, reliable | Vendor lock-in |

### When to Cache vs When to Queue

```javascript
// USE CACHING when:
// - Same data read frequently
// - Data doesn't change often
// - You can afford stale data
// - Performance is critical

const cachingUseCases = [
  'User profiles (read-heavy)',
  'Product catalog',
  'Category listings',
  'Configuration data',
  'Session data',
  'API responses',
];

// USE QUEUES when:
// - Work needs to be done asynchronously
// - You need reliability/retries
// - Workload varies over time
// - Multiple services need events

const queueUseCases = [
  'Sending emails',
  'Processing images',
  'Generating reports',
  'Notifications',
  'Order fulfillment',
  'Audit logging',
];
```

---

## 9. Security Concerns

### Cache Security

```javascript
// File: security/cacheSecurity.js

// 1. Never cache sensitive data
const badCaching = async (req, res) => {
  // BAD - Caching password reset tokens!
  await redis.setex(`reset:${token}`, 300, userId);
  res.json({ message: 'Email sent' });
};

const goodCaching = async (req, res) => {
  // GOOD - Don't cache sensitive data
  // Or use encrypted cache values
  const encrypted = encrypt(token);
  // ... process
  res.json({ message: 'Email sent' });
};

// 2. Rate limit cache access
const rateLimitedCache = {
  async get(key) {
    const rateKey = `rate:get:${req.ip}`;
    const current = await redis.incr(rateKey);
    
    if (current === 1) {
      await redis.expire(rateKey, 60);
    }
    
    if (current > 100) {
      throw new Error('Rate limit exceeded');
    }
    
    return redis.get(key);
  },
};

// 3. Input validation before cache keys
const sanitizeCacheKey = (key) => {
  // Prevent cache poisoning
  return key.replace(/[^a-zA-Z0-9:_-]/g, '').substring(0, 256);
};

// 4. Use separate cache for different tenants
const tenantCache = {
  getKey(key, tenantId) {
    return `tenant:${tenantId}:${sanitizeCacheKey(key)}`;
  },
};
```

### Queue Security

```javascript
// File: security/queueSecurity.js

// 1. Validate messages
const validateMessage = (message) => {
  const schema = {
    type: 'object',
    required: ['type', 'payload'],
    properties: {
      type: { type: 'string' },
      payload: { type: 'object' },
    },
  };
  
  const { error } = ajv.validate(schema, message);
  if (error) {
    throw new Error('Invalid message format');
  }
};

// 2. Sanitize queue names
const sanitizeQueueName = (name) => {
  return name.replace(/[^a-zA-Z0-9-]/g, '').substring(0, 128);
};

// 3. Limit queue sizes
const queueOptions = {
  maxSize: 10000, // Maximum messages
  maxSizeBytes: 1024 * 1024 * 100, // 100MB
  messageTtl: 86400000, // 24 hours
};

// 4. Dead letter queues for failed messages
const dlqOptions = {
  deadLetterExchange: 'dlx',
  deadLetterRoutingKey: 'dead-letter',
};
```

---

## 10. Performance Optimization

### Cache Optimization

```javascript
// File: performance/cacheOptimization.js

// 1. Pipeline multiple operations
const pipelineExample = async (keys) => {
  const pipeline = redis.pipeline();
  
  keys.forEach((key) => {
    pipeline.get(key);
  });
  
  const results = await pipeline.exec();
  return results.map(([err, value]) => err ? null : JSON.parse(value));
};

// 2. Use Redis hashes for grouped data
const hashExample = async (userId) => {
  // Instead of multiple keys
  await redis.setex(`user:${userId}:name`, 3600, 'John');
  await redis.setex(`user:${userId}:email`, 3600, 'john@example.com');
  
  // Use hash
  await redis.hset(`user:${userId}`, {
    name: 'John',
    email: 'john@example.com',
    created: Date.now(),
  });
  
  // Get all
  const user = await redis.hgetall(`user:${userId}`);
  
  // Get specific field
  const name = await redis.hget(`user:${userId}`, 'name');
};

// 3. Use sorted sets for leaderboards
const leaderboard = {
  async addScore(userId, score) {
    await redis.zadd('leaderboard', score, userId);
  },

  async getTop(n = 10) {
    return redis.zrevrange('leaderboard', 0, n - 1, 'WITHSCORES');
  },

  async getRank(userId) {
    return redis.zrevrank('leaderboard', userId);
  },
};

// 4. Use Lua scripts for atomic operations
const luaScript = `
  local key = KEYS[1]
  local limit = tonumber(ARGV[1])
  local window = tonumber(ARGV[2])
  
  local current = tonumber(redis.call('GET', key) or '0')
  if current >= limit then
    return 0
  end
  
  redis.call('INCR', key)
  if current == 0 then
    redis.call('EXPIRE', key, window)
  end
  
  return 1
`;

const rateLimitScript = redis.defineCommand('rateLimit', {
  numberOfKeys: 1,
  lua: luaScript,
});
```

### Queue Optimization

```javascript
// File: performance/queueOptimization.js

// 1. Batch processing
const batchProcessor = new Worker('batch', async (job) => {
  const { batch } = job.data;
  
  // Process in batches of 100
  const chunks = _.chunk(batch, 100);
  
  for (const chunk of chunks) {
    await bulkProcess(chunk);
    job.updateProgress(/* progress */);
  }
}, { concurrency: 5 });

// 2. Prioritized queues
const prioritizedWorker = new Worker('tasks', async (job) => {
  // Higher priority jobs run first
}, {
  connection,
  defaultJobOptions: {
    priority: 1,
  },
});

// Add with priority
await queue.add('task', data, { priority: 1 }); // High
await queue.add('task', data, { priority: 10 }); // Low

// 3. Scalable workers
// Multiple worker instances can process from same queue
const scalableWorker = new Worker('tasks', processTask, {
  connection,
  concurrency: 10,
  lockDuration: 30000, // Auto-extend lock
});

// 4. Backpressure handling
const backpressureWorker = new Worker('tasks', async (job) => {
  const activeCount = await queue.getActiveCount();
  
  if (activeCount > 1000) {
    // Pause processing
    await scalableWorker.pause();
    
    // Wait for queue to drain
    while (await queue.getActiveCount() > 100) {
      await new Promise(r => setTimeout(r, 1000));
    }
    
    await scalableWorker.resume();
  }
});
```

---

## 11. Scaling Challenges

### Distributed Caching

```javascript
// File: scaling/distributedCache.js

// Redis Cluster for horizontal scaling
const redisCluster = new Redis.Cluster([
  { host: '10.0.0.1', port: 6379 },
  { host: '10.0.0.2', port: 6379 },
  { host: '10.0.0.3', port: 6379 },
], {
  redisOptions: {
    password: process.env.REDIS_PASSWORD,
  },
  slotsRefreshTimeout: 10000,
});

// Consistent hashing for key distribution
class ConsistentHashCache {
  constructor(nodes) {
    this.ring = {};
    this.sortedKeys = [];
    this.nodes = nodes;
    this.buildRing();
  }

  buildRing() {
    for (const node of this.nodes) {
      for (let i = 0; i < 100; i++) {
        const key = this.hash(`${node}:${i}`);
        this.ring[key] = node;
        this.sortedKeys.push(key);
      }
    }
    this.sortedKeys.sort((a, b) => a - b);
  }

  getNode(key) {
    const hash = this.hash(key);
    for (const sortedKey of this.sortedKeys) {
      if (hash <= sortedKey) {
        return this.ring[sortedKey];
      }
    }
    return this.ring[this.sortedKeys[0]];
  }
}

// Local cache + distributed cache
class MultiLayerCache {
  constructor() {
    this.local = new LRUCache(1000); // Local LRU
    this.distributed = redisCluster;
  }

  async get(key) {
    // Try local first
    let value = this.local.get(key);
    if (value) return value;

    // Try distributed
    value = await this.distributed.get(key);
    if (value) {
      this.local.set(key, value); // Populate local
    }

    return value;
  }
}
```

### Queue Scaling

```javascript
// File: scaling/queueScaling.js

// Auto-scaling workers based on queue depth
class QueueScaler {
  constructor(queue, workerOptions) {
    this.queue = queue;
    this.workerOptions = workerOptions;
    this.workers = [];
    this.minWorkers = 1;
    this.maxWorkers = 20;
  }

  async start() {
    await this.scale();
    // Check every 30 seconds
    this.interval = setInterval(() => this.scale(), 30000);
  }

  async scale() {
    const jobCounts = await this.queue.getJobCounts();
    const totalJobs = jobCounts.waiting + jobCounts.active;
    
    // Calculate target workers
    let targetWorkers = Math.ceil(totalJobs / 10); // 1 worker per 10 jobs
    targetWorkers = Math.max(this.minWorkers, Math.min(this.maxWorkers, targetWorkers));

    if (targetWorkers > this.workers.length) {
      // Add workers
      for (let i = this.workers.length; i < targetWorkers; i++) {
        const worker = new Worker(this.queue.name, this.workerOptions);
        this.workers.push(worker);
        console.log(`Added worker ${i + 1}`);
      }
    } else if (targetWorkers < this.workers.length) {
      // Remove workers
      while (this.workers.length > targetWorkers) {
        const worker = this.workers.pop();
        await worker.close();
        console.log('Removed worker');
      }
    }
  }

  async stop() {
    clearInterval(this.interval);
    for (const worker of this.workers) {
      await worker.close();
    }
  }
}
```

---

## 12. Best Practices

### Caching Best Practices

```markdown
# Caching Best Practices

## 1. Cache Strategy Selection
- Read-heavy: Cache-aside
- Write-heavy: Write-through
- Complex data: Read-through

## 2. TTL Selection
- Static content: Long TTL (hours/days)
- User-generated: Medium TTL (minutes)
- Real-time: Short TTL or no cache
- Never cache: Passwords, tokens, payment data

## 3. Cache Invalidation
- Time-based expiration
- Event-based invalidation
- Version-based keys
- Tag-based invalidation

## 4. Key Naming
- Consistent pattern: {entity}:{id}:{field}
- Include version: user:123:v2:profile
- Use namespaced keys: app:module:key

## 5. Monitoring
- Hit/miss ratio
- Memory usage
- Eviction rate
- Latency percentiles

## 6. Security
- Never cache sensitive data
- Encrypt if necessary
- Rate limit cache access
- Separate caches by tenant
```

### Queue Best Practices

```markdown
# Queue Best Practices

## 1. Message Design
- Idempotent messages
- Include correlation IDs
- Version messages
- Keep payloads small

## 2. Error Handling
- Dead letter queues
- Retry with backoff
- Max retry limits
- Alert on failures

## 3. Monitoring
- Queue depth
- Processing time
- Error rate
- Worker utilization

## 4. Ordering
- Use sequence numbers if needed
- Partition by entity for ordering
- Accept eventual ordering if acceptable

## 5. Scaling
- Horizontal worker scaling
- Multiple queue consumers
- Auto-scaling based on depth

## 6. Testing
- Test with realistic payloads
- Test retry logic
- Test dead letter handling
- Load test for throughput
```

---

## 13. Common Mistakes

### Caching Mistakes

```javascript
// MISTAKE 1: Caching everything
// BAD - Caching user-specific data
app.get('/api/user/profile', async (req, res) => {
  const profile = await getProfile(req.user.id);
  await redis.setex(`user:${req.user.id}`, 3600, JSON.stringify(profile));
  res.json(profile);
});
// Problem: Different users get each other's data!

// GOOD - Cache by user ID
app.get('/api/user/profile', async (req, res) => {
  const cacheKey = `user:${req.user.id}:profile`;
  const cached = await redis.get(cacheKey);
  if (cached) return res.json(JSON.parse(cached));
  
  const profile = await getProfile(req.user.id);
  await redis.setex(cacheKey, 3600, JSON.stringify(profile));
  res.json(profile);
});

// MISTAKE 2: No cache invalidation strategy
// BAD - Cache never invalidated
app.post('/api/user', async (req, res) => {
  const user = await createUser(req.body);
  // Cache updated but old data still in cache!
  await redis.setex(`user:${user.id}`, 3600, JSON.stringify(user));
  res.json(user);
});

// GOOD - Define invalidation strategy
app.post('/api/user', async (req, res) => {
  const user = await createUser(req.body);
  // Add to cache
  await redis.setex(`user:${user.id}`, 3600, JSON.stringify(user));
  // Invalidate list caches
  await redis.del('users:list:*');
  res.json(user);
});

// MISTAKE 3: Too long TTL
// BAD - Data becomes stale
await redis.setex('config', 86400, JSON.stringify(config)); // 24 hours!
// Problem: Config changed but users still see old!

// GOOD - Appropriate TTL
await redis.setex('config', 300, JSON.stringify(config)); // 5 minutes
// Or use event-based invalidation
```

### Queue Mistakes

```javascript
// MISTAKE 1: Not handling failures
// BAD - Job fails silently
worker.process(async (job) => {
  await processOrder(job.data);
  // No error handling!
});

// GOOD - Proper error handling
worker.process(async (job) => {
  try {
    await processOrder(job.data);
  } catch (error) {
    console.error('Order processing failed:', error);
    throw error; // Re-throw to trigger retry
  }
});

// MISTAKE 2: No idempotency
// BAD - Processing same message twice
worker.process(async (job) => {
  await sendEmail(job.data.email);
  // If job fails and retries, email sent twice!
});

// GOOD - Make idempotent
worker.process(async (job) => {
  const { email, orderId } = job.data;
  
  // Check if already processed
  const sent = await redis.get(`email:sent:${orderId}`);
  if (sent) return; // Already sent
  
  await sendEmail(email);
  
  // Mark as sent
  await redis.setex(`email:sent:${orderId}`, 86400, '1');
});

// MISTAKE 3: Not monitoring queues
// BAD - No visibility into queue health
const worker = new Worker('orders', handler);
// No monitoring = blind!

// GOOD - Monitor everything
worker.on('completed', (job) => {
  metrics.increment('queue.jobs.completed');
});
worker.on('failed', (job, err) => {
  metrics.increment('queue.jobs.failed');
  alert('Job failed:', job.id);
});
worker.on('progress', (job, progress) => {
  metrics.gauge('queue.job.progress', progress);
});
```

---

## 14. Interview Questions

### Caching & Queues Interview Q&A

```markdown
Q1: What is cache invalidation and why is it hard?
A: Cache invalidation = removing/update stale data from cache.
   It's hard because:
   - Multiple cache layers
   - Distributed systems
   - Race conditions
   - Complex dependencies

Q2: Difference between cache-aside and write-through?
A: Cache-aside: App manages cache manually. Write to DB, then cache.
   Write-through: Write to cache and DB simultaneously.
   Cache-aside = lazy, Write-through = eager.

Q3: What is thundering herd problem?
A: When cache expires, multiple requests try to fetch same data.
   Solutions: Locks, probabilistic early expiration, randomized TTL.

Q4: When would you use a message queue?
A: - Async processing (emails, notifications)
   - Decoupling services
   - Handling bursts
   - Reliable task execution
   - Event-driven architecture

Q5: Difference between queues and event streaming?
A: Queues (SQS, RabbitMQ): Point-to-point, message deleted after read.
   Streams (Kafka): Multiple consumers can read same message.

Q6: What is dead letter queue?
A: Queue for failed messages after max retries.
   Allows inspection/debugging without losing data.

Q7: How do you ensure message ordering?
A: - Single consumer
   - Partition by entity (all events for user X go to same partition)
   - Use sequence numbers
   - Accept eventual ordering
```

---

## 15. Latest 2026 Fullstack Engineering Patterns

### Modern Caching & Queue Patterns 2026

```typescript
// 1. Edge Caching with Cloudflare Workers
// File: edge/caching.ts
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    // Cache at edge for 1 hour
    const cache = await caches.default.match(request);
    if (cache) {
      // Return stale, but update in background
      fetch(request).then(async (response) => {
        if (response.ok) {
          const newCache = new Response(response.body, response);
          newCache.headers.set('Cache-Control', 'public, max-age=3600');
          await caches.default.put(request, newCache);
        }
      });
      
      return cache;
    }
    
    const response = await fetch(request);
    
    if (response.ok) {
      const newCache = new Response(response.body, response);
      newCache.headers.set('Cache-Control', 'public, max-age=3600');
      await caches.default.put(request, newCache);
    }
    
    return response;
  },
};

// 2. Serverless Queue Processing
// File: serverless/queueHandler.ts
import { SQSEvent, SQSHandler } from 'aws-lambda';

export const processOrderQueue: SQSHandler = async (event: SQSEvent) => {
  for (const record of event.Records) {
    const order = JSON.parse(record.body);
    
    try {
      await processOrder(order);
    } catch (error) {
      // Move to DLQ after retries
      if (record.messageId) {
        await sqs.sendMessage({
          QueueUrl: process.env.DEAD_LETTER_QUEUE_URL!,
          MessageBody: JSON.stringify({
            original: order,
            error: (error as Error).message,
          }),
        });
      }
    }
  }
};

// 3. Real-time with Redis Streams
// File: realtime/redisStreams.ts
class RedisStreamService {
  async addEvent(stream: string, event: object) {
    return this.redis.xadd(stream, '*', ...this.flatten(event));
  }

  async consumeStream(stream: string, group: string, consumer: string) {
    // Create consumer group if not exists
    try {
      await this.redis.xgroup('CREATE', stream, group, '0');
    } catch (e) {
      // Group already exists
    }

    // Read new messages
    const messages = await this.redis.xreadgroup(
      'GROUP', group, consumer,
      'COUNT', 10,
      'BLOCK', 5000,
      'STREAMS', stream, '>'
    );

    return messages;
  }

  async acknowledge(stream: string, group: string, messageId: string) {
    await this.redis.xack(stream, group, messageId);
  }
}

// 4. CQRS with Event Sourcing
// File: cqrs/eventSourcing.ts
class EventSourcedOrder {
  async apply(event: Event) {
    switch (event.type) {
      case 'OrderCreated':
        this.state = { status: 'CREATED', ...event.data };
        break;
      case 'OrderPaid':
        this.state.status = 'PAID';
        break;
      case 'OrderShipped':
        this.state.status = 'SHIPPED';
        break;
    }
    
    // Store event
    await eventStore.append(event);
    
    // Rebuild projections
    await projections.rebuild(event);
  }
}

// 5. Vector Cache for AI
// File: ai/vectorCache.ts
import { Pinecone } from '@pinecone-database/pinecone';

class VectorCache {
  async index(embeddings: number[], metadata: object) {
    return this.pinecone.index('embeddings').upsert([{
      id: crypto.randomUUID(),
      values: embeddings,
      metadata,
    }]);
  }

  async search(queryEmbedding: number[], topK: number = 5) {
    const results = await this.pinecone.index('embeddings')
      .query({
        vector: queryEmbedding,
        topK,
        includeMetadata: true,
      });
    
    return results.matches;
  }
}
```

---

## Summary

Bhai, caching aur queues dono performance aur reliability ke liye bahut important hain:

1. **Caching** - Data ko fast access ke liye store karo
2. **Queues** - Async processing aur reliability ke liye
3. **Redis** - Best for caching, sessions, pub/sub
4. **BullMQ** - Task queue for Node.js
5. **Kafka** - Event streaming, high throughput
6. **Cache Invalidation** - Sabse mushkil kaam!
7. **2026 Trends** - Edge caching, serverless queues, vector databases

Remember: Caching solution nahi, optimization hai. Pehle application ko seedha karo, phir cache karo!

---

*Previous: [Backend Architecture](./Backend_Architecture.md) | Next: [Realtime Backend](./Realtime_Backend.md)*
