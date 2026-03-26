# ☁️ Serverless Fullstack - Complete Guide

> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master serverless deployment with Vercel, Netlify, Lambda, and edge functions.

---

## 🧭 Core Concepts (Concept-First)

- Serverless Basics: Functions, cold starts, billing
- Vercel: Next.js deployment, edge functions
- Netlify: Functions, forms, identity
- AWS Lambda: API Gateway, layers, async
- Edge Computing: CDN functions, latency

---

## 📋 Complete Guide

### 1️⃣ Vercel Deployment

**vercel.json Configuration:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    }
  ],
  "env": {
    "DATABASE_URL": "@database-url"
  },
  "regions": ["iad1"],
  "functions": {
    "api/*.ts": {
      "runtime": "nodejs18.x"
    }
  }
}
```

**API Routes:**
```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const page = searchParams.get('page') || '1'
  
  const users = await getUsers({ page: +page, limit: 10 })
  
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const body = await request.json()
  
  const user = await createUser(body)
  
  return NextResponse.json(user, { status: 201 })
}
```

### 2️⃣ Edge Functions

**Edge Runtime:**
```typescript
// app/api/edge/route.ts
export const runtime = 'edge'

export async function GET(request: Request) {
  // Edge functions run closer to users
  const geo = request.geo
  
  return new Response(
    JSON.stringify({
      location: geo?.city,
      country: geo?.country,
      region: geo?.region
    }),
    {
      headers: { 'Content-Type': 'application/json' }
    }
  )
}
```

**Middleware:**
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Add security headers
  const response = NextResponse.next()
  
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  
  // Check auth
  const token = request.cookies.get('token')
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
}
```

### 3️⃣ Netlify Functions

**Function Structure:**
```typescript
// netlify/functions/api.ts
import type { Handler, HandlerEvent, HandlerContext } from '@netlify/functions'

const handler: Handler = async (
  event: HandlerEvent,
  context: HandlerContext
) => {
  // Parse path
  const path = event.path.replace('/.netlify/functions/api', '')
  
  if (event.httpMethod === 'GET' && path === '/users') {
    const users = await getUsers()
    return {
      statusCode: 200,
      body: JSON.stringify(users)
    }
  }
  
  return {
    statusCode: 404,
    body: JSON.stringify({ error: 'Not found' })
  }
}

export { handler }
```

**toml Configuration:**
```toml
[build]
  command = "npm run build"
  publish = "dist"
  functions = "netlify/functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200
```

### 4️⃣ AWS Lambda Integration

**Lambda Handler:**
```javascript
exports.handler = async (event) => {
  const { httpMethod, path, body, headers } = event
  
  // Parse request
  const requestBody = body ? JSON.parse(body) : {}
  
  if (httpMethod === 'GET' && path === '/users') {
    const users = await database.users.findMany()
    
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(users)
    }
  }
  
  return {
    statusCode: 404,
    body: JSON.stringify({ error: 'Not found' })
  }
}
```

**API Gateway:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: my-api
      
  MyResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      RestApiId: !Ref MyApi
      PathPart: users
      
  MyMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      RestApiId: !Ref MyApi
      ResourceId: !Ref MyResource
      HttpMethod: GET
      Integration:
        Type: AWS_PROXY
        IntegrationUri: !GetAtt MyFunction.Arn
```

### 5️⃣ Cold Start Optimization

**Keep Functions Warm:**
```typescript
// API route with scheduled warm-up
export async function GET() {
  // Pre-warm database connection
  await prisma.$connect
  
  return Response.json({ status: 'ok' })
}

// cron job - runs every 5 minutes
// 0 */5 * * * curl https://your-app.com/api/warmup
```

**Lazy Loading:**
```typescript
// Don't initialize heavy stuff at top level
let db: Database | null = null

async function getDb() {
  if (!db) {
    db = await connectToDatabase()
  }
  return db
}

export async function GET() {
  const database = await getDb()
  // Use database...
}
```

### 6️⃣ Environment & Secrets

**Vercel Environment:**
```
# .env.local (development)
DATABASE_URL=postgres://localhost:5432/mydb

# Vercel Dashboard (production)
# Add these in Environment Variables settings:
DATABASE_URL=postgres://user:pass@host:5432/mydb
API_SECRET=your-secret-key
```

**Netlify CLI:**
```bash
# Set secrets
netlify env:set API_SECRET "your-secret"

# Pull env vars
netlify env:import .env
```

---

## 🎯 Best Practices Checklist

- [ ] Use API routes instead of separate backend
- [ ] Implement proper error handling
- [ ] Use environment variables for secrets
- [ ] Implement caching headers
- [ ] Handle cold starts gracefully
- [ ] Use edge functions for low latency
- [ ] Monitor function execution time

---

## 🔗 Related Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Netlify Functions](https://docs.netlify.com/functions/overview/)
- [AWS Lambda Best Practices](https://aws.amazon.com/blogs/compute/best-practices-for-developing-aws-lambda-functions/)

---

> 💡 **Tip:** Serverless functions have execution time limits. Use proper timeouts and handle long-running tasks with queues!