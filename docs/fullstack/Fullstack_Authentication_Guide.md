# 🔐 Fullstack Authentication - Complete Guide

> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master authentication patterns for fullstack applications with NextAuth, JWT, OAuth, and RBAC.

---

## 🧭 Core Concepts (Concept-First)

- Authentication: JWT, sessions, tokens
- Authorization: RBAC, permissions, middleware
- OAuth: Google, GitHub, social login
- Security: Password hashing, CSRF, XSS
- NextAuth: Provider setup, callbacks

---

## 📋 Complete Guide

### 1️⃣ NextAuth.js (Auth.js)

**Setup:**
```bash
npm install next-auth
```

**Configuration:**
```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import GitHubProvider from 'next-auth/providers/github'
import CredentialsProvider from 'next-auth/providers/credentials'

const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    }),
    GitHubProvider({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!
    }),
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        const user = await verifyUser(credentials?.email, credentials?.password)
        if (user) return user
        return null
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role
        token.id = user.id
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.role = token.role
        session.user.id = token.id
      }
      return session
    }
  },
  pages: {
    signIn: '/login',
    error: '/auth/error'
  }
})

export { handler as GET, handler as POST }
```

**Use in Components:**
```typescript
// app/components/AuthProvider.tsx
'use client'
import { SessionProvider } from 'next-auth/react'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>
}

// Usage
'use client'
import { useSession, signIn, signOut } from 'next-auth/react'

export function UserMenu() {
  const { data: session } = useSession()
  
  if (session) {
    return (
      <div>
        <p>{session.user?.name}</p>
        <button onClick={() => signOut()}>Sign Out</button>
      </div>
    )
  }
  
  return <button onClick={() => signIn()}>Sign In</button>
}
```

### 2️⃣ JWT Implementation

**Token Generation:**
```javascript
const jwt = require('jsonwebtoken')

function generateTokens(user) {
  const accessToken = jwt.sign(
    { 
      userId: user.id, 
      email: user.email,
      role: user.role 
    },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  )
  
  const refreshToken = jwt.sign(
    { userId: user.id },
    process.env.REFRESH_SECRET,
    { expiresIn: '7d' }
  )
  
  return { accessToken, refreshToken }
}
```

**Token Verification:**
```javascript
function verifyToken(token) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET)
  } catch (error) {
    return null
  }
}

// Middleware
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1]
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' })
  }
  
  const decoded = verifyToken(token)
  
  if (!decoded) {
    return res.status(401).json({ error: 'Invalid token' })
  }
  
  req.user = decoded
  next()
}
```

### 3️⃣ OAuth Integration

**Google OAuth:**
```typescript
// Google OAuth flow
const GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
const GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'

async function getGoogleUser(accessToken) {
  const response = await fetch(
    'https://www.googleapis.com/oauth2/v2/userinfo',
    {
      headers: { Authorization: `Bearer ${accessToken}` }
    }
  )
  return response.json()
}

// Redirect URL
const authUrl = `${GOOGLE_AUTH_URL}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=openid email profile`
```

### 4️⃣ Role-Based Access Control (RBAC)

**Role Definition:**
```typescript
enum Role {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator'
}

enum Permission {
  READ = 'read',
  WRITE = 'write',
  DELETE = 'delete',
  MANAGE_USERS = 'manage_users'
}

const rolePermissions: Record<Role, Permission[]> = {
  [Role.ADMIN]: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.MANAGE_USERS],
  [Role.MODERATOR]: [Permission.READ, Permission.WRITE, Permission.DELETE],
  [Role.USER]: [Permission.READ]
}
```

**Middleware:**
```typescript
function authorize(...allowedRoles: Role[]) {
  return (req, res, next) => {
    const userRole = req.user.role
    
    if (!allowedRoles.includes(userRole)) {
      return res.status(403).json({ error: 'Forbidden' })
    }
    
    next()
  }
}

// Usage
app.get('/admin/users', authenticate, authorize(Role.ADMIN), getAllUsers)
```

### 5️⃣ Password Security

**Bcrypt Hashing:**
```javascript
const bcrypt = require('bcrypt')

async function hashPassword(password) {
  const saltRounds = 12
  return bcrypt.hash(password, saltRounds)
}

async function verifyPassword(password, hash) {
  return bcrypt.compare(password, hash)
}
```

**Validation:**
```typescript
const z = require('zod')

const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
  name: z.string().min(2)
})

function validateRegister(data) {
  try {
    return registerSchema.parse(data)
  } catch (error) {
    throw new Error('Invalid input')
  }
}
```

### 6️⃣ Session Management

**Secure Session Config:**
```typescript
// NextAuth session config
session: {
  strategy: 'jwt',
  maxAge: 30 * 24 * 60 * 60, // 30 days
  updateAge: 24 * 60 * 60 // 24 hours
},
cookies: {
  sessionToken: {
    name: `__Secure-session`,
    options: {
      httpOnly: true,
      secure: true,
      sameSite: 'lax',
      path: '/',
      maxAge: 30 * 24 * 60 * 60
    }
  }
}
```

---

## 🎯 Best Practices Checklist

- [ ] Use HTTPS in production
- [ ] Implement proper password validation
- [ ] Use httpOnly cookies
- [ ] Implement CSRF protection
- [ ] Use secure session configuration
- [ ] Implement proper logout
- [ ] Use refresh tokens

---

## 🔗 Related Resources

- [NextAuth.js Documentation](https://next-auth.js.org)
- [OAuth 2.0 RFC](https://tools.ietf.org/html/rfc6749)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

> 💡 **Tip:** Always use HTTPS! Even in development, use localhost with TLS!