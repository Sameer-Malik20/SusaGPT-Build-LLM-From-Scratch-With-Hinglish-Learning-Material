# MongoDB: Complete Guide for Fullstack Engineers

## Hinglish Explanation (Beginner Level)

Bhai, MongoDB ek different tarah ka database hai - yeh document-based hai, matlab yeh JSON-like documents store karta hai instead of rows and tables.

Socho tum ek book store manage kar rahe ho:
- **SQL mein**: Har book ki entry ek row mein hoti hai with columns like title, author, price
- **MongoDB mein**: Har book ek document hai jisme title, author, price, reviews, chapters sab kuch ek hi jagah!

```javascript
// MongoDB document example - ek object mein sab kuch
{
  "title": "JavaScript Basics",
  "author": {
    "name": "Rahul Kumar",
    "email": "rahul@example.com",
    "social": {
      "twitter": "@rahul",
      "github": "rahulgithub"
    }
  },
  "chapters": [
    { "name": "Variables", "pages": 10 },
    { "name": "Functions", "pages": 25 }
  ],
  "price": 299.99,
  "inStock": true,
  "tags": ["javascript", "web", "programming"]
}
```

MongoDB ka naam "humongous" se aaya hai - matlab bahut bada data handle kar sakta hai. Yeh flexible hai, fast hai, aur scaling ke liye best hai.

Yeh companies jaise Uber, Netflix, MongoDB khud use karte hain kyunki Yeh real-time applications aur rapid development ke liye excellent hai.

## Deep Technical Explanation

MongoDB ek NoSQL document database hai jo BSON (Binary JSON) format mein data store karta hai. Yeh horizontal scaling, flexible schema, aur high availability provide karta hai.

### MongoDB Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MongoDB Cluster                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│    ┌─────────────────────────────────────────────────────────────┐   │
│    │                    Config Server Replica Set                 │   │
│    │  ┌─────────┐  ┌─────────┐  ┌─────────┐                       │   │
│    │  │ Config  │  │ Config  │  │ Config  │                       │   │
│    │  │ Server 1│  │ Server 2│  │ Server 3│  (Metadata storage)   │   │
│    │  └────┬────┘  └────┬────┘  └────┬────┘                       │   │
│    └───────┼────────────┼────────────┼───────────────────────────┘   │
│            │            │            │                               │
│            └────────────┴────────────┘                               │
│                         │                                             │
│    ┌────────────────────┼───────────────────────────────────────┐   │
│    │                    │              Shard Replica Sets       │   │
│    │                    ▼                                       │   │
│    │  ┌───────────────────────────────────────────────────────┐ │   │
│    │  │                    Shard 1 (Chunk 0-100)              │ │   │
│    │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐               │ │   │
│    │  │  │Primary  │  │Secondary│  │Secondary│               │ │   │
│    │  │  │         │◄─│(Read)   │  │(Read)   │               │ │   │
│    │  │  └────┬────┘  └─────────┘  └─────────┘               │ │   │
│    │  └───────┼────────────────────────────────────────────────┘ │   │
│    │          │                                                   │   │
│    │  ┌───────────────────────────────────────────────────────┐ │   │
│    │  │                    Shard 2 (Chunk 101-200)            │ │   │
│    │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐               │ │   │
│    │  │  │Primary  │  │Secondary│  │Secondary│               │ │   │
│    │  │  │         │◄─│(Read)   │  │(Read)   │               │ │   │
│    │  │  └────┬────┘  └─────────┘  └─────────┘               │ │   │
│    │  └───────┼────────────────────────────────────────────────┘ │   │
│    │          │                                                   │   │
│    │  ┌───────────────────────────────────────────────────────┐ │   │
│    │  │                    Shard 3 (Chunk 201-300)            │ │   │
│    │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐               │ │   │
│    │  │  │Primary  │  │Secondary│  │Secondary│               │ │   │
│    │  │  │         │◄─│(Read)   │  │(Read)   │               │ │   │
│    │  │  └────┬────┘  └─────────┘  └─────────┘               │ │   │
│    │  └───────┼────────────────────────────────────────────────┘ │   │
│    └──────────┼───────────────────────────────────────────────────┘   │
│               │                                                         │
│               ▼                                                         │
│    ┌───────────────────────────────────────────────────────────────┐   │
│    │                      mongos (Query Router)                      │   │
│    │                    Port: 27017                                  │   │
│    └────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        Application Layer                             │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐   │  │
│  │  │ Node.js │  │ Python  │  │  Java   │  │    Go           │   │  │
│  │  │ Mongoose│  │ PyMongo │  │ MongoDB │  │   mongo-go      │   │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘   │  │
│  └────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Document Structure Deep Dive

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MongoDB Document                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  {                                                                   │
│    "_id": ObjectId("507f1f77bcf86cd799439011"),  // Primary Key      │
│                                                                      │
│    "stringField": "Hello World",              // String             │
│    "numberField": 42,                          // Number (Int/Double│
│    "boolField": true,                           // Boolean           │
│    "nullField": null,                           // Null              │
│    "dateField": ISODate("2026-05-12T10:00:00Z"), // Date              │
│                                                                      │
│    "arrayField": [1, 2, 3, 4, 5],               // Array              │
│                                                                      │
│    "objectField": {                             // Embedded Object  │
│      "nestedKey": "nestedValue",               │
│      "deeplyNested": {                         │
│        "level": 2                              │
│      }                                         │
│    },                                                                  │
│                                                                      │
│    "docsCollection": [                         // Array of Objects  │
│      { "item": "book", "qty": 5 },             │
│      { "item": "pen", "qty": 10 }              │
│    ],                                                                  │
│                                                                      │
│    "geoField": {                               // GeoJSON           │
│      "type": "Point",                          │
│      "coordinates": [-73.97, 40.78]            │
│    },                                                                  │
│                                                                      │
│    "binaryField": BinData(0, "YmluYXJ5"),      // Binary Data       │
│                                                                      │
│    "objectIdField": ObjectId("..."),           // Reference         │
│                                                                      │
│    "mixedField": { "$type": "mixed" },          // Schema-less       │
│                                                                      │
│    "customField1": "..."                        // Any custom field  │
│  }                                                                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### WiredTiger Storage Engine

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WiredTiger Storage Engine                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Collection Data (documents)                │  │
│  │                                                               │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ WT Table: users.db                                      │  │  │
│  │  │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │  │  │
│  │  │ │Doc: {_id│ │Doc: {_id│ │Doc: {_id│ │Doc: {_id│  ...    │  │  │
│  │  │ │ : 1 ... │ │ : 2 ... │ │ : 3 ... │ │ : 4 ... │        │  │  │
│  │  │ │  }      │ │  }      │ │  }      │ │  }      │        │  │  │
│  │  │ └─────────┘ └─────────┘ └─────────┘ └─────────┘        │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                               │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ WT Index: users_email_idx                                │  │  │
│  │  │ Key: email value → Document pointer                      │  │  │
│  │  │                                                         │  │  │
│  │  │ "a@.com" → [Doc 1]                                       │  │  │
│  │  │ "b@.com" → [Doc 2]                                       │  │  │
│  │  │ "c@.com" → [Doc 3]                                       │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                           │                                          │
│                           ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Write-Ahead Log (WAL)                       │  │
│  │  - All writes logged before applying                         │  │
│  │  - Crash recovery support                                     │  │
│  │  - Durability guarantee                                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                           │                                          │
│                           ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    System Cache (RAM)                          │  │
│  │  - 50% of total RAM (configurable)                           │  │
│  │  - Recently accessed data + indexes                           │  │
│  │  - LRU eviction policy                                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                           │                                          │
│                           ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Disk Files (.wt)                           │  │
│  │  - collection-*.wt (data)                                     │  │
│  │  - index-*.wt (indexes)                                       │  │
│  │  - journal/WiredTigerLog.* (WAL)                              │  │
│  │  - mongod.lock                                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Architecture Diagram: Fullstack Integration

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Frontend (React/Vue)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ React Query   │  │ Apollo Client│  │  SWR                     │ │
│  │ (TanStack)    │  │ (GraphQL)    │  │  (Stale-while-revalidate)│ │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘ │
└─────────┼─────────────────┼───────────────────────┼────────────────┘
          │                 │                       │
          ▼                 ▼                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    API Layer (Node.js/Express/NestJS)                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      Middleware                                │  │
│  │  - Authentication (JWT)                                       │  │
│  │  - Rate Limiting (express-rate-limit)                        │  │
│  │  - Validation (Zod/Joi)                                       │  │
│  │  - Logging (Pino/Winston)                                     │  │
│  └─────────────────────────┬────────────────────────────────────┘  │
│                            │                                         │
│  ┌─────────────────────────▼────────────────────────────────────┐  │
│  │                   Service Layer                                 │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐  │  │
│  │  │ UserService     │  │ OrderService     │  │ ProductService│  │  │
│  │  │ - CRUD ops      │  │ - Business logic │  │ - Search      │  │  │
│  │  │ - Validation    │  │ - Calculations   │  │ - Aggregation │  │  │
│  │  └─────────────────┘  └─────────────────┘  └───────────────┘  │  │
│  └─────────────────────────┬────────────────────────────────────┘  │
└────────────────────────────┼───────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   ODM Layer (Mongoose/MongoDB ODM)                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │ Mongoose         │  │ Prisma (MongoDB)  │  │ Typegoose        │  │
│  │ - Schema def.    │  │ - Type-safe       │  │ - TypeScript     │  │
│  │ - Middleware     │  │ - Auto-generated  │  │ - Mongoose wrapper│  │
│  │ - Virtuals       │  │ - Validation      │  │                  │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  │
└───────────┼──────────────────────┼─────────────────────┼────────────┘
            │                      │                     │
            ▼                      ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     MongoDB Driver                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Connection Pool Manager                                      │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                │  │
│  │  │Conn 1 │ │Conn 2 │ │Conn 3 │ │Conn N │  ...              │  │
│  │  └────────┘ └────────┘ └────────┘ └────────┘                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MongoDB Cluster (Sharded/Replica Set)             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Primary (Writes)  ←→  Secondary (Reads)  ←→  Secondary       │  │
│  │  10.0.0.1:27017         10.0.0.2:27017      10.0.0.3:27017    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Frontend + Backend Integration Examples

### Backend Setup with Mongoose (Node.js)

```typescript
// src/models/user.model.ts
import mongoose, { Schema, Document, Model } from 'mongoose';

// TypeScript interface for type safety
export interface IAddress {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}

export interface ISocialLinks {
  twitter?: string;
  github?: string;
  linkedin?: string;
}

export interface IUser extends Document {
  _id: mongoose.Types.ObjectId;
  email: string;
  name: string;
  password: string;
  age?: number;
  address: IAddress;
  socialLinks: ISocialLinks;
  roles: string[];
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

const addressSchema = new Schema<IAddress>(
  {
    street: { type: String, required: true },
    city: { type: String, required: true },
    state: { type: String, required: true },
    zipCode: { type: String, required: true },
    country: { type: String, default: 'India' },
  },
  { _id: false }
);

const socialLinksSchema = new Schema<ISocialLinks>(
  {
    twitter: String,
    github: String,
    linkedin: String,
  },
  { _id: false }
);

const userSchema = new Schema<IUser>(
  {
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      lowercase: true,
      trim: true,
      match: [/^\S+@\S+\.\S+$/, 'Please enter a valid email'],
      index: true,
    },
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
      minlength: [2, 'Name must be at least 2 characters'],
      maxlength: [100, 'Name cannot exceed 100 characters'],
    },
    password: {
      type: String,
      required: [true, 'Password is required'],
      minlength: [8, 'Password must be at least 8 characters'],
      select: false, // Don't include in queries by default
    },
    age: {
      type: Number,
      min: [0, 'Age cannot be negative'],
      max: [150, 'Age seems invalid'],
    },
    address: {
      type: addressSchema,
      required: true,
    },
    socialLinks: {
      type: socialLinksSchema,
      default: {},
    },
    roles: {
      type: [String],
      enum: ['user', 'admin', 'moderator'],
      default: ['user'],
    },
    isActive: {
      type: Boolean,
      default: true,
    },
  },
  {
    timestamps: true, // Adds createdAt and updatedAt
    toJSON: {
      transform: function (doc, ret) {
        ret.id = ret._id;
        delete ret._id;
        delete ret.__v;
        delete ret.password;
        return ret;
      },
    },
  }
);

// Compound indexes
userSchema.index({ email: 1 });
userSchema.index({ 'address.city': 1, 'address.state': 1 });
userSchema.index({ roles: 1, isActive: 1 });

// Text index for search
userSchema.index({ name: 'text', email: 'text' });

// Middleware hooks
userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  
  const bcrypt = await import('bcryptjs');
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

userSchema.methods.comparePassword = async function (candidatePassword: string): Promise<boolean> {
  const bcrypt = await import('bcryptjs');
  return bcrypt.compare(candidatePassword, this.password);
};

// Virtual property
userSchema.virtual('fullAddress').get(function () {
  return `${this.address.street}, ${this.address.city}, ${this.address.state} - ${this.address.zipCode}`;
});

// Enable virtuals in JSON
userSchema.set('toJSON', { virtuals: true });
userSchema.set('toObject', { virtuals: true });

export const User: Model<IUser> = mongoose.model<IUser>('User', userSchema);
```

### Database Connection Manager

```typescript
// src/config/database.ts
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/myapp';

interface CachedConnection {
  conn: typeof mongoose | null;
  promise: Promise<typeof mongoose> | null;
}

const cached: CachedConnection = { conn: null, promise: null };

export async function connectDB(): Promise<typeof mongoose> {
  // Return cached connection if exists
  if (cached.conn) {
    return cached.conn;
  }

  // Create new connection if not exists
  if (!cached.promise) {
    const opts = {
      bufferCommands: false, // Disable mongoose buffering
      maxPoolSize: 10, // Connection pool size
      serverSelectionTimeoutMS: 5000, // Server selection timeout
      socketTimeoutMS: 45000, // Socket timeout
    };

    cached.promise = mongoose.connect(MONGODB_URI, opts);
  }

  try {
    cached.conn = await cached.promise;
  } catch (e) {
    cached.promise = null;
    throw e;
  }

  return cached.conn;
}

// Graceful shutdown
async function gracefulShutdown(signal: string) {
  console.log(`Received ${signal}. Closing MongoDB connection...`);
  
  await mongoose.connection.close();
  console.log('MongoDB connection closed');
  
  process.exit(0);
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

### Service Layer with Repository Pattern

```typescript
// src/services/user.service.ts
import { User, IUser } from '../models/user.model';
import { NotFoundError, ValidationError } from '../errors';

export class UserService {
  async createUser(data: Partial<IUser>): Promise<IUser> {
    // Check for existing user
    const existingUser = await User.findOne({ email: data.email });
    if (existingUser) {
      throw new ValidationError('Email already exists');
    }

    const user = new User(data);
    return user.save();
  }

  async getUserById(id: string): Promise<IUser> {
    if (!mongoose.Types.ObjectId.isValid(id)) {
      throw new ValidationError('Invalid user ID');
    }

    const user = await User.findById(id);
    if (!user) {
      throw new NotFoundError('User not found');
    }

    return user;
  }

  async getUserByEmail(email: string): Promise<IUser | null> {
    return User.findOne({ email: email.toLowerCase() }).select('+password');
  }

  async getUsers(options: {
    page?: number;
    limit?: number;
    search?: string;
    roles?: string[];
    isActive?: boolean;
  }): Promise<{ users: IUser[]; total: number; page: number; totalPages: number }> {
    const { page = 1, limit = 10, search, roles, isActive } = options;
    const skip = (page - 1) * limit;

    const query: any = {};

    if (search) {
      query.$text = { $search: search };
    }

    if (roles && roles.length > 0) {
      query.roles = { $in: roles };
    }

    if (typeof isActive === 'boolean') {
      query.isActive = isActive;
    }

    const [users, total] = await Promise.all([
      User.find(query)
        .skip(skip)
        .limit(limit)
        .sort({ createdAt: -1 }),
      User.countDocuments(query),
    ]);

    return {
      users,
      total,
      page,
      totalPages: Math.ceil(total / limit),
    };
  }

  async updateUser(id: string, data: Partial<IUser>): Promise<IUser> {
    const user = await User.findByIdAndUpdate(
      id,
      { $set: data },
      { new: true, runValidators: true }
    );

    if (!user) {
      throw new NotFoundError('User not found');
    }

    return user;
  }

  async deleteUser(id: string): Promise<void> {
    const result = await User.findByIdAndDelete(id);
    if (!result) {
      throw new NotFoundError('User not found');
    }
  }

  async softDeleteUser(id: string): Promise<IUser> {
    return this.updateUser(id, { isActive: false });
  }

  async addRoleToUser(id: string, role: string): Promise<IUser> {
    return User.findByIdAndUpdate(
      id,
      { $addToSet: { roles: role } },
      { new: true }
    );
  }

  async getActiveAdmins(): Promise<IUser[]> {
    return User.find({
      roles: 'admin',
      isActive: true,
    });
  }
}

export const userService = new UserService();
```

### API Routes (Express)

```typescript
// src/routes/user.routes.ts
import { Router, Request, Response, NextFunction } from 'express';
import { userService } from '../services/user.service';
import { validateRequest } from '../middleware/validateRequest';
import { z } from 'zod';

const router = Router();

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  password: z.string().min(8),
  age: z.number().int().positive().optional(),
  address: z.object({
    street: z.string(),
    city: z.string(),
    state: z.string(),
    zipCode: z.string(),
    country: z.string().optional(),
  }),
  roles: z.array(z.enum(['user', 'admin', 'moderator'])).optional(),
});

const updateUserSchema = createUserSchema.partial();

// Error handler wrapper
const asyncHandler = (fn: Function) => 
  (req: Request, res: Response, next: NextFunction) => 
    Promise.resolve(fn(req, res, next)).catch(next);

// POST /api/users - Create user
router.post(
  '/',
  validateRequest(createUserSchema),
  asyncHandler(async (req: Request, res: Response) => {
    const user = await userService.createUser(req.body);
    res.status(201).json({ success: true, data: user });
  })
);

// GET /api/users - List users
router.get(
  '/',
  asyncHandler(async (req: Request, res: Response) => {
    const { page, limit, search, roles, isActive } = req.query;
    
    const result = await userService.getUsers({
      page: page ? parseInt(page as string) : undefined,
      limit: limit ? parseInt(limit as string) : undefined,
      search: search as string,
      roles: roles ? (roles as string).split(',') : undefined,
      isActive: isActive ? isActive === 'true' : undefined,
    });

    res.json({ success: true, ...result });
  })
);

// GET /api/users/:id - Get user by ID
router.get(
  '/:id',
  asyncHandler(async (req: Request, res: Response) => {
    const user = await userService.getUserById(req.params.id);
    res.json({ success: true, data: user });
  })
);

// PUT /api/users/:id - Update user
router.put(
  '/:id',
  validateRequest(updateUserSchema),
  asyncHandler(async (req: Request, res: Response) => {
    const user = await userService.updateUser(req.params.id, req.body);
    res.json({ success: true, data: user });
  })
);

// DELETE /api/users/:id - Delete user
router.delete(
  '/:id',
  asyncHandler(async (req: Request, res: Response) => {
    await userService.deleteUser(req.params.id);
    res.status(204).send();
  })
);

// PATCH /api/users/:id/roles - Add role
router.patch(
  '/:id/roles',
  asyncHandler(async (req: Request, res: Response) => {
    const { role } = req.body;
    const user = await userService.addRoleToUser(req.params.id, role);
    res.json({ success: true, data: user });
  })
);

export default router;
```

### Frontend Integration (React + React Query)

```typescript
// src/api/users.ts
import { apiClient } from './client';

export interface Address {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country?: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  age?: number;
  address: Address;
  roles: string[];
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreateUserInput {
  email: string;
  name: string;
  password: string;
  age?: number;
  address: Address;
  roles?: string[];
}

export interface UpdateUserInput extends Partial<CreateUserInput> {}

export interface PaginatedResponse<T> {
  success: boolean;
  users: T[];
  total: number;
  page: number;
  totalPages: number;
}

export const userApi = {
  create: async (data: CreateUserInput): Promise<User> => {
    const response = await apiClient.post<User>('/api/users', data);
    return response.data;
  },

  list: async (params?: {
    page?: number;
    limit?: number;
    search?: string;
    roles?: string[];
    isActive?: boolean;
  }): Promise<PaginatedResponse<User>> => {
    const response = await apiClient.get<PaginatedResponse<User>>('/api/users', {
      params: params as any,
    });
    return response.data;
  },

  getById: async (id: string): Promise<User> => {
    const response = await apiClient.get<User>(`/api/users/${id}`);
    return response.data;
  },

  update: async (id: string, data: UpdateUserInput): Promise<User> => {
    const response = await apiClient.put<User>(`/api/users/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/users/${id}`);
  },

  addRole: async (id: string, role: string): Promise<User> => {
    const response = await apiClient.patch<User>(`/api/users/${id}/roles`, { role });
    return response.data;
  },
};

// src/hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi, CreateUserInput, UpdateUserInput } from '../api/users';

export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: Record<string, any>) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

export function useUsers(filters: {
  page?: number;
  limit?: number;
  search?: string;
  roles?: string[];
  isActive?: boolean;
} = {}) {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => userApi.list(filters),
    staleTime: 5 * 60 * 1000,
  });
}

export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => userApi.getById(id),
    enabled: !!id,
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
    mutationFn: ({ id, data }: { id: string; data: UpdateUserInput }) =>
      userApi.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: userKeys.list({}) });
      queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) });
    },
  });
}

export function useDeleteUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => userApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}
```

## Real-World Production Examples

### Example 1: E-commerce Product Catalog

```javascript
// Product model with variants
const productSchema = new mongoose.Schema({
  name: { type: String, required: true, text: true },
  description: { type: String },
  basePrice: { type: Number, required: true },
  
  // Dynamic attributes based on product type
  attributes: {
    type: Map,
    of: mongoose.Schema.Types.Mixed,
  },
  
  // Variants for sizes, colors, etc.
  variants: [{
    sku: { type: String, required: true, unique: true },
    size: String,
    color: String,
    price: Number,
    stock: { type: Number, default: 0 },
    images: [String],
  }],
  
  // Category hierarchy
  category: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Category',
  },
  
  // Tags for filtering
  tags: [{ type: String, index: true }],
  
  // Rating and reviews
  ratings: {
    average: { type: Number, default: 0 },
    count: { type: Number, default: 0 },
  },
  
  isActive: { type: Boolean, default: true },
  
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date },
});

// Aggregation pipeline for product search with facets
async function searchProducts(query: string, filters: any) {
  const matchStage: any = { isActive: true };
  
  if (query) {
    matchStage.$text = { $search: query };
  }
  
  if (filters.category) {
    matchStage.category = new mongoose.Types.ObjectId(filters.category);
  }
  
  if (filters.minPrice || filters.maxPrice) {
    matchStage.basePrice = {};
    if (filters.minPrice) matchStage.basePrice.$gte = filters.minPrice;
    if (filters.maxPrice) matchStage.basePrice.$lte = filters.maxPrice;
  }
  
  if (filters.tags && filters.tags.length > 0) {
    matchStage.tags = { $in: filters.tags };
  }
  
  const pipeline = [
    { $match: matchStage },
    
    // Facet for pagination and facets
    {
      $facet: {
        products: [
          { $sort: { [filters.sort || 'createdAt']: -1 } },
          { $skip: (filters.page - 1) * filters.limit },
          { $limit: filters.limit },
          {
            $project: {
              name: 1,
              description: 1,
              basePrice: 1,
              tags: 1,
              'ratings.average': 1,
              'ratings.count': 1,
            }
          }
        ],
        totalCount: [
          { $count: 'count' }
        ],
        // Facet aggregations
        categories: [
          { $group: { _id: '$category', count: { $sum: 1 } } }
        ],
        priceRange: [
          {
            $group: {
              _id: null,
              min: { $min: '$basePrice' },
              max: { $max: '$basePrice' }
            }
          }
        ],
        tagCounts: [
          { $unwind: '$tags' },
          { $group: { _id: '$tags', count: { $sum: 1 } } },
          { $sort: { count: -1 } },
          { $limit: 20 }
        ]
      }
    }
  ];
  
  return Product.aggregate(pipeline);
}
```

### Example 2: Real-time Chat Application

```javascript
// Message model for chat
const messageSchema = new mongoose.Schema({
  conversationId: { 
    type: mongoose.Schema.Types.ObjectId, 
    ref: 'Conversation',
    index: true 
  },
  senderId: { 
    type: mongoose.Schema.Types.ObjectId, 
    ref: 'User',
    index: true 
  },
  content: {
    type: String,
    maxlength: [5000, 'Message too long'],
  },
  messageType: {
    type: String,
    enum: ['text', 'image', 'file', 'system'],
    default: 'text'
  },
  metadata: {
    fileUrl: String,
    fileSize: Number,
    mimeType: String,
    thumbnailUrl: String,
  },
  status: {
    type: String,
    enum: ['sent', 'delivered', 'read'],
    default: 'sent'
  },
  readBy: [{
    userId: { type: mongoose.Schema.Types.ObjectId },
    readAt: { type: Date, default: Date.now }
  }],
  reactions: [{
    emoji: String,
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    createdAt: { type: Date, default: Date.now }
  }],
  replyTo: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Message'
  },
  createdAt: { type: Date, default: Date.now, index: true },
  updatedAt: { type: Date },
});

// Indexes for efficient queries
messageSchema.index({ conversationId: 1, createdAt: -1 });
messageSchema.index({ senderId: 1, createdAt: -1 });

// Change streams for real-time updates
export async function setupMessageStream(io: any, conversationId: string) {
  const collection = mongoose.connection.collection('messages');
  
  const changeStream = collection.watch([
    { $match: { 'fullDocument.conversationId': new mongoose.Types.ObjectId(conversationId) } }
  ], { fullDocument: 'updateLookup' });
  
  changeStream.on('change', async (change) => {
    if (change.operationType === 'insert') {
      // Broadcast new message
      io.to(conversationId).emit('newMessage', change.fullDocument);
    } else if (change.operationType === 'update') {
      // Broadcast message update
      io.to(conversationId).emit('messageUpdated', change.fullDocument);
    }
  });
  
  return changeStream;
}
```

### Example 3: Analytics Event Tracking

```javascript
// Event model with TTL index for auto-cleanup
const eventSchema = new mongoose.Schema({
  eventType: { 
    type: String, 
    required: true,
    index: true 
  },
  userId: { 
    type: mongoose.Schema.Types.ObjectId, 
    ref: 'User',
    sparse: true  // Only index when userId exists
  },
  sessionId: { type: String, required: true },
  
  // Flexible event data
  properties: {
    type: Map,
    of: mongoose.Schema.Types.Mixed,
    default: {}
  },
  
  // Geolocation data
  location: {
    type: { type: String, enum: ['Point'], default: 'Point' },
    coordinates: { type: [Number], default: [0, 0] } // [longitude, latitude]
  },
  
  // User agent info
  userAgent: {
    browser: String,
    version: String,
    os: String,
    device: String,
    isMobile: Boolean,
  },
  
  // Timestamp
  timestamp: { type: Date, default: Date.now, index: true },
  
  // Processing status
  processed: { type: Boolean, default: false },
  processedAt: Date,
});

// TTL index - auto-delete events after 90 days
eventSchema.index({ timestamp: 1 }, { expireAfterSeconds: 90 * 24 * 60 * 60 });

// Geospatial index for location queries
eventSchema.index({ 'location': '2dsphere' });

// Compound index for user analytics
eventSchema.index({ userId: 1, eventType: 1, timestamp: -1 });

// Aggregation for daily metrics
async function getDailyMetrics(date: Date) {
  const startOfDay = new Date(date);
  startOfDay.setHours(0, 0, 0, 0);
  
  const endOfDay = new Date(date);
  endOfDay.setHours(23, 59, 59, 999);
  
  return Event.aggregate([
    {
      $match: {
        timestamp: { $gte: startOfDay, $lte: endOfDay }
      }
    },
    {
      $group: {
        _id: {
          eventType: '$eventType',
          hour: { $hour: '$timestamp' }
        },
        count: { $sum: 1 },
        uniqueUsers: { $addToSet: '$userId' },
        uniqueSessions: { $addToSet: '$sessionId' }
      }
    },
    {
      $project: {
        _id: 1,
        count: 1,
        uniqueUsers: { $size: '$uniqueUsers' },
        uniqueSessions: { $size: '$uniqueSessions' }
      }
    },
    { $sort: { '_id.hour': 1 } }
  ]);
}
```

## Failure Cases

### Case 1: Schema Validation Bypass

**Problem**: Mongoose doesn't enforce validation on updates by default.

```javascript
// BAD: This bypasses validation!
User.findByIdAndUpdate(id, { email: 'invalid-email' }, { new: true });

// Also bypasses validation:
user.email = 'invalid-email';
user.save(); // Won't validate unless runValidators: true

// GOOD: Always run validators
await User.findByIdAndUpdate(id, 
  { email: 'invalid-email' },
  { new: true, runValidators: true }
);

// GOOD: Explicit validation before save
user.email = 'invalid-email';
await user.validate(); // Throws if invalid
```

### Case 2: Connection Pool Exhaustion

**Problem**: Too many connections from mongoose buffering.

```javascript
// BAD: Mongoose buffering can create many connections
mongoose.set('bufferCommands', true); // Default - waits indefinitely

// GOOD: Disable buffering, handle connection manually
mongoose.set('bufferCommands', false);

async function saveUser(data) {
  if (mongoose.connection.readyState !== 1) {
    throw new Error('Database not connected');
  }
  return User.create(data);
}

// GOOD: Proper connection pool settings
mongoose.connect(MONGODB_URI, {
  maxPoolSize: 10, // Max connections in pool
  minPoolSize: 2,  // Min connections to maintain
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
});
```

### Case 3: Memory Leaks with Change Streams

```javascript
// BAD: Not closing change streams causes memory leaks
async function setupStream() {
  const stream = Message.watch();
  
  stream.on('change', handleChange);
  // If this function is called multiple times, streams accumulate!
}

// GOOD: Properly manage and close streams
class MessageStreamManager {
  private streams: Map<string, ChangeStream> = new Map();
  
  async getStream(conversationId: string): Promise<ChangeStream> {
    if (this.streams.has(conversationId)) {
      return this.streams.get(conversationId)!;
    }
    
    const stream = Message.watch(
      [{ $match: { 'fullDocument.conversationId': new mongoose.Types.ObjectId(conversationId) } }],
      { fullDocument: 'updateLookup' }
    );
    
    stream.on('close', () => {
      this.streams.delete(conversationId);
    });
    
    this.streams.set(conversationId, stream);
    return stream;
  }
  
  async closeAll() {
    for (const stream of this.streams.values()) {
      await stream.close();
    }
    this.streams.clear();
  }
}
```

## Debugging Guide

### Using MongoDB explain()

```javascript
// Analyze query execution
const explanation = await User.find({ email: 'test@example.com' })
  .explain('executionStats');

// Key metrics to check:
explanation.executionStats:
  - executionStages.nReturned: Number of documents returned
  - executionStages.totalDocsExamined: Documents scanned (should be close to nReturned)
  - executionStages.executionTimeMillis: Query execution time
  - executionStages.indexName: Index used
  - executionStages.inputStages: Any COLLSCAN (bad) or IXSCAN (good)

// Check for collection scan
const hasCollectionScan = explanation.executionStats.executionStages
  .inputStages.some(stage => stage.stage === 'COLLSCAN');
```

### Monitoring with db.currentOp()

```javascript
// In MongoDB shell - find long-running operations
db.currentOp({
  "active": true,
  "secs_running": { "$gt": 5 },
  "ns": { "$ne": "admin.$cmd" }
});

// Kill a running operation
db.killOp(opid);

// Using mongoose for real-time monitoring
mongoose.connection.on('commandStarted', (event) => {
  console.log('MongoDB Command:', event.commandName);
  console.log('Database:', event.dbName);
  console.log('Command:', event.command);
});
```

### Profiling

```javascript
// Enable profiler (production mein sirf for debugging)
db.setProfilingLevel(2, { slowms: 100 }); // Log operations > 100ms

// Check profiler data
db.system.profile.find({ millis: { $gt: 100 } }).sort({ ts: -1 }).limit(10);

// Disable profiler
db.setProfilingLevel(0);

// Mongoose middleware for query logging
mongoose.set('debug', (collectionName, method, query, doc) => {
  console.log(`${method} ${collectionName}`, JSON.stringify(query, null, 2));
});
```

## Tradeoffs

### MongoDB vs PostgreSQL

| Aspect | MongoDB | PostgreSQL |
|--------|---------|------------|
| Data Model | Document/JSON | Relational |
| Schema | Flexible (schema-less) | Fixed |
| Joins | $lookup / embedded | Native joins |
| Transactions | Multi-doc ACID (v4+) | Native ACID |
| Write Speed | Fast (no joins) | Moderate |
| Read Speed | Fast (embedded) | Fast (indexed) |
| Scaling | Horizontal (sharding) | Vertical (mostly) |
| Data Integrity | Flexible | Strict |

### When to Use MongoDB

1. **Rapid prototyping** - No schema migrations needed
2. **Hierarchical data** - Comments in posts, categories in products
3. **Variable schema** - Different attributes per document
4. **Real-time analytics** - High write throughput
5. **Content management** - Flexible content types
6. **Logs and events** - Time-series with flexible fields

### When to Avoid MongoDB

1. **Complex transactions** - Multiple collections need atomic updates
2. **Strong relationships** - Too many lookups hurt performance
3. **Structured reporting** - SQL aggregations are more powerful
4. **Compliance requirements** - Need strict data validation

## Security Concerns

### NoSQL Injection Prevention

```javascript
// BAD: Never interpolate user input directly in queries!
const query = { email: req.body.email }; // Can be exploited
User.find({ $where: `this.email == '${req.body.email}'` }); // DANGEROUS!

// GOOD: Use parameterized queries
User.find({ email: req.body.email });

// GOOD: Validate input with Zod
const schema = z.object({
  email: z.string().email(),
});
const data = schema.parse(req.body);
User.find(data);

// GOOD: Sanitize object keys
function sanitizeQuery(obj: any): any {
  const allowed = ['email', 'name', 'age', 'isActive'];
  const sanitized: any = {};
  
  for (const key of allowed) {
    if (obj[key] !== undefined) {
      sanitized[key] = obj[key];
    }
  }
  
  return sanitized;
}
```

### Field-Level Security

```javascript
// Use projections to hide sensitive fields
User.findById(id, '-password -__v');

// Or explicitly select allowed fields
User.findById(id, 'email name roles');

// In schema, mark sensitive fields
const userSchema = new mongoose.Schema({
  password: { type: String, select: false }, // Hidden by default
  ssn: { type: String, select: false },     // Hidden by default
  creditCard: { type: String, select: false },
});

// Explicitly select sensitive fields when needed
User.findById(id).select('+password');
```

### Authentication and Authorization

```javascript
// Role-based access control middleware
function authorize(...allowedRoles) {
  return async (req, res, next) => {
    const user = await User.findById(req.userId);
    
    if (!user) {
      return res.status(401).json({ error: 'Not authenticated' });
    }
    
    const hasRole = user.roles.some(role => allowedRoles.includes(role));
    
    if (!hasRole) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    req.user = user;
    next();
  };
}

// Usage
router.delete('/:id', authenticate, authorize('admin'), deleteUser);
```

## Performance Optimization

### Indexing Strategies

```javascript
// Single field index
userSchema.index({ email: 1 });

// Compound index (order matters for queries)
orderSchema.index({ userId: 1, createdAt: -1 }); // For user's recent orders
productSchema.index({ category: 1, price: 1 }); // For category + price filter

// Multi-key index (for array fields)
productSchema.index({ tags: 1 }); // Index on each tag

// Text index for search
userSchema.index({ name: 'text', description: 'text' });

// Partial index - only index specific documents
orderSchema.index(
  { userId: 1, createdAt: -1 },
  { partialFilterExpression: { status: 'pending' } }
);

// Wildcard index - index all fields
eventSchema.index({ properties: 'ascending' }); // Index all properties fields

// Ensure index creation in production (no locking)
await User.createIndexes({ background: true });
```

### Query Optimization

```javascript
// BAD: Loading unnecessary fields
const users = await User.find({}).select('+password'); // Loads all fields!

// GOOD: Project only needed fields
const users = await User.find({}, 'name email roles');

// GOOD: Use lean() for read-only queries (faster, less memory)
const users = await User.find({ isActive: true })
  .lean(); // Returns plain objects, not mongoose documents

// GOOD: Limit results
const recentUsers = await User.find({})
  .sort({ createdAt: -1 })
  .limit(100);

// GOOD: Pagination with cursor (more efficient than skip)
const lastId = req.query.cursor;
const users = await User.find({
    createdAt: { $lt: lastId ? new Date(lastId) : new Date() }
  })
  .sort({ createdAt: -1 })
  .limit(20);

// BAD: Inefficient aggregation
const result = await User.aggregate([
  { $match: { isActive: true } },
  { $group: { _id: '$roles', count: { $sum: 1 } } }
]);

// GOOD: Use $facet for multiple aggregations in single pass
const result = await User.aggregate([
  { $match: { isActive: true } },
  {
    $facet: {
      byRole: [
        { $group: { _id: '$roles', count: { $sum: 1 } } }
      ],
      totalCount: [
        { $count: 'count' }
      ],
      avgAge: [
        { $group: { _id: null, avgAge: { $avg: '$age' } } }
      ]
    }
  }
]);
```

### Connection Pool Settings

```javascript
// Optimal settings for production
const MONGODB_URI = process.env.MONGODB_URI;

mongoose.connect(MONGODB_URI, {
  // Connection pool
  maxPoolSize: 10,          // Max connections (CPU cores * 2)
  minPoolSize: 2,           // Min connections to maintain
  maxIdleTimeMS: 30000,     // Close idle connections after 30s
  
  // Timeouts
  serverSelectionTimeoutMS: 5000,  // Server discovery timeout
  socketTimeoutMS: 45000,           // Socket timeout
  connectTimeoutMS: 10000,          // Initial connection timeout
  
  // Retry
  retryWrites: true,        // Retry failed writes
  retryReads: true,         // Retry failed reads
  
  // Compression
  compressors: 'zstd',      // Enable compression
});
```

## Scaling Challenges

### Sharding Setup

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MongoDB Sharded Cluster                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    mongos (Query Router)                        │ │
│  │                      client connections                          │ │
│  └─────────────────────────┬──────────────────────────────────────┘ │
│                            │                                        │
│              ┌─────────────┼─────────────┐                         │
│              │             │             │                          │
│              ▼             ▼             ▼                          │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐            │
│  │    Shard 1    │ │    Shard 2    │ │    Shard 3    │            │
│  │  {_id: 0-100} │ │ {_id: 101-200}│ │ {_id: 201-300}│            │
│  │               │ │               │ │               │            │
│  │ ┌───┐┌───┐┌───┐│ │ ┌───┐┌───┐┌───┐│ │ ┌───┐┌───┐┌───┐│            │
│  │ │   ││   ││   ││ │ │   ││   ││   ││ │ │   ││   ││   ││            │
│  │ │ P ││ S ││ S ││ │ │ P ││ S ││ S ││ │ │ P ││ S ││ S ││            │
│  │ └───┘└───┘└───┘│ │ └───┘└───┘└───┘│ │ └───┘└───┘└───┘│            │
│  └───────────────┘ └───────────────┘ └───────────────┘            │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                Config Servers (3-node replica set)             │ │
│  │     Stores metadata: shard membership, chunk distribution      │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

```javascript
// Enable sharding from MongoDB shell
sh.enableSharding('myapp');

sh.shardCollection('myapp.users', { email: 'hashed' });
sh.shardCollection('myapp.orders', { userId: 'hashed', createdAt: 1 });

// Hash-based sharding for even distribution
// Range-based sharding for time-series data
```

### Replica Set Read Preferences

```javascript
// Read from secondary replicas for better performance
const options = {
  readPreference: 'secondaryPreferred', // Read from secondary, primary if none
};

// For analytics, always read from secondary
const analyticsDb = mongoose.createConnection(
  MONGODB_URI,
  { readPreference: 'secondary' }
);

// Tag-based routing for specific data needs
const options = {
  readPreference: { 
    mode: 'secondaryPreferred',
    tags: [{ region: 'us-east' }]
  }
};
```

## Best Practices

### 1. Always Use Schema Validation

```javascript
// Define strict schemas with validation
const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\S+@\S+\.\S+$/, 'Invalid email format'],
    index: true,
  },
  age: {
    type: Number,
    min: [0, 'Age cannot be negative'],
    max: [150, 'Age seems invalid'],
  },
  status: {
    type: String,
    enum: ['active', 'inactive', 'suspended'],
    default: 'active',
  },
}, {
  timestamps: true,
  strict: 'throw', // Throw on unknown fields
});
```

### 2. Use Transactions for Multi-Document Operations

```javascript
async function transferCredits(fromUserId: string, toUserId: string, amount: number) {
  const session = await mongoose.startSession();
  
  try {
    session.startTransaction({
      readConcern: { level: 'snapshot' },
      writeConcern: { w: 'majority' }
    });
    
    // Debit from source
    const fromUser = await User.findByIdAndUpdate(
      fromUserId,
      { $inc: { credits: -amount } },
      { new: true, session }
    );
    
    if (fromUser.credits < 0) {
      throw new Error('Insufficient credits');
    }
    
    // Credit to destination
    await User.findByIdAndUpdate(
      toUserId,
      { $inc: { credits: amount } },
      { new: true, session }
    );
    
    // Log transaction
    await Transaction.create([{
      fromUserId,
      toUserId,
      amount,
      type: 'transfer'
    }], { session });
    
    await session.commitTransaction();
    
  } catch (error) {
    await session.abortTransaction();
    throw error;
  } finally {
    session.endSession();
  }
}
```

### 3. Implement Soft Deletes

```javascript
// Add deletedAt for soft delete
const userSchema = new mongoose.Schema({
  // ... fields
  deletedAt: { type: Date, default: null },
  deletedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
});

// Query helper to exclude deleted
userSchema.query.byActive = function() {
  return this.where({ deletedAt: null });
};

// Usage
const activeUsers = await User.find().byActive();

// Default query exclusion in model
userSchema.pre(/^find/, function(next) {
  // Don't return deleted documents by default
  if (this.getQuery().deletedAt === undefined) {
    this.where({ deletedAt: null });
  }
  next();
});
```

### 4. Use Aggregation Pipelines for Complex Operations

```javascript
// Efficient aggregation instead of multiple queries
async function getUserDashboard(userId: string) {
  return User.aggregate([
    { $match: { _id: new mongoose.Types.ObjectId(userId) } },
    
    // Lookup orders
    {
      $lookup: {
        from: 'orders',
        localField: '_id',
        foreignField: 'userId',
        as: 'orders'
      }
    },
    
    // Lookup reviews
    {
      $lookup: {
        from: 'reviews',
        localField: '_id',
        foreignField: 'userId',
        as: 'reviews'
      }
    },
    
    // Calculate stats
    {
      $addFields: {
        totalOrders: { $size: '$orders' },
        totalSpent: { $sum: '$orders.totalAmount' },
        avgReviewRating: { $avg: '$reviews.rating' },
        membershipTier: {
          $switch: {
            branches: [
              { case: { $gte: ['$totalSpent', 10000] }, then: 'gold' },
              { case: { $gte: ['$totalSpent', 5000] }, then: 'silver' },
            ],
            default: 'bronze'
          }
        }
      }
    },
    
    // Project final fields
    {
      $project: {
        _id: 1,
        name: 1,
        email: 1,
        totalOrders: 1,
        totalSpent: 1,
        avgReviewRating: 1,
        membershipTier: 1,
      }
    }
  ]);
}
```

## Common Mistakes

### Mistake 1: Not Using Projections

```javascript
// BAD: Fetches all fields including large ones
const user = await User.findById(id);

// GOOD: Only fetch needed fields
const user = await User.findById(id, 'name email profilePicture');
```

### Mistake 2: Using findOneAndUpdate Without Return

```javascript
// BAD: Missing return statement
await User.findOneAndUpdate(
  { email },
  { $set: { lastLogin: new Date() } }
);
// User document returned but not used

// GOOD: Capture the result
const updatedUser = await User.findOneAndUpdate(
  { email },
  { $set: { lastLogin: new Date() } },
  { new: true }
);
```

### Mistake 3: Not Handling Connection Events

```javascript
// BAD: No connection monitoring
mongoose.connect(MONGODB_URI);

// GOOD: Handle connection events
mongoose.connection.on('connected', () => {
  console.log('MongoDB connected');
});

mongoose.connection.on('error', (err) => {
  console.error('MongoDB error:', err);
});

mongoose.connection.on('disconnected', () => {
  console.warn('MongoDB disconnected');
});
```

## Interview Questions

### Q1: Explain MongoDB's document model and when to use embedding vs referencing

**Answer**: Embedding stores related data in a single document, ideal for 1:1 or 1:few relationships where data is accessed together. Referencing stores data in separate documents and uses $lookup to join, ideal for many:many relationships or when data is frequently updated independently.

### Q2: What is a Change Stream in MongoDB?

**Answer**: Change streams allow applications to subscribe to real-time changes in a collection, using MongoDB's underlying replication mechanism. It's used for building real-time features like notifications, sync, and event-driven architectures.

### Q3: How does MongoDB handle transactions?

**Answer**: Since MongoDB 4.0, multi-document ACID transactions are supported using snapshot isolation. Transactions require replica set or sharded cluster. Use session.startTransaction() and session.commitTransaction() for atomic operations across documents.

### Q4: What is the difference between sharding and replication?

**Answer**: Replication copies data across multiple nodes for redundancy and read scaling. Sharding distributes data across shards for write scaling and horizontal scalability. MongoDB typically uses both: replica sets per shard, with multiple shards in a cluster.

### Q5: Explain MongoDB indexes and their types

**Answer**: Indexes improve query performance. Types include: single field, compound (multiple fields), multi-key (arrays), text, geospatial (2dsphere), hashed (for sharding), and partial (subset of documents).

### Q6: What is the WiredTiger storage engine?

**Answer**: WiredTiger is MongoDB's default storage engine since 3.2. It provides document-level locking, compression, and in-memory caching. It uses checkpoint snapshots and write-ahead logging for crash recovery.

### Q7: How would you design a schema for a messaging app?

**Answer**: Consider embedding recent messages in conversations for quick access, use separate messages collection for full history. Index on conversationId + timestamp. Use recipientId index for inbox queries. Consider lastMessage virtual for conversation preview.

## Latest 2026 Fullstack Engineering Patterns

### Pattern 1: Multi-Tenant SaaS with MongoDB

```javascript
// Tenant isolation at database level
class TenantManager {
  private connections: Map<string, mongoose.Connection> = new Map();
  
  async getConnection(tenantId: string): Promise<mongoose.Connection> {
    if (this.connections.has(tenantId)) {
      return this.connections.get(tenantId)!;
    }
    
    const conn = mongoose.createConnection(
      `${MONGODB_URI}/${tenantId}`,
      {
        maxPoolSize: 5,
        minPoolSize: 1,
      }
    );
    
    this.connections.set(tenantId, conn);
    return conn;
  }
  
  // Each tenant gets their own database
  // URL: mongodb://host:27017/tenant_abc123
}

// Usage in API
app.use('/api/:tenantId', async (req, res, next) => {
  const { tenantId } = req.params;
  req.tenantDb = await tenantManager.getConnection(tenantId);
  next();
});
```

### Pattern 2: Event Sourcing with MongoDB

```javascript
// Event store pattern
const eventSchema = new mongoose.Schema({
  aggregateId: { type: String, required: true, index: true },
  aggregateType: { type: String, required: true },
  eventType: { type: String, required: true },
  eventData: { type: mongoose.Schema.Types.Mixed, required: true },
  metadata: { type: mongoose.Schema.Types.Mixed },
  version: { type: Number, required: true },
  timestamp: { type: Date, default: Date.now },
});

eventSchema.index({ aggregateId: 1, version: 1 }, { unique: true });

// Projections for read models
async function handleAccountCreated(event: any) {
  await Account.create({
    accountId: event.aggregateId,
    balance: event.eventData.initialBalance,
    currency: event.eventData.currency,
    createdAt: event.timestamp,
  });
}

// Rebuild projection from events
async function rebuildProjection(accountId: string) {
  const events = await Event.find({ aggregateId: accountId })
    .sort({ version: 1 });
  
  for (const event of events) {
    await applyEvent(event);
  }
}
```

### Pattern 3: GraphQL with MongoDB

```javascript
// Resolvers with DataLoader for N+1 prevention
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await User.find({ _id: { $in: ids } });
  const userMap = new Map(users.map(u => [u._id.toString(), u]));
  return ids.map(id => userMap.get(id) || null);
});

// GraphQL resolvers
const resolvers = {
  Post: {
    author: (post) => userLoader.load(post.authorId),
  },
  
  User: {
    posts: async (user) => {
      return Post.find({ authorId: user._id });
    },
  },
  
  Query: {
    user: async (_, { id }) => userLoader.load(id),
    users: async (_, { limit }) => User.find().limit(limit),
  },
  
  Mutation: {
    createPost: async (_, { input }) => {
      return Post.create(input);
    },
  },
};
```

### Pattern 4: Real-time Subscriptions with MongoDB

```javascript
// MongoDB Change Streams with Socket.io
import { Server } from 'socket.io';
import mongoose from 'mongoose';

function setupRealtimeSync(io: Server) {
  const collection = mongoose.connection.collection('tasks');
  
  const changeStream = collection.watch([], {
    fullDocument: 'updateLookup'
  });
  
  changeStream.on('change', async (change) => {
    const affectedTasks = await getAffectedTaskIds(change);
    
    for (const taskId of affectedTasks) {
      io.to(`task:${taskId}`).emit('taskUpdated', {
        taskId,
        change: transformChange(change),
      });
    }
  });
  
  return changeStream;
}

// Socket.io handlers
io.on('connection', (socket) => {
  socket.on('subscribe:task', (taskId) => {
    socket.join(`task:${taskId}`);
  });
  
  socket.on('unsubscribe:task', (taskId) => {
    socket.leave(`task:${taskId}`);
  });
});
```

This comprehensive guide covers MongoDB from basics to advanced production patterns. Practice these concepts and always consider the tradeoffs when choosing database solutions for your fullstack applications.
