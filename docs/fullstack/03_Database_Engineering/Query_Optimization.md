# Query Optimization: Complete Guide for Fullstack Engineers

## Hinglish Explanation (Beginner Level)

Bhai, query optimization matlab apni database queries ko fast banana. Jaise tum agar library mein ek book dhundh rahe ho, toh agar tum systematically shelf check karoge toh jaldi milega - database bhi similarly indexes aur optimized queries se fast results deta hai.

Socho tumhari database mein lakho records hain. Agar tum simple query likhte ho:
```sql
SELECT * FROM users WHERE name = 'Rahul'
```

Toh database ko har ek row check karna padega (full table scan) - yeh slow hai. Lekin agar tum `name` field pe index banao:
```sql
CREATE INDEX idx_users_name ON users(name)
```

Toh ab database directly 'Rahul' wale records find kar lega - yeh bahut fast hai!

**Query optimization ke key concepts:**
1. **Indexing** - Data ko quickly find karne ka tarika
2. **EXPLAIN plans** - Dekho query kaise execute ho rahi hai
3. **Query rewriting** - Same result with better performance
4. **Connection pooling** - Resources efficiently use karna

## Deep Technical Explanation

Query optimization is the process of improving the performance of database queries through various techniques including indexing, query restructuring, and configuration tuning.

### How Database Query Processing Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Query Processing Pipeline                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  1. PARSING                                                   │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  SQL Query ──► Parse Tree ──► Abstract Syntax Tree (AST) │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                               │                                       │
│                               ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  2. QUERY REWRITING (Logical Optimization)                      │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  • Subquery flattening                                    │  │  │
│  │  │  • View merging                                          │  │  │
│  │  │  • Predicate pushdown                                     │  │  │
│  │  │  • Constant folding                                       │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                               │                                       │
│                               ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  3. COST-BASED OPTIMIZATION                                    │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  Statistics:                                             │  │  │
│  │  │  • Table cardinality (row count)                         │  │  │
│  │  │  • Column distinct values                                │  │  │
│  │  │  • Data distribution (histograms)                        │  │  │
│  │  │  • Index statistics                                     │  │  │
│  │  │                                                           │  │  │
│  │  │  Cost Model:                                              │  │  │
│  │  │  • I/O cost (disk reads)                                 │  │  │
│  │  │  • CPU cost (row processing)                             │  │  │
│  │  │  • Memory usage                                          │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                               │                                       │
│                               ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  4. PLAN GENERATION (Physical Optimization)                    │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │                                                           │  │  │
│  │  │  Sequential Scan  ──► Full table scan                   │  │  │
│  │  │        │                                               │  │  │
│  │  │        ▼                                               │  │  │
│  │  │  Index Scan ──► B-tree, Hash, GIN, GiST               │  │  │
│  │  │        │                                               │  │  │
│  │  │        ▼                                               │  │  │
│  │  │  Nested Loop ──► For JOINs                            │  │  │
│  │  │        │                                               │  │  │
│  │  │        ▼                                               │  │  │
│  │  │  Hash Join ──► Large joins                            │  │  │
│  │  │        │                                               │  │  │
│  │  │        ▼                                               │  │  │
│  │  │  Merge Join ──► Sorted inputs                         │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                               │                                       │
│                               ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  5. PLAN EXECUTION                                             │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  Execute chosen plan, return results                     │  │  │
│  │  │  Monitor execution, collect statistics                   │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Index Types and Their Uses

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Index Types                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  B-TREE INDEX (Default in PostgreSQL, MySQL)                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │       Root                                                     │  │
│  │      /    \\                                                    │  │
│  │    [50]    [75]                                               │  │
│  │    /  \\   /  \\                                              │  │
│  │  [10] [25][60] [90]                                         │  │
│  │  ...   ...  ...   ...                                        │  │
│  │                                                               │  │
│  │  Use for: =, <, >, <=, >=, BETWEEN, LIKE 'prefix%'          │  │
│  │  Example: CREATE INDEX ON users(email);                       │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  HASH INDEX                                                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Key          │  Hash Value                                   │  │
│  │  ─────────────┼────────────────────                          │  │
│  │  "rahul"      │  0x7f3a2b1c                                 │  │
│  │  "priya"      │  0x9a1b2c3d                                 │  │
│  │                                                               │  │
│  │  Use for: =, IN, equality checks only                        │  │
│  │  Example: CREATE INDEX ON sessions(token) USING HASH;         │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  GIN INDEX (Generalized Inverted Index)                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  Document: ["javascript", "tutorial", "beginners"]          │  │
│  │                                                               │  │
│  │  Inverted Index:                                             │  │
│  │  ┌─────────────────┐                                         │  │
│  │  │ Term           │ DocIDs                                   │  │
│  │  ├─────────────────┼────────────────────                     │  │
│  │  │ javascript      │ [1, 3, 5, 7, ...]                       │  │
│  │  │ tutorial        │ [1, 2, 4, 8, ...]                       │  │
│  │  │ beginners       │ [1, 5, 9, ...]                          │  │
│  │  └─────────────────┘                                         │  │
│  │                                                               │  │
│  │  Use for: Full-text search, JSONB containment                 │  │
│  │  Example: CREATE INDEX ON articles USING GIN(search_vector); │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  GiST INDEX (Generalized Search Tree)                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  Use for: Geospatial (PostGIS), Range types, Full-text       │  │
│  │  Example:                                                     │  │
│  │  CREATE INDEX ON locations USING GIST(coordinates);           │  │
│  │                                                               │  │
│  │  Supports:                                                    │  │
│  │  • KNN queries (nearest neighbor)                            │  │
│  │  • Bounding box searches                                      │  │
│  │  • Overlap checks                                            │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Query Execution Plans

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EXPLAIN ANALYZE Output Example                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)                            │
│  SELECT u.name, COUNT(o.id) as order_count                          │
│  FROM users u                                                       │
│  LEFT JOIN orders o ON u.id = o.user_id                             │
│  WHERE u.created_at > '2025-01-01'                                  │
│  GROUP BY u.id                                                      │
│  ORDER BY order_count DESC                                          │
│  LIMIT 10;                                                          │
│                                                                      │
│  Output:                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  Limit  (cost=100.50..102.00 rows=10 width=24)                │  │
│  │        (actual time=5.234..5.567 rows=10 loops=1)            │  │
│  │  Buffers: shared hit=234 read=56                              │  │
│  │    ->  Sort  (cost=100.50..100.75 rows=10 width=24)           │  │
│  │          (actual time=5.200..5.345 rows=10 loops=1)          │  │
│  │          Sort Key: (count(o.id)) DESC                        │  │
│  │          Sort Method: top-N heapsort  Memory: 26kB            │  │
│  │          Buffers: shared hit=234 read=56                      │  │
│  │          ->  HashAggregate  (cost=50.00..75.00 rows=100 ...) │  │
│  │                (actual time=3.456..4.123 rows=100 loops=1)   │  │
│  │                Group Key: u.id                                │  │
│  │                Buffers: shared hit=234 read=56               │  │
│  │                ->  Hash Left Join  (cost=25.00..50.00 ...)    │  │
│  │                      (actual time=1.234..2.567 rows=1000 ...) │  │
│  │                      Hash Cond: (u.id = o.user_id)            │  │
│  │                      Buffers: shared hit=234 read=56          │  │
│  │                      ->  Seq Scan on users u  (cost=0..25 ...)│  │
│  │                            (actual time=0.010..0.456 rows=500)│  │
│  │                            Filter: (created_at > '2025-01-01')│  │
│  │                            Rows Removed by Filter: 400        │  │
│  │                            Buffers: shared hit=200            │  │
│  │                      ->  Hash  (cost=12.50..25.00 ...)       │  │
│  │                            (actual time=0.500..0.800 rows=1000)│  │
│  │                            Buckets: 1024  Batches: 1         │  │
│  │                            ->  Seq Scan on orders o           │  │
│  │                                  (cost=0..12.50 rows=1000)   │  │
│  │                                  Buffers: shared hit=34 read=56│  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Key Metrics:                                                        │
│  • cost=...: Estimated cost (before actual=...: actual execution)  │
│  • rows=X: Estimated rows returned                                  │
│  • Buffers: Pages read from cache (hit) vs disk (read)             │
│  • Seq Scan: Full table scan - consider adding index                │
│  • Rows Removed by Filter: Rows eliminated after scan              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Frontend + Backend Integration Examples

### PostgreSQL Query Optimization with Prisma

```typescript
// src/services/product.service.ts
import { PrismaClient, Prisma } from '@prisma/client';

const prisma = new PrismaClient();

// ============================================
// OPTIMIZATION 1: SELECT ONLY NEEDED COLUMNS
// ============================================

// BAD: Selecting all columns
async function getProductsBad() {
  return prisma.product.findMany({
    where: { isActive: true },
  }); // Returns: id, name, description, price, stock, images, created_at...
}

// GOOD: Select only needed columns
async function getProductsGood() {
  return prisma.product.findMany({
    where: { isActive: true },
    select: {
      id: true,
      name: true,
      slug: true,
      price: true,
      images: {
        select: { url: true },
        where: { isPrimary: true },
        take: 1,
      },
    },
  });
}

// ============================================
// OPTIMIZATION 2: USE CURSOR-BASED PAGINATION
// ============================================

// BAD: OFFSET pagination (slow for large datasets)
async function getProductsOffset(page: number, limit: number) {
  return prisma.product.findMany({
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { createdAt: 'desc' },
  });
}

// GOOD: Cursor-based pagination (efficient)
async function getProductsCursor(cursor?: string, limit: number = 20) {
  return prisma.product.findMany({
    take: limit + 1, // Take one extra to check if there's more
    ...(cursor && {
      cursor: { id: cursor },
      skip: 1,
    }),
    orderBy: { createdAt: 'desc' },
    select: {
      id: true,
      name: true,
      price: true,
      createdAt: true,
    },
  });
}

// ============================================
// OPTIMIZATION 3: USE RAW QUERIES FOR COMPLEX AGGREGATIONS
// ============================================

async function getProductAnalytics(productId: string) {
  // Prisma aggregation is limited
  const result = await prisma.$queryRaw`
    SELECT 
      p.id,
      p.name,
      COUNT(DISTINCT o.id) as order_count,
      SUM(oi.quantity) as total_sold,
      AVG(oi.unit_price) as avg_price,
      MAX(o.created_at) as last_order_date,
      p.stock_quantity
    FROM products p
    LEFT JOIN order_items oi ON p.id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.id
    WHERE p.id = ${productId}
    GROUP BY p.id, p.name, p.stock_quantity
  `;

  return result[0];
}

// ============================================
// OPTIMIZATION 4: BATCH OPERATIONS
// ============================================

// BAD: Individual queries in loop
async function updateProductPricesBad(updates: Array<{ id: string; price: number }>) {
  for (const update of updates) {
    await prisma.product.update({
      where: { id: update.id },
      data: { price: update.price },
    });
  }
}

// GOOD: Batch update with raw SQL
async function updateProductPricesGood(updates: Array<{ id: string; price: number }>) {
  if (updates.length === 0) return;

  // Use raw SQL for bulk update
  await prisma.$executeRaw`
    UPDATE products AS p
    SET price = CASE p.id
      ${Prisma.join(
        updates.map(u => Prisma.sql`WHEN ${u.id} THEN ${u.price}`),
        ' '
      )}
      ELSE p.price
    END,
    updated_at = NOW()
    WHERE p.id IN (${Prisma.join(updates.map(u => u.id))})
  `;
}

// ============================================
// OPTIMIZATION 5: EXPLAIN QUERY PLAN
// ============================================

async function explainQuery(query: string) {
  const result = await prisma.$queryRaw<Array<{ "Query Plan": string }>>`
    EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
    ${Prisma.raw(query)}
  `;
  return result.map(r => r["Query Plan"]).join('\n');
}
```

### MongoDB Query Optimization with Mongoose

```typescript
// src/services/product.service.ts
import mongoose, { Model, PipelineStage } from 'mongoose';

// ============================================
// OPTIMIZATION 1: USE PROJECTION
// ============================================

// BAD: Returns all fields
async function getProductsBad() {
  return Product.find({ isActive: true });
}

// GOOD: Only return needed fields
async function getProductsGood() {
  return Product.find(
    { isActive: true },
    { name: 1, slug: 1, price: 1, 'images.url': 1 } // Projection
  );
}

// ============================================
// OPTIMIZATION 2: EXPLAIN QUERY
// ============================================

async function analyzeQuery() {
  const explanation = await Product.find({
    category: new mongoose.Types.ObjectId('category-id'),
    isActive: true,
  })
  .sort({ createdAt: -1 })
  .explain('executionStats');

  // Key metrics
  console.log({
    nReturned: explanation.executionStats.nReturned,
    totalDocsExamined: explanation.executionStats.totalDocsExamined,
    executionTimeMillis: explanation.executionStats.executionTimeMillis,
    indexUsed: explanation.executionStats.executionStages.inputStages?.[0]?.indexName,
  });

  // Should aim for: nReturned close to totalDocsExamined
  // If totalDocsExamined >> nReturned, need better index
}

// ============================================
// OPTIMIZATION 3: AGGREGATION PIPELINE OPTIMIZATION
// ============================================

async function getProductStats(categoryId: string) {
  const pipeline: PipelineStage[] = [
    // $match FIRST to reduce document flow
    { $match: { 
      category: new mongoose.Types.ObjectId(categoryId),
      isActive: true,
    }},
    
    // $lookup with pipeline for better performance
    { $lookup: {
      from: 'orders',
      let: { productId: '$_id' },
      pipeline: [
        { $match: { 
          $expr: { $in: ['$$productId', '$items.productId'] },
          createdAt: { $gte: new Date('2025-01-01') },
        }},
        { $group: { _id: null, totalSold: { $sum: '$items.quantity' }}},
      ],
      as: 'sales',
    }},
    
    // Unwind and handle missing data
    { $unwind: { 
      path: '$sales', 
      preserveNullAndEmptyArrays: true 
    }},
    
    // Add computed fields
    { $addFields: {
      totalSold: { $ifNull: ['$sales.totalSold', 0] },
      revenue: { 
        $multiply: [{ $ifNull: ['$sales.totalSold', 0] }, '$price'] 
      },
    }},
    
    // Project final fields
    { $project: {
      name: 1,
      price: 1,
      stock: 1,
      totalSold: 1,
      revenue: 1,
      roi: { $divide: ['$revenue', '$costPrice'] },
    }},
    
    // Sort and limit
    { $sort: { revenue: -1 }},
    { $limit: 100 },
  ];

  return Product.aggregate(pipeline);
}

// ============================================
// OPTIMIZATION 4: USE COVERED INDEX QUERIES
// ============================================

// Query that can be served entirely from index
async function getProductNames(categoryId: string) {
  // Index: { category: 1, name: 1, _id: 1 }
  return Product.find(
    { category: new mongoose.Types.ObjectId(categoryId), isActive: true },
    { name: 1 } // Only name field, no need to access document
  ).hint({ category: 1, name: 1 }); // Force index usage
}

// ============================================
// OPTIMIZATION 5: PIPELINE FOR PAGINATION
// ============================================

async function getPaginatedProducts(page: number, limit: number, filters: any) {
  const pipeline: PipelineStage[] = [
    // Match stage
    { $match: {
      isActive: true,
      ...(filters.category && { 
        category: new mongoose.Types.ObjectId(filters.category) 
      }),
      ...(filters.minPrice && { price: { $gte: filters.minPrice } }),
      ...(filters.maxPrice && { price: { $lte: filters.maxPrice } }),
    }},
    
    // Facet for pagination + data in single query
    { $facet: {
      metadata: [
        { $count: 'total' },
        { $addFields: { 
          page, 
          totalPages: { $ceil: { $divide: ['$total', limit] }},
        }},
      ],
      data: [
        { $sort: { [filters.sort || 'createdAt']: -1 }},
        { $skip: (page - 1) * limit },
        { $limit: limit },
        { $project: { name: 1, price: 1, images: 1 }},
      ],
    }},
  ];

  const [result] = await Product.aggregate(pipeline);
  return {
    products: result.data,
    total: result.metadata[0]?.total || 0,
    page,
    totalPages: result.metadata[0]?.totalPages || 0,
  };
}
```

### API Routes with Query Optimization

```typescript
// src/routes/product.routes.ts
import { Router, Request, Response } from 'express';
import { productService } from '../services/product.service';
import { z } from 'zod';

const router = Router();

const productQuerySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
  category: z.string().optional(),
  minPrice: z.coerce.number().positive().optional(),
  maxPrice: z.coerce.number().positive().optional(),
  sort: z.enum(['price', '-price', 'createdAt', '-createdAt', 'name']).default('-createdAt'),
  cursor: z.string().optional(), // For cursor pagination
});

// GET /api/products - Optimized listing
router.get('/', async (req: Request, res: Response) => {
  try {
    const params = productQuerySchema.parse(req.query);

    let result;
    if (params.cursor) {
      // Cursor-based pagination (faster for large datasets)
      result = await productService.getProductsCursor(params.cursor, params.limit);
    } else {
      // Offset pagination
      result = await productService.getPaginatedProducts(params);
    }

    res.json({
      success: true,
      ...result,
    });
  } catch (error) {
    res.status(400).json({ success: false, error: (error as Error).message });
  }
});

// GET /api/products/analytics/:id - Complex analytics
router.get('/analytics/:id', async (req: Request, res: Response) => {
  try {
    const analytics = await productService.getProductAnalytics(req.params.id);
    res.json({ success: true, data: analytics });
  } catch (error) {
    res.status(500).json({ success: false, error: (error as Error).message });
  }
});

// GET /api/products/explain - Debug query plan
router.get('/explain', async (req: Request, res: Response) => {
  if (process.env.NODE_ENV !== 'development') {
    return res.status(403).json({ success: false, message: 'Only available in development' });
  }

  try {
    const { query } = req.query;
    const plan = await productService.explainQuery(query as string);
    res.json({ success: true, plan });
  } catch (error) {
    res.status(400).json({ success: false, error: (error as Error).message });
  }
});
```

## Real-World Production Examples

### Example 1: Real-time Dashboard Optimization

```sql
-- Dashboard queries must be fast (<100ms)
-- Use materialized views for pre-aggregation

-- 1. Create materialized view for dashboard metrics
CREATE MATERIALIZED VIEW dashboard_metrics AS
SELECT 
    date_trunc('day', o.created_at) as date,
    p.category_id,
    c.name as category_name,
    COUNT(DISTINCT o.id) as order_count,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(o.total) as revenue,
    AVG(o.total) as avg_order_value,
    SUM(oi.quantity) as items_sold
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE o.status NOT IN ('cancelled', 'refunded')
GROUP BY 1, 2, 3
WITH DATA;

-- Create unique index for concurrent refresh
CREATE UNIQUE INDEX ON dashboard_metrics(date, category_id);

-- 2. Create indexes for filtering
CREATE INDEX ON dashboard_metrics(date DESC);

-- 3. Refresh function (schedule with pg_cron)
CREATE OR REPLACE FUNCTION refresh_dashboard()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard_metrics;
END;
$$ LANGUAGE plpgsql;

-- Add to crontab: 0 */15 * * * SELECT refresh_dashboard();

-- 4. Fast dashboard query (<50ms)
SELECT 
    date,
    category_name,
    order_count,
    unique_customers,
    revenue,
    avg_order_value
FROM dashboard_metrics
WHERE date >= NOW() - INTERVAL '30 days'
ORDER BY date DESC, revenue DESC;
```

### Example 2: Search Optimization with Elasticsearch-style

```sql
-- PostgreSQL full-text search (Elasticsearch alternative)
-- 1. Add search vector column
ALTER TABLE products ADD COLUMN search_vector TSVECTOR;

-- 2. Create trigger to auto-update search vector
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW.tags, ' '), '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_search_vector_update
    BEFORE INSERT OR UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- 3. Create GIN index
CREATE INDEX idx_products_search ON products USING GIN(search_vector);

-- 4. Optimized search query
CREATE OR REPLACE FUNCTION search_products(
    search_query TEXT,
    category_filter UUID DEFAULT NULL,
    min_price DECIMAL DEFAULT NULL,
    max_price DECIMAL DEFAULT NULL,
    page INT DEFAULT 1,
    page_size INT DEFAULT 20
)
RETURNS TABLE (
    id UUID,
    name VARCHAR(500),
    slug VARCHAR(500),
    price DECIMAL,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.name,
        p.slug,
        p.price,
        ts_rank(p.search_vector, plainto_tsquery('english', search_query)) as rank
    FROM products p
    WHERE 
        p.is_active = true
        AND p.search_vector @@ plainto_tsquery('english', search_query)
        AND (category_filter IS NULL OR p.category_id = category_filter)
        AND (min_price IS NULL OR p.price >= min_price)
        AND (max_price IS NULL OR p.price <= max_price)
    ORDER BY rank DESC, p.name
    LIMIT page_size
    OFFSET (page - 1) * page_size;
END;
$$ LANGUAGE plpgsql;

-- Usage: SELECT * FROM search_products('javascript tutorial', NULL, 100, 500, 1, 20);
```

### Example 3: Time-Series Optimization

```sql
-- Partitioning and clustering for time-series data
-- 1. Create partitioned table
CREATE TABLE events (
    id BIGSERIAL,
    event_type VARCHAR(100),
    user_id UUID,
    properties JSONB,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- 2. Create monthly partitions
CREATE TABLE events_2026_01 
    PARTITION OF events FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE events_2026_02 
    PARTITION OF events FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- 3. Create BRIN index (efficient for sorted data)
CREATE INDEX idx_events_brin ON events_2026_01 USING BRIN(created_at);

-- 4. Create B-tree index for common queries
CREATE INDEX idx_events_user_type ON events_2026_01(user_id, event_type);

-- 5. Optimize queries for partition pruning
-- PostgreSQL automatically selects correct partition
SELECT * FROM events 
WHERE created_at >= '2026-01-15' 
  AND created_at < '2026-01-20'
  AND event_type = 'page_view';

-- 6. Automated partition creation
CREATE OR REPLACE FUNCTION create_monthly_partition()
RETURNS void AS $$
DECLARE
    partition_date DATE;
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    partition_date := date_trunc('month', NOW()) + INTERVAL '1 month';
    partition_name := 'events_' || to_char(partition_date, 'YYYY_MM');
    start_date := partition_date::DATE;
    end_date := (partition_date + INTERVAL '1 month')::DATE;
    
    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF events 
         FOR VALUES FROM (%L) TO (%L)',
        partition_name, start_date, end_date
    );
END;
$$ LANGUAGE plpgsql;
```

## Failure Cases

### Case 1: Missing Index Causing Full Table Scan

```sql
-- BAD: Full table scan on 10 million rows
SELECT * FROM orders 
WHERE customer_email = 'rahul@example.com';

-- Check with EXPLAIN
EXPLAIN SELECT * FROM orders WHERE customer_email = 'rahul@example.com';
-- Output: Seq Scan on orders (cost=0..100000 rows=1)

-- SOLUTION: Add index
CREATE INDEX idx_orders_customer_email ON orders(customer_email);

-- Now check again
EXPLAIN SELECT * FROM orders WHERE customer_email = 'rahul@example.com';
-- Output: Index Scan using idx_orders_customer_email (cost=0..5 rows=1)
```

### Case 2: Function on Indexed Column

```sql
-- BAD: Function prevents index usage
SELECT * FROM users 
WHERE LOWER(email) = 'rahul@example.com';

-- EXPLAIN shows: Seq Scan (function on column)

-- SOLUTION 1: Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'rahul@example.com';
-- Now uses index

-- SOLUTION 2: Trigram index for LIKE
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_users_email_trgm ON users USING GIN(email gin_trgm_ops);
SELECT * FROM users WHERE email ILIKE '%rahul%';
```

### Case 3: Too Many Indexes

```sql
-- BAD: Many indexes on write-heavy table
-- Each INSERT/UPDATE must update ALL indexes
-- Table: 1GB, Indexes: 5GB

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan;

-- Find unused indexes
SELECT 
    schemaname || '.' || tablename as table,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelid NOT IN (
    SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
)
ORDER BY pg_relation_size(indexrelid) DESC;

-- Drop unused indexes
DROP INDEX IF EXISTS idx_unused;
```

## Debugging Guide

### PostgreSQL Query Analysis

```sql
-- Enable query logging
-- Add to postgresql.conf:
-- log_min_duration_statement = 1000  -- Log queries > 1s
-- log_statement = 'all'

-- Find slow queries
SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Table statistics
SELECT 
    schemaname,
    relname,
    n_live_tup,
    n_dead_tup,
    n_mod_since_analyze,
    last_vacuum,
    last_autovacuum,
    last_analyze
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Index statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Check bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    n_dead_tup,
    CASE 
        WHEN n_live_tup > 0 
        THEN ROUND(100.0*n_dead_tup/(n_live_tup+n_dead_tup), 2)
        ELSE 0
    END as dead_tuple_percent
FROM pg_stat_user_tables
ORDER BY dead_tuple_percent DESC;
```

### MongoDB Query Analysis

```javascript
// Enable profiling
db.setProfilingLevel(2, { slowms: 100 });

// Find slow operations
db.system.profile.find({ millis: { $gt: 100 } }).sort({ ts: -1 }).limit(10);

// Check query execution
db.products.find({ category: ObjectId('...') }).explain('executionStats');

// Check indexes
db.products.getIndexes();

// Find missing indexes (slow queries without index)
db.products.aggregate([
  { $stage: { $indexStats: {} }},
  { $group: { 
      _id: '$name',
      accesses: { $sum: 1 }
  }},
  { $sort: { accesses: -1 }},
  { $limit: 10 }
]);

// Check collection statistics
db.products.stats();
db.products.stats({ indexDetails: true });
```

## Tradeoffs

### Index vs No Index

| Aspect | Without Index | With Index |
|--------|---------------|-------------|
| SELECT Speed | Slow for large tables | Fast |
| INSERT/UPDATE | Faster | Slower (index updates) |
| Storage | Less | More |
| Memory | Less | More |
| Best For | Write-heavy | Read-heavy |

### Covering Index vs Regular Index

| Aspect | Regular Index | Covering Index |
|--------|--------------|----------------|
| Size | Smaller | Larger |
| SELECT Speed | May need table access | Faster (index-only) |
| UPDATE Speed | Faster | Slower |
| Best For | Specific filters | Queries with SELECT |

## Security Concerns

### Query Injection Prevention

```typescript
// BAD: SQL Injection vulnerability
const query = `SELECT * FROM users WHERE email = '${userInput}'`;

// GOOD: Parameterized queries
const result = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = ${userInput}
`;

// GOOD: ORM with proper escaping
const result = await prisma.user.findMany({
  where: { email: userInput },
});

// Validate and sanitize all inputs
import { z } from 'zod';
const userInputSchema = z.string().email().max(255);
const validated = userInputSchema.parse(userInput);
```

## Performance Optimization

### Connection Pooling

```typescript
// PostgreSQL with PgBouncer
const connectionString = process.env.DATABASE_URL;
const url = new URL(connectionString);

// Pool settings
url.searchParams.set('connection_limit', '20');
url.searchParams.set('pool_timeout', '10');
url.searchParams.set('statement_timeout', '30000');

// Prisma configuration
const prisma = new PrismaClient({
  datasources: { db: { url: url.toString() } },
  log: process.env.NODE_ENV === 'development' ? ['query'] : ['error'],
});
```

### Caching Strategies

```typescript
// Redis caching layer
class QueryCache {
  constructor(private redis: typeof redis, private ttl = 300) {}

  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(`query:${key}`);
    return cached ? JSON.parse(cached) : null;
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    await this.redis.setex(
      `query:${key}`,
      ttl || this.ttl,
      JSON.stringify(value)
    );
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(`query:${pattern}`);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}

// Cache-aside pattern
async function getProductsCached(categoryId: string) {
  const cacheKey = `products:cat:${categoryId}`;
  
  // Try cache
  const cached = await queryCache.get<Product[]>(cacheKey);
  if (cached) return cached;
  
  // Query database
  const products = await prisma.product.findMany({
    where: { categoryId, isActive: true },
  });
  
  // Cache result
  await queryCache.set(cacheKey, products, 300); // 5 min TTL
  
  return products;
}
```

## Best Practices

### 1. Always Analyze Query Plans

```sql
-- Before deployment, always check EXPLAIN
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE customer_id = $1;
```

### 2. Monitor Slow Queries

```typescript
// Middleware to log slow queries
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    if (duration > 1000) {
      console.warn(`Slow request: ${req.method} ${req.path} - ${duration}ms`);
    }
  });
  next();
});
```

### 3. Use Connection Pooling

```typescript
// Prisma with pool settings
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: `${process.env.DATABASE_URL}?connection_limit=10&pool_timeout=20`,
    },
  },
});
```

## Common Mistakes

### Mistake 1: SELECT *

```sql
-- BAD: Returns all columns including large text fields
SELECT * FROM products;

-- GOOD: Select only needed columns
SELECT id, name, slug, price FROM products WHERE is_active = true;
```

### Mistake 2: Not Using Pagination

```sql
-- BAD: Returns thousands of rows
SELECT * FROM orders;

-- GOOD: Paginate results
SELECT * FROM orders ORDER BY created_at DESC LIMIT 100 OFFSET 0;
```

### Mistake 3: Functions on Columns

```sql
-- BAD: Prevents index usage
SELECT * FROM users WHERE YEAR(created_at) = 2026;

-- GOOD: Use range queries
SELECT * FROM users WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01';
```

## Interview Questions

### Q1: What is the difference between clustered and non-clustered indexes?

**Answer**: Clustered index determines physical data order (one per table, usually PK). Non-clustered index is separate structure pointing to data (multiple allowed). PostgreSQL uses heap storage, MySQL InnoDB uses clustered PK.

### Q2: What is a covering index?

**Answer**: A covering index includes all columns needed by a query, allowing index-only scans without accessing the table. Created with INCLUDE clause in SQL Server or covering columns in index definition.

### Q3: What is query plan?

**Answer**: Query plan shows how database will execute a query, including scan types, join methods, sort operations, and cost estimates. Use EXPLAIN (ANALYZE, BUFFERS) to view.

### Q4: What is partition pruning?

**Answer**: Partition pruning eliminates irrelevant partitions from query execution. Only partitions containing relevant data are scanned. Achieved through partition key predicates in WHERE clause.

### Q5: What is BRIN index?

**Answer**: Block Range Index - stores min/max values for block ranges. Efficient for naturally ordered data (timestamps) and uses minimal space. Inefficient for random data distribution.

### Q6: How to optimize a slow query?

**Answer**: Use EXPLAIN ANALYZE to identify bottlenecks. Check for sequential scans, missing indexes, incorrect join order. Add covering indexes, rewrite queries, consider materialized views.

### Q7: What is N+1 query problem?

**Answer**: N+1 occurs when fetching parent records then N queries for each child's related data. Solutions: JOIN, include/eager loading, batch loading, or data loader pattern.

## Latest 2026 Fullstack Engineering Patterns

### Pattern 1: AI-Powered Query Optimization

```typescript
// Using AI to suggest indexes and query improvements
class QueryOptimizer {
  async analyzeAndSuggest(query: string) {
    // Get current query plan
    const currentPlan = await this.explain(query);
    
    // Send to AI for suggestions
    const suggestions = await ai.analyze({
      query,
      currentPlan,
      tableStats: await this.getTableStats(),
      indexStats: await this.getIndexStats(),
    });
    
    return suggestions;
  }
}

// Automatic index creation based on slow queries
async function autoOptimize() {
  const slowQueries = await getSlowQueries();
  
  for (const query of slowQueries) {
    const suggested = await queryOptimizer.analyzeAndSuggest(query.sql);
    
    if (suggested.newIndexes) {
      for (const index of suggested.newIndexes) {
        await createIndex(index);
      }
    }
  }
}
```

### Pattern 2: Edge Caching with Stale-While-Revalidate

```typescript
// Next.js with ISR (Incremental Static Regeneration)
export async function getStaticProps() {
  // This runs at build time and on revalidation
  const products = await prisma.product.findMany({
    where: { isActive: true },
    take: 100,
  });
  
  return {
    props: { products },
    revalidate: 60, // Regenerate every 60 seconds if new requests
  };
}

// SWR pattern with Redis
async function getWithSWR<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 60
): Promise<T> {
  // Try cache
  const cached = await redis.get(`swr:${key}`);
  if (cached) {
    // Return cached, revalidate in background
    revalidateInBackground(key, fetcher, ttl);
    return JSON.parse(cached);
  }
  
  // Fetch fresh
  const data = await fetcher();
  await redis.setex(`swr:${key}`, ttl, JSON.stringify(data));
  
  return data;
}

async function revalidateInBackground(key: string, fetcher: () => Promise<any>, ttl: number) {
  // Re-fetch and update cache in background
  setTimeout(async () => {
    try {
      const fresh = await fetcher();
      await redis.setex(`swr:${key}`, ttl, JSON.stringify(fresh));
    } catch (e) {
      console.error('Background revalidation failed:', e);
    }
  }, 0);
}
```

This comprehensive guide covers query optimization from basics to advanced production patterns. Practice these concepts and always monitor your database performance in production.
