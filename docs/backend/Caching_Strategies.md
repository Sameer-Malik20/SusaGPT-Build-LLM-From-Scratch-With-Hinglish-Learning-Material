# 💾 Caching Strategies - High-Performance Data Access
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Caching systems design, implementation, aur optimization master karna
## 🧭 Core Concepts (Concept-First)
+- Caching Fundamentals: Understanding cache benefits, trade-offs, and why caching improves performance
+- Cache Hierarchy: Client-side, application, database, distributed, and specialized caching layers
+- Caching Strategies: HTTP caching, Redis/Memcached, query caching, and CDN implementations
+- Cache Invalidation: Techniques for maintaining data consistency when underlying data changes
+- Performance Optimization: Cache warming, prefetching, and monitoring cache hit/miss ratios
+- Practical Implementation: Code examples, configuration patterns, and production considerations
---

## 📋 Table of Contents: Caching Stack

| Layer | Cache Type | Technologies |
|-------|-----------|--------------|
| **Client-side** | Browser caching, CDN | HTTP caching, CloudFront |
| **Application** | In-memory cache | Redis, Memcached |
| **Database** | Query cache, Buffer pool | MySQL query cache, PostgreSQL |
| **Distributed** | Distributed cache | Redis Cluster, Memcached |
| **Specialized** | Search cache, Session cache | Elasticsearch, Redis |

---

## 1. 🎯 Caching Fundamentals

### A. Cache Benefits & Trade-offs

#### Benefits:
- **Performance:** 10-100x faster data access
- **Scalability:** Reduced database load
- **Availability:** Fallback during outages
- **Cost reduction:** Fewer database resources

#### Trade-offs:
- **Complexity:** Cache invalidation challenges
- **Consistency:** Stale data risk
- **Memory usage:** Resource consumption
- **Debugging difficulty:** Harder to trace issues

### B. Cache Hit/Miss Analysis

#### Cache Hit Ratio Calculation:
```
Cache Hit Ratio = (Number of cache hits) / (Total requests) × 100%

Example:
- Total requests: 10,000
- Cache hits: 8,500
- Cache misses: 1,500
- Hit ratio: 85%
```

#### Performance Impact:
```javascript
// Without cache: 100ms database call
const user = await db.users.findById(userId); // 100ms

// With cache: 1ms cache + occasional 100ms database
let user = await cache.get(`user:${userId}`);
if (!user) {
    user = await db.users.findById(userId); // 100ms (on miss)
    await cache.set(`user:${userId}`, user, 3600); // 1ms
}
// Total: 1ms (hit) or 101ms (miss)
```

---

## 2. 🏪 Client-side Caching

### A. HTTP Caching Headers

#### Browser Cache Control:
```http
# Strong caching (1 year)
Cache-Control: public, max-age=31536000, immutable
ETag: "abc123"
Last-Modified: Wed, 15 Jan 2024 10:30:00 GMT

# Weak caching (revalidation required)
Cache-Control: public, max-age=3600, must-revalidate
ETag: "def456"

# No caching
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0
```

#### CDN Caching:
```javascript
// CloudFront distribution configuration
const distributionConfig = {
    DefaultCacheBehavior: {
        TargetOriginId: 'api-gateway',
        ViewerProtocolPolicy: 'redirect-to-https',
        MinTTL: 0,
        DefaultTTL: 3600, // 1 hour
        MaxTTL: 86400,    // 1 day
        ForwardedValues: {
            QueryString: false,
            Cookies: { Forward: 'none' },
            Headers: ['Authorization']
        }
    }
};
```

### B. Service Worker Caching

#### Progressive Web App Caching:
```javascript
// service-worker.js
const CACHE_NAME = 'v1';
const urlsToCache = [
    '/',
    '/styles/main.css',
    '/scripts/app.js',
    '/images/logo.png'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Cache hit - return response
                if (response) {
                    return response;
                }
                
                // Clone the request
                const fetchRequest = event.request.clone();
                
                return fetch(fetchRequest).then(response => {
                    // Check if valid response
                    if (!response || response.status !== 200) {
                        return response;
                    }
                    
                    // Clone response and cache it
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                });
            })
    );
});
```

---

## 3. ⚡ Application-level Caching

### A. Redis Implementation

#### Basic Redis Operations:
```javascript
const redis = require('redis');
const client = redis.createClient();

// String operations
await client.set('user:1001', JSON.stringify(user));
await client.expire('user:1001', 3600); // 1 hour TTL

const userJson = await client.get('user:1001');
const user = JSON.parse(userJson);

// Hash operations
await client.hSet('user:1001', 'name', 'John Doe');
await client.hSet('user:1001', 'email', 'john@example.com');
await client.expire('user:1001', 3600);

const userName = await client.hGet('user:1001', 'name');
```

#### Advanced Redis Patterns:
```javascript
// Pipeline multiple operations
const pipeline = client.multi();
pipeline.set('key1', 'value1');
pipeline.set('key2', 'value2');
pipeline.expire('key1', 3600);
pipeline.expire('key2', 3600);
await pipeline.exec();

// Lua scripting for atomic operations
const script = `
    local current = redis.call('GET', KEYS[1])
    if current then
        redis.call('SET', KEYS[1], current + ARGV[1])
    else
        redis.call('SET', KEYS[1], ARGV[1])
    end
`;
await client.eval(script, 1, 'counter', 1);
```

### B. Cache-Aside Pattern

#### Implementation:
```javascript
class UserService {
    constructor(db, cache) {
        this.db = db;
        this.cache = cache;
    }
    
    async getUser(userId) {
        const cacheKey = `user:${userId}`;
        
        // Try cache first
        let user = await this.cache.get(cacheKey);
        if (user) {
            console.log('Cache hit for user:', userId);
            return JSON.parse(user);
        }
        
        console.log('Cache miss for user:', userId);
        // Cache miss - fetch from database
        user = await this.db.users.findById(userId);
        
        if (user) {
            // Set cache with TTL
            await this.cache.setex(cacheKey, 3600, JSON.stringify(user));
        }
        
        return user;
    }
    
    async updateUser(userId, updates) {
        // Update database
        const user = await this.db.users.update(userId, updates);
        
        // Invalidate cache
        await this.cache.del(`user:${userId}`);
        
        return user;
    }
}
```

---

## 4. 🔄 Cache Invalidation Strategies

### A. Time-based Invalidation

#### TTL (Time-to-Live):
```javascript
// Simple TTL-based caching
await cache.setex('popular_products', 300, JSON.stringify(products)); // 5 minutes

// Stale-while-revalidate pattern
async function getDataWithSWR(key, fetchFunction, ttl = 300, staleTtl = 600) {
    let data = await cache.get(key);
    
    if (data) {
        const ttlRemaining = await cache.ttl(key);
        
        // If data is stale but not expired, return stale data and refresh in background
        if (ttlRemaining < 0) {
            data = JSON.parse(data);
            
            // Refresh in background
            setTimeout(async () => {
                try {
                    const freshData = await fetchFunction();
                    await cache.setex(key, ttl + staleTtl, JSON.stringify(freshData));
                } catch (error) {
                    console.error('Background refresh failed:', error);
                }
            }, 0);
            
            return data;
        }
        
        return JSON.parse(data);
    }
    
    // Cache miss
    data = await fetchFunction();
    await cache.setex(key, ttl + staleTtl, JSON.stringify(data));
    return data;
}
```

### B. Event-based Invalidation

#### Write-through Cache:
```javascript
class WriteThroughCache {
    constructor(db, cache) {
        this.db = db;
        this.cache = cache;
    }
    
    async set(key, value) {
        // Write to database first
        await this.db.set(key, value);
        
        // Then update cache
        await this.cache.set(key, value);
    }
    
    async get(key) {
        let value = await this.cache.get(key);
        
        if (!value) {
            // Cache miss - read from database
            value = await this.db.get(key);
            
            if (value) {
                // Update cache
                await this.cache.set(key, value);
            }
        }
        
        return value;
    }
}
```

#### Write-behind Cache:
```javascript
class WriteBehindCache {
    constructor(db, cache, batchSize = 100, flushInterval = 5000) {
        this.db = db;
        this.cache = cache;
        this.batchSize = batchSize;
        this.flushInterval = flushInterval;
        this.writeQueue = new Map();
        this.startFlushWorker();
    }
    
    async set(key, value) {
        // Write to cache immediately
        await this.cache.set(key, value);
        
        // Queue for database write
        this.writeQueue.set(key, value);
        
        // Flush if queue reaches batch size
        if (this.writeQueue.size >= this.batchSize) {
            await this.flushToDatabase();
        }
    }
    
    startFlushWorker() {
        setInterval(async () => {
            if (this.writeQueue.size > 0) {
                await this.flushToDatabase();
            }
        }, this.flushInterval);
    }
    
    async flushToDatabase() {
        const batch = Array.from(this.writeQueue.entries());
        this.writeQueue.clear();
        
        try {
            await this.db.batchWrite(batch);
        } catch (error) {
            // Retry logic or dead letter queue
            console.error('Batch write failed:', error);
        }
    }
}
```

---

## 5. 🌐 Distributed Caching

### A. Redis Cluster Setup

#### Cluster Configuration:
```javascript
const Redis = require('ioredis');
const cluster = new Redis.Cluster([
    { host: 'redis-node-1', port: 6379 },
    { host: 'redis-node-2', port: 6379 },
    { host: 'redis-node-3', port: 6379 }
], {
    scaleReads: 'slave',
    retryDelayOnFailover: 100,
    maxRedirections: 16
});

// Automatic key distribution
await cluster.set('user:1001', 'user data'); // Goes to appropriate node
const user = await cluster.get('user:1001');   // Fetched from correct node
```

#### Sharding Strategies:
```javascript
// Consistent hashing for key distribution
function getShardKey(key, totalShards) {
    const hash = crypto.createHash('md5').update(key).digest('hex');
    const shardIndex = parseInt(hash.substring(0, 8), 16) % totalShards;
    return shardIndex;
}

// Shard-aware client
class ShardedRedisClient {
    constructor(shards) {
        this.shards = shards;
    }
    
    async set(key, value) {
        const shardIndex = getShardKey(key, this.shards.length);
        return await this.shards[shardIndex].set(key, value);
    }
    
    async get(key) {
        const shardIndex = getShardKey(key, this.shards.length);
        return await this.shards[shardIndex].get(key);
    }
}
```

### B. Cache Coherence Patterns

#### Read-Through Cache:
```javascript
class ReadThroughCache {
    constructor(fetchFunction, cache) {
        this.fetchFunction = fetchFunction;
        this.cache = cache;
    }
    
    async get(key) {
        let value = await this.cache.get(key);
        
        if (!value) {
            value = await this.fetchFunction(key);
            
            if (value) {
                await this.cache.set(key, value);
            }
        }
        
        return value;
    }
}

// Usage
const userCache = new ReadThroughCache(
    async (userId) => await db.users.findById(userId),
    redisClient
);

const user = await userCache.get('1001');
```

---

## 6. 📊 Cache Monitoring & Optimization

### A. Performance Metrics

#### Key Cache Metrics:
- **Hit ratio:** Percentage of cache hits
- **Latency:** Average response time
- **Memory usage:** Cache size and utilization
- **Eviction rate:** How often items are removed
- **Network usage:** For distributed caches

#### Redis Monitoring:
```bash
# Redis CLI monitoring
redis-cli info stats
redis-cli info memory
redis-cli info keyspace

# Custom metrics collection
const usedMemory = await client.info('memory');
const keyspace = await client.info('keyspace');
const stats = await client.info('stats');
```

### B. Cache Optimization Techniques

#### Memory Optimization:
```javascript
// Use efficient data structures
// Instead of storing entire objects
await client.set('user:1001:name', 'John Doe');
await client.set('user:1001:email', 'john@example.com');

// Use hashes for related data
await client.hSet('user:1001', {
    name: 'John Doe',
    email: 'john@example.com',
    lastLogin: Date.now()
});

// Compression for large values
const zlib = require('zlib');
const compressed = zlib.deflateSync(JSON.stringify(largeObject));
await client.set('large:data', compressed);
```

#### Cache Warming:
```javascript
// Pre-load cache during startup
async function warmCache() {
    const popularUsers = await db.users.findPopular();
    
    for (const user of popularUsers) {
        await cache.set(`user:${user.id}`, user, 3600);
    }
    
    const recentProducts = await db.products.findRecent();
    await cache.set('recent_products', recentProducts, 300);
}

// Schedule periodic warming
setInterval(warmCache, 300000); // Every 5 minutes
```

---

## 7. 🧪 Practical Caching Exercises

### Exercise 1: Cache Implementation
1. Redis cache setup karo local environment mein
2. Cache-aside pattern implement karo user service ke liye
3. Performance testing conduct karo with and without cache
4. Hit ratio aur latency metrics measure karo

### Exercise 2: Cache Invalidation
1. Write-through cache implement karo
2. Event-based invalidation add karo
3. Cache coherence test karo multiple clients ke saath
4. Race conditions handle karo

### Exercise 3: Distributed Caching
1. Redis cluster setup simulate karo
2. Sharding strategy implement karo
3. Failover testing conduct karo
4. Performance under load test karo

---

## 📚 Resources

### Caching Technologies
- **Redis Documentation:** In-memory data structure store
- **Memcached Documentation:** Distributed memory caching
- **CDN Providers:** CloudFront, Cloudflare, Akamai
- **HTTP Caching:** MDN Web Docs

### Learning Resources
- "Designing Data-Intensive Applications" (Book)
- Redis University: Free Redis courses
- High Scalability: Caching patterns and case studies

### Monitoring Tools
- **Redis Insight:** Redis GUI and monitoring
- **Prometheus:** Metrics collection
- **Grafana:** Visualization and dashboards
- **New Relic:** Application performance monitoring

---

## 🏆 Checklist
- [ ] Different caching layers understand kar sakte hain
- [ ] Cache-aside pattern implement kar sakte hain
- [ ] Cache invalidation strategies apply kar sakte hain
- [ ] Distributed caching setup kar sakte hain
- [ ] Performance monitoring conduct kar sakte hain
- [ ] Cache optimization techniques implement kar sakte hain
- [ ] Real-world caching scenarios handle kar sakte hain

> **Pro Tip:** Caching complexity comes from invalidation. Start simple with TTL-based caching, then gradually add sophistication. Always measure cache effectiveness with hit ratios and latency metrics.