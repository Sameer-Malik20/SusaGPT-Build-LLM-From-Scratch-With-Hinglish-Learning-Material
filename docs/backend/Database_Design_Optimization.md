# 🗄️ Database Design & Optimization - Scalable Data Architecture
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Database design, optimization, aur scaling techniques master karna

---

## 📋 Table of Contents: Database Stack

| Area | Focus | Technologies |
|------|-------|--------------|
| **Database Design** | Schema design, Normalization | PostgreSQL, MySQL |
| **Query Optimization** | Performance tuning, Indexing | SQL optimization |
| **Scalability** | Sharding, Replication | Horizontal scaling |
| **NoSQL** | Document, Key-Value, Graph | MongoDB, Redis, Neo4j |
| **Data Modeling** | Relationships, Constraints | ER diagrams, Data types |

---

## 1. 🏗️ Database Design Principles

### A. Normalization Process

#### 1. **First Normal Form (1NF)**
- Atomic values (no repeating groups)
- Primary key for each row

```sql
-- Before 1NF (repeating groups)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    items VARCHAR(255) -- "item1,item2,item3"
);

-- After 1NF (atomic values)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    item_name VARCHAR(100),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

#### 2. **Second Normal Form (2NF)**
- 1NF + no partial dependencies
- All non-key attributes depend on entire primary key

#### 3. **Third Normal Form (3NF)**
- 2NF + no transitive dependencies
- Non-key attributes depend only on primary key

### B. Denormalization Strategies

#### When to Denormalize:
- **Read-heavy workloads:** Frequent queries with joins
- **Performance requirements:** Faster read operations
- **Reporting systems:** Aggregated data access

```sql
-- Denormalized table for performance
CREATE TABLE user_orders_summary (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100),
    total_orders INT,
    total_amount DECIMAL(10,2),
    last_order_date DATE
);

-- Instead of joining multiple tables every time
```

---

## 2. ⚡ Query Optimization

### A. Indexing Strategies

#### 1. **B-tree Indexes (Most Common)**
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (multiple columns)
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Partial index (filtered)
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Unique index
CREATE UNIQUE INDEX idx_users_username ON users(username);
```

#### 2. **Index Selection Guidelines**
- **High cardinality columns:** Good for indexing
- **Frequently queried columns:** Worth indexing
- **Foreign keys:** Usually benefit from indexes
- **Low cardinality columns:** Poor indexing candidates

### B. Query Performance Analysis

#### EXPLAIN Command:
```sql
EXPLAIN ANALYZE 
SELECT u.name, o.order_date, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.country = 'India'
AND o.order_date >= '2024-01-01';

-- Output analysis:
-- Seq Scan vs Index Scan
-- Filter conditions
-- Join type (Nested Loop, Hash Join, Merge Join)
```

#### Query Optimization Techniques:
```sql
-- Avoid SELECT *
SELECT id, name, email FROM users WHERE active = true;

-- Use WHERE clauses effectively
SELECT * FROM orders 
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
AND status = 'completed';

-- Limit results appropriately
SELECT * FROM products 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 0;
```

---

## 3. 📈 Database Scaling

### A. Vertical Scaling

#### 1. **Hardware Upgrades**
- **CPU:** More cores for parallel processing
- **RAM:** Larger buffer pool for caching
- **Storage:** Faster SSDs for I/O operations
- **Network:** Higher bandwidth for replication

#### 2. **Database Configuration**
```sql
-- PostgreSQL configuration
shared_buffers = '25% of total RAM'  -- Cache size
effective_cache_size = '75% of total RAM'  -- OS cache estimation
work_mem = '256MB'  -- Memory for sorting/hashing
maintenance_work_mem = '1GB'  -- Maintenance operations
```

### B. Horizontal Scaling

#### 1. **Read Replicas**
```sql
-- Primary database (writes)
-- Replica databases (reads)

-- Application configuration
const dbConfig = {
  write: {
    host: 'primary-db.example.com',
    port: 5432
  },
  read: [
    { host: 'replica1.example.com', port: 5432 },
    { host: 'replica2.example.com', port: 5432 }
  ]
};
```

#### 2. **Sharding Strategies**
```sql
-- Range-based sharding
-- Shard 1: user_id 1-1000000
-- Shard 2: user_id 1000001-2000000

-- Hash-based sharding
shard_id = hash(user_id) % total_shards

-- Geographic sharding
-- Shard 1: North America users
-- Shard 2: Europe users
-- Shard 3: Asia users
```

---

## 4. 🔄 NoSQL Databases

### A. Document Databases (MongoDB)

#### Document Structure:
```javascript
// User document with embedded orders
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  name: "John Doe",
  email: "john@example.com",
  address: {
    street: "123 Main St",
    city: "Mumbai",
    country: "India"
  },
  orders: [
    {
      order_id: "ORD001",
      date: ISODate("2024-01-15"),
      total: 2999.99,
      items: [
        { product_id: "P001", quantity: 2, price: 999.99 }
      ]
    }
  ]
}
```

#### MongoDB Indexing:
```javascript
// Single field index
db.users.createIndex({ email: 1 });

// Compound index
db.orders.createIndex({ user_id: 1, order_date: -1 });

// Text index for search
db.products.createIndex({ name: "text", description: "text" });

// Geospatial index
db.stores.createIndex({ location: "2dsphere" });
```

### B. Key-Value Stores (Redis)

#### Redis Data Structures:
```javascript
// Strings
SET user:1001:name "John Doe"
SET user:1001:email "john@example.com"

// Hashes
HSET user:1001 name "John Doe" email "john@example.com"

// Lists
LPUSH recent_users "user:1001"
LPUSH recent_users "user:1002"

// Sets
SADD online_users "user:1001"

// Sorted Sets
ZADD leaderboard 100 "player:1001"
ZADD leaderboard 95 "player:1002"
```

#### Redis Caching Patterns:
```javascript
// Cache aside pattern
async function getUser(userId) {
  const cacheKey = `user:${userId}`;
  
  // Try cache first
  let user = await redis.get(cacheKey);
  if (user) {
    return JSON.parse(user);
  }
  
  // Cache miss - fetch from database
  user = await db.users.findById(userId);
  if (user) {
    // Set cache with expiration
    await redis.setex(cacheKey, 3600, JSON.stringify(user));
  }
  
  return user;
}
```

---

## 5. 📊 Data Modeling

### A. Entity-Relationship Diagrams

#### ERD Components:
```
Entities: User, Order, Product, Category
Attributes: id, name, email, created_at
Relationships: One-to-Many, Many-to-Many
```

#### Relationship Types:
```sql
-- One-to-Many
Users (1) → (Many) Orders

-- Many-to-Many (via junction table)
Users (Many) ←→ (Many) Products
-- Junction table: User_Products

-- One-to-One
Users (1) ←→ (1) User_Profiles
```

### B. Advanced Data Types

#### PostgreSQL Advanced Types:
```sql
-- JSON/JSONB for flexible data
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    attributes JSONB,  -- Flexible attributes
    created_at TIMESTAMP DEFAULT NOW()
);

-- Array types
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    items TEXT[],  -- Array of item names
    quantities INT[]  -- Array of quantities
);

-- Enumerated types
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered');
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    status order_status DEFAULT 'pending'
);
```

---

## 6. 🔧 Performance Monitoring

### A. Database Metrics

#### Key Performance Indicators:
- **Query throughput:** Queries per second
- **Latency:** Average response time
- **Connection pool usage:** Active connections
- **Cache hit ratio:** Buffer cache effectiveness
- **Lock contention:** Waiting transactions

#### Monitoring Queries:
```sql
-- Active queries
SELECT pid, query, state, age(clock_timestamp(), query_start) as duration
FROM pg_stat_activity 
WHERE state != 'idle' 
ORDER BY duration DESC;

-- Table sizes and bloat
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage statistics
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_all_indexes 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY idx_scan DESC;
```

### B. Optimization Techniques

#### Query Rewriting:
```sql
-- Original query (inefficient)
SELECT * FROM orders 
WHERE EXTRACT(YEAR FROM order_date) = 2024;

-- Optimized query
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' 
AND order_date < '2025-01-01';

-- Using date ranges instead of functions
```

#### Connection Pooling:
```javascript
// Using connection pools
const { Pool } = require('pg');
const pool = new Pool({
  host: 'localhost',
  database: 'mydb',
  user: 'dbuser',
  password: 'password',
  port: 5432,
  max: 20, // maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Use pool instead of direct connections
const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
```

---

## 7. 🧪 Practical Exercises

### Exercise 1: Database Design
1. E-commerce system ka complete database design karo
2. Normalization rules apply karo
3. Indexing strategy define karo
4. ER diagram create karo

### Exercise 2: Query Optimization
1. Slow queries identify karo
2. EXPLAIN ANALYZE use karo performance analysis ke liye
3. Queries optimize karo
4. Indexes add karo where beneficial

### Exercise 3: Scaling Strategy
1. Read replica setup simulate karo
2. Sharding strategy design karo
3. Caching implementation add karo
4. Performance testing conduct karo

---

## 📚 Resources

### Database Documentation
- **PostgreSQL Documentation:** Comprehensive SQL reference
- **MySQL Documentation:** Popular relational database
- **MongoDB University:** Free NoSQL courses
- **Redis Documentation:** In-memory data structure store

### Learning Platforms
- **DB-Engines:** Database comparison and rankings
- **Use The Index, Luke:** SQL indexing guide
- **SQL Performance Explained:** Query optimization book

### Tools & Utilities
- **pgAdmin:** PostgreSQL administration tool
- **MySQL Workbench:** MySQL GUI tool
- **Redis Insight:** Redis GUI client
- **MongoDB Compass:** MongoDB GUI tool

---

## 🏆 Checklist
- [ ] Database normalization principles apply kar sakte hain
- [ ] Query optimization techniques implement kar sakte hain
- [ ] Indexing strategies design kar sakte hain
- [ ] Scaling strategies implement kar sakte hain
- [ ] NoSQL databases use kar sakte hain
- [ ] Data modeling aur ER diagrams create kar sakte hain
- [ ] Performance monitoring aur optimization conduct kar sakte hain

> **Pro Tip:** Database performance optimization iterative process hai. Regular monitoring, analysis, aur incremental improvements karte raho. Always test changes in staging environment before production deployment.