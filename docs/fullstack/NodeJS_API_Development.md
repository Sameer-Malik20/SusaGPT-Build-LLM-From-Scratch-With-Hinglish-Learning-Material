# 🚂 Node.js API Development - Complete Guide

> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master Node.js API development with Express, Fastify, REST, and GraphQL.

---

## 🧭 Core Concepts (Concept-First)

- Node.js Runtime: Event loop, async/await, buffers
- Express.js: Middleware, routing, error handling
- Fastify: Performance, schema validation
- REST API Design: Best practices, status codes
- GraphQL: Schema, resolvers, subscriptions

---

## 📋 Complete Guide

### 1️⃣ Express.js Fundamentals

**Basic Server:**
```javascript
const express = require('express')
const app = express()

app.use(express.json()) // Middleware

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date() })
})

app.listen(3000, () => {
  console.log('Server running on port 3000')
})
```

**Route with Parameters:**
```javascript
app.get('/api/users/:id', async (req, res) => {
  try {
    const { id } = req.params
    const user = await getUserById(id)
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' })
    }
    
    res.json(user)
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' })
  }
})
```

**Middleware Pattern:**
```javascript
// Logger middleware
const logger = (req, res, next) => {
  console.log(`${req.method} ${req.url} - ${new Date()}`)
  next() // Important: call next()
}

// Auth middleware
const authenticate = async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '')
  
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' })
  }
  
  try {
    const user = await verifyToken(token)
    req.user = user
    next()
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' })
  }
}

// Use middleware
app.use('/api', logger)
app.use('/api/protected', authenticate)
```

### 2️⃣ Fastify for Performance

**Fastify Setup:**
```javascript
const fastify = require('fastify')({ logger: true })

// Schema validation
const userSchema = {
  body: {
    type: 'object',
    required: ['email', 'password'],
    properties: {
      email: { type: 'string', format: 'email' },
      password: { type: 'string', minLength: 8 }
    }
  }
}

fastify.post('/api/register', { schema: userSchema }, async (request, reply) => {
  const { email, password } = request.body
  
  // Hash password
  const hashedPassword = await bcrypt.hash(password, 10)
  
  const user = await createUser({ email, password: hashedPassword })
  
  return reply.status(201).send(user)
})

// Start server
fastify.listen({ port: 3000 })
```

### 3️⃣ REST API Best Practices

**CRUD Operations:**
```javascript
// GET - Read
app.get('/api/users', async (req, res) => {
  const { page = 1, limit = 10 } = req.query
  const users = await User.find()
    .limit(limit * 1)
    .skip((page - 1) * limit)
  
  return res.json({
    users,
    total: await User.countDocuments(),
    page: +page,
    pages: Math.ceil(await User.countDocuments() / limit)
  })
})

// POST - Create
app.post('/api/users', async (req, res) => {
  const user = new User(req.body)
  await user.save()
  return res.status(201).send(user)
})

// PUT - Update (full)
app.put('/api/users/:id', async (req, res) => {
  const user = await User.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true, runValidators: true }
  )
  return res.send(user)
})

// PATCH - Update (partial)
app.patch('/api/users/:id', async (req, res) => {
  const user = await User.findByIdAndUpdate(
    req.params.id,
    { $set: req.body },
    { new: true }
  )
  return res.send(user)
})

// DELETE - Delete
app.delete('/api/users/:id', async (req, res) => {
  await User.findByIdAndDelete(req.params.id)
  return res.status(204).send()
})
```

**Status Codes:**
```javascript
// 200 - OK
res.status(200).json(data)

// 201 - Created
res.status(201).json(createdItem)

// 204 - No Content
res.status(204).send()

// 400 - Bad Request
res.status(400).json({ error: 'Invalid input' })

// 401 - Unauthorized
res.status(401).json({ error: 'Not authenticated' })

// 403 - Forbidden
res.status(403).json({ error: 'Access denied' })

// 404 - Not Found
res.status(404).json({ error: 'Not found' })

// 500 - Internal Server Error
res.status(500).json({ error: 'Server error' })
```

### 4️⃣ Error Handling

**Global Error Handler:**
```javascript
class AppError extends Error {
  constructor(message, statusCode) {
    super(message)
    this.statusCode = statusCode
    this.isOperational = true
    Error.captureStackTrace(this, this.constructor)
  }
}

const errorHandler = (err, req, res, next) => {
  err.statusCode = err.statusCode || 500
  err.status = err.status || 'error'
  
  if (process.env.NODE_ENV === 'development') {
    res.status(err.statusCode).json({
      status: err.status,
      error: err,
      message: err.message,
      stack: err.stack
    })
  } else {
    res.status(err.statusCode).json({
      status: err.status,
      message: err.isOperational ? err.message : 'Something went wrong'
    })
  }
}

app.use(errorHandler)
```

**Async Error Wrapper:**
```javascript
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next)
}

// Usage
app.get('/api/users/:id', asyncHandler(async (req, res) => {
  const user = await getUserById(req.params.id)
  if (!user) throw new AppError('User not found', 404)
  res.json(user)
}))
```

### 5️⃣ Authentication

**JWT Authentication:**
```javascript
const jwt = require('jsonwebtoken')

// Generate token
const generateToken = (userId) => {
  return jwt.sign(
    { userId },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  )
}

// Verify token middleware
const verifyToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1]
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' })
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    req.user = decoded
    next()
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' })
  }
}

// Login endpoint
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body
  
  const user = await User.findOne({ email })
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' })
  }
  
  const isMatch = await bcrypt.compare(password, user.password)
  if (!isMatch) {
    return res.status(401).json({ error: 'Invalid credentials' })
  }
  
  const token = generateToken(user._id)
  res.json({ token, user: { id: user._id, email: user.email } })
})
```

### 6️⃣ Rate Limiting & Security

**Rate Limiting:**
```javascript
const rateLimit = require('express-rate-limit')

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later'
})

app.use('/api', limiter)
```

**Security Headers:**
```javascript
const helmet = require('helmet')
app.use(helmet())

// CORS
const cors = require('cors')
app.use(cors({
  origin: ['https://example.com'],
  credentials: true
}))
```

---

## 🎯 Best Practices Checklist

- [ ] Use async/await for all async operations
- [ ] Implement proper error handling
- [ ] Use environment variables
- [ ] Implement rate limiting
- [ ] Use security headers (helmet)
- [ ] Validate all inputs
- [ ] Use proper status codes
- [ ] Implement proper logging

---

## 🔗 Related Resources

- [Express.js Documentation](https://expressjs.com)
- [Fastify Documentation](https://www.fastify.io)
- [RESTful API Design Best Practices](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-development/)

---

> 💡 **Tip:** Fastify Express se 2-3x faster hai. High-performance APIs ke liye use karo!