# Node.js and Runtime Deep Dive

Bhai, Node.js samajhna zaroori hai agar tu fullstack developer banna chahta hai. Ye JavaScript ko browser ke bahar le jaata hai aur server pe chalata hai. Chalo detail mein sab kuch samajhte hain!

---

## 1. Beginner-Friendly Hinglish Explanation

### Kya Hai Node.js?

Soch ki tu ek **Chrome browser** mein JavaScript likhta tha. Us browser mein ek engine hota hai jo JS code samajhta aur execute karta hai - uska naam **V8** hai. Ab Node.js bhi usi V8 engine ko use karta hai, bas browser ke bahar!

Matlab JavaScript ab sirf web pages banana nahi seekh raha, balki:
- Server pe API bana sakta hai
- Files read/write kar sakta hai
- Database se connect ho sakta hai
- Background tasks kar sakta hai

### Event Loop Samjho

Node.js ka sabse bada USP hai **Event Loop**. Soch iseaise:
- Tu ek **waiter** hai ek restaurant mein
- Customer order deta hai, tu order kitchen mein deta hai
- Kitchen kaam kar raha hai, tu meanwhile dusre customer ka order le sakta hai
- Jab kitchen ready hai, tu food pickup karta hai aur deliver karta hai

Isse **non-blocking** kahte hain. Matlab Node.js ek task complete hone ka wait nahi karta, directly next task shuru kar deta hai.

### npm - Node Package Manager

npm hai jaise ek big supermarket jahan har cheez milti hai:
- React, Vue, Angular libraries
- Express, FastAPI server frameworks
- Database drivers
- Testing tools
- Utility libraries

Bas `npm install package-name` likh aur library use kar!

---

## 2. Deep Technical Explanation

### Node.js Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Node.js API                          │
│  (fs, http, crypto, buffer, stream, events, path, etc.)     │
├─────────────────────────────────────────────────────────────┤
│                    Node.js Bindings                          │
│           (C++ Addons via node-gyp, NAN)                    │
├─────────────────────────────────────────────────────────────┤
│                     libuv Library                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Event Loop   │  │ Thread Pool  │  │ Async I/O Ops    │  │
│  │ (4 phases)   │  │ (4 threads)  │  │ (network, fs)    │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    V8 JavaScript Engine                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Parser       │  │ Ignition     │  │ TurboFan         │  │
│  │ (AST)        │  │ (Interpreter)│  │ (Optimizing      │  │
│  │              │  │              │  │ Compiler)        │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                     Operating System                         │
│              (Windows, Linux, macOS)                         │
└─────────────────────────────────────────────────────────────┘
```

### Event Loop Phases Detail

```javascript
// Event Loop ke 6 phases hote hain:

/*
 * Phase 1: timers
 *   - setTimeout() callbacks execute hote hain
 *   - First! Phases start hote hi ye run hote hain
 *
 * Phase 2: pending callbacks
 *   - Pending callbacks execute hote hain
 *   - I/O callbacks jo phaseleag gaye the
 *
 * Phase 3: idle, prepare
 *   - Internal use only, ignore this
 *
 * Phase 4: poll
 *   - NEW! I/O callbacks execute hote hain
 *   - System agar koi timers/files ready hain
 *
 * Phase 5: check
 *   - setImmediate() callbacks yahan execute hote hain
 *
 * Phase 6: close callbacks
 *   - close event callbacks (socket.destroy, etc.)
 */

// Wahi phir se timers se shuru!
// process.nextTick() aur Promise.then() bahut special hain
// Ye current phase ke baad, next phase se pehle run hote hain
```

### V8 Engine Optimization

```javascript
// V8 JIT (Just-In-Time) Compilation

// 1. Baseline Compilation (Ignition)
function add(a, b) {
  return a + b;
}

// 2. Optimization (TurboFan)
// Agar function multiple baar same types ke saath call ho,
// TurboFan optimize kar deta hai

// 3. Deoptimization
// Agar type change ho gayi, TurboFan backtrack kar sakta hai

// Example: V8 optimization tips
class User {
  constructor(name, age) {
    this.name = name;      // String
    this.age = age;         // Number
    this.createdAt = Date.now();
  }

  // Methods ko prototype pe define karo (better optimization)
  getProfile() {
    return `${this.name} (${this.age})`;
  }
}

// Yeh avoid karo - inline methods (memory bacha, perf better)
// Bad: constructor mein method define karna
```

### libuv Thread Pool

```javascript
// libuv 4 threads ka pool rakhta hai (default)
// Ye tasks handle karta hai:
// - File system operations
// - DNS lookups (dns.lookup)
// - Compression (zlib)
// - Crypto operations
// - Some native addon async operations

// Thread pool size badhana (environment variable se)
process.env.UV_THREADPOOL_SIZE = 8; // Max 1024

// Example: File operations thread pool use karte hain
const fs = require('fs');

console.time('file-read');
fs.readFile('./large-file.txt', 'utf8', (err, data) => {
  console.timeEnd('file-read'); // Slow - thread pool use hota hai
});
```

---

## 3. Architecture Diagrams

### Monolithic vs Microservices Architecture with Node.js

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MONOLITHIC NODE.JS APP                          │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │   Routes    │  │ Controllers │  │   Services  │  │  Database │ │
│  │   Layer     │──│   Layer     │──│   Layer     │──│  (MySQL)  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘ │
│         │               │               │                         │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    Single Process                           │  │
│  │                  (All code together)                         │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                  MICROSERVICES ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │  API Gateway │───>│ Auth Service │    │ User Service         │  │
│  │  (Kong/Nginx)│    │  :3001       │    │  :3002                │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│         │                   │                      │               │
│         v                   v                      v               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │ Order Service│    │Notify Service│    │ Product Service      │  │
│  │  :3003       │    │  :3004       │    │  :3005               │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│         │                   │                      │               │
│         v                   v                      v               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │ Order DB     │    │Notify Queue  │    │ Product DB          │  │
│  │ (PostgreSQL) │    │   (Redis)    │    │  (MongoDB)          │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Node.js Cluster Mode

```
┌─────────────────────────────────────────────────────────────────────┐
│                      MASTER PROCESS                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Load Balancer                              │   │
│  │   ┌─────────────────────────────────────────────────────┐   │   │
│  │   │           Round Robin / Least Connections            │   │   │
│  │   └─────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│           ┌──────────────────┼──────────────────┐                 │
│           │                  │                  │                  │
│           v                  v                  v                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │
│  │   Worker 1   │    │   Worker 2   │    │   Worker N   │        │
│  │   (PID: 123) │    │   (PID: 124) │    │   (PID: 125) │        │
│  │   Port: 3000 │    │   Port: 3000 │    │   Port: 3000 │        │
│  └──────────────┘    └──────────────┘    └──────────────┘        │
│         │                 │                  │                    │
│         v                 v                  v                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │
│  │  CPU Core 1  │    │  CPU Core 2  │    │  CPU Core N  │        │
│  └──────────────┘    └──────────────┘    └──────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
```

### Express.js Request-Response Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         REQUEST FLOW                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Client Request                                                    │
│   GET /api/users/123                                                │
│         │                                                           │
│         v                                                           │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    EXPRESS MIDDLEWARE                       │   │
│   │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐ │   │
│   │  │ cors()    │──│helmet()   │──│json()     │──│  auth   │ │   │
│   │  │ middleware│  │ security  │  │ body-    │  │ verify  │ │   │
│   │  └───────────┘  └───────────┘  │ parser   │  └─────────┘ │   │
│   │                                 └───────────┘               │   │
│   └─────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         v                                                           │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                      ROUTES                                  │   │
│   │   app.get('/api/users/:id', userController.getUser)          │   │
│   └─────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         v                                                           │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                   CONTROLLER                                 │   │
│   │   - Extract params, query, body                             │   │
│   │   - Call service layer                                      │   │
│   │   - Handle errors                                            │   │
│   └─────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         v                                                           │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    SERVICE LAYER                             │   │
│   │   - Business logic                                           │   │
│   │   - Database queries via Repository                          │   │
│   │   - Cache checks (Redis)                                     │   │
│   └─────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         v                                                           │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                   DATABASE                                   │   │
│   │              PostgreSQL / MongoDB                            │   │
│   └─────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         v                                                           │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    RESPONSE                                 │   │
│   │          { success: true, data: { id: 123, ... } }          │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Frontend + Backend Integration Examples

### React + Node.js Integration

```javascript
// BACKEND: Express Server Setup
// File: server/index.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const { PrismaClient } = require('@prisma/client');

const app = express();
const prisma = new PrismaClient();

// Middleware Stack
app.use(helmet());           // Security headers
app.use(cors({
  origin: ['http://localhost:3000', 'https://myapp.com'],
  credentials: true
}));
app.use(morgan('combined')); // Logging
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Health Check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Routes
const userRoutes = require('./routes/users');
const productRoutes = require('./routes/products');
const orderRoutes = require('./routes/orders');

app.use('/api/users', userRoutes);
app.use('/api/products', productRoutes);
app.use('/api/orders', orderRoutes);

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('Error:', err);
  
  if (err.name === 'ValidationError') {
    return res.status(400).json({
      success: false,
      error: 'Validation failed',
      details: err.message
    });
  }
  
  if (err.code === 'P2002') { // Prisma unique constraint
    return res.status(409).json({
      success: false,
      error: 'Resource already exists'
    });
  }
  
  res.status(err.status || 500).json({
    success: false,
    error: process.env.NODE_ENV === 'production' 
      ? 'Internal server error' 
      : err.message
  });
});

// Graceful Shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully');
  await prisma.$disconnect();
  server.close(() => {
    console.log('Process terminated');
    process.exit(0);
  });
});

const PORT = process.env.PORT || 3000;
const server = app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = { app, server };
```

```javascript
// BACKEND: Controller with Service Layer
// File: server/controllers/userController.js
const userService = require('../services/userService');
const { validationResult } = require('express-validator');

exports.getUser = async (req, res, next) => {
  try {
    const { id } = req.params;
    
    const user = await userService.findById(id);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      });
    }
    
    res.json({
      success: true,
      data: user
    });
  } catch (error) {
    next(error);
  }
};

exports.createUser = async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const { name, email, password, role } = req.body;
    
    const user = await userService.create({
      name,
      email,
      password,
      role: role || 'user'
    });
    
    res.status(201).json({
      success: true,
      data: user,
      message: 'User created successfully'
    });
  } catch (error) {
    next(error);
  }
};

exports.updateUser = async (req, res, next) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    
    const user = await userService.update(id, updates);
    
    res.json({
      success: true,
      data: user
    });
  } catch (error) {
    next(error);
  }
};

exports.deleteUser = async (req, res, next) => {
  try {
    const { id } = req.params;
    
    await userService.delete(id);
    
    res.json({
      success: true,
      message: 'User deleted successfully'
    });
  } catch (error) {
    next(error);
  }
};
```

```typescript
// FRONTEND: React API Client
// File: client/src/api/client.ts
import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

// Create axios instance with defaults
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // For cookies/CORS
});

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('authToken');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token expired - redirect to login
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;

// File: client/src/api/users.ts
import apiClient from './client';
import { User, CreateUserDto, UpdateUserDto } from '../types';

export const userApi = {
  getAll: async (params?: { page?: number; limit?: number }) => {
    const response = await apiClient.get<{
      success: boolean;
      data: User[];
      pagination: { total: number; page: number; limit: number };
    }>('/users', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await apiClient.get<{ success: boolean; data: User }>(
      `/users/${id}`
    );
    return response.data;
  },

  create: async (data: CreateUserDto) => {
    const response = await apiClient.post<{ success: boolean; data: User }>(
      '/users',
      data
    );
    return response.data;
  },

  update: async (id: string, data: UpdateUserDto) => {
    const response = await apiClient.put<{ success: boolean; data: User }>(
      `/users/${id}`,
      data
    );
    return response.data;
  },

  delete: async (id: string) => {
    await apiClient.delete(`/users/${id}`);
  },
};

// File: client/src/hooks/useUsers.ts
import { useState, useEffect, useCallback } from 'react';
import { userApi } from '../api/users';
import { User } from '../types';

export function useUsers(initialPage = 1, initialLimit = 10) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    page: initialPage,
    limit: initialLimit,
    total: 0,
  });

  const fetchUsers = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await userApi.getAll({
        page: pagination.page,
        limit: pagination.limit,
      });
      setUsers(result.data);
      setPagination((prev) => ({ ...prev, total: result.pagination.total }));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch users');
    } finally {
      setLoading(false);
    }
  }, [pagination.page, pagination.limit]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const nextPage = () => setPagination((p) => ({ ...p, page: p.page + 1 }));
  const prevPage = () => setPagination((p) => ({ ...p, page: Math.max(1, p.page - 1) }));

  return { users, loading, error, pagination, nextPage, prevPage, refetch: fetchUsers };
}
```

---

## 5. Real-World Production Examples

### Netflix-Style Node.js Architecture

```javascript
// Production-grade Node.js setup with clustering
// File: server.js
const cluster = require('cluster');
const os = require('os');
const express = require('express');

const numCPUs = process.env.WEB_CONCURRENCY || os.cpus().length;

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`);
  console.log(`Forking for ${numCPUs} CPUs...`);

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Handle worker exit
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    console.log('Starting a new worker...');
    cluster.fork();
  });

  // Restart stuck workers
  cluster.on('listening', (worker, address) => {
    console.log(`Worker ${worker.process.pid} started`);
  });
} else {
  // Worker process - run Express app
  const app = express();
  
  // ... your app setup
  
  app.listen(3000);
  console.log(`Worker ${process.pid} handling requests on port 3000`);
}
```

### WhatsApp-Style Message Queue System

```javascript
// Using BullMQ for job queues (like WhatsApp message processing)
// File: workers/messageWorker.js
const { Worker, Queue, QueueEvents } = require('bullmq');
const IORedis = require('ioredis');

// Redis connection
const connection = new IORedis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  maxRetriesPerRequest: null,
  enableReadyCheck: false,
});

// Message Queue
const messageQueue = new Queue('messages', { connection });

// Add jobs to queue
async function sendMessage(message) {
  await messageQueue.add('send-message', {
    messageId: message.id,
    from: message.from,
    to: message.to,
    content: message.content,
    timestamp: Date.now(),
  }, {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: 100,
    removeOnFail: 1000,
  });
}

// Worker
const messageWorker = new Worker('messages', async (job) => {
  console.log(`Processing message ${job.data.messageId}`);
  
  // Simulate sending message
  await sendToExternalService(job.data);
  
  // Update database
  await prisma.message.update({
    where: { id: job.data.messageId },
    data: { status: 'delivered', deliveredAt: new Date() },
  });
  
}, { connection });

// Queue events for monitoring
const queueEvents = new QueueEvents('messages', { connection });

queueEvents.on('completed', ({ jobId }) => {
  console.log(`Job ${jobId} completed`);
});

queueEvents.on('failed', ({ jobId, failedReason }) => {
  console.log(`Job ${jobId} failed: ${failedReason}`);
  // Send to dead letter queue or alerting
});

module.exports = { sendMessage, messageQueue };
```

### Instagram-Style Image Processing Pipeline

```javascript
// Image processing with sharp and BullMQ
// File: workers/imageProcessor.js
const { Worker } = require('bullmq');
const sharp = require('sharp');
const { Storage } = require('@google-cloud/storage');
const path = require('path');
const connection = new (require('ioredis'))({ /* config */ });

const imageWorker = new Worker('image-processing', async (job) => {
  const { imageId, originalPath, userId } = job.data;
  
  console.log(`Processing image ${imageId} for user ${userId}`);
  
  // Get image buffer from storage
  const storage = new Storage();
  const bucket = storage.bucket('my-app-images');
  const file = bucket.file(originalPath);
  const [buffer] = await file.download();
  
  // Generate multiple sizes
  const sizes = [
    { name: 'thumbnail', width: 150, height: 150 },
    { name: 'small', width: 320, height: 320 },
    { name: 'medium', width: 640, height: 640 },
    { name: 'large', width: 1280, height: 1280 },
  ];
  
  const processedImages = {};
  
  for (const size of sizes) {
    const processedBuffer = await sharp(buffer)
      .resize(size.width, size.height, {
        fit: 'cover',
        position: 'center',
      })
      .jpeg({ quality: 80 })
      .toBuffer();
    
    const outputPath = `users/${userId}/${size.name}/${imageId}.jpg`;
    await bucket.file(outputPath).save(processedBuffer);
    
    processedImages[size.name] = outputPath;
  }
  
  // Update database with processed image URLs
  await prisma.image.update({
    where: { id: imageId },
    data: {
      thumbnailUrl: processedImages.thumbnail,
      smallUrl: processedImages.small,
      mediumUrl: processedImages.medium,
      largeUrl: processedImages.large,
      status: 'processed',
    },
  });
  
  return processedImages;
}, { connection });
```

---

## 6. Failure Cases

### Case 1: Event Loop Blocking

```javascript
// PROBLEM: Synchronous code blocks event loop
// File: bad-example.js

// THIS IS BAD - Never do this in production!
app.get('/api/heavy-computation', (req, res) => {
  let result = 0;
  
  // Heavy computation - blocks event loop for seconds!
  for (let i = 0; i < 10000000000; i++) {
    result += Math.sqrt(i);
  }
  
  res.json({ result });
});

// What happens:
// 1. Request hits server
// 2. Loop starts executing (blocks all other requests)
// 3. All other users see "connection timeout" or very slow response
// 4. Server appears frozen/dead

// SOLUTION: Use async patterns or worker threads
// Good approach with worker threads
const { Worker } = require('worker_threads');

function runHeavyComputation(data) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./heavy-task.js', {
      workerData: data,
    });
    
    worker.on('message', resolve);
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`));
    });
  });
}

app.get('/api/heavy-computation', async (req, res) => {
  try {
    // Offload to worker thread - event loop stays free
    const result = await runHeavyComputation(req.query.data);
    res.json({ result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Case 2: Memory Leaks

```javascript
// PROBLEM: Growing memory usage over time
// File: memory-leak-example.js

// BAD: Event listeners accumulating
const eventEmitter = new (require('events').EventEmitter)();

app.post('/api/events', (req, res) => {
  // Every request adds a new listener - memory leak!
  eventEmitter.on('data', (data) => {
    console.log('Processing:', data);
  });
  
  eventEmitter.emit('data', req.body);
  res.json({ success: true });
});

// BAD: Global arrays growing unbounded
const requestLog = []; // Keeps growing forever!

app.use((req, res, next) => {
  // This array will use all memory eventually
  requestLog.push({
    timestamp: Date.now(),
    path: req.path,
  });
  next();
});

// BAD: Closures holding references
function createHandler() {
  const largeData = new Array(10000).fill('*'); // 10KB
  
  return function handler(req, res) {
    // largeData stays in memory as long as handler exists
    // If handlers are created repeatedly, memory grows
    res.json({ data: largeData });
  };
}

// SOLUTIONS:
app.set('trust proxy', true);

// 1. Use bounded data structures
const LRUCache = require('lru-cache');
const cache = new LRUCache({ max: 500, ttl: 1000 * 60 * 5 });

// 2. Remove event listeners
app.post('/api/events', (req, res) => {
  const handler = (data) => console.log('Processing:', data);
  eventEmitter.emit('data', req.body);
  eventEmitter.off('data', handler); // Clean up!
  res.json({ success: true });
});

// 3. Monitor with memory profiling
if (process.env.NODE_ENV === 'production') {
  setInterval(() => {
    const used = process.memoryUsage();
    console.log({
      rss: `${Math.round(used.rss / 1024 / 1024)} MB`,
      heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)} MB`,
      heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)} MB`,
    });
  }, 30000);
}
```

### Case 3: Unhandled Promise Rejections

```javascript
// PROBLEM: Unhandled rejections crash the process
// File: unhandled-rejection.js

// This WILL crash your server in Node 15+
async function riskyOperation() {
  const data = await fetch('http://external-api.com/data');
  if (!data.ok) throw new Error('API failed');
  return data.json();
}

app.get('/api/data', async (req, res) => {
  // If this throws, and you don't catch it, server might crash
  const result = await riskyOperation();
  res.json(result);
});

// Without proper error handling:
// 1. Promise rejects
// 2. No .catch() handler
// 3. Node 15+ crashes the process
// 4. All users get "Connection reset"

// SOLUTIONS:

// 1. Always use try/catch
app.get('/api/data', async (req, res, next) => {
  try {
    const result = await riskyOperation();
    res.json(result);
  } catch (error) {
    next(error); // Pass to error handler
  }
});

// 2. Handle unhandled rejections globally
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Log to monitoring service
  // Sentry.captureException(reason);
});

// 3. Use express-async-errors
require('express-async-errors');
// Now you don't need try/catch in every route!
app.get('/api/data', async (req, res) => {
  const result = await riskyOperation(); // Errors auto-caught
  res.json(result);
});

// 4. Domain-based isolation (legacy but useful for critical operations)
const domain = require('domain');
const d = domain.create();

d.on('error', (err) => {
  console.error('Domain error:', err);
  res.status(500).json({ error: 'Something went wrong' });
});

d.run(() => {
  const server = app.listen(3000);
  server.on('close', () => d.exit());
});
```

---

## 7. Debugging Guide

### Node.js Debugging Techniques

```javascript
// 1. Built-in debugger
// Start with: node --inspect server.js
// Then open chrome://inspect in Chrome browser

// 2. VS Code launch.json configuration
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Server",
      "program": "${workspaceFolder}/server.js",
      "runtimeExecutable": "nodemon",
      "restart": true,
      "env": { "NODE_ENV": "development" },
      "console": "integratedTerminal"
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Process",
      "port": 9229
    }
  ]
}

// 3. Performance debugging with --prof
// node --prof server.js
// Run some requests
// node --prof-process isolate-*.log > profile.txt
// Analyze the output

// 4. Heap snapshots
const v8 = require('v8');
const fs = require('fs');

app.post('/debug/heap-snapshot', (req, res) => {
  const filename = `heap-${Date.now()}.heapsnapshot`;
  const snapshotStream = v8.writeHeapSnapshot(filename);
  
  // Also get current memory
  const mem = process.memoryUsage();
  
  res.json({
    message: 'Snapshot created',
    filename,
    memory: {
      rss: `${Math.round(mem.rss / 1024 / 1024)}MB`,
      heapUsed: `${Math.round(mem.heapUsed / 1024 / 1024)}MB`,
      heapTotal: `${Math.round(mem.heapTotal / 1024 / 1024)}MB`,
    }
  });
});

// 5. Clinical (flamegraph) profiling
// npm install clinic
// clinic doctor -- node server.js
// clinic flame -- node server.js

// 6. Debug specific modules
// DEBUG=express:* node server.js
// DEBUG=sql:* node server.js
// DEBUG=* node server.js (see everything)

// 7. Memory leak detection
const heapdump = require('heapdump');

// Take snapshot on SIGUSR2
process.on('SIGUSR2', () => {
  heapdump.writeSnapshot('./' + Date.now() + '.heapsnapshot');
});

// 8. Async stack traces
// npm install stackman
const stackman = require('stackman')();

function logAsyncError(error) {
  stackman(error, (err, stack) => {
    console.log('Error:', err);
    console.log('Stack:', stack);
  });
}
```

### Express.js Request Logging

```javascript
// Custom morgan tokenizer for detailed logging
const morgan = require('morgan');
const os = require('os');

// Custom token for request body
morgan.token('body', (req) => {
  if (Object.keys(req.body || {}).length > 0) {
    return JSON.stringify(req.body);
  }
  return '-';
});

// Custom token for response time with color
morgan.token('color-status', (req, res) => {
  const status = res.statusCode;
  const color = status >= 500 ? 31 : status >= 400 ? 33 : status >= 300 ? 36 : 32;
  return `\x1b[${color}m${status}\x1b[0m`;
});

// Combined format for production
const productionFormat = morgan.compile(
  ':method :url :color-status :response-time ms - :res[content-length] :body'
);

// Use in app
app.use(morgan(productionFormat, {
  skip: (req) => req.url === '/health',
  stream: process.stdout,
}));

// Request timing middleware
const requestTiming = (req, res, next) => {
  const startTime = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - startTime;
    console.log({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip,
      userAgent: req.get('User-Agent'),
    });
    
    // Alert if slow
    if (duration > 5000) {
      console.warn('SLOW REQUEST DETECTED!', { path: req.path, duration });
      // Send to monitoring
    }
  });
  
  next();
};

app.use(requestTiming);
```

---

## 8. Tradeoffs

### Node.js vs Other Languages

| Aspect | Node.js | Python/Django | Go | Java/Spring |
|--------|---------|---------------|-----|-------------|
| **Performance** | Good for I/O | Moderate | Excellent | Excellent |
| **Developer Speed** | Very Fast | Fast | Moderate | Moderate |
| **Type Safety** | TypeScript helps | Dynamic | Static, strict | Static |
| **Ecosystem** | Huge npm | Large | Growing | Huge enterprise |
| **CPU Tasks** | Not ideal | Better | Excellent | Excellent |
| **Real-time** | Excellent (ws) | Moderate | Good | Good |
| **Learning Curve** | Easy (JS devs) | Easy | Moderate | Steep |
| **Memory Usage** | Higher | Moderate | Low | High |
| **Concurrency** | Event loop | GIL limits | Goroutines | Threads/async |

### When to Use Node.js

```javascript
// GREAT for Node.js:
const goodUseCases = [
  'REST APIs with heavy I/O',
  'Real-time applications (chat, live updates)',
  'Microservices architecture',
  'GraphQL APIs',
  'Streaming services',
  'Proxy servers',
  'CRUD applications',
  'WebSocket servers',
];

// NOT GREAT for Node.js:
const badUseCases = [
  'Heavy computation (image processing, video encoding)',
  'CPU-intensive ML models',
  'Real-time trading with sub-millisecond latency',
  'Large-scale data processing pipelines',
];

// For CPU-heavy tasks, use:
const alternatives = {
  go: 'Go for microservices and networking',
  rust: 'Rust for performance-critical components',
  python: 'Python with proper async (FastAPI)',
  'c++': 'C++ for image/video processing',
};
```

### Single Thread vs Multi Thread

```javascript
// Node.js single-threaded model
// Each process is single-threaded but:
// - Multiple processes via clustering
// - Worker threads for CPU tasks
// - libuv handles async I/O in thread pool

// When single-thread is FINE:
const tasks = [
  'API requests',        // Mostly waiting for DB/network
  'File uploads',        // Async stream processing
  'Database queries',    // Non-blocking
  'WebSocket comms',    // Event-driven
  'Authentication',      // Fast crypto operations
];

// When single-thread is PROBLEMATIC:
const problematicTasks = [
  'Video transcoding',
  'Machine learning inference',
  'Complex calculations',
  'Image manipulation',
  'Large data processing',
];

// Solution: Worker Threads
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

if (isMainThread) {
  // Main thread - offload CPU work
  const worker = new Worker(__filename, {
    workerData: { data: hugeArray },
  });
  
  worker.on('message', (result) => {
    console.log('Worker result:', result);
  });
} else {
  // Worker thread - do CPU work
  const result = heavyComputation(workerData.data);
  parentPort.postMessage(result);
}
```

---

## 9. Security Concerns

### Node.js Security Best Practices

```javascript
// 1. Dependency scanning
// npm audit, npm audit fix
// npm install -g npm-check-updates
// ncu (check for updates)

// 2. Helmet for security headers
const helmet = require('helmet');
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}));

// 3. Rate limiting
const rateLimit = require('express-rate-limit');
const slowDown = require('express-slow-down');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

const speedLimiter = slowDown({
  windowMs: 15 * 60 * 1000,
  delayAfter: 50,
  delayMs: 500,
});

app.use('/api', [limiter, speedLimiter]);

// 4. Input validation
const { body, param, query, validationResult } = require('express-validator');

app.post('/api/users',
  [
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({ min: 8 }).matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
    body('age').isInt({ min: 18, max: 120 }),
  ],
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  },
  userController.create
);

// 5. SQL/NoSQL injection prevention
// Using Prisma (parameterized queries)
const user = await prisma.user.findFirst({
  where: { email: req.body.email }, // Safe!
});

// BAD: String concatenation (SQL injection)
// await prisma.$queryRaw`SELECT * FROM users WHERE email = ${req.body.email}`

// 6. Secure headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.removeHeader('X-Powered-By');
  next();
});

// 7. Environment variables (NEVER commit secrets!)
// .env file (add to .gitignore)
const dotenv = require('dotenv');
dotenv.config();

const config = {
  dbUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
  apiKey: process.env.EXTERNAL_API_KEY,
  // NEVER hardcode secrets!
};
```

---

## 10. Performance Optimization

### Node.js Performance Tips

```javascript
// 1. Compression middleware
const compression = require('compression');
app.use(compression({
  filter: (req, res) => {
    if (req.headers['x-no-compression']) return false;
    return compression.filter(req, res);
  },
  level: 6, // 0-9, balanced
}));

// 2. Caching strategies
const responseCache = new Map();
const CACHE_TTL = 60000; // 1 minute

function cacheResponse(key, ttl = CACHE_TTL) {
  return (req, res, next) => {
    const cached = responseCache.get(key(req));
    
    if (cached && Date.now() - cached.timestamp < ttl) {
      return res.json(cached.data);
    }
    
    // Override res.json to cache response
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      responseCache.set(key(req), { data, timestamp: Date.now() });
      return originalJson(data);
    };
    
    next();
  };
}

// 3. Connection pooling (Prisma handles this)
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL + '?connection_limit=10',
    },
  },
  log: ['warn', 'error'],
});

// 4. Stream responses for large data
app.get('/api/export/users', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Content-Disposition', 'attachment; filename=users.json');
  
  const usersStream = prisma.user.findMany().stream();
  
  res.write('[');
  let first = true;
  
  usersStream.on('data', (user) => {
    if (!first) res.write(',');
    res.write(JSON.stringify(user));
    first = false;
  });
  
  usersStream.on('end', () => res.end(']'));
  usersStream.on('error', (err) => {
    res.end(']'); // Close JSON properly
    console.error(err);
  });
});

// 5. Lazy loading and code splitting
// In Express with require:
app.get('/api/reports', async (req, res, next) => {
  // Only load report generator when needed
  const { generateReport } = await import('./services/reportGenerator.mjs');
  const report = await generateReport(req.query);
  res.json(report);
});

// 6. Usefasthttp
const fastify = require('fastify')({
  logger: true,
  trustProxy: true,
});

// Fastify is ~30% faster than Express for typical APIs
// Great for high-performance needs
```

---

## 11. Scaling Challenges

### Horizontal vs Vertical Scaling

```javascript
// VERTICAL SCALING: More resources on single machine
// - Add more CPU cores (cluster mode)
// - Add more RAM
// - SSD storage
// - Limited by single machine capacity

// HORIZONTAL SCALING: More machines
// - Stateless design required
// - Load balancer in front
// - Database as single source of truth
// - Redis for shared session/cache

// Load Balancer (Nginx)
upstream backend {
  least_conn;  // Route to least busy server
  server 10.0.0.1:3000 weight=3;
  server 10.0.0.2:3000;
  server 10.0.0.3:3000;
  
  keepalive 64; // Keep connections alive
}

server {
  listen 80;
  
  location / {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
  
  location /socket.io/ {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
  }
}

// Kubernetes Deployment
// deployment.yaml
/*
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    spec:
      containers:
      - name: api
        image: myapp/api:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
*/
```

### Database Scaling Patterns

```javascript
// READ REPLICAS
// Configuration for read replica load balancing
const { PrismaClient } = require('@prisma/client');

const primaryDb = new PrismaClient({
  datasources: { db: process.env.DATABASE_URL_PRIMARY },
});

const readReplicas = [
  process.env.DATABASE_URL_READ1,
  process.env.DATABASE_URL_READ2,
  process.env.DATABASE_URL_READ3,
];

// Simple round-robin for reads
let currentReplica = 0;
const getReadReplica = () => {
  const replica = readReplicas[currentReplica];
  currentReplica = (currentReplica + 1) % readReplicas.length;
  return replica;
};

// For Prisma, use separate clients (or middleware)
// Read-heavy queries use replica
app.get('/api/users', async (req, res, next) => {
  try {
    // This read could go to replica
    const users = await primaryDb.user.findMany();
    res.json(users);
  } catch (error) {
    next(error);
  }
});

// Writes always go to primary
app.post('/api/users', async (req, res, next) => {
  try {
    // This write goes to primary
    const user = await primaryDb.user.create({ data: req.body });
    res.json(user);
  } catch (error) {
    next(error);
  }
});
```

---

## 12. Best Practices

### Node.js Best Practices Summary

```javascript
// 1. Project Structure
const projectStructure = {
  'src/': {
    'config/': ['database.js', 'redis.js', 'env.js'],
    'controllers/': ['userController.js', 'productController.js'],
    'services/': ['userService.js', 'productService.js'],
    'models/': ['userModel.js', 'productModel.js'],
    'middleware/': ['auth.js', 'validation.js', 'errorHandler.js'],
    'routes/': ['userRoutes.js', 'productRoutes.js'],
    'utils/': ['logger.js', 'helpers.js'],
    'validators/': ['userValidator.js'],
    'app.js': 'Main Express app',
    'server.js': 'Server entry point',
  },
  'tests/': {
    'unit/': 'Unit tests',
    'integration/': 'Integration tests',
  },
  'scripts/': 'Deployment scripts',
};

// 2. Error handling pattern
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(message, errors) {
    super(message, 400);
    this.errors = errors;
  }
}

class NotFoundError extends AppError {
  constructor(resource) {
    super(`${resource} not found`, 404);
  }
}

// 3. Async error wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Usage
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.findById(req.params.id);
  if (!user) throw new NotFoundError('User');
  res.json(user);
}));

// 4. Graceful shutdown
const gracefulShutdown = async (signal) => {
  console.log(`${signal} received, starting graceful shutdown`);
  
  server.close(async () => {
    console.log('HTTP server closed');
    
    try {
      await prisma.$disconnect();
      console.log('Database disconnected');
      
      await redis.quit();
      console.log('Redis disconnected');
      
      process.exit(0);
    } catch (error) {
      console.error('Error during shutdown:', error);
      process.exit(1);
    }
  });
  
  // Force shutdown after 30 seconds
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, 30000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

---

## 13. Common Mistakes

### Top 10 Node.js Mistakes

```javascript
// MISTAKE 1: Not handling async errors properly
// BAD
app.get('/users', async (req, res) => {
  const users = await db.query('SELECT * FROM users');
  res.json(users);
  // If db.query throws, error is silently lost!
});

// GOOD
app.get('/users', async (req, res, next) => {
  try {
    const users = await db.query('SELECT * FROM users');
    res.json(users);
  } catch (error) {
    next(error);
  }
});

// MISTAKE 2: Using synchronous code in request handlers
// BAD
app.get('/process', (req, res) => {
  const result = JSON.parse(fs.readFileSync('data.json')); // BLOCKS!
  res.json(result);
});

// GOOD
app.get('/process', async (req, res, next) => {
  try {
    const data = await fs.promises.readFile('data.json');
    const result = JSON.parse(data);
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// MISTAKE 3: Not validating/sanitizing input
// BAD
app.get('/user/:id', (req, res) => {
  const user = db.query(`SELECT * FROM users WHERE id = '${req.params.id}'`);
  // SQL Injection possible!
});

// GOOD
app.get('/user/:id', async (req, res, next) => {
  try {
    const user = await db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
    if (!user) return res.status(404).json({ error: 'Not found' });
    res.json(user);
  } catch (error) {
    next(error);
  }
});

// MISTAKE 4: Blocking the event loop
// BAD - Heavy computation in request handler
app.post('/calculate', (req, res) => {
  let result = 0;
  for (let i = 0; i < 1000000000; i++) {
    result += Math.sqrt(i);
  }
  res.json({ result });
});

// GOOD - Use worker threads or message queue
const { Worker } = require('worker_threads');
app.post('/calculate', async (req, res, next) => {
  const worker = new Worker('./calculate-worker.js', {
    workerData: { iterations: 1000000000 }
  });
  worker.on('message', (result) => res.json({ result }));
  worker.on('error', next);
});

// MISTAKE 5: Not implementing rate limiting
// Always limit requests!
const rateLimit = require('express-rate-limit');
app.use('/api/', rateLimit({ windowMs: 60000, max: 100 }));

// MISTAKE 6: Storing secrets in code
// BAD
const apiKey = 'sk_live_abc123xyz'; // NEVER!

// GOOD
const apiKey = process.env.STRIPE_SECRET_KEY;

// MISTAKE 7: Not using connection pooling
// Create new DB connection per request - BAD!
app.use((req, res, next) => {
  req.db = mysql.createConnection(config); // New connection each time!
  next();
});

// Use pool - GOOD
const pool = mysql.createPool(config);
app.use((req, res, next) => {
  req.db = pool; // Reuse connections
  next();
});

// MISTAKE 8: Not implementing proper logging
// BAD
console.log('User logged in');

// GOOD
const logger = require('./utils/logger');
logger.info('User logged in', { userId: user.id, ip: req.ip, timestamp: new Date() });

// MISTAKE 9: Forgetting to close connections
// GOOD
process.on('SIGTERM', async () => {
  await pool.end();
  await redis.quit();
  process.exit(0);
});

// MISTAKE 10: Not using process managers in production
// BAD
node server.js

// GOOD - Use PM2, systemd, or container orchestration
// pm2 start server.js -i max (max instances based on CPU cores)
```

---

## 14. Interview Questions

### Common Node.js Interview Q&A

```markdown
Q1: Explain the Node.js event loop.
A: The event loop is the core of Node.js non-blocking I/O. It has 6 phases:
   1. timers - executes setTimeout/setInterval callbacks
   2. pending callbacks - I/O callbacks deferred
   3. idle, prepare - internal use
   4. poll - retrieve new I/O events
   5. check - setImmediate callbacks
   6. close callbacks - e.g., socket.on('close')
   process.nextTick and Promises queue microtasks between phases.

Q2: Difference between process.nextTick and setImmediate?
A: process.nextTick fires immediately after current operation completes,
   before event loop continues. setImmediate fires in 'check' phase,
   after poll phase completes. nextTick has higher priority and can
   starve I/O if abused.

Q3: How does clustering work in Node.js?
A: Node.js cluster module allows spawning child processes (workers)
   that share server ports. Master process distributes load using
   round-robin (default on Linux) or OS load balancing. Each worker
   is a separate V8 instance,有自己的event loop.

Q4: What is libuv and its role?
A: libuv is a C library that handles async I/O operations in Node.js.
   It manages the event loop, thread pool for blocking operations
   (fs, dns, crypto), and provides cross-platform async APIs.

Q5: How do you prevent memory leaks in Node.js?
A: 1. Avoid global arrays growing unbounded
   2. Remove event listeners when done
   3. Use bounded data structures (LRU cache)
   4. Monitor with heap snapshots
   5. Don't store unnecessary references in closures
   6. Use WeakMap/WeakSet where appropriate

Q6: Node.js vs Deno - what's the difference?
A: Deno is secure by default (no file/network access without permission),
   uses ES modules natively, has built-in TypeScript support, and doesn't
   have npm - instead imports from URLs. Node.js has larger ecosystem,
   more libraries, and more production battle-testing.

Q7: Explain middleware pattern in Express.
A: Express middleware are functions with (req, res, next) signature.
   They execute in order, can modify req/res, end response, or call
   next(). Built-in middleware like express.json(), third-party like
   cors, helmet, and custom middleware for auth, logging, validation.

Q8: How does the V8 engine optimize JavaScript?
A: V8 uses JIT compilation with two tiers:
   - Ignition interpreter for quick startup
   - TurboFan optimizing compiler for hot functions
   It uses hidden classes for objects, inline caching for property
   access, and can deoptimize if assumptions break (e.g., type changes).

Q9: What are streams in Node.js?
A: Streams are collections of data that might not be available all at
   once. Four types: Readable, Writable, Duplex (both), Transform
   (modify data). Useful for handling large files, real-time data,
   and memory efficiency. Pipe connects streams: readable.pipe(writable).

Q10: How do you handle errors in async Node.js code?
A: Use try/catch blocks in async functions, pass errors to next()
   for Express error handlers, use async wrapper utilities,
   handle unhandledRejection events globally, and use domains or
   worker threads for critical error isolation.
```

---

## 15. Latest 2026 Fullstack Engineering Patterns

### Modern Node.js Patterns for 2026

```javascript
// 1. Server Components with Edge Runtime
// Bun, Deno Deploy, Cloudflare Workers support
// file: edge-handler.ts
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    // Edge-compatible database (Turso, PlanetScale)
    const db = await createDatabase(process.env.DATABASE_URL);
    
    const user = await db
      .selectFrom('users')
      .where('id', '=', url.searchParams.get('id'))
      .executeTakeFirst();
    
    return Response.json(user);
  },
};

// 2. Server Actions (React 19 pattern)
// file: app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  
  const user = await prisma.user.create({
    data: { name, email }
  });
  
  revalidatePath('/users');
  return { success: true, userId: user.id };
}

// 3. AI-Integrated Backend Patterns
// file: services/aiService.ts
class AIService {
  private client: Anthropic;
  
  async generateContent(prompt: string, context: Record<string, any>) {
    const cached = await this.getCache(prompt);
    if (cached) return cached;
    
    const response = await this.client.messages.create({
      model: 'claude-opus-4-5',
      max_tokens: 4096,
      messages: [{
        role: 'user',
        content: `Context: ${JSON.stringify(context)}\n\nPrompt: ${prompt}`
      }],
      thinking: {
        type: 'enabled',
        budget_tokens: 1024
      }
    });
    
    await this.setCache(prompt, response.content);
    return response.content;
  }
}

// 4. Observability with OpenTelemetry
// file: instrumentation.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'my-api-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

// 5. Database-per-tenant pattern (2026 SaaS)
// file: multi-tenant.ts
class TenantManager {
  private connections = new Map<string, PrismaClient>();
  
  async getClient(tenantId: string): Promise<PrismaClient> {
    if (this.connections.has(tenantId)) {
      return this.connections.get(tenantId)!;
    }
    
    const connectionString = await this.getTenantConnection(tenantId);
    const client = new PrismaClient({
      datasources: { db: { url: connectionString } }
    });
    
    this.connections.set(tenantId, client);
    return client;
  }
  
  // Row-level security alternative
  async queryAsTenant<T>(
    tenantId: string,
    query: (prisma: PrismaClient) => Promise<T>
  ): Promise<T> {
    const prisma = this.getClient(tenantId);
    return prisma.$transaction(async (tx) => {
      // Set tenant context
      await tx.$executeRaw`SET app.current_tenant = ${tenantId}`;
      return query(tx);
    });
  }
}

// 6. Reactive Programming with RxJS in Node.js
// file: reactive/streams.ts
import { Subject, debounceTime, switchMap, catchError } from 'rxjs';

class ReactiveAPI {
  private searchSubject = new Subject<SearchRequest>();
  
  constructor() {
    this.searchSubject.pipe(
      debounceTime(300),
      switchMap((request) => this.executeSearch(request)),
      catchError((error) => {
        console.error('Search error:', error);
        return [];
      })
    ).subscribe((results) => {
      this.broadcastResults(results);
    });
  }
  
  search(request: SearchRequest) {
    this.searchSubject.next(request);
  }
}

// 7. WASM Integration for Performance-Critical Code
// file: wasm/processor.ts
import init, { processImage } from './image-processor.wasm';

let wasmInitialized = false;

async function initWasm() {
  if (!wasmInitialized) {
    await init();
    wasmInitialized = true;
  }
}

export async function processWithWasm(imageBuffer: Buffer) {
  await initWasm();
  return processImage(imageBuffer);
}

// 8. GraphQL Subscriptions with Server-Sent Events fallback
// file: subscriptions/sse.ts
app.get('/api/events/:userId', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  
  const userId = req.params.userId;
  
  const handler = (event) => {
    if (event.userId === userId) {
      res.write(`data: ${JSON.stringify(event)}\n\n`);
    }
  };
  
  eventEmitter.on('update', handler);
  
  req.on('close', () => {
    eventEmitter.off('update', handler);
  });
  
  // Heartbeat
  const interval = setInterval(() => {
    res.write(': heartbeat\n\n');
  }, 30000);
  
  req.on('close', () => clearInterval(interval));
});
```

---

## Summary

Bhai, Node.js ek powerful platform hai fullstack development ke liye. Key takeaways:

1. **Event Loop** samjho - ye Node.js ka heart hai
2. **Non-blocking** code likho - async/await is your friend
3. **Security** pe dhyan do - validate inputs, rate limit karo
4. **Performance** ke liye caching, streaming, worker threads use karo
5. **Scaling** ke liye stateless design aur load balancing
6. **2026 patterns** mein Edge computing, AI integration, observability

Fullstack developer banne ke liye sirf Node.js nahi, balki poori ecosystem samajhna zaroori hai - databases, caching, queues, security, aur deployment bhi!

---

*Next: [Express and FastAPI](./Express_and_FastAPI.md)*
