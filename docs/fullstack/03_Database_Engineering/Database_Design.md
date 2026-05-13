# Database Design: Complete Guide for Fullstack Engineers

## Hinglish Explanation (Beginner Level)

Bhai, database design matlab tumhare data ko kaise organize karoge - kaunse tables banenge, unke beech kya relationship hogi, aur sab kuch efficiently kaise store hoga.

Socho tum ek school management system bana rahe ho:
- Students table mein naam, class, roll number
- Teachers table mein naam, subject, salary
- Attendance table mein student kaunsa din aaya/naa aaya

Yeh sab tables ke beech connections (relationships) hote hain - student belongs to class, teacher teaches subject, attendance belongs to student.

**Database design ka matlab hai data ko properly structure karna taki:**
1. Data consistently store ho
2. Queries fast hon
3. Data integrity maintained rahe
4. Future changes ke liye flexible ho

MongoDB mein documents design karna hai - embedded vs referenced documents ka decision lena hai. SQL mein normalization ka concept samajhna hai.

## Deep Technical Explanation

Database design encompasses the logical and physical design of a database, including entity-relationship modeling, normalization, indexing strategies, and scalability considerations.

### Database Design Process

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Database Design Process                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. REQUIREMENT ANALYSIS                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐ │  │
│  │  │ User Stories    │  │ Business Rules │  │ System Reqs   │ │  │
│  │  │ - As a user...  │  │ - Each order   │  │ - 1000 users  │ │  │
│  │  │ - As admin...   │  │   has customer │  │ - 10k orders  │ │  │
│  │  └─────────────────┘  └─────────────────┘  └───────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                            │                                         │
│                            ▼                                         │
│  2. CONCEPTUAL DESIGN (ER Model)                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                                  │  │
│  │    ┌────────┐         ┌────────┐         ┌────────┐        │  │
│  │    │Customer│ 1    N  │ Orders │ N    1  │Product │        │  │
│  │    │        │─────────│        │─────────│        │        │  │
│  │    └────────┘         └────────┘         └────────┘        │  │
│  │                              │                               │  │
│  │                              │ 1:N                          │  │
│  │                              ▼                               │  │
│  │                        ┌────────┐                           │  │
│  │                        │Order   │                           │  │
│  │                        │Items   │                           │  │
│  │                        └────────┘                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                            │                                         │
│                            ▼                                         │
│  3. LOGICAL DESIGN (Schema)                                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                                  │  │
│  │  customers:                                                    │  │
│  │  - customer_id (PK)                                            │  │
│  │  - name                                                         │  │
│  │  - email                                                        │  │
│  │                                                                  │  │
│  │  orders:                                                        │  │
│  │  - order_id (PK)                                                │  │
│  │  - customer_id (FK) → customers                                 │  │
│  │  - order_date                                                   │  │
│  │  - status                                                       │  │
│  │                                                                  │  │
│  │  order_items:                                                   │  │
│  │  - order_item_id (PK)                                           │  │
│  │  - order_id (FK) → orders                                       │  │
│  │  - product_id (FK) → products                                   │  │
│  │  - quantity                                                     │  │
│  │                                                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                            │                                         │
│                            ▼                                         │
│  4. PHYSICAL DESIGN (Implementation)                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                                  │  │
│  │  PostgreSQL / MongoDB / MySQL Schema                           │  │
│  │  - Data types                                                  │  │
│  │  - Indexes (B-tree, Hash, GIN)                                 │  │
│  │  - Constraints                                                 │  │
│  │  - Partitioning strategy                                       │  │
│  │                                                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Entity-Relationship (ER) Models

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Entity-Relationship Cardinalities                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ONE-TO-ONE (1:1)                                                   │
│  ┌───────────┐         ┌───────────┐                                │
│  │  Person   │─────────│  Passport │  Each person has one passport │
│  │           │    1:1   │           │  Each passport belongs to one  │
│  └───────────┘         └───────────┘  person                         │
│                                                                      │
│  - In SQL: Add passport_id to persons OR person_id to passports      │
│  - In MongoDB: Embed or reference depending on access pattern        │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ONE-TO-MANY (1:N)                                                  │
│  ┌───────────┐         ┌───────────┐                                │
│  │  Author   │───┐     │   Book    │  One author writes many books  │
│  │           │   │ N:1 │           │  Each book has one author       │
│  └───────────┘       └───────────┘                                │
│                                                                      │
│  - In SQL: Add author_id to books (FK in "many" side)               │
│  - In MongoDB: Typically reference, rarely embed                     │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  MANY-TO-MANY (M:N)                                                 │
│  ┌───────────┐         ┌───────────┐                                │
│  │  Student  │─────────│  Course   │  Students enroll in many       │
│  │           │─────────│           │  courses. Courses have many     │
│  └───────────┘   M:N    └───────────┘  students                     │
│                                                                      │
│  - In SQL: Junction/Join table required                              │
│    students_courses (student_id, course_id)                         │
│                                                                      │
│  - In MongoDB: Array of references in either collection             │
│    students: { courseIds: [ObjectId, ...] }                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Normalization Forms

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Database Normalization Forms                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1NF (First Normal Form)                                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ✓ Atomic values (no repeating groups)                       │  │
│  │  ✓ Each column contains single value                         │  │
│  │  ✓ Each row is unique (Primary Key)                          │  │
│  │                                                               │  │
│  │  BAD:                           GOOD:                       │  │
│  │  ┌────┬────────────┐          ┌────┬────┬────────┐          │  │
│  │  │ id │ phones     │          │ id │ p1 │ p2    │          │  │
│  │  ├────┼────────────┤          ├────┼────┼────────┤          │  │
│  │  │ 1  │ 123,456,789│          │ 1  │123 │ 456   │          │  │
│  │  └────┴────────────┘          └────┴────┴────────┘          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  2NF (Second Normal Form)                                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ✓ 1NF satisfied                                              │  │
│  │  ✓ No partial dependencies (non-key columns depend on        │  │
│  │    entire primary key, not just part of composite key)        │  │
│  │                                                               │  │
│  │  BAD (partial dependency):           GOOD:                   │  │
│  │  ┌───────┬───────┬─────────┐         ┌────────┬────────┐     │  │
│  │  │ord_id│prod_id│prod_name│         │ord_id │prod_id│     │  │
│  │  ├───────┼───────┼─────────┤         ├────────┼────────┤     │  │
│  │  │   1   │   1   │  Phone  │         │   1   │   1   │     │  │
│  │  └───────┴───────┴─────────┘         └────────┴────────┘     │  │
│  │  prod_name depends only on prod_id,   Separate tables         │  │
│  │  not on ord_id (partial dependency)                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  3NF (Third Normal Form)                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ✓ 2NF satisfied                                              │  │
│  │  ✓ No transitive dependencies (non-key columns depend       │  │
│  │    only on PK, not on other non-key columns)                 │  │
│  │                                                               │  │
│  │  BAD (transitive dependency):      GOOD:                      │  │
│  │  ┌────┬──────────┬──────────┐      ┌────┬──────────┐         │  │
│  │  │ id │city_id  │city_name │      │ id │city_id  │         │  │
│  │  ├────┼──────────┼──────────┤      ├────┼──────────┤         │  │
│  │  │ 1  │    1     │ Mumbai   │      │ 1  │    1     │         │  │
│  │  └────┴──────────┴──────────┘      └────┴──────────┘         │  │
│  │  city_name depends on city_id,     Separate city table         │  │
│  │  not directly on id                                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  BCNF (Boyce-Codd Normal Form)                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ✓ 3NF satisfied                                              │  │
│  │  ✓ For every dependency A→B, A must be a superkey           │  │
│  │                                                               │  │
│  │  Example:                                                     │  │
│  │  teacher_id, subject_id → max_students (composite PK)       │  │
│  │  subject_id → teacher_id (teacher depends on subject)        │  │
│  │  subject_id is not a superkey → violates BCNF               │  │
│  │  SOLUTION: Split into tables                                  │  │
│  │  - teacher_subjects (teacher_id, subject_id)                │  │
│  │  - subject_capacity (subject_id, max_students, teacher_id)   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Architecture Diagram: SQL vs MongoDB Design

```
┌─────────────────────────────────────────────────────────────────────┐
│              SQL (Relational) vs MongoDB (Document) Design           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────┐                            │
│  │           SQL Design                 │                            │
│  │                                      │                            │
│  │    users ──────── orders            │                            │
│  │      │              │                │                            │
│  │      │ 1:N          │ 1:N           │                            │
│  │      │              │                │                            │
│  │      ▼              ▼                │                            │
│  │  addresses     order_items           │                            │
│  │                       │              │                            │
│  │                       │ N:1          │                            │
│  │                       ▼              │                            │
│  │                   products           │                            │
│  │                                      │                            │
│  │  - Normalized tables                 │                            │
│  │  - Foreign key constraints           │                            │
│  │  - JOINs for related data            │                            │
│  │  - ACID transactions                 │                            │
│  └─────────────────────────────────────┘                            │
│                                                                      │
│  ┌─────────────────────────────────────┐                            │
│  │         MongoDB Design               │                            │
│  │                                      │                            │
│  │  Option 1: Embedded Documents        │                            │
│  │  ┌───────────────────────────────┐  │                            │
│  │  │ {                             │  │                            │
│  │  │  _id: ObjectId,               │  │                            │
│  │  │  user: "Rahul",               │  │                            │
│  │  │  orders: [                    │  │                            │
│  │  │    { id: 1, items: [...], total: 100 }, │  │                  │
│  │  │    { id: 2, items: [...], total: 200 }   │  │                │
│  │  │  ]                             │  │                            │
│  │  │ }                             │  │                            │
│  │  └───────────────────────────────┘  │                            │
│  │                                      │                            │
│  │  Option 2: References               │                            │
│  │  ┌───────────────────────────────┐  │                            │
│  │  │ users collection:              │  │                            │
│  │  │ { _id, name, address_ids: [...] }  │  │                       │
│  │  │                                  │  │                            │
│  │  │ addresses collection:            │  │                            │
│  │  │ { _id, user_id, street, city }  │  │                            │
│  │  └───────────────────────────────┘  │                            │
│  │                                      │                            │
│  │  - Flexible schema                   │                            │
│  │  - Choose embed vs reference         │                            │
│  │  - Denormalization is common         │                            │
│  └─────────────────────────────────────┘                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Frontend + Backend Integration Examples

### SQL Schema with Prisma

```typescript
// schema.prisma - Complete e-commerce schema
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ============================================
// USER MANAGEMENT
// ============================================

model User {
  id            String    @id @default(uuid())
  email         String    @unique
  name          String
  passwordHash  String
  
  // Profile
  avatarUrl     String?
  phone         String?
  dateOfBirth   DateTime?
  
  // Relations
  accounts      Account[]
  sessions      Session[]
  orders        Order[]
  reviews       Review[]
  addresses     Address[]
  wishlists     WishlistItem[]
  
  // Cart
  cart          Cart?
  
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  deletedAt     DateTime? // Soft delete
  
  @@index([email])
  @@index([createdAt])
}

model Account {
  id            String    @id @default(uuid())
  userId        String
  provider      String    // 'google', 'github', 'credentials'
  providerId    String
  accessToken   String?
  refreshToken  String?
  expiresAt     DateTime?
  
  user          User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@unique([provider, providerId])
  @@index([userId])
}

model Session {
  id            String    @id @default(uuid())
  userId        String
  token         String    @unique
  ipAddress     String?
  userAgent     String?
  expiresAt     DateTime
  createdAt     DateTime  @default(now())
  
  user          User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@index([token])
  @@index([userId])
  @@index([expiresAt])
}

// ============================================
// E-COMMERCE CORE
// ============================================

model Product {
  id            String    @id @default(uuid())
  sku           String    @unique
  name          String
  slug          String    @unique
  description   String?
  price         Decimal   @db.Decimal(10, 2)
  comparePrice  Decimal?  @db.Decimal(10, 2)
  
  // Inventory
  stockQuantity Int       @default(0)
  trackInventory Boolean  @default(true)
  lowStockThreshold Int   @default(10)
  
  // Media
  images        ProductImage[]
  
  // Attributes
  categoryId    String
  category      Category  @relation(fields: [categoryId], references: [id])
  tags          ProductTag[]
  attributes    ProductAttribute[]
  variants      ProductVariant[]
  
  // Reviews
  reviews       Review[]
  
  // SEO
  metaTitle     String?
  metaDescription String?
  
  // Status
  isActive      Boolean   @default(true)
  isFeatured    Boolean   @default(false)
  
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  @@index([sku])
  @@index([slug])
  @@index([categoryId])
  @@index([price])
  @@index([isActive, isFeatured])
}

model ProductVariant {
  id            String    @id @default(uuid())
  productId     String
  sku           String    @unique
  name          String    // "Large / Blue"
  price         Decimal?  @db.Decimal(10, 2)
  stockQuantity Int       @default(0)
  attributes    Json      // { "size": "L", "color": "blue" }
  
  product       Product   @relation(fields: [productId], references: [id], onDelete: Cascade)
  orderItems    OrderItem[]
  
  @@index([productId])
  @@index([sku])
}

model ProductImage {
  id            String    @id @default(uuid())
  productId     String
  url           String
  altText       String?
  position      Int       @default(0)
  isPrimary     Boolean   @default(false)
  
  product       Product   @relation(fields: [productId], references: [id], onDelete: Cascade)
  
  @@index([productId])
}

model Category {
  id            String    @id @default(uuid())
  name          String
  slug          String    @unique
  description   String?
  parentId      String?
  imageUrl      String?
  
  parent        Category? @relation("CategoryHierarchy", fields: [parentId], references: [id])
  children      Category[] @relation("CategoryHierarchy")
  products      Product[]
  
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  @@index([slug])
  @@index([parentId])
}

model ProductAttribute {
  id            String    @id @default(uuid())
  productId     String
  name          String    // "Material"
  value         String    // "Cotton"
  
  product       Product   @relation(fields: [productId], references: [id], onDelete: Cascade)
  
  @@unique([productId, name])
  @@index([productId])
}

model ProductTag {
  id            String    @id @default(uuid())
  name          String    @unique
  slug          String    @unique
  
  products      Product[]
}

model Order {
  id            String    @id @default(uuid())
  orderNumber   String    @unique // "ORD-2026-00001"
  
  userId        String?
  user          User?     @relation(fields: [userId], references: [id])
  
  // Totals
  subtotal      Decimal   @db.Decimal(10, 2)
  taxAmount     Decimal   @db.Decimal(10, 2)
  shippingAmount Decimal  @db.Decimal(10, 2)
  discountAmount Decimal   @db.Decimal(10, 2) @default(0)
  total         Decimal   @db.Decimal(10, 2)
  
  // Status
  status        OrderStatus @default(PENDING)
  paymentStatus PaymentStatus @default(PENDING)
  
  // Shipping
  shippingAddressId String?
  shippingAddress   Address?  @relation(fields: [shippingAddressId], references: [id])
  shippingMethod   String?
  trackingNumber   String?
  
  // Payment
  paymentMethod   String?
  paymentId       String?
  
  // Notes
  customerNote   String?
  internalNote   String?
  
  items          OrderItem[]
  
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  @@index([orderNumber])
  @@index([userId])
  @@index([status])
  @@index([createdAt])
}

enum OrderStatus {
  PENDING
  CONFIRMED
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
  REFUNDED
}

enum PaymentStatus {
  PENDING
  PAID
  FAILED
  REFUNDED
}

model OrderItem {
  id            String    @id @default(uuid())
  orderId       String
  productId     String?
  variantId     String?
  variant       ProductVariant? @relation(fields: [variantId], references: [id])
  
  name          String    // Snapshot at order time
  sku           String
  price         Decimal   @db.Decimal(10, 2) // Snapshot
  quantity      Int
  total         Decimal   @db.Decimal(10, 2)
  
  order         Order     @relation(fields: [orderId], references: [id], onDelete: Cascade)
  
  @@index([orderId])
  @@index([productId])
}

// ============================================
// USER DATA
// ============================================

model Address {
  id            String    @id @default(uuid())
  userId        String?
  user          User?     @relation(fields: [userId], references: [id])
  
  type          AddressType @default(SHIPPING)
  name          String
  phone         String
  addressLine1  String
  addressLine2  String?
  city          String
  state         String
  postalCode    String
  country       String    @default("India")
  isDefault     Boolean   @default(false)
  
  orders        Order[]
  
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  @@index([userId])
}

enum AddressType {
  SHIPPING
  BILLING
}

model Review {
  id            String    @id @default(uuid())
  productId     String
  userId        String
  
  rating        Int       // 1-5
  title         String?
  content       String?
  
  isVerified    Boolean   @default(false)
  isPublished   Boolean   @default(false)
  
  helpfulCount  Int       @default(0)
  
  product       Product   @relation(fields: [productId], references: [id], onDelete: Cascade)
  user          User      @relation(fields: [userId], references: [id])
  
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  @@index([productId])
  @@index([userId])
  @@index([rating])
}

model Cart {
  id            String    @id @default(uuid())
  userId        String    @unique
  user          User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  items         CartItem[]
  
  updatedAt     DateTime  @updatedAt
}

model CartItem {
  id            String    @id @default(uuid())
  cartId        String
  productId     String
  variantId     String?
  quantity      Int       @default(1)
  
  cart          Cart      @relation(fields: [cartId], references: [id], onDelete: Cascade)
  
  @@unique([cartId, productId, variantId])
}

model WishlistItem {
  id            String    @id @default(uuid())
  userId        String
  productId     String
  
  user          User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  createdAt     DateTime  @default(now())
  
  @@unique([userId, productId])
}
```

### MongoDB Schema with Mongoose

```typescript
// models/ecommerce.mongo.ts
import mongoose, { Schema, Document } from 'mongoose';

// ============================================
// PRODUCT (Document Model)
// ============================================

const productSchema = new Schema({
  // Basic info
  sku: { type: String, required: true, unique: true },
  name: { type: String, required: true, index: true },
  slug: { type: String, required: true, unique: true },
  description: String,
  
  // Pricing
  price: { type: Number, required: true, min: 0 },
  comparePrice: { type: Number, min: 0 },
  costPrice: { type: Number, min: 0 }, // For profit calculation
  
  // Inventory
  stock: {
    quantity: { type: Number, default: 0 },
    track: { type: Boolean, default: true },
    lowStockThreshold: { type: Number, default: 10 },
  },
  
  // Variants (embedded)
  variants: [{
    sku: { type: String, required: true },
    name: { type: String }, // "Large / Blue"
    price: Number,
    stock: { type: Number, default: 0 },
    attributes: { type: Map, of: String }, // { size: "L", color: "blue" }
    images: [String],
    isActive: { type: Boolean, default: true },
  }],
  
  // Media gallery
  images: [{
    url: String,
    alt: String,
    position: { type: Number, default: 0 },
    isPrimary: { type: Boolean, default: false },
  }],
  
  // Category (reference)
  category: { 
    type: Schema.Types.ObjectId, 
    ref: 'Category',
    index: true 
  },
  
  // Tags (array of strings)
  tags: [{ type: String, index: true }],
  
  // Flexible attributes
  attributes: { type: Map, of: Schema.Types.Mixed },
  
  // Reviews
  reviews: [{
    userId: { type: Schema.Types.ObjectId, ref: 'User' },
    userName: String,
    rating: { type: Number, min: 1, max: 5 },
    title: String,
    content: String,
    isVerified: { type: Boolean, default: false },
    helpful: { type: Number, default: 0 },
    createdAt: { type: Date, default: Date.now },
  }],
  
  // Aggregated ratings
  rating: {
    average: { type: Number, default: 0 },
    count: { type: Number, default: 0 },
  },
  
  // SEO
  seo: {
    title: String,
    description: String,
    keywords: [String],
  },
  
  // Status
  isActive: { type: Boolean, default: true, index: true },
  isFeatured: { type: Boolean, default: false },
  
  // Timestamps
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now },
}, {
  timestamps: true,
});

// Indexes
productSchema.index({ price: 1 });
productSchema.index({ 'category': 1, 'price': 1 });
productSchema.index({ tags: 1, isActive: 1 });
productSchema.index({ name: 'text', description: 'text' });
productSchema.index({ createdAt: -1 });

// Methods
productSchema.methods.getFinalPrice = function() {
  return this.comparePrice && this.comparePrice < this.price 
    ? this.comparePrice 
    : this.price;
};

productSchema.methods.isInStock = function(quantity = 1) {
  if (!this.stock.track) return true;
  return this.stock.quantity >= quantity;
};

productSchema.methods.updateRating = async function() {
  if (this.reviews.length === 0) {
    this.rating = { average: 0, count: 0 };
  } else {
    const total = this.reviews.reduce((sum, r) => sum + r.rating, 0);
    this.rating = {
      average: total / this.reviews.length,
      count: this.reviews.length,
    };
  }
  await this.save();
};

// Static methods
productSchema.statics.findBySlug = function(slug: string) {
  return this.findOne({ slug, isActive: true });
};

productSchema.statics.searchProducts = function(query: string, filters: any = {}) {
  const searchQuery: any = {
    isActive: true,
    $text: { $search: query },
  };
  
  if (filters.category) {
    searchQuery.category = new mongoose.Types.ObjectId(filters.category);
  }
  
  if (filters.minPrice || filters.maxPrice) {
    searchQuery.price = {};
    if (filters.minPrice) searchQuery.price.$gte = filters.minPrice;
    if (filters.maxPrice) searchQuery.price.$lte = filters.maxPrice;
  }
  
  if (filters.tags && filters.tags.length > 0) {
    searchQuery.tags = { $in: filters.tags };
  }
  
  return this.find(searchQuery)
    .select('name slug price images rating')
    .sort({ score: { $meta: 'textScore' } });
};

export const Product = mongoose.model('Product', productSchema);

// ============================================
// ORDER (Document Model with Embedded Items)
// ============================================

const orderItemSchema = new Schema({
  productId: { type: Schema.Types.ObjectId, ref: 'Product', required: true },
  variantId: { type: Schema.Types.ObjectId },
  
  // Denormalized for performance
  productName: String,
  productSku: String,
  variantName: String,
  image: String,
  
  price: { type: Number, required: true },
  quantity: { type: Number, required: true, min: 1 },
  total: { type: Number, required: true },
  
  // For digital products
  downloadUrl: String,
  licenseKey: String,
});

const orderSchema = new Schema({
  orderNumber: { type: String, required: true, unique: true },
  
  customer: {
    userId: { type: Schema.Types.ObjectId, ref: 'User' },
    email: { type: String, required: true },
    name: String,
    phone: String,
  },
  
  // Embedded items (no separate collection needed)
  items: [orderItemSchema],
  
  // Totals
  subtotal: { type: Number, required: true },
  discount: {
    code: String,
    type: { type: String, enum: ['percentage', 'fixed'] },
    value: Number,
    amount: { type: Number, default: 0 },
  },
  tax: { type: Number, default: 0 },
  shipping: {
    method: String,
    cost: { type: Number, default: 0 },
    address: {
      name: String,
      phone: String,
      line1: String,
      line2: String,
      city: String,
      state: String,
      postalCode: String,
      country: String,
    },
    tracking: {
      carrier: String,
      number: String,
      url: String,
    },
  },
  total: { type: Number, required: true },
  
  // Status workflow
  status: {
    type: String,
    enum: ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded'],
    default: 'pending',
    index: true,
  },
  
  // Payment
  payment: {
    method: { type: String, enum: ['card', 'upi', 'netbanking', 'wallet', 'cod'] },
    status: { type: String, enum: ['pending', 'paid', 'failed', 'refunded'] },
    transactionId: String,
    paidAt: Date,
  },
  
  // Notes
  notes: {
    customer: String,
    internal: String,
  },
  
  // Timeline
  timeline: [{
    status: String,
    message: String,
    createdAt: { type: Date, default: Date.now },
  }],
  
  // Metadata
  ipAddress: String,
  userAgent: String,
  
  // For refunds
  refund: {
    reason: String,
    amount: Number,
    processedAt: Date,
    processedBy: String,
  },
}, {
  timestamps: true,
});

// Indexes
orderSchema.index({ 'customer.userId': 1, createdAt: -1 });
orderSchema.index({ orderNumber: 1 });
orderSchema.index({ 'payment.transactionId': 1 });
orderSchema.index({ createdAt: -1 });
orderSchema.index({ status: 1, createdAt: 1 });

// Pre-save hook to generate order number
orderSchema.pre('save', async function(next) {
  if (this.isNew) {
    const count = await mongoose.model('Order').countDocuments();
    const year = new Date().getFullYear();
    this.orderNumber = `ORD-${year}-${String(count + 1).padStart(5, '0')}`;
  }
  next();
});

// Method to update status
orderSchema.methods.updateStatus = async function(newStatus: string, message?: string) {
  this.status = newStatus;
  this.timeline.push({
    status: newStatus,
    message: message || `Status changed to ${newStatus}`,
    createdAt: new Date(),
  });
  await this.save();
};

export const Order = mongoose.model('Order', orderSchema);

// ============================================
// USER (with embedded cart)
// ============================================

const cartItemSchema = new Schema({
  productId: { type: Schema.Types.ObjectId, ref: 'Product', required: true },
  variantId: { type: Schema.Types.ObjectId },
  quantity: { type: Number, required: true, min: 1 },
  
  // Denormalized
  productName: String,
  productSlug: String,
  variantName: String,
  image: String,
  price: Number,
});

const userSchema = new Schema({
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String }, // Null for OAuth-only users
  name: { type: String, required: true },
  
  // Profile
  avatar: String,
  phone: String,
  dateOfBirth: Date,
  gender: { type: String, enum: ['male', 'female', 'other'] },
  
  // Addresses (array of embedded documents)
  addresses: [{
    type: { type: String, enum: ['shipping', 'billing'], default: 'shipping' },
    isDefault: { type: Boolean, default: false },
    name: String,
    phone: String,
    line1: String,
    line2: String,
    city: String,
    state: String,
    postalCode: String,
    country: { type: String, default: 'India' },
  }],
  
  // Cart (embedded, no separate collection)
  cart: {
    items: [cartItemSchema],
    updatedAt: Date,
  },
  
  // Wishlist (array of product refs)
  wishlist: [{
    type: Schema.Types.ObjectId,
    ref: 'Product',
    addedAt: { type: Date, default: Date.now },
  }],
  
  // OAuth
  accounts: [{
    provider: { type: String, enum: ['google', 'github', 'facebook'] },
    providerId: String,
    accessToken: String,
    refreshToken: String,
  }],
  
  // Preferences
  preferences: {
    newsletter: { type: Boolean, default: true },
    notifications: {
      email: { type: Boolean, default: true },
      sms: { type: Boolean, default: false },
    },
    currency: { type: String, default: 'INR' },
    language: { type: String, default: 'en' },
  },
  
  // Roles
  role: { type: String, enum: ['user', 'admin'], default: 'user' },
  
  // Status
  isActive: { type: Boolean, default: true },
  emailVerified: { type: Boolean, default: false },
  
  // Timestamps
  lastLoginAt: Date,
}, {
  timestamps: true,
});

// Indexes
userSchema.index({ email: 1 });
userSchema.index({ 'accounts.provider': 1, 'accounts.providerId': 1 });

// Virtual for cart total
userSchema.virtual('cartTotal').get(function() {
  if (!this.cart?.items?.length) return 0;
  return this.cart.items.reduce((sum: number, item: any) => sum + item.price * item.quantity, 0);
});

// Methods
userSchema.methods.addToCart = async function(productId: string, variantId?: string, quantity = 1) {
  const existingIndex = this.cart.items.findIndex(
    item => item.productId.toString() === productId && 
            (variantId ? item.variantId?.toString() === variantId : !item.variantId)
  );
  
  if (existingIndex >= 0) {
    this.cart.items[existingIndex].quantity += quantity;
  } else {
    const product = await Product.findById(productId);
    this.cart.items.push({
      productId,
      variantId,
      quantity,
      productName: product?.name,
      productSlug: product?.slug,
      variantName: variantId ? 'Selected variant' : undefined,
      image: product?.images?.[0]?.url,
      price: product?.price,
    });
  }
  
  this.cart.updatedAt = new Date();
  await this.save();
};

userSchema.methods.removeFromCart = async function(productId: string, variantId?: string) {
  this.cart.items = this.cart.items.filter(
    item => !(item.productId.toString() === productId && 
             (variantId ? item.variantId?.toString() === variantId : !item.variantId))
  );
  this.cart.updatedAt = new Date();
  await this.save();
};

userSchema.methods.clearCart = async function() {
  this.cart.items = [];
  this.cart.updatedAt = new Date();
  await this.save();
};

export const User = mongoose.model('User', userSchema);
```

## Real-World Production Examples

### Example 1: Multi-Tenant SaaS Schema

```sql
-- Multi-tenant database design patterns

-- PATTERN 1: Shared database, shared schema (discriminator column)
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    customer_name VARCHAR(255),
    total DECIMAL(10, 2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE INDEX idx_orders_tenant ON orders(tenant_id);
CREATE INDEX idx_orders_tenant_date ON orders(tenant_id, created_at DESC);

-- Row-level security (PostgreSQL)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- PATTERN 2: Shared database, separate schemas per tenant
-- Each tenant gets their own schema
CREATE SCHEMA tenant_abc123;
CREATE SCHEMA tenant_def456;

CREATE TABLE tenant_abc123.orders (...);
CREATE TABLE tenant_def456.orders (...);

-- PATTERN 3: Separate database per tenant (for enterprise)
-- URL: postgres://host/tenant_abc123
-- URL: postgres://host/tenant_def456
```

### Example 2: Time-Series Data Design

```sql
-- IoT sensor data schema
CREATE TABLE sensor_readings (
    id BIGSERIAL PRIMARY KEY,
    device_id UUID NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    value DECIMAL(15, 4) NOT NULL,
    unit VARCHAR(20),
    quality VARCHAR(20) DEFAULT 'good', -- 'good', 'uncertain', 'bad'
    recorded_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Partition by time (monthly)
CREATE TABLE sensor_readings_partitioned (
    LIKE sensor_readings INCLUDING ALL
) PARTITION BY RANGE (recorded_at);

CREATE TABLE sensor_readings_2026_01
    PARTITION OF sensor_readings_partitioned
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE sensor_readings_2026_02
    PARTITION OF sensor_readings_partitioned
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Downsampled table for dashboards (materialized)
CREATE TABLE sensor_readings_hourly (
    device_id UUID NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    hour TIMESTAMPTZ NOT NULL,
    avg_value DECIMAL(15, 4),
    min_value DECIMAL(15, 4),
    max_value DECIMAL(15, 4),
    count INTEGER,
    PRIMARY KEY (device_id, sensor_type, hour)
);

-- Aggregation function
CREATE OR REPLACE FUNCTION aggregate_hourly_readings()
RETURNS void AS $$
BEGIN
    INSERT INTO sensor_readings_hourly
    SELECT 
        device_id,
        sensor_type,
        date_trunc('hour', recorded_at) as hour,
        AVG(value)::DECIMAL(15, 4) as avg_value,
        MIN(value)::DECIMAL(15, 4) as min_value,
        MAX(value)::DECIMAL(15, 4) as max_value,
        COUNT(*) as count
    FROM sensor_readings
    WHERE recorded_at >= NOW() - INTERVAL '2 hours'
    GROUP BY device_id, sensor_type, date_trunc('hour', recorded_at)
    ON CONFLICT (device_id, sensor_type, hour)
    DO UPDATE SET
        avg_value = EXCLUDED.avg_value,
        min_value = EXCLUDED.min_value,
        max_value = EXCLUDED.max_value,
        count = EXCLUDED.count;
END;
$$ LANGUAGE plpgsql;
```

### Example 3: Event Sourcing Schema

```sql
-- Event sourcing pattern for orders
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

CREATE INDEX idx_events_aggregate ON events(aggregate_id, version);
CREATE INDEX idx_events_type ON events(event_type, created_at);
CREATE INDEX idx_events_metadata ON events USING GIN (metadata);

-- Projection tables (denormalized for reads)
CREATE TABLE order_snapshots (
    order_id UUID PRIMARY KEY,
    customer_id UUID,
    status VARCHAR(50),
    total_amount DECIMAL(10, 2),
    item_count INTEGER,
    last_event_version INTEGER,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE customer_order_summary (
    customer_id UUID PRIMARY KEY,
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(15, 2) DEFAULT 0,
    avg_order_value DECIMAL(10, 2),
    last_order_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Rebuild projection from events
CREATE OR REPLACE FUNCTION rebuild_order_snapshot(order_uuid UUID)
RETURNS void AS $$
DECLARE
    current_state JSONB := '{}';
BEGIN
    FOR event_data IN 
        SELECT event_data, version 
        FROM events 
        WHERE aggregate_id = order_uuid 
        ORDER BY version
    LOOP
        current_state := current_state || event_data.event_data;
    END LOOP;
    
    INSERT INTO order_snapshots (order_id, customer_id, status, total_amount, item_count, last_event_version)
    VALUES (
        order_uuid,
        (current_state->>'customerId')::UUID,
        current_state->>'status',
        (current_state->>'totalAmount')::DECIMAL(10, 2),
        jsonb_array_length(current_state->'items'),
        (SELECT MAX(version) FROM events WHERE aggregate_id = order_uuid)
    )
    ON CONFLICT (order_id) DO UPDATE SET
        status = EXCLUDED.status,
        total_amount = EXCLUDED.total_amount,
        item_count = EXCLUDED.item_count,
        last_event_version = EXCLUDED.last_event_version,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;
```

## Failure Cases

### Case 1: Over-Normalization

**Problem**: Too many tables causing complex JOINs and poor performance.

```sql
-- BAD: Over-normalized to 6NF (impractical)
-- Address split into: street, city, state, zip, country tables
-- Each order JOINs 10+ tables for full data

-- GOOD: Practical normalization (3NF/BANF)
-- Keep address as single JSONB or composite type for PostgreSQL
CREATE TYPE postal_address AS (
    line1 VARCHAR(255),
    line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    shipping_address postal_address,
    billing_address postal_address
);
```

### Case 2: Under-Normalization (No Normalization)

**Problem**: Data redundancy, update anomalies.

```sql
-- BAD: Repeating data
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255),  -- Repeats for every order
    customer_email VARCHAR(255), -- Repeats for every order
    customer_phone VARCHAR(20),  -- Repeats for every order
    product_name VARCHAR(255),   -- Repeats
    product_category VARCHAR(100), -- Repeats
    ...
);

-- If customer changes email, must update ALL their orders!

-- GOOD: Proper normalization
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category_id INT REFERENCES categories(id)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    ...
);
```

## Debugging Guide

### Database Diagram Generation

```bash
# Using PostgreSQL
# Install: npm install -g pgsql-schema-to-erd

# Generate ERD from existing database
pg_dump -h localhost -U user -d database --schema-only > schema.sql

# Use schema spy
java -jar schemaSpy.jar -t pgsql -db database -host localhost -u user -p password

# Using MySQL Workbench
# File > Reverse Engineer

# Online tools
# dbdiagram.io - Import SQL, get visual diagram
# dbdesigner.net
```

### Query Analysis for Design Issues

```sql
-- Find tables with too many columns (> 20 suggests possible redesign)
SELECT 
    table_name,
    count(*) as column_count
FROM information_schema.columns
WHERE table_schema = 'public'
GROUP BY table_name
HAVING count(*) > 20
ORDER BY column_count DESC;

-- Find tables without primary keys
SELECT 
    table_name
FROM information_schema.tables t
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
AND NOT EXISTS (
    SELECT 1 
    FROM information_schema.table_constraints tc
    WHERE tc.table_name = t.table_name
    AND tc.constraint_type = 'PRIMARY KEY'
);

-- Find columns with too many NULLs (possible missing normalization)
SELECT 
    table_name,
    column_name,
    null_percentage,
    total_rows
FROM (
    SELECT 
        table_name,
        column_name,
        ROUND(100.0 * null_count / total_count, 2) as null_percentage,
        total_count as total_rows
    FROM information_schema.columns c
    CROSS JOIN (
        SELECT COUNT(*) as total_count 
        FROM information_schema.tables t
        WHERE t.table_name = c.table_name
    ) counts
    WHERE table_schema = 'public'
) sub
WHERE null_percentage > 50
ORDER BY null_percentage DESC;

-- Find tables without indexes (except PK)
SELECT 
    t.table_name,
    count(*) as column_count
FROM information_schema.tables t
JOIN information_schema.columns c ON t.table_name = c.table_name
WHERE t.table_schema = 'public'
AND t.table_type = 'BASE TABLE'
AND NOT EXISTS (
    SELECT 1 
    FROM information_schema.statistics s
    WHERE s.table_name = t.table_name
    AND s.index_name != 'PRIMARY'
)
GROUP BY t.table_name;
```

## Tradeoffs

### Normalization vs Denormalization

| Aspect | Normalized | Denormalized |
|--------|-----------|--------------|
| Data Integrity | High | Moderate |
| Storage Space | Less | More |
| Write Speed | Faster | Slower (multiple writes) |
| Read Speed | Slower (JOINs) | Faster (less JOINs) |
| Complexity | Higher | Lower |
| Query Simplicity | Complex | Simple |

### When to Denormalize

1. **Read-heavy workloads** - Real-time dashboards, reporting
2. **Aggregated data** - Totals, counts, averages
3. **Hierarchical data** - Comments on posts, folder structures
4. **Frequently accessed together** - User profile + last order
5. **Performance critical** - Avoid complex JOINs in hot paths

### When to Normalize

1. **Write-heavy workloads** - Real-time data entry
2. **Data integrity critical** - Financial transactions
3. **Shared reference data** - Countries, categories
4. **Complex relationships** - Many-to-many with attributes

## Security Concerns

### Data Masking and Anonymization

```sql
-- Create masked versions for different roles
CREATE VIEW customer_pii_masked AS
SELECT 
    id,
    name,
    -- Mask email: first 2 chars visible
    CONCAT(LEFT(email, 2), '***', RIGHT(email, 4)) as email,
    -- Mask phone
    CONCAT('****', RIGHT(phone, 4)) as phone,
    -- Keep non-PII data
    created_at,
    total_orders
FROM customers;

-- Anonymize production data for testing
UPDATE customers 
SET 
    email = CONCAT('test_', id, '@test.com'),
    phone = '0000000000',
    name = 'Test User ' || id;
```

### Row-Level Security

```sql
-- Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policies per role
CREATE POLICY tenant_isolation ON orders
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::UUID);

CREATE POLICY admin_full_access ON orders
    FOR ALL
    TO admin_role
    USING (true)
    WITH CHECK (true);

-- Application sets tenant context
SET app.current_tenant_id = 'tenant-uuid-here';
```

## Performance Optimization

### Indexing Strategy

```sql
-- Covering index for common query pattern
CREATE INDEX idx_orders_customer_covering 
ON orders(customer_id, created_at DESC) 
INCLUDE (total, status);

-- Partial index for active records only
CREATE INDEX idx_products_active 
ON products(category_id, price) 
WHERE is_active = true;

-- Expression index for computed columns
CREATE INDEX idx_users_email_lower 
ON users(LOWER(email));

CREATE INDEX idx_orders_month 
ON orders(date_trunc('month', created_at));

-- Composite index ordering (most selective first for equality)
CREATE INDEX idx_events_type_created 
ON events(event_type, created_at DESC);
```

### Materialized Views for Reports

```sql
-- Create materialized view for expensive aggregation
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT 
    date_trunc('month', created_at) as month,
    status,
    COUNT(*) as order_count,
    SUM(total) as total_revenue,
    AVG(total) as avg_order_value
FROM orders
GROUP BY 1, 2
WITH DATA;

CREATE UNIQUE INDEX ON monthly_sales(month, status);

-- Refresh on schedule
CREATE OR REPLACE FUNCTION refresh_monthly_sales()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;
END;
$$ LANGUAGE plpgsql;

-- pg_cron for automatic refresh
-- Add to crontab:
-- 0 1 * * * SELECT refresh_monthly_sales();
```

## Best Practices

### 1. Always Use UUIDs for Distributed Systems

```sql
-- Better for: Microservices, multi-tenant, horizontal scaling
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ...
);

-- For high-volume inserts (UUID v7 for time-ordering)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ...
);
```

### 2. Implement Soft Deletes

```sql
-- Add deleted_at column
ALTER TABLE orders ADD COLUMN deleted_at TIMESTAMPTZ;

-- Soft delete trigger
CREATE OR REPLACE FUNCTION soft_delete()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders SET deleted_at = NOW() WHERE id = OLD.id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_soft_delete_order
    INSTEAD OF DELETE ON orders_view
    FOR EACH ROW EXECUTE FUNCTION soft_delete();
```

### 3. Audit Trail

```sql
-- Create audit log table
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by UUID,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    ip_address INET
);

-- Trigger function
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, OLD.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_data)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables
CREATE TRIGGER audit_users
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger();
```

## Common Mistakes

### Mistake 1: Not Using Foreign Keys

```sql
-- BAD: No referential integrity
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT,  -- No FK constraint!
    ...
);

-- GOOD: Foreign keys with proper actions
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id)
        ON DELETE RESTRICT  -- Prevent customer deletion if orders exist
        ON UPDATE CASCADE,   -- Update if customer ID changes
    ...
);

-- For soft delete, use SET NULL
CREATE TABLE orders (
    ...
    deleted_at TIMESTAMPTZ,
    CONSTRAINT fk_customer 
        FOREIGN KEY (customer_id) 
        REFERENCES customers(id) 
        ON DELETE SET NULL
);
```

### Mistake 2: Not Using Check Constraints

```sql
-- BAD: No validation
CREATE TABLE products (
    price DECIMAL(10, 2)  -- Can be negative!
);

-- GOOD: Check constraints
CREATE TABLE products (
    price DECIMAL(10, 2) CHECK (price >= 0),
    rating DECIMAL(2, 1) CHECK (rating >= 1 AND rating <= 5)
);

CREATE TABLE orders (
    status VARCHAR(20) CHECK (status IN ('pending', 'paid', 'shipped', 'delivered'))
);
```

## Interview Questions

### Q1: Explain database normalization and its forms

**Answer**: Normalization organizes data to reduce redundancy and improve integrity. Forms include 1NF (atomic values), 2NF (no partial dependencies on composite keys), 3NF (no transitive dependencies), BCNF (every determinant is a candidate key). Higher forms exist but rarely used in practice.

### Q2: What is the difference between clustered and non-clustered indexes?

**Answer**: Clustered index determines physical storage order of data (one per table), typically on primary key. Non-clustered index is separate structure pointing to data (multiple per table). SQL Server uses clustered by default on PK, PostgreSQL uses heap storage with B-tree indexes.

### Q3: When would you denormalize a database?

**Answer**: For read-heavy applications requiring fast queries, aggregated reports, frequently accessed combinations. When JOINs become too expensive, or when using CQRS pattern where read and write models differ.

### Q4: Explain the different relationship types

**Answer**: One-to-one (each row in A matches one in B), One-to-many (each A can have multiple B), Many-to-many (A and B both have multiple of each other, requires junction table). PostgreSQL supports these directly, MongoDB handles through embedding or references.

### Q5: What is sharding and when is it needed?

**Answer**: Sharding horizontally partitions data across multiple databases/nodes. Needed when single database cannot handle write volume, storage limits reached, or geographic distribution required. Tradeoffs include query complexity and cross-shard transactions.

### Q6: How do you choose between SQL and NoSQL?

**Answer**: SQL when: relational integrity critical, structured data, complex queries/JOINs, ACID transactions needed. NoSQL when: flexible schema, horizontal scaling required, document hierarchy matches domain, high write throughput.

### Q7: What is the CAP theorem?

**Answer**: States that distributed database can only guarantee 2 of 3: Consistency (all nodes see same data), Availability (every request gets response), Partition tolerance (system works despite network failures). PostgreSQL prioritizes C, many NoSQL databases prioritize A/P.

## Latest 2026 Fullstack Engineering Patterns

### Pattern 1: GraphQL Schema-First Design

```typescript
// Define types first, generate resolvers
// schema.graphql

type User {
  id: ID!
  email: String!
  name: String!
  orders: [Order!]!
  orderCount: Int!
  totalSpent: Decimal!
  recentOrders(limit: Int = 5): [Order!]!
}

type Order {
  id: ID!
  orderNumber: String!
  items: [OrderItem!]!
  total: Decimal!
  status: OrderStatus!
  createdAt: DateTime!
}

type OrderItem {
  id: ID!
  product: Product!
  quantity: Int!
  price: Decimal!
}

enum OrderStatus {
  PENDING
  CONFIRMED
  PROCESSING
  SHIPPED
  DELIVERED
}

input CreateOrderInput {
  items: [OrderItemInput!]!
  shippingAddressId: ID!
  paymentMethod: PaymentMethod!
}

// Generate Prisma schema from GraphQL
// Uses @model, @id directives
```

### Pattern 2: CQRS with Separate Read/Write Models

```typescript
// Write Model (Command)
interface CreateOrderCommand {
  customerId: string;
  items: Array<{ productId: string; quantity: number }>;
  shippingAddressId: string;
}

async function createOrder(cmd: CreateOrderCommand): Promise<Order> {
  // Validate
  // Apply business rules
  // Persist to write database
  
  const order = await prisma.order.create({
    data: {
      customerId: cmd.customerId,
      items: { create: cmd.items },
      // ...
    }
  });
  
  // Publish event for read model update
  await eventBus.publish(new OrderCreatedEvent(order));
  
  return order;
}

// Read Model (Query) - Denormalized for fast reads
interface OrderReadModel {
  orderId: string;
  orderNumber: string;
  customerName: string;
  customerEmail: string;
  itemCount: number;
  itemNames: string[]; // Denormalized
  total: number;
  status: string;
  createdAt: Date;
}

async function getOrderReadModel(orderId: string): Promise<OrderReadModel> {
  return readDb.query(`
    SELECT * FROM v_orders_full
    WHERE order_id = $1
  `, [orderId]);
}
```

### Pattern 3: Multi-Region Active-Active Database

```
┌─────────────────────────────────────────────────────────────────────┐
│                 Multi-Region Active-Active Architecture              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Region: Mumbai                   Region: Singapore                  │
│  ┌──────────────────┐           ┌──────────────────┐               │
│  │ Primary Write    │◄─────────►│ Primary Write    │               │
│  │ (Mumbai)         │  Sync     │ (Singapore)      │               │
│  │                  │  (CRDT)   │                  │               │
│  └────────┬─────────┘           └────────┬─────────┘               │
│           │                              │                          │
│           │ Local reads                  │ Local reads              │
│           ▼                              ▼                          │
│  ┌──────────────────┐           ┌──────────────────┐               │
│  │ Local Postgres   │           │ Local Postgres   │               │
│  │ Read Replicas    │           │ Read Replicas   │               │
│  └──────────────────┘           └──────────────────┘               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

// Conflict resolution: Last-writer-wins, or CRDT for specific fields
// Tools: CockroachDB, YugabyteDB, AWS Aurora Global Tables
```

This comprehensive guide covers database design from basics to advanced patterns. Practice these concepts and always consider the tradeoffs when designing databases for your fullstack applications.
