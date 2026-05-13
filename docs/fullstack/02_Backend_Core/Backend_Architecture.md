# Backend Architecture - System Design Deep Dive

Bhai, backend architecture samajhna bahut zaroori hai kyunki ye decide karta hai ki tumhara application kitni der tak scale kar sakti hai, kitni stable hai, aur kitni maintainable hai. Chalo detail mein samajhte hain!

---

## 1. Beginner-Friendly Hinglish Explanation

### Architecture Kya Hai?

Soch ki tu ek **building** bana raha hai:
- **Single Story House** = Single server application
- **Multi-story Building** = Layered architecture
- **Multiple Buildings with Roads** = Microservices
- **Smart City** = Distributed system

Architecture basically ye decide karta hai ki tumhare components kaise organize hain aur unke beech kaise communication hota hai.

### Common Architecture Patterns

1. **Monolithic** - Sab kuch ek box mein (like big restaurant with everything)
2. **Layered** - Layers mein divide (like restaurant with separate kitchen, counter, service)
3. **Microservices** - Alag services jo baat karte hain (like food court with different stalls)
4. **Event-Driven** - Events ke based pe kaam hota hai (like notification system)
5. **Serverless** - Sirf code likho, infrastructure ka dhyan nahi (like cloud kitchen)

### Ek Simple Analogy

```
Restaurant ka analogy:

Monolithic = Ek chef jo sab kuch khud karta hai
Microservices = Chef, Waiter, Manager, Cleaner alag-alag

Backend bhi aise hi:
Monolithic = API server + Database + Auth sab ek mein
Microservices = Auth service, User service, Payment service alag
```

---

## 2. Deep Technical Explanation

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                      BACKEND ARCHITECTURE LAYERS                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                      CLIENT LAYER                          │     │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │     │
│  │  │ Web App │  │Mobile   │  │Desktop  │  │ IoT Devices     │ │     │
│  │  │(React)  │  │(React   │  │(Electron│  │                 │ │     │
│  │  │         │  │ Native) │  │         │  │                 │ │     │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘ │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                    LOAD BALANCER / CDN                       │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │     │
│  │  │   Nginx/     │  │   Cloudflare │  │   AWS ALB /          │ │     │
│  │  │   HAProxy    │  │   /Fastly    │  │   Azure Load Balancer│ │     │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘ │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                    GATEWAY / API LAYER                      │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │     │
│  │  │  Kong /      │  │   GraphQL    │  │   Rate Limiting     │ │     │
│  │  │  AWS API GW  │  │   Federation │  │   & Auth Middleware │ │     │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘ │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                    BUSINESS LOGIC LAYER                     │     │
│  │                                                              │     │
│  │  ┌──────────────────────────────────────────────────────┐  │     │
│  │  │                      SERVICES                          │  │     │
│  │  │   ┌───────────┐  ┌───────────┐  ┌───────────┐        │  │     │
│  │  │   │   User    │  │  Product  │  │  Payment  │        │  │     │
│  │  │   │  Service  │  │  Service  │  │  Service  │        │  │     │
│  │  │   └───────────┘  └───────────┘  └───────────┘        │  │     │
│  │  │   ┌───────────┐  ┌───────────┐  ┌───────────┐        │  │     │
│  │  │   │  Order   │  │  Notifi-  │  │   Email   │        │  │     │
│  │  │   │  Service │  │  cation   │  │  Service  │        │  │     │
│  │  │   │          │  │  Service  │  │          │        │  │     │
│  │  │   └───────────┘  └───────────┘  └───────────┘        │  │     │
│  │  └──────────────────────────────────────────────────────┘  │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                      DATA ACCESS LAYER                      │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │     │
│  │  │ Repository   │  │   Unit of    │  │   Database          │ │     │
│  │  │   Pattern   │  │   Work       │  │   Migrations        │ │     │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘ │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                        DATA LAYER                            │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │     │
│  │  │ PostgreSQL  │  │    Redis    │  │   MongoDB   │          │     │
│  │  │  (Primary)  │  │   (Cache)   │  │  (Audit)   │          │     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘          │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │     │
│  │  │    S3 /     │  │   Kafka /   │  │  Elasticsearch │      │     │
│  │  │   GCS       │  │   RabbitMQ  │  │              │      │     │
│  │  │ (Files)     │  │   (Queue)   │  │   (Search)  │          │     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘          │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Service-to-Service Communication

```
┌─────────────────────────────────────────────────────────────────────┐
│                  SERVICE COMMUNICATION PATTERNS                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐                          ┌──────────────┐          │
│  │  Service A   │─── Synchronous ────────>│  Service B   │          │
│  │              │   (HTTP/gRPC)           │              │          │
│  └──────────────┘                          └──────────────┘          │
│                                                                     │
│  ┌──────────────┐                          ┌──────────────┐          │
│  │  Service A   │─── Async ───────────────>│    Queue    │          │
│  │              │   (Events)               │  (Kafka)    │          │
│  └──────────────┘                          └──────────────┘          │
│                                                     │                │
│                                                     v                │
│                                            ┌──────────────┐          │
│                                            │  Service B   │          │
│                                            │              │          │
│                                            └──────────────┘          │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                         API GATEWAY PATTERN                          │
│                                                                     │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐    │
│  │  Client  │────>│ Gateway  │────>│ Users    │     │ Orders   │    │
│  │          │     │          │     │ Service  │     │ Service  │    │
│  └──────────┘     └──────────┘     └──────────┘     └──────────┘    │
│                       │                                          │
│                       │            ┌──────────┐                  │
│                       ├───────────>│ Payments │                  │
│                       │            │ Service  │                  │
│                       │            └──────────┘                  │
│                       │                                           │
│                       │            ┌──────────┐                   │
│                       └───────────>│Notificati│                   │
│                                    │  ons     │                   │
│                                    └──────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Architecture Patterns Implementation

### Monolithic Architecture

```javascript
// File: server/app.js
const express = require('express');
const app = express();

// All in one application
app.use('/api/users', require('./routes/users'));
app.use('/api/products', require('./routes/products'));
app.use('/api/orders', require('./routes/orders'));
app.use('/api/payments', require('./routes/payments'));

// Single database
const { prisma } = require('./database');

// Shared services
const { emailService } = require('./services/email');
const { notificationService } = require('./services/notifications');

// All routes use same server
app.listen(3000);
```

### Microservices Architecture

```javascript
// File: user-service/server.js
const express = require('express');
const app = express();

// User service - only handles user operations
app.use('/users', require('./routes/users'));
app.use('/auth', require('./routes/auth'));

app.listen(3001);

// File: order-service/server.js
const express = require('express');
const app = express();

// Order service - only handles orders
app.use('/orders', require('./routes/orders'));
app.use('/cart', require('./routes/cart'));

app.listen(3002);

// File: payment-service/server.js
const express = require('express');
const app = express();

// Payment service - only handles payments
app.use('/payments', require('./routes/payments'));
app.use('/refunds', require('./routes/refunds'));

app.listen(3003);

// File: api-gateway/server.js
const httpProxy = require('http-proxy');

// API Gateway routes to microservices
const proxy = httpProxy.createProxyServer({});

app.all('/api/users/:path*', (req, res) => {
  proxy.web(req, res, { target: 'http://localhost:3001' });
});

app.all('/api/orders/:path*', (req, res) => {
  proxy.web(req, res, { target: 'http://localhost:3002' });
});

app.all('/api/payments/:path*', (req, res) => {
  proxy.web(req, res, { target: 'http://localhost:3003' });
});

app.listen(3000);
```

### Service Communication Patterns

```javascript
// File: services/httpClient.js
const axios = require('axios');

class ServiceClient {
  constructor(serviceName, baseUrl) {
    this.serviceName = serviceName;
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: 5000,
    });
    
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error(`${serviceName} error:`, error.message);
        throw error;
      }
    );
  }

  async get(path, params) {
    return this.client.get(path, { params });
  }

  async post(path, data) {
    return this.client.post(path, data);
  }
}

// Service clients
const userService = new ServiceClient('users', process.env.USER_SERVICE_URL);
const paymentService = new ServiceClient('payments', process.env.PAYMENT_SERVICE_URL);
const notificationService = new ServiceClient('notifications', process.env.NOTIFICATION_SERVICE_URL);

// File: services/orderService.js
class OrderService {
  async createOrder(orderData) {
    const { userId, items, paymentMethod } = orderData;

    // Call user service to verify user
    const userResponse = await userService.get(`/users/${userId}`);
    if (!userResponse.data) {
      throw new Error('User not found');
    }

    // Process payment
    const paymentResponse = await paymentService.post('/payments', {
      userId,
      amount: this.calculateTotal(items),
      method: paymentMethod,
    });

    // Create order
    const order = await prisma.order.create({
      data: {
        userId,
        items: JSON.stringify(items),
        total: paymentResponse.data.amount,
        status: 'CONFIRMED',
      },
    });

    // Send notification (fire and forget)
    notificationService.post('/notifications', {
      userId,
      type: 'ORDER_CONFIRMED',
      orderId: order.id,
    }).catch(err => console.error('Notification failed:', err));

    return order;
  }
}
```

### Event-Driven Architecture

```javascript
// File: events/eventEmitter.js
const { EventEmitter } = require('events');
const eventBus = new EventEmitter();

// Increase max listeners
eventBus.setMaxListeners(100);

// Event types
const EVENTS = {
  USER_CREATED: 'user.created',
  USER_UPDATED: 'user.updated',
  USER_DELETED: 'user.deleted',
  ORDER_CREATED: 'order.created',
  ORDER_UPDATED: 'order.updated',
  PAYMENT_COMPLETED: 'payment.completed',
  PAYMENT_FAILED: 'payment.failed',
};

// Publish event
async function publishEvent(event, data) {
  const eventData = {
    id: generateUUID(),
    type: event,
    payload: data,
    timestamp: new Date().toISOString(),
  };

  // Store in database for replay/debugging
  await prisma.outbox.create({
    data: {
      event,
      payload: JSON.stringify(data),
      createdAt: new Date(),
    },
  });

  // Emit locally
  eventBus.emit(event, eventData);

  // Publish to message queue for other services
  await kafka.publish('events', eventData);
}

// Subscribe to events
eventBus.on(EVENTS.USER_CREATED, async (data) => {
  console.log('User created:', data);
  // Send welcome email
  await emailService.sendWelcomeEmail(data.payload.email);
  // Initialize user preferences
  await initializeUserPreferences(data.payload.id);
});

module.exports = { eventBus, publishEvent, EVENTS };
```

---

## 4. Frontend + Backend Integration

### Service Layer Pattern

```typescript
// File: client/src/services/apiService.ts
import axios, { AxiosInstance, AxiosError } from 'axios';

class ApiService {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: { 'Content-Type': 'application/json' },
    });

    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('authToken');
          window.location.href = '/login';
        }
        throw error;
      }
    );
  }

  async get<T>(url: string, params?: any) {
    const response = await this.client.get<T>(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any) {
    const response = await this.client.post<T>(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any) {
    const response = await this.client.put<T>(url, data);
    return response.data;
  }

  async delete<T>(url: string) {
    const response = await this.client.delete<T>(url);
    return response.data;
  }
}

// Create service instances
export const userService = new ApiService('/api/users');
export const orderService = new ApiService('/api/orders');
export const paymentService = new ApiService('/api/payments');

// File: client/src/stores/userStore.ts
import { create } from 'zustand';
import { userService } from '../services/apiService';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'user' | 'admin';
}

interface UserState {
  users: User[];
  loading: boolean;
  error: string | null;
  fetchUsers: () => Promise<void>;
  createUser: (data: Partial<User>) => Promise<void>;
  updateUser: (id: string, data: Partial<User>) => Promise<void>;
  deleteUser: (id: string) => Promise<void>;
}

export const useUserStore = create<UserState>((set, get) => ({
  users: [],
  loading: false,
  error: null,

  fetchUsers: async () => {
    set({ loading: true, error: null });
    try {
      const response = await userService.get<{ data: User[] }>('/');
      set({ users: response.data, loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },

  createUser: async (data) => {
    await userService.post<User>('/', data);
    await get().fetchUsers();
  },

  updateUser: async (id, data) => {
    await userService.put<User>(`/${id}`, data);
    await get().fetchUsers();
  },

  deleteUser: async (id) => {
    await userService.delete(`/${id}`);
    await get().fetchUsers();
  },
}));
```

### BFF Pattern (Backend for Frontend)

```javascript
// File: bff/server.js
const express = require('express');
const app = express();

// BFF aggregates data from multiple services
app.get('/api/web/home', async (req, res, next) => {
  try {
    // Fetch from multiple services in parallel
    const [featuredProducts, categories, userRecommendations] = await Promise.all([
      productService.get('/featured'),
      categoryService.get('/'),
      userService.get(`/${req.userId}/recommendations`),
    ]);

    res.json({
      featuredProducts,
      categories,
      recommendations: userRecommendations,
    });
  } catch (error) {
    next(error);
  }
});

// Mobile-specific endpoint
app.get('/api/mobile/home', async (req, res, next) => {
  try {
    // Optimized for mobile - different data structure
    const [products, banner] = await Promise.all([
      productService.get('/featured', { format: 'mobile' }),
      bannerService.get('/active'),
    ]);

    res.json({
      products,
      banner,
      // ... mobile-specific response
    });
  } catch (error) {
    next(error);
  }
});
```

---

## 5. Real-World Production Examples

### E-commerce Platform Architecture

```javascript
// File: architecture/ecommerce.js
/*
 * E-commerce Platform Architecture
 * 
 * Services:
 * - API Gateway (Port 3000)
 * - User Service (Port 3001)
 * - Product Service (Port 3002)
 * - Order Service (Port 3003)
 * - Payment Service (Port 3004)
 * - Notification Service (Port 3005)
 * - Search Service (Port 3006)
 * - Review Service (Port 3007)
 */

const microservicesArchitecture = {
  gateway: {
    port: 3000,
    responsibilities: [
      'Authentication & Authorization',
      'Rate Limiting',
      'Request Routing',
      'Load Balancing',
    ],
  },

  services: {
    user: {
      port: 3001,
      database: 'users_db',
      cache: 'redis_user',
      endpoints: ['/register', '/login', '/profile', '/addresses'],
    },

    product: {
      port: 3002,
      database: 'products_db',
      cache: 'redis_products',
      searchEngine: 'elasticsearch',
      endpoints: ['/products', '/categories', '/inventory'],
    },

    order: {
      port: 3003,
      database: 'orders_db',
      queue: 'kafka',
      endpoints: ['/orders', '/cart', '/checkout'],
      dependsOn: ['user', 'product', 'payment'],
    },

    payment: {
      port: 3004,
      database: 'payments_db',
      endpoints: ['/pay', '/refund', '/transactions'],
      externalIntegrations: ['stripe', 'paypal'],
    },

    notification: {
      port: 3005,
      queue: 'kafka',
      endpoints: ['/send', '/templates'],
      channels: ['email', 'sms', 'push'],
    },

    search: {
      port: 3006,
      engine: 'elasticsearch',
      indexes: ['products', 'categories', 'autocomplete'],
    },

    review: {
      port: 3007,
      database: 'reviews_db',
      endpoints: ['/reviews', '/ratings'],
    },
  },

  dataStores: {
    postgresql: ['users', 'orders', 'products', 'payments'],
    mongodb: ['reviews', 'audit_logs', 'sessions'],
    redis: ['sessions', 'cache', 'rate_limits'],
    elasticsearch: ['product_search', 'logs'],
    kafka: ['order_events', 'payment_events', 'notifications'],
  },
};
```

### Social Media Platform Architecture

```javascript
// File: architecture/social-media.js
const socialMediaArchitecture = {
  // Core services
  services: {
    apiGateway: { port: 3000 },
    
    userService: {
      port: 3001,
      functions: ['signup', 'login', 'profile', 'follow', 'unfollow'],
    },

    postService: {
      port: 3002,
      functions: ['createPost', 'deletePost', 'share', 'like', 'comment'],
      storage: 'S3 for media files',
    },

    feedService: {
      port: 3003,
      functions: ['getFeed', 'refreshFeed', 'suggestions'],
      cache: 'Redis for feed cache',
    },

    timelineService: {
      port: 3004,
      functions: ['userTimeline', 'hashtagTimeline'],
    },

    mediaService: {
      port: 3005,
      functions: ['upload', 'transcode', 'thumbnail'],
      storage: 'S3 + CloudFront CDN',
    },

    messageService: {
      port: 3006,
      type: 'websocket',
      functions: ['sendMessage', 'getConversations'],
    },

    notificationService: {
      port: 3007,
      type: 'event-driven',
      channels: ['push', 'email', 'in-app'],
    },

    searchService: {
      port: 3008,
      engine: 'elasticsearch',
      indexes: ['posts', 'users', 'hashtags'],
    },

    analyticsService: {
      port: 3009,
      functions: ['trackEvent', 'getInsights', 'reports'],
      storage: 'ClickHouse for analytics',
    },
  },

  realTimeFeatures: {
    websocket: {
      port: 3006,
      protocol: 'Socket.IO',
      events: ['message', 'typing', 'online'],
    },
    streaming: {
      port: 3010,
      protocol: 'Server-Sent Events',
      events: ['liveUpdates', 'notifications'],
    },
  },
};
```

---

## 6. Failure Cases

### Common Architecture Failures

```javascript
// FAILURE 1: Distributed Monolith (Anti-pattern)
const badArchitecture = {
  // Microservices by name only!
  // Actually tightly coupled - changing one breaks all
  services: {
    user: { port: 3001 },
    order: { port: 3002, dependsOn: ['user'] },
    payment: { port: 3003, dependsOn: ['order', 'user'] },
    shipping: { port: 3004, dependsOn: ['order', 'user', 'payment'] },
    notification: { port: 3005, dependsOn: ['user', 'order', 'payment', 'shipping'] },
  },
  
  problems: [
    'If user service goes down, all services fail',
    'Every service must be deployed together',
    'Shared database between services',
    'Synchronous dependencies everywhere',
  ],
};

// SOLUTION: True microservices with async communication
const goodArchitecture = {
  services: {
    user: { port: 3001 },
    order: { port: 3002 },
    payment: { port: 3003 },
    notification: { port: 3005 },
  },
  
  communication: {
    // Async via events
    events: ['order.created', 'payment.completed', 'user.created'],
    messageQueue: 'kafka',
  },
  
  eachServiceOwnsItsData: true,
};

// FAILURE 2: Not handling partial failures
const badServiceCall = async () => {
  const [user, orders, recommendations] = await Promise.all([
    userService.get('/me'),
    orderService.get('/recent'),
    recommendationService.get('/'),
  ]);
  
  // If recommendationService fails, entire request fails!
  // Even though we have user and orders data.
};

// SOLUTION: Handle partial failures
const goodServiceCall = async () => {
  const results = await Promise.allSettled([
    userService.get('/me'),
    orderService.get('/recent'),
    recommendationService.get('/'),
  ]);

  const user = results[0].status === 'fulfilled' ? results[0].value : null;
  const orders = results[1].status === 'fulfilled' ? results[1].value : [];
  const recommendations = results[2].status === 'fulfilled' ? results[2].value : [];

  // Return partial data with graceful degradation
  return { user, orders, recommendations };
};

// FAILURE 3: No circuit breaker
const badCircuitBreaker = async () => {
  while (true) {
    try {
      await callExternalService();
    } catch (error) {
      // Retry immediately - can overload failing service!
      await delay(100);
    }
  }
};

// SOLUTION: Implement circuit breaker
const CircuitBreaker = require('opossum');

const circuitBreaker = new CircuitBreaker(callExternalService, {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000,
});

circuitBreaker.fallback(() => ({ data: [], fromCache: true }));

circuitBreaker.on('open', () => console.log('Circuit opened!'));
circuitBreaker.on('halfOpen', () => console.log('Circuit half-open'));
circuitBreaker.on('close', () => console.log('Circuit closed'));
```

---

## 7. Debugging Guide

### Distributed Tracing

```javascript
// File: tracing/setup.js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { HttpTraceContext } = require('@opentelemetry/core');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { PrismaInstrumentation } = require('@opentelemetry/instrumentation-prisma');

const sdk = new NodeSDK({
  traceExporter: new JaegerExporter({
    endpoint: 'http://jaeger:14268/api/traces',
  }),
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
    new PrismaInstrumentation(),
  ],
});

sdk.start();

// Trace context propagation
const { trace, context, SpanKind } = require('@opentelemetry/api');

const tracer = trace.getTracer('order-service');

async function createOrder(orderData) {
  const span = tracer.startSpan('createOrder', {
    kind: SpanKind.INTERNAL,
    attributes: {
      'order.items': orderData.items.length,
      'order.total': orderData.total,
    },
  });

  try {
    const ctx = trace.setSpan(context.active(), span);
    
    // Call other services with trace context
    await context.with(ctx, async () => {
      const user = await userService.get(`/users/${orderData.userId}`);
      const payment = await paymentService.post('/payments', orderData.payment);
      const order = await prisma.order.create({ data: orderData });
      
      span.setAttribute('order.id', order.id);
      return order;
    });

    span.setStatus({ code: SpanStatusCode.OK });
    return order;
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR });
    throw error;
  } finally {
    span.end();
  }
}

// File: middleware/tracing.js
const { trace, context } = require('@opentelemetry/api');

const tracingMiddleware = (req, res, next) => {
  const span = trace.getActiveSpan();
  
  if (span) {
    span.setAttribute('http.method', req.method);
    span.setAttribute('http.url', req.url);
    span.setAttribute('http.user_agent', req.get('user-agent'));
    
    // Add user ID if authenticated
    if (req.user) {
      span.setAttribute('user.id', req.user.id);
    }
  }
  
  next();
};
```

### Logging Strategy

```javascript
// File: utils/structuredLogger.js
const pino = require('pino');

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    targets: [
      {
        target: 'pino/file',
        options: { destination: 1 }, // stdout
      },
      {
        target: 'pino-pretty',
        options: { colorize: true },
      },
    ],
  },
  base: {
    pid: process.pid,
    hostname: require('os').hostname(),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Create child logger with context
const createRequestLogger = (requestId, userId) => {
  return logger.child({ requestId, userId });
};

// Log levels
const logRequest = (req, res, duration) => {
  logger.info({
    type: 'request',
    method: req.method,
    path: req.path,
    statusCode: res.statusCode,
    duration,
    userId: req.user?.id,
    requestId: req.headers['x-request-id'],
  });
};

// Log errors with stack trace
const logError = (error, context = {}) => {
  logger.error({
    type: 'error',
    message: error.message,
    stack: error.stack,
    ...context,
  });
};

// Log business events
const logBusinessEvent = (event, data) => {
  logger.info({
    type: 'business_event',
    event,
    ...data,
  });
};
```

---

## 8. Tradeoffs

### Architecture Decisions Matrix

| Factor | Monolithic | Modular Monolith | Microservices |
|--------|------------|------------------|---------------|
| **Development Speed** | Fast to start | Fast to start | Slow to start |
| **Team Size** | Small (1-10) | Medium (5-20) | Large (20+) |
| **Complexity** | Low | Medium | High |
| **Deployment** | Single unit | Single unit | Multiple |
| **Scaling** | Vertical only | Vertical + horizontal | Independent |
| **Tech Stack** | Uniform | Uniform | Mixed |
| **Debugging** | Easy | Easy | Complex |
| **Cost (Small)** | Low | Low | High |
| **Cost (Large)** | High | Medium | Optimized |
| **Fault Isolation** | Poor | Good | Excellent |
| **Data Isolation** | Shared | Per module | Per service |

### When to Use What

```javascript
// MONOLITHIC - Good for:
const monolithUseCases = [
  'Starting a new project',
  'Small team (< 10 developers)',
  'Limited budget',
  'Proof of concept',
  'Simple CRUD application',
  'Tight timeline',
];

// MODULAR MONOLITH - Good for:
const modularUseCases = [
  'Growing team (5-20)',
  'Need clear boundaries',
  'Different release cycles',
  'Want to migrate to microservices later',
  'Clear domain boundaries',
];

// MICROSERVICES - Good for:
const microservicesUseCases = [
  'Large team (20+)',
  'Multiple autonomous teams',
  'Different scalability needs',
  'Different tech requirements',
  'Mission-critical systems',
  'Very large scale',
];
```

---

## 9. Security Concerns

### Backend Security Architecture

```javascript
// File: security/multiLayerSecurity.js

// Layer 1: Network Security
const networkSecurity = {
  // Use private subnets for services
  vpcConfig: {
    publicSubnets: ['Load Balancer'],
    privateSubnets: ['API Services'],
    databaseSubnets: ['PostgreSQL', 'Redis'],
  },
  
  // Security groups
  securityGroups: {
    loadBalancer: { inbound: [80, 443], outbound: [3000] },
    apiService: { inbound: [3000], outbound: [5432, 6379, otherServices] },
    database: { inbound: [5432], outbound: [] },
  },
};

// Layer 2: Authentication
const authConfig = {
  // JWT tokens
  jwt: {
    accessTokenExpiry: '15m',
    refreshTokenExpiry: '7d',
    algorithm: 'RS256',
  },
  
  // OAuth2
  oauth: {
    providers: ['google', 'github', 'apple'],
    callbackUrl: '/api/auth/callback',
  },
  
  // API keys for services
  serviceApiKeys: {
    rotationDays: 90,
    minLength: 32,
  },
};

// Layer 3: Authorization
const authorizationConfig = {
  rbac: {
    roles: ['admin', 'moderator', 'user', 'guest'],
    permissions: {
      admin: ['*'],
      moderator: ['read', 'write', 'delete:own'],
      user: ['read', 'write:own'],
      guest: ['read:public'],
    },
  },
  
  // Resource-based policies
  resourcePolicies: {
    userProfile: {
      owner: ['read', 'write', 'delete'],
      others: ['read:public'],
    },
    order: {
      owner: ['read'],
      admin: ['read', 'write', 'delete'],
    },
  },
};

// Layer 4: Data Security
const dataSecurity = {
  encryption: {
    atRest: 'AES-256',
    inTransit: 'TLS 1.3',
  },
  
  sensitiveData: {
    fieldsToEncrypt: ['password', 'ssn', 'creditCard'],
    fieldsToHash: ['password'],
    fieldsToMask: ['phone', 'email'],
  },
};

// Layer 5: Audit Logging
const auditConfig = {
  logEvents: [
    'user.login',
    'user.logout',
    'user.password_change',
    'user.role_change',
    'data.export',
    'data.delete',
    'admin.action',
  ],
  
  retentionDays: 365,
  
  storage: 'immutable audit log',
};
```

---

## 10. Performance Optimization

### Caching Strategy

```javascript
// File: caching/cacheManager.js
const { Redis } = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);

// Cache patterns
const CachePattern = {
  // Cache Aside (most common)
  async cacheAside(key, fetchFn, ttl = 3600) {
    // Try cache first
    const cached = await redis.get(key);
    if (cached) return JSON.parse(cached);

    // Fetch from database
    const data = await fetchFn();

    // Store in cache
    await redis.setex(key, ttl, JSON.stringify(data));

    return data;
  },

  // Write Through
  async writeThrough(key, data, ttl = 3600) {
    // Write to database
    await db.update(key, data);

    // Write to cache immediately
    await redis.setex(key, ttl, JSON.stringify(data));

    return data;
  },

  // Write Behind
  async writeBehind(key, data) {
    // Write to database
    await db.update(key, data);

    // Queue cache update
    await redis.lpush('cache:writeBehind', JSON.stringify({ key, data }));
  },

  // Cache Invalidation
  async invalidatePattern(pattern) {
    const keys = await redis.keys(pattern);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  },
};

// Multi-level caching
const multiLevelCache = {
  l1: new Map(), // In-memory LRU cache
  l2: redis,      // Redis

  async get(key) {
    // Check L1 first
    if (this.l1.has(key)) {
      return this.l1.get(key);
    }

    // Check L2
    const value = await redis.get(key);
    if (value) {
      this.l1.set(key, JSON.parse(value)); // Populate L1
      return JSON.parse(value);
    }

    return null;
  },

  async set(key, value, ttl = 3600) {
    this.l1.set(key, value);
    await redis.setex(key, ttl, JSON.stringify(value));
  },
};
```

### Database Optimization

```javascript
// File: database/queryOptimization.js

// Connection pooling
const poolConfig = {
  min: 5,
  max: 20,
  acquireTimeoutMillis: 30000,
  idleTimeoutMillis: 60000,
  reapIntervalMillis: 1000,
};

// Query optimization
const optimizedQueries = {
  // Use indexes
  indexStrategy: `
    CREATE INDEX idx_users_email ON users(email);
    CREATE INDEX idx_users_role ON users(role);
    CREATE INDEX idx_orders_user_id ON orders(user_id);
    CREATE INDEX idx_orders_created ON orders(created_at DESC);
    CREATE INDEX idx_products_category ON products(category_id);
    CREATE INDEX idx_products_price ON products(price);
    CREATE INDEX CONCURRENTLY idx_sessions_token ON sessions(token);
  `,

  // Eager loading to prevent N+1
  eagerLoading: async (userId) => {
    return prisma.user.findUnique({
      where: { id: userId },
      include: {
        orders: { include: { items: true } },
        addresses: true,
        preferences: true,
      },
    });
  },

  // Pagination
  paginatedQuery: async (page = 1, limit = 10) => {
    return prisma.user.findMany({
      skip: (page - 1) * limit,
      take: limit,
      orderBy: { createdAt: 'desc' },
    });
  },

  // Cursor-based pagination for large datasets
  cursorPagination: async (cursor, limit = 10) => {
    return prisma.user.findMany({
      take: limit + 1,
      ...(cursor && { cursor: { id: cursor }, skip: 1 }),
      orderBy: { createdAt: 'desc' },
    });
  },
};
```

---

## 11. Scaling Challenges

### Horizontal Scaling

```javascript
// File: scaling/horizontalScale.js

// Load Balancer Configuration (Nginx)
const nginxConfig = `
upstream backend {
  least_conn;
  
  server 10.0.0.1:3000 weight=3;
  server 10.0.0.2:3000 weight=3;
  server 10.0.0.3:3000 weight=3;
  
  keepalive 64;
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
    
    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    
    # Buffers
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
  }
}
`;

// Kubernetes Deployment
const k8sDeployment = {
  apiVersion: 'apps/v1',
  kind: 'Deployment',
  metadata: { name: 'api-server' },
  spec: {
    replicas: 3,
    selector: { matchLabels: { app: 'api-server' } },
    template: {
      spec: {
        containers: [{
          name: 'api',
          image: 'myapp/api:latest',
          ports: [{ containerPort: 3000 }],
          resources: {
            requests: { memory: '256Mi', cpu: '250m' },
            limits: { memory: '512Mi', cpu: '500m' },
          },
          readinessProbe: {
            httpGet: { path: '/health', port: 3000 },
            initialDelaySeconds: 5,
            periodSeconds: 5,
          },
          livenessProbe: {
            httpGet: { path: '/health', port: 3000 },
            initialDelaySeconds: 30,
            periodSeconds: 10,
          },
        }],
      },
    },
  },
};
```

### Database Scaling

```javascript
// File: scaling/databaseScale.js

// Read replicas
const readReplicaConfig = {
  primary: {
    url: process.env.DATABASE_PRIMARY_URL,
    role: 'write',
  },
  replicas: [
    { url: process.env.DATABASE_REPLICA_1, role: 'read' },
    { url: process.env.DATABASE_REPLICA_2, role: 'read' },
    { url: process.env.DATABASE_REPLICA_3, role: 'read' },
  ],
};

// Sharding
const shardingConfig = {
  strategy: 'hash',
  shardKey: 'userId',
  shards: [
    { id: 0, range: '0-99', connection: 'postgres://shard0:5432/db' },
    { id: 1, range: '100-199', connection: 'postgres://shard1:5432/db' },
    { id: 2, range: '200-299', connection: 'postgres://shard2:5432/db' },
    { id: 3, range: '300-399', connection: 'postgres://shard3:5432/db' },
  ],
  
  getShard: (userId) => {
    const shardId = parseInt(userId) % 4;
    return shardingConfig.shards[shardId];
  },
};

// Data partitioning
const partitioningConfig = {
  type: 'range', // or 'list', 'hash'
  column: 'created_at',
  partitions: [
    { name: 'p_2024_q1', range: '< 2024-04-01' },
    { name: 'p_2024_q2', range: '>= 2024-04-01 AND < 2024-07-01' },
    { name: 'p_2024_q3', range: '>= 2024-07-01 AND < 2024-10-01' },
    { name: 'p_2024_q4', range: '>= 2024-10-01 AND < 2025-01-01' },
  ],
};
```

---

## 12. Best Practices

### Architecture Best Practices

```markdown
# Architecture Best Practices

## 1. Design Principles
- Single Responsibility: Each service does one thing well
- Loose Coupling: Services should be independent
- High Cohesion: Related functionality grouped together
- Domain-Driven Design: Model based on business domain

## 2. Service Design
- Stateless services for horizontal scaling
- Idempotent operations for reliability
- Graceful degradation for fault tolerance
- Circuit breakers for external dependencies

## 3. Data Management
- Each service owns its data
- Eventual consistency acceptable
- CQRS for complex domains
- Saga pattern for distributed transactions

## 4. Communication
- Async over sync when possible
- API contracts are stable
- Version APIs properly
- Document everything

## 5. Security
- Zero trust architecture
- Defense in depth
- Principle of least privilege
- Regular security audits

## 6. Observability
- Structured logging
- Distributed tracing
- Metrics and alerts
- Health checks

## 7. Deployment
- CI/CD pipelines
- Blue-green deployments
- Feature flags
- Infrastructure as code
```

---

## 13. Common Mistakes

### Architecture Anti-Patterns

```javascript
// MISTAKE 1: Premature optimization - going microservices too early
// BAD: Starting with 20 microservices for a new app
const badStart = {
  services: 20,
  team: 3,
  time: 'week 1',
  result: 'chaos',
};

// GOOD: Start monolithic, extract when needed
const goodStart = {
  type: 'monolith',
  services: 1,
  team: 3,
  time: 'week 1',
  result: 'working product',
};

// MISTAKE 2: Shared database between microservices
// BAD: Two services directly query same tables
const badSharedDB = {
  serviceA: { directlyAccesses: ['users', 'orders', 'products'] },
  serviceB: { directlyAccesses: ['users', 'orders'] },
  // Problem: Tight coupling, deployment issues
};

// GOOD: Each service has its own database
const goodIsolation = {
  userService: { database: 'users_db' },
  orderService: { database: 'orders_db' },
  // Loose coupling via events
};

// MISTAKE 3: Not planning for failure
// BAD: Synchronous waterfall calls
const badWaterfall = async () => {
  const user = await getUser();
  const orders = await getOrders(user.id);
  const products = await getProducts(orders);
  const reviews = await getReviews(products);
  // If any step fails, everything fails!
};

// GOOD: Parallel calls with fallback
const goodParallel = async () => {
  const results = await Promise.allSettled([
    getUser(),
    getOrders(),
    getProducts(),
  ]);
  
  return {
    user: results[0].value || defaultUser,
    orders: results[1].value || [],
    products: results[2].value || [],
  };
};

// MISTAKE 4: Ignoring data consistency
// BAD: No plan for distributed transactions
const badNoPlan = {
  step1: 'Update order status',
  step2: 'Send email',
  step3: 'Update inventory',
  // Problem: If step3 fails, order and email already sent!
};

// GOOD: Use Saga pattern
const sagaPattern = {
  pattern: 'compensating-transactions',
  steps: [
    { action: 'createOrder', compensate: 'cancelOrder' },
    { action: 'reserveInventory', compensate: 'releaseInventory' },
    { action: 'processPayment', compensate: 'refundPayment' },
    { action: 'sendEmail', compensate: 'sendCancellationEmail' },
  ],
};
```

---

## 14. Interview Questions

### System Design Interview Q&A

```markdown
Q1: Explain the difference between monolithic and microservices architecture.
A: Monolith = Single deployable unit with all code together.
   Microservices = Small, independent services that communicate via network.
   Monolith: Simpler, faster to develop, harder to scale individually.
   Microservices: Complex setup, but independent scaling and deployment.

Q2: How do you handle data consistency in microservices?
A: Use Saga pattern with compensating transactions.
   Use event sourcing for audit trail.
   Accept eventual consistency.
   Use distributed transactions only when absolutely necessary.

Q3: What is API Gateway and why use it?
A: Single entry point for all clients.
   Handles cross-cutting concerns: auth, rate limiting, logging.
   Routes requests to appropriate services.
   Can aggregate responses from multiple services.

Q4: Explain Circuit Breaker pattern.
A: Prevents cascading failures.
   States: Closed (normal), Open (failing), Half-Open (testing).
   When a service fails repeatedly, circuit "opens" and returns fallback.
   Periodically tests if service is healthy again.

Q5: What is CQRS?
A: Command Query Responsibility Segregation.
   Separate models for reading and writing.
   Write side: Handles updates, stores in write database.
   Read side: Optimized for queries, can use different storage.

Q6: How do you design for failure?
A: Implement circuit breakers.
   Use timeouts for all external calls.
   Implement retries with exponential backoff.
   Have fallback responses.
   Use health checks and graceful degradation.
   Log everything for debugging.

Q7: What is Event Sourcing?
A: Store all changes as events, not current state.
   Events are immutable and stored in order.
   Current state = replay all events.
   Great for audit trails and complex domains.
```

---

## 15. Latest 2026 Fullstack Engineering Patterns

### Modern Architecture Patterns 2026

```typescript
// 1. Micro-frontends Architecture
// File: microfrontend/shell.tsx
const microFrontendConfig = {
  shell: {
    name: 'shell-app',
    container: document.getElementById('root'),
    routes: ['/dashboard', '/settings'],
  },
  
  remotes: {
    catalog: {
      url: 'http://localhost:3001',
      module: './CatalogApp',
    },
    cart: {
      url: 'http://localhost:3002',
      module: './CartApp',
    },
    checkout: {
      url: 'http://localhost:3003',
      module: './CheckoutApp',
    },
  },
};

// Module Federation (Webpack 5)
const moduleFederationConfig = {
  name: 'shell',
  remotes: {
    catalog: 'catalog@http://localhost:3001/remoteEntry.js',
    cart: 'cart@http://localhost:3002/remoteEntry.js',
  },
  shared: ['react', 'react-dom'],
};

// 2. Serverless Architecture with AWS Lambda
// File: serverless/userHandler.ts
import { APIGatewayProxyHandler } from 'aws-lambda';

export const createUser: APIGatewayProxyHandler = async (event) => {
  const userData = JSON.parse(event.body);
  
  await prisma.user.create({ data: userData });
  
  return {
    statusCode: 201,
    body: JSON.stringify({ message: 'User created' }),
  };
};

// Event-driven with SQS
export const processOrder: APIGatewayProxyHandler = async (event) => {
  for (const record of event.Records) {
    const order = JSON.parse(record.body);
    await processOrderLogic(order);
  }
  
  return { statusCode: 200 };
};

// 3. Edge Computing with Cloudflare Workers
// File: edge/worker.ts
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    // Edge-compatible database
    const db = await useDatabase(url.pathname);
    
    // Cache at edge
    const cache = await caches.default.match(request);
    if (cache) return cache;
    
    const response = await fetch(request);
    
    // Cache response for 1 hour
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('Cache-Control', 'public, max-age=3600');
    
    return newResponse;
  },
};

// 4. AI-Integrated Backend
// File: ai-integration/agentService.ts
class AIAgentService {
  async processUserRequest(userMessage: string, context: UserContext) {
    // Route to appropriate AI model
    const intent = await this.detectIntent(userMessage);
    
    switch (intent) {
      case 'code_generation':
        return this.handleCodeGeneration(userMessage);
      case 'data_analysis':
        return this.handleDataAnalysis(userMessage, context);
      case 'customer_support':
        return this.handleCustomerSupport(userMessage, context);
      default:
        return this.handleGeneralQuery(userMessage);
    }
  }
  
  // RAG (Retrieval Augmented Generation)
  async ragQuery(query: string) {
    // 1. Embed query
    const queryEmbedding = await this.embedQuery(query);
    
    // 2. Search vector database
    const relevantDocs = await vectorDB.search(queryEmbedding, { topK: 5 });
    
    // 3. Generate with context
    const response = await this.llm.generate({
      prompt: query,
      context: relevantDocs,
    });
    
    return response;
  }
}

// 5. Observability with OpenTelemetry
// File: observability/sdk.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

---

## Summary

Bhai, backend architecture ek vast topic hai. Key takeaways:

1. **Start Simple** - Monolith se shuru karo, microservices tabhi jab zarurat ho
2. **Clear Boundaries** - Services ke beech clean interfaces
3. **Plan for Failure** - Circuit breakers, retries, fallbacks
4. **Data Ownership** - Har service apna data khud manage kare
5. **Observability** - Logging, tracing, monitoring essential hai
6. **Security** - Multiple layers of defense
7. **2026 Trends** - Serverless, Edge computing, AI integration, Micro-frontends

Architecture ka choice business requirements, team size, aur scale pe depend karta hai. No single solution fits all!

---

*Previous: [REST and GraphQL APIs](./REST_and_GraphQL_APIs.md) | Next: [Caching and Queues](./Caching_and_Queues.md)*
