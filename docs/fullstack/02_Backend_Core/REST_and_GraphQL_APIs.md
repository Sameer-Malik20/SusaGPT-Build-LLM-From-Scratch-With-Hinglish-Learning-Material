# REST and GraphQL APIs - Complete Guide

Bhai, API design fullstack development ka heart hai. REST aur GraphQL dono apne time mein best hain, par samajhna zaroori hai ki kab kaunsa use karna hai. Chalo detail mein dono ko cover karte hain!

---

## 1. Beginner-Friendly Hinglish Explanation

### REST API Kya Hai?

Soch ki tu ek **restaurant** mein baith gaya:
- Menu dekho (GET - data dekho)
- Order karo (POST - naya create karo)
- Quantity badlo (PUT/PATCH - update karo)
- Cancel karo (DELETE - delete karo)

Ye hi REST ka concept hai! Standard HTTP methods use karta hai aur har cheez **resource** pe based hai.

**Example:**
```
GET    /users      → Sab users ki list
GET    /users/1    → User id 1 ki details
POST   /users      → Naya user banao
PUT    /users/1    → User 1 ko full update karo
PATCH  /users/1    → User 1 ka partial update karo
DELETE /users/1    → User 1 delete karo
```

### GraphQL Kya Hai?

GraphQL soch jaise **buffet** mein:
- Tu ek checklist leke jaata hai
- Sirf wo cheezen leti hai jo tu khana chahta hai
- Kitchen ko ek baar batao, sab kuch ek saath aajata hai

REST mein agar tu user + uski posts + comments chahta hai, toh 3 API calls maangni padti hain. GraphQL mein ek hi query mein sab kuch maang sakta hai!

**Example:**
```graphql
query {
  user(id: "1") {
    name
    email
    posts {
      title
      comments {
        text
        author
      }
    }
  }
}
```

### REST vs GraphQL Kab Use Karna Hai?

| Scenario | Best Choice |
|----------|------------|
| Simple CRUD operations | REST |
| Mobile apps (bandwidth save) | GraphQL |
| Complex nested data | GraphQL |
| Public API (standard) | REST |
| Real-time updates | GraphQL Subscriptions |
| Team knows SQL well | GraphQL |

---

## 2. Deep Technical Explanation

### REST API Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         REST API ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      CLIENTS                                │   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │   │
│  │   │ Web App │  │Mobile   │  │IoT Dev  │  │ Third Party    │ │   │
│  │   │(React)  │  │ (React  │  │Devices  │  │ Integrations   │ │   │
│  │   │         │  │ Native) │  │         │  │                │ │   │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    API GATEWAY                               │   │
│  │   ┌──────────────────────────────────────────────────────┐  │   │
│  │   │ Rate Limiting | Auth | Logging | Load Balancing     │  │   │
│  │   └──────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      REST ENDPOINTS                         │   │
│  │                                                              │   │
│  │   GET    /api/v1/users        → List all users             │   │
│  │   GET    /api/v1/users/:id    → Get single user            │   │
│  │   POST   /api/v1/users        → Create new user            │   │
│  │   PUT    /api/v1/users/:id    → Full update user           │   │
│  │   PATCH  /api/v1/users/:id    → Partial update user        │   │
│  │   DELETE /api/v1/users/:id    → Delete user               │   │
│  │                                                              │   │
│  │   GET    /api/v1/posts        → List all posts            │   │
│  │   POST   /api/v1/posts        → Create new post           │   │
│  │   GET    /api/v1/users/:id/posts → Get user's posts       │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    RESPONSE FORMAT                          │   │
│  │                                                              │   │
│  │   {                                                          │   │
│  │     "success": true,                                         │   │
│  │     "data": { ... },                                         │   │
│  │     "meta": { "pagination": {...} }                         │   │
│  │   }                                                          │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
├──────────────────────────────┼──────────────────────────────────────┤
│                         DATA LAYER                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │
│  │ PostgreSQL  │  │    Redis    │  │   MongoDB   │  │ External  │  │
│  │  (Primary)  │  │   (Cache)   │  │  (Audit)    │  │   APIs    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### GraphQL Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GRAPHQL ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                        CLIENTS                               │   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐                     │   │
│  │   │ Web App │  │Mobile   │  │Dashboard│                     │   │
│  │   │(Apollo) │  │(Apollo) │  │(Relay)  │                     │   │
│  │   └─────────┘  └─────────┘  └─────────┘                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   GRAPHQL SERVER                            │   │
│  │                                                              │   │
│  │   ┌──────────────────────────────────────────────────────┐  │   │
│  │   │                    SCHEMA                             │  │   │
│  │   │                                                          │  │   │
│  │   │   type User {                                           │  │   │
│  │   │     id: ID!                                             │  │   │
│  │   │     name: String!                                       │  │   │
│  │   │     email: String!                                      │  │   │
│  │   │     posts: [Post!]!                                      │  │   │
│  │   │   }                                                      │  │   │
│  │   │                                                          │  │   │
│  │   │   type Post {                                           │  │   │
│  │   │     id: ID!                                              │  │   │
│  │   │     title: String!                                       │  │   │
│  │   │     content: String                                      │  │   │
│  │   │     author: User!                                        │  │   │
│  │   │     comments: [Comment!]!                                │  │   │
│  │   │   }                                                      │  │   │
│  │   │                                                          │  │   │
│  │   └──────────────────────────────────────────────────────┘  │   │
│  │                                                              │   │
│  │   ┌──────────────────────────────────────────────────────┐  │   │
│  │   │                   RESOLVERS                           │  │   │
│  │   │                                                          │  │   │
│  │   │   Query:  user(id: ID!): User                         │  │   │
│  │   │           users: [User!]!                              │  │   │
│  │   │                                                          │  │   │
│  │   │   Mutation: createUser(input: UserInput!): User!       │  │   │
│  │   │             updateUser(id: ID!, input: UserInput!): User│  │   │
│  │   │             deleteUser(id: ID!): Boolean!              │  │   │
│  │   │                                                          │  │   │
│  │   │   Subscription: userCreated: User!                      │  │   │
│  │   │                 postUpdated: Post!                      │  │   │
│  │   │                                                          │  │   │
│  │   └──────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    DATA SOURCES                             │   │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │   │
│  │   │ PostgreSQL  │  │    Redis    │  │ External    │         │   │
│  │   │             │  │   (Cache)   │  │ REST APIs   │         │   │
│  │   └─────────────┘  └─────────────┘  └─────────────┘         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │               AUTO-GENERATED DOCUMENTATION                   │   │
│  │                   /graphql (GraphiQL)                        │   │
│  │                   /docs (Schema Docs)                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. REST API Implementation

### Complete REST API with Express.js

```javascript
// REST API Implementation
// File: server/routes/users.js
const express = require('express');
const router = express.Router();
const { body, param, query, validationResult } = require('express-validator');
const { userService } = require('../services');
const { asyncHandler } = require('../utils/asyncHandler');
const { AppError } = require('../errors');

// Validation middleware
const validateRequest = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    throw new AppError('Validation failed', 400, 'VALIDATION_ERROR');
  }
  next();
};

// GET /users - List all users with pagination
router.get('/',
  [
    query('page').optional().isInt({ min: 1 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
    query('sortBy').optional().isIn(['name', 'email', 'createdAt']),
    query('sortOrder').optional().isIn(['asc', 'desc']),
    query('search').optional().trim().isLength({ max: 100 }),
  ],
  validateRequest,
  asyncHandler(async (req, res) => {
    const {
      page = 1,
      limit = 10,
      sortBy = 'createdAt',
      sortOrder = 'desc',
      search,
    } = req.query;

    const result = await userService.findAll({
      page,
      limit,
      sortBy,
      sortOrder,
      search,
    });

    res.json({
      success: true,
      data: result.users,
      meta: {
        pagination: result.pagination,
      },
    });
  })
);

// GET /users/:id - Get single user
router.get('/:id',
  [
    param('id').isUUID().withMessage('Invalid user ID format'),
  ],
  validateRequest,
  asyncHandler(async (req, res) => {
    const user = await userService.findById(req.params.id);

    if (!user) {
      throw new AppError('User not found', 404, 'USER_NOT_FOUND');
    }

    res.json({
      success: true,
      data: user,
    });
  })
);

// POST /users - Create new user
router.post('/',
  [
    body('name').trim().isLength({ min: 2, max: 100 }).withMessage('Name must be 2-100 characters'),
    body('email').isEmail().normalizeEmail().withMessage('Invalid email'),
    body('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters'),
    body('role').optional().isIn(['user', 'admin', 'moderator']).withMessage('Invalid role'),
    body('profile').optional().isObject().withMessage('Profile must be an object'),
    body('profile.bio').optional().isString().isLength({ max: 500 }),
    body('profile.avatar').optional().isURL().withMessage('Avatar must be a valid URL'),
  ],
  validateRequest,
  asyncHandler(async (req, res) => {
    const { name, email, password, role, profile } = req.body;

    const user = await userService.create({
      name,
      email,
      password,
      role: role || 'user',
      profile,
    });

    res.status(201).json({
      success: true,
      data: user,
      message: 'User created successfully',
    });
  })
);

// PUT /users/:id - Full update
router.put('/:id',
  [
    param('id').isUUID().withMessage('Invalid user ID'),
    body('name').optional().trim().isLength({ min: 2, max: 100 }),
    body('email').optional().isEmail().normalizeEmail(),
    body('password').optional().isLength({ min: 8 }),
    body('role').optional().isIn(['user', 'admin', 'moderator']),
    body('profile').optional().isObject(),
  ],
  validateRequest,
  asyncHandler(async (req, res) => {
    const user = await userService.update(req.params.id, req.body);

    if (!user) {
      throw new AppError('User not found', 404, 'USER_NOT_FOUND');
    }

    res.json({
      success: true,
      data: user,
      message: 'User updated successfully',
    });
  })
);

// PATCH /users/:id - Partial update
router.patch('/:id',
  [
    param('id').isUUID(),
    body('name').optional().trim().isLength({ min: 2, max: 100 }),
    body('profile.bio').optional().isString().isLength({ max: 500 }),
  ],
  validateRequest,
  asyncHandler(async (req, res) => {
    const user = await userService.patchUpdate(req.params.id, req.body);

    if (!user) {
      throw new AppError('User not found', 404, 'USER_NOT_FOUND');
    }

    res.json({
      success: true,
      data: user,
    });
  })
);

// DELETE /users/:id - Delete user
router.delete('/:id',
  [
    param('id').isUUID(),
  ],
  validateRequest,
  asyncHandler(async (req, res) => {
    const deleted = await userService.delete(req.params.id);

    if (!deleted) {
      throw new AppError('User not found', 404, 'USER_NOT_FOUND');
    }

    res.json({
      success: true,
      message: 'User deleted successfully',
    });
  })
);

module.exports = router;
```

### REST API Service Layer

```javascript
// File: server/services/userService.js
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcrypt');
const { AppError } = require('../errors');

class UserService {
  constructor() {
    this.prisma = new PrismaClient();
  }

  async findAll({ page, limit, sortBy, sortOrder, search }) {
    const skip = (page - 1) * limit;

    const where = search
      ? {
          OR: [
            { name: { contains: search, mode: 'insensitive' } },
            { email: { contains: search, mode: 'insensitive' } },
          ],
        }
      : {};

    const [users, total] = await Promise.all([
      this.prisma.user.findMany({
        where,
        skip,
        take: limit,
        orderBy: { [sortBy]: sortOrder },
        select: {
          id: true,
          name: true,
          email: true,
          role: true,
          profile: true,
          createdAt: true,
          updatedAt: true,
          _count: {
            select: { posts: true, comments: true },
          },
        },
      }),
      this.prisma.user.count({ where }),
    ]);

    return {
      users,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
        hasNext: page * limit < total,
        hasPrev: page > 1,
      },
    };
  }

  async findById(id) {
    const user = await this.prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        name: true,
        email: true,
        role: true,
        profile: true,
        createdAt: true,
        updatedAt: true,
        posts: {
          take: 10,
          orderBy: { createdAt: 'desc' },
          select: {
            id: true,
            title: true,
            published: true,
            createdAt: true,
          },
        },
        _count: {
          select: { posts: true, comments: true },
        },
      },
    });

    return user;
  }

  async create(data) {
    // Check duplicate
    const existing = await this.prisma.user.findUnique({
      where: { email: data.email },
    });

    if (existing) {
      throw new AppError('Email already exists', 409, 'EMAIL_EXISTS');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(data.password, 12);

    const user = await this.prisma.user.create({
      data: {
        ...data,
        password: hashedPassword,
      },
      select: {
        id: true,
        name: true,
        email: true,
        role: true,
        profile: true,
        createdAt: true,
      },
    });

    return user;
  }

  async update(id, data) {
    // Remove password if present (use separate endpoint)
    delete data.password;
    delete data.email; // Email should not be changed via update

    return this.prisma.user.update({
      where: { id },
      data,
      select: {
        id: true,
        name: true,
        email: true,
        role: true,
        profile: true,
        updatedAt: true,
      },
    });
  }

  async patchUpdate(id, data) {
    // Only allow specific fields for patch
    const allowedFields = ['name', 'profile'];
    const filteredData = Object.keys(data)
      .filter((key) => allowedFields.includes(key))
      .reduce((obj, key) => {
        obj[key] = data[key];
        return obj;
      }, {});

    return this.prisma.user.update({
      where: { id },
      data: filteredData,
      select: {
        id: true,
        name: true,
        profile: true,
        updatedAt: true,
      },
    });
  }

  async delete(id) {
    try {
      await this.prisma.user.delete({ where: { id } });
      return true;
    } catch (error) {
      if (error.code === 'P2025') {
        return false;
      }
      throw error;
    }
  }
}

module.exports = { userService: new UserService() };
```

---

## 4. GraphQL Implementation

### Complete GraphQL API with Apollo Server

```javascript
// GraphQL Implementation
// File: server/graphql/schema.js
const { gql } = require('apollo-server-express');

const typeDefs = gql`
  # Scalars
  scalar DateTime
  scalar JSON

  # Enums
  enum Role {
    USER
    ADMIN
    MODERATOR
  }

  enum SortOrder {
    ASC
    DESC
  }

  # Inputs
  input CreateUserInput {
    name: String!
    email: String!
    password: String!
    role: Role
    profile: ProfileInput
  }

  input UpdateUserInput {
    name: String
    role: Role
    profile: ProfileInput
  }

  input ProfileInput {
    bio: String
    avatar: String
    website: String
    location: String
  }

  input UserFilterInput {
    search: String
    role: Role
  }

  # Types
  type User {
    id: ID!
    name: String!
    email: String!
    role: Role!
    profile: Profile
    posts: [Post!]!
    postCount: Int!
    commentCount: Int!
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type Profile {
    bio: String
    avatar: String
    website: String
    location: String
  }

  type Post {
    id: ID!
    title: String!
    slug: String!
    content: String
    excerpt: String
    published: Boolean!
    author: User!
    comments: [Comment!]!
    commentCount: Int!
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type Comment {
    id: ID!
    text: String!
    author: User!
    post: Post!
    createdAt: DateTime!
  }

  # Pagination
  type UserConnection {
    edges: [UserEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
  }

  type UserEdge {
    node: User!
    cursor: String!
  }

  type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
  }

  # Response types
  type DeleteResponse {
    success: Boolean!
    message: String
  }

  # Queries
  type Query {
    # User queries
    users(
      first: Int
      after: String
      last: Int
      before: String
      filter: UserFilterInput
      sortBy: String
      sortOrder: SortOrder
    ): UserConnection!

    user(id: ID!): User
    userByEmail(email: String!): User
    me: User

    # Post queries
    posts(first: Int, after: String, last: Int, before: String): PostConnection!
    post(id: ID!): Post
    postBySlug(slug: String!): Post

    # Comment queries
    comments(postId: ID!): [Comment!]!
  }

  # Mutations
  type Mutation {
    # User mutations
    createUser(input: CreateUserInput!): User!
    updateUser(id: ID!, input: UpdateUserInput!): User!
    deleteUser(id: ID!): DeleteResponse!
    changePassword(oldPassword: String!, newPassword: String!): User!

    # Post mutations
    createPost(title: String!, content: String, published: Boolean): Post!
    updatePost(id: ID!, title: String, content: String, published: Boolean): Post!
    deletePost(id: ID!): DeleteResponse!

    # Comment mutations
    createComment(postId: ID!, text: String!): Comment!
    deleteComment(id: ID!): DeleteResponse!
  }

  # Subscriptions
  type Subscription {
    userCreated: User!
    postCreated: Post!
    postUpdated(id: ID!): Post!
    commentAdded(postId: ID!): Comment!
  }
`;

module.exports = typeDefs;
```

### GraphQL Resolvers

```javascript
// File: server/graphql/resolvers.js
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcrypt');
const { AuthenticationError, ForbiddenError } = require('apollo-server-express');

const prisma = new PrismaClient();

// Helper function for cursor-based pagination
function encodeCursor(id) {
  return Buffer.from(`cursor:${id}`).toString('base64');
}

function decodeCursor(cursor) {
  return Buffer.from(cursor, 'base64').toString('utf-8').replace('cursor:', '');
}

const resolvers = {
  // Scalar resolvers
  DateTime: {
    __parseValue(value) {
      return new Date(value).toISOString();
    },
    __serialize(value) {
      return value instanceof Date ? value.toISOString() : value;
    },
    __parseLiteral(ast) {
      return ast.kind === 'StringValue' ? ast.value : null;
    },
  },

  // Query resolvers
  Query: {
    // User queries
    users: async (parent, args, { user }) => {
      if (!user) throw new AuthenticationError('Not authenticated');

      const { first = 10, after, filter, sortBy = 'createdAt', sortOrder = 'DESC' } = args;

      const where = {};
      if (filter?.search) {
        where.OR = [
          { name: { contains: filter.search, mode: 'insensitive' } },
          { email: { contains: filter.search, mode: 'insensitive' } },
        ];
      }
      if (filter?.role) {
        where.role = filter.role;
      }

      const orderBy = { [sortBy.toLowerCase()]: sortOrder.toLowerCase() };

      const users = await prisma.user.findMany({
        where,
        take: first + 1,
        ...(after && { skip: 1, cursor: { id: decodeCursor(after) } }),
        orderBy,
        include: {
          _count: { select: { posts: true, comments: true } },
        },
      });

      const hasNextPage = users.length > first;
      const edges = users.slice(0, first).map((user) => ({
        node: {
          ...user,
          postCount: user._count.posts,
          commentCount: user._count.comments,
        },
        cursor: encodeCursor(user.id),
      }));

      return {
        edges,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: edges.length > 0 ? edges[0].cursor : null,
          endCursor: edges.length > 0 ? edges[edges.length - 1].cursor : null,
        },
        totalCount: await prisma.user.count({ where }),
      };
    },

    user: async (parent, { id }) => {
      return prisma.user.findUnique({
        where: { id },
        include: {
          posts: {
            where: { published: true },
            take: 10,
          },
          _count: { select: { posts: true, comments: true } },
        },
      });
    },

    userByEmail: async (parent, { email }) => {
      return prisma.user.findUnique({
        where: { email },
      });
    },

    me: async (parent, args, { user }) => {
      if (!user) throw new AuthenticationError('Not authenticated');
      return prisma.user.findUnique({ where: { id: user.id } });
    },

    // Post queries
    posts: async (parent, args) => {
      const { first = 10, after } = args;

      const posts = await prisma.post.findMany({
        where: { published: true },
        take: first + 1,
        ...(after && { skip: 1, cursor: { id: decodeCursor(after) } }),
        orderBy: { createdAt: 'desc' },
        include: {
          author: true,
          _count: { select: { comments: true } },
        },
      });

      const hasNextPage = posts.length > first;
      const edges = posts.slice(0, first).map((post) => ({
        node: {
          ...post,
          commentCount: post._count.comments,
        },
        cursor: encodeCursor(post.id),
      }));

      return {
        edges,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: edges.length > 0 ? edges[0].cursor : null,
          endCursor: edges.length > 0 ? edges[edges.length - 1].cursor : null,
        },
      };
    },

    post: async (parent, { id }) => {
      return prisma.post.findUnique({
        where: { id },
        include: {
          author: true,
          comments: {
            include: { author: true },
          },
        },
      });
    },

    postBySlug: async (parent, { slug }) => {
      return prisma.post.findUnique({
        where: { slug },
        include: { author: true },
      });
    },

    comments: async (parent, { postId }) => {
      return prisma.comment.findMany({
        where: { postId },
        include: { author: true },
        orderBy: { createdAt: 'desc' },
      });
    },
  },

  // Mutation resolvers
  Mutation: {
    createUser: async (parent, { input }) => {
      const { name, email, password, role, profile } = input;

      const existing = await prisma.user.findUnique({ where: { email } });
      if (existing) {
        throw new Error('Email already exists');
      }

      const hashedPassword = await bcrypt.hash(password, 12);

      return prisma.user.create({
        data: {
          name,
          email,
          password: hashedPassword,
          role: role || 'USER',
          profile: profile ? { create: profile } : undefined,
        },
        include: { profile: true },
      });
    },

    updateUser: async (parent, { id, input }, { user }) => {
      if (!user) throw new AuthenticationError('Not authenticated');
      if (user.id !== id && user.role !== 'ADMIN') {
        throw new ForbiddenError('Not authorized');
      }

      return prisma.user.update({
        where: { id },
        data: {
          ...input,
          profile: input.profile ? { upsert: { update: input.profile, create: input.profile } } : undefined,
        },
        include: { profile: true },
      });
    },

    deleteUser: async (parent, { id }, { user }) => {
      if (!user) throw new AuthenticationError('Not authenticated');
      if (user.id !== id && user.role !== 'ADMIN') {
        throw new ForbiddenError('Not authorized');
      }

      await prisma.user.delete({ where: { id } });
      return { success: true, message: 'User deleted' };
    },

    createPost: async (parent, { title, content, published = false }, { user }) => {
      if (!user) throw new AuthenticationError('Not authenticated');

      const slug = title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '');

      return prisma.post.create({
        data: {
          title,
          slug,
          content,
          published,
          authorId: user.id,
        },
        include: { author: true },
      });
    },

    createComment: async (parent, { postId, text }, { user }) => {
      if (!user) throw new AuthenticationError('Not authenticated');

      return prisma.comment.create({
        data: {
          text,
          postId,
          authorId: user.id,
        },
        include: { author: true },
      });
    },
  },

  // Field resolvers (nested resolvers)
  User: {
    posts: async (parent) => {
      return prisma.post.findMany({
        where: { authorId: parent.id },
        orderBy: { createdAt: 'desc' },
      });
    },

    createdAt: (parent) => parent.createdAt.toISOString(),
    updatedAt: (parent) => parent.updatedAt?.toISOString(),
  },

  Post: {
    author: (parent) => prisma.user.findUnique({ where: { id: parent.authorId } }),
    comments: (parent) => prisma.comment.findMany({ where: { postId: parent.id } }),
    createdAt: (parent) => parent.createdAt.toISOString(),
  },

  Comment: {
    author: (parent) => prisma.user.findUnique({ where: { id: parent.authorId } }),
    createdAt: (parent) => parent.createdAt.toISOString(),
  },
};

module.exports = resolvers;
```

---

## 5. Frontend Integration

### React + REST API Client

```typescript
// File: client/src/api/rest-client.ts
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

class RestClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('authToken');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, params?: Record<string, any>) {
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

  async patch<T>(url: string, data?: any) {
    const response = await this.client.patch<T>(url, data);
    return response.data;
  }

  async delete<T>(url: string) {
    const response = await this.client.delete<T>(url);
    return response.data;
  }
}

export const apiClient = new RestClient();

// File: client/src/api/users-rest.ts
import { apiClient } from './rest-client';

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'user' | 'admin' | 'moderator';
  profile?: {
    bio?: string;
    avatar?: string;
  };
  createdAt: string;
  updatedAt: string;
}

export interface CreateUserDto {
  name: string;
  email: string;
  password: string;
  role?: 'user' | 'admin' | 'moderator';
  profile?: {
    bio?: string;
    avatar?: string;
  };
}

export interface PaginationParams {
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  search?: string;
}

export const userApi = {
  getAll: (params?: PaginationParams) =>
    apiClient.get<{
      success: boolean;
      data: User[];
      meta: { pagination: { page: number; limit: number; total: number; totalPages: number } };
    }>('/users', params),

  getById: (id: string) =>
    apiClient.get<{ success: boolean; data: User }>(`/users/${id}`),

  create: (data: CreateUserDto) =>
    apiClient.post<{ success: boolean; data: User }>('/users', data),

  update: (id: string, data: Partial<CreateUserDto>) =>
    apiClient.put<{ success: boolean; data: User }>(`/users/${id}`, data),

  patch: (id: string, data: Partial<CreateUserDto>) =>
    apiClient.patch<{ success: boolean; data: User }>(`/users/${id}`, data),

  delete: (id: string) =>
    apiClient.delete<{ success: boolean; message: string }>(`/users/${id}`),
};
```

### React + GraphQL with Apollo Client

```typescript
// File: client/src/api/graphql-client.ts
import { ApolloClient, InMemoryCache, HttpLink, from } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';

const httpLink = new HttpLink({
  uri: import.meta.env.VITE_GRAPHQL_URL || 'http://localhost:3000/graphql',
});

// Auth link
const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('authToken');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    },
  };
});

// Error link
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) => {
      console.error(`[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`);

      if (message === 'Not authenticated') {
        localStorage.removeItem('authToken');
        window.location.href = '/login';
      }
    });
  }

  if (networkError) {
    console.error(`[Network error]: ${networkError}`);
  }
});

export const apolloClient = new ApolloClient({
  link: from([errorLink, authLink, httpLink]),
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          users: {
            keyArgs: false,
            merge(existing, incoming, { args }) {
              if (!args?.after) {
                return incoming;
              }
              return {
                ...incoming,
                edges: [...(existing?.edges || []), ...incoming.edges],
              };
            },
          },
        },
      },
      User: {
        keyFields: ['id'],
      },
      Post: {
        keyFields: ['id'],
      },
    },
  }),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
    },
  },
});

// File: client/src/api/graphql-queries.ts
import { gql } from '@apollo/client';

export const GET_USERS = gql`
  query GetUsers($first: Int, $after: String, $filter: UserFilterInput) {
    users(first: $first, after: $after, filter: $filter) {
      edges {
        node {
          id
          name
          email
          role
          profile {
            bio
            avatar
          }
          postCount
          commentCount
          createdAt
        }
        cursor
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
    }
  }
`;

export const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
      role
      profile {
        bio
        avatar
        website
        location
      }
      posts {
        id
        title
        slug
        published
        createdAt
      }
      postCount
      commentCount
      createdAt
    }
  }
`;

export const GET_ME = gql`
  query GetMe {
    me {
      id
      name
      email
      role
      profile {
        bio
        avatar
      }
    }
  }
`;

export const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      id
      name
      email
      role
      createdAt
    }
  }
`;

export const UPDATE_USER = gql`
  mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
    updateUser(id: $id, input: $input) {
      id
      name
      email
      role
      profile {
        bio
        avatar
        website
        location
      }
      updatedAt
    }
  }
`;

export const DELETE_USER = gql`
  mutation DeleteUser($id: ID!) {
    deleteUser(id: $id) {
      success
      message
    }
  }
`;

export const USER_CREATED_SUBSCRIPTION = gql`
  subscription OnUserCreated {
    userCreated {
      id
      name
      email
      createdAt
    }
  }
`;
```

---

## 6. Real-World Production Examples

### REST API Versioning Strategy

```javascript
// REST API Versioning
// File: server/app.js

// Version 1 - Original API
const v1Routes = require('./routes/v1');
// Version 2 - Breaking changes
const v2Routes = require('./routes/v2');

// Versioned routes
app.use('/api/v1', v1Routes);
app.use('/api/v2', v2Routes);

// Deprecation headers
app.use((req, res, next) => {
  if (req.path.startsWith('/api/v1')) {
    res.setHeader('X-API-Deprecated', 'true');
    res.setHeader('X-API-Migration-Guide', 'https://docs.myapp.com/v1-to-v2');
  }
  next();
});
```

### GraphQL Federation

```javascript
// GraphQL Federation for Microservices
// File: gateway/server.js
const { ApolloGateway } = require('@apollo/gateway');
const { ApolloServer } = require('apollo-server-express');
const express = require('express');

const gateway = new ApolloGateway({
  serviceList: [
    { name: 'users', url: 'http://localhost:4001/graphql' },
    { name: 'posts', url: 'http://localhost:4002/graphql' },
    { name: 'orders', url: 'http://localhost:4003/graphql' },
  ],
});

const server = new ApolloServer({
  gateway,
  subscriptions: false,
});

const app = express();
server.applyMiddleware({ app });

app.listen(4000, () => {
  console.log('Gateway ready at http://localhost:4000/graphql');
});
```

---

## 7. Debugging Guide

### REST API Debugging

```javascript
// Request logging middleware
const requestLogger = (req, res, next) => {
  const start = Date.now();
  
  debug(`--> ${req.method} ${req.url}`);
  debug(`Headers: ${JSON.stringify(req.headers)}`);
  debug(`Body: ${JSON.stringify(req.body)}`);
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    debug(`<-- ${req.method} ${req.url} ${res.statusCode} (${duration}ms)`);
  });
  
  next();
};

// Response body logging
const responseLogger = (req, res, next) => {
  const originalJson = res.json;
  
  res.json = function(body) {
    debug(`Response: ${JSON.stringify(body)}`);
    return originalJson.call(this, body);
  };
  
  next();
};
```

### GraphQL Debugging

```javascript
// GraphQL request logging
const loggingPlugin = {
  async requestDidStart({ request, queryString, variables }) {
    console.log('GraphQL Query:', queryString);
    console.log('Variables:', variables);
    
    return {
      async didResolveOperation({ operationName }) {
        console.log('Operation:', operationName);
      },
      async willSendResponse({ response }) {
        console.log('Response:', JSON.stringify(response));
      },
    };
  },
};

// Use in Apollo Server
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [loggingPlugin],
});
```

---

## 8. Tradeoffs

### REST vs GraphQL Comparison

| Aspect | REST | GraphQL |
|--------|------|---------|
| **Over-fetching** | Common (get all fields) | Eliminated (ask for what you need) |
| **Under-fetching** | Multiple requests | Single request |
| **Caching** | HTTP caching | Custom caching |
| **Documentation** | Manual/OpenAPI | Auto-generated |
| **Error handling** | HTTP status codes | Structured errors |
| **File uploads** | Native | Requires extra setup |
| **Learning curve** | Easy | Moderate |
| **Tooling** | Mature | Growing |
| **Security** | Well-understood | Must be careful (query depth) |
| **Performance** | Good for simple APIs | Can be slower (flexibility cost) |

---

## 9. Security Concerns

### REST API Security

```javascript
// Security middleware
const securityMiddleware = [
  // Rate limiting
  rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
  }),
  
  // Input validation
  expressValidator([
    body('email').isEmail(),
    body('password').isLength({ min: 8 }),
  ]),
  
  // CORS
  cors({
    origin: process.env.ALLOWED_ORIGINS.split(','),
    credentials: true,
  }),
  
  // Helmet
  helmet(),
  
  // SQL injection prevention
  // Use parameterized queries (handled by Prisma)
];

// Prevent mass assignment
const safeUpdate = (data, allowedFields) => {
  return Object.keys(data)
    .filter(key => allowedFields.includes(key))
    .reduce((obj, key) => ({ ...obj, [key]: data[key] }), {});
};
```

### GraphQL Security

```javascript
// GraphQL Security
const { makeExecutableSchema } = require('@graphql-tools/schema');
const { costAnalysisPlugin } = require('@graphql-inspector/graphql-cost-analysis');

const schema = makeExecutableSchema({
  typeDefs,
  resolvers,
});

// Validation rules
const { createComplexityLimitRule } = require('graphql-complexity');

const complexityLimitRule = createComplexityLimitRule(schema, {
  maxComplexity: 1000,
  onCost: (cost) => console.log('Query cost:', cost),
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [complexityLimitRule],
  plugins: [
    costAnalysisPlugin({
      maxCost: 1000,
    }),
  ],
});

// Query depth limiting
const { depthLimit } = require('graphql-depth-limit');
const depthRule = depthLimit(10);

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthRule],
});
```

---

## 10. Performance Optimization

### REST Performance

```javascript
// Response caching
const cacheMiddleware = (ttl = 60) => {
  const cache = new Map();
  
  return (req, res, next) => {
    const key = `${req.method}:${req.originalUrl}`;
    const cached = cache.get(key);
    
    if (cached && Date.now() - cached.timestamp < ttl * 1000) {
      return res.json(cached.data);
    }
    
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      cache.set(key, { data, timestamp: Date.now() });
      return originalJson(data);
    };
    
    next();
  };
};

// Pagination
const paginatedResponse = (page = 1, limit = 10) => ({
  skip: (page - 1) * limit,
  take: limit,
});

// ETag support
app.set('etag', true);
app.use((req, res, next) => {
  res.sendFile = (path, options, callback) => {
    // Add ETag based on file hash
    // Compare with If-None-Match header
    // Return 304 if matches
  };
  next();
});
```

### GraphQL Performance

```javascript
// DataLoader for N+1 problem
const DataLoader = require('dataloader');

const userLoader = new DataLoader(async (ids) => {
  const users = await prisma.user.findMany({
    where: { id: { in: ids } },
  });
  
  const userMap = new Map(users.map(u => [u.id, u]));
  return ids.map(id => userMap.get(id));
});

// In resolver
User: {
  posts: async (parent, args, { userLoader }) => {
    return userLoader.load(parent.id);
  },
}

// Persisted queries
const { ApolloServerPluginLandingPageProductionDefault } = require('apollo-server-core');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginLandingPageProductionDefault({
      embed: {
        endpointIsEditable: false,
      },
    }),
  ],
});
```

---

## 11. Scaling Challenges

### REST Scaling

```javascript
// Horizontal scaling with Redis session store
const session = require('express-session');
const RedisStore = require('connect-redis').default;

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    httpOnly: true,
    maxAge: 1000 * 60 * 60 * 24, // 1 day
  },
}));

// Database connection pooling
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### GraphQL Scaling

```javascript
// Query caching
const { responseCachePlugin } = require('apollo-server-plugin-response-cache');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    responseCachePlugin({
      cacheControl: {
        defaultMaxAge: 60,
        stripFormattedExtensions: false,
        calculateHttpHeaders: true,
      },
    }),
  ],
});

// Persisted queries stored in Redis
const { PersistedQueryRegistry } = require('apollo-server-core');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    cache: new RedisForLiveQueries(),
  },
});
```

---

## 12. Best Practices

### REST Best Practices

```markdown
# REST API Best Practices

1. Use nouns for resources: GET /users, not GET /getUsers
2. Use plural names: /users not /user
3. Use HTTP methods correctly:
   - GET: Read
   - POST: Create
   - PUT: Full replace
   - PATCH: Partial update
   - DELETE: Remove
4. Use query parameters for filtering: /users?role=admin
5. Use path parameters for resources: /users/:id
6. Return proper status codes:
   - 200: Success
   - 201: Created
   - 400: Bad request
   - 401: Unauthorized
   - 403: Forbidden
   - 404: Not found
   - 500: Server error
7. Version your API: /api/v1/users
8. Use pagination: ?page=1&limit=10
9. Include metadata in responses
10. Secure all endpoints
```

### GraphQL Best Practices

```markdown
# GraphQL Best Practices

1. Design schema first - think about client needs
2. Use connections for pagination
3. Name mutations with verb prefix: createUser, updateUser
4. Use input types for mutations
5. Implement proper error handling
6. Use DataLoader to prevent N+1 queries
7. Set complexity limits
8. Implement query depth limits
9. Use persisted queries for production
10. Monitor query performance
11. Cache at multiple levels
12. Document your schema
```

---

## 13. Common Mistakes

### REST Mistakes

```javascript
// MISTAKE 1: Using verbs instead of nouns
// BAD
app.get('/getUsers')
app.post('/createUser')
app.post('/updateUser')

// GOOD
app.get('/users')
app.post('/users')
app.patch('/users/:id')

// MISTAKE 2: Not using proper status codes
// BAD - 200 for everything
res.status(200).json({ error: 'Not found' });

// GOOD
res.status(404).json({ error: 'Not found' });

// MISTAKE 3: Exposing sensitive data
// BAD
res.json(user); // includes password!

// GOOD
res.json({
  id: user.id,
  name: user.name,
  email: user.email,
});
```

### GraphQL Mistakes

```javascript
// MISTAKE 1: N+1 queries
// BAD - queries inside loop
const resolvers = {
  User: {
    posts: async (parent) => {
      return Promise.all(parent.map(u => getPostsForUser(u.id)));
    },
  },
};

// GOOD - use DataLoader
const resolvers = {
  User: {
    posts: async (parent, args, { userLoader }) => {
      return userLoader.loadMany(parent.id);
    },
  },
};

// MISTAKE 2: No query complexity limits
// Can lead to expensive queries
const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(10), createComplexityLimitRule(schema, { maxComplexity: 1000 })],
});

// MISTAKE 3: Exposing sensitive fields
// BAD
type User {
  password: String!
  apiKey: String!
}

// GOOD - exclude sensitive fields
type User {
  id: ID!
  name: String!
  email: String!
}
```

---

## 14. Interview Questions

### API Design Interview Q&A

```markdown
Q1: What is the difference between PUT and PATCH?
A: PUT is for full resource replacement - send complete object.
   PATCH is for partial updates - send only fields to update.

Q2: How do you handle authentication in REST vs GraphQL?
A: REST: Usually in headers (Bearer token) or cookies.
   GraphQL: Same, but can also pass in context.

Q3: What is the N+1 problem in GraphQL?
A: When fetching list of items, resolver runs once per item.
   Solution: Use DataLoader to batch and cache requests.

Q4: How do you implement pagination in REST vs GraphQL?
A: REST: offset/limit or cursor-based in query params.
   GraphQL: Connections pattern with cursor-based pagination.

Q5: What is idempotency?
A: Same request produces same result. GET, PUT, DELETE are idempotent.
   POST and PATCH are not necessarily idempotent.

Q6: When would you choose REST over GraphQL?
A: When you need simple CRUD, HTTP caching, public APIs,
   or when team is more familiar with REST patterns.

Q7: How do you secure a GraphQL API?
A: Implement query complexity limits, depth limits,
   rate limiting, authentication, authorization, and input validation.
```

---

## 15. Latest 2026 Fullstack Engineering Patterns

### Modern API Patterns 2026

```typescript
// 1. tRPC - Type-safe APIs without GraphQL
// File: server/trpc.ts
import { initTRPC } from '@trpc/server';
import { z } from 'zod';

const t = initTRPC.create();

export const appRouter = t.router({
  user: t.router({
    getAll: t.procedure
      .input(z.object({
        page: z.number().optional(),
        limit: z.number().optional(),
      }))
      .query(async ({ input }) => {
        return prisma.user.findMany({
          take: input.limit || 10,
          skip: ((input.page || 1) - 1) * (input.limit || 10),
        });
      }),
    
    create: t.procedure
      .input(z.object({
        name: z.string().min(2),
        email: z.string().email(),
      }))
      .mutation(async ({ input }) => {
        return prisma.user.create({ data: input });
      }),
  }),
});

export type AppRouter = typeof appRouter;

// File: client/src/api/trpc.ts
import { createTRPCClient, httpBatchLink } from '@trpc/client';
import { AppRouter } from '../server/trpc';

export const trpc = createTRPCClient<AppRouter>({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000/trpc',
    }),
  ],
});

// Usage
const users = await trpc.user.getAll.query({ page: 1 });
await trpc.user.create.mutate({ name: 'John', email: 'john@example.com' });
```

```python
# 2. Hono - Lightweight framework for any runtime
from fastapi import FastAPI
from hono import Honoz

app = Honoz()

@app.get("/users")
async def get_users():
    return {"users": [...]}

@app.post("/users")
async def create_user(data: UserCreate):
    return {"id": "123", **data.model_dump()}
```

```typescript
// 3. gRPC for microservices communication
// protocol buffer
syntax = "proto3";

service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (ListUsersResponse);
  rpc CreateUser (CreateUserRequest) returns (User);
}

message GetUserRequest {
  string id = 1;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
}
```

```typescript
// 4. OpenAPI with FastAPI - auto-generated docs
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    description="Production API with OpenAPI spec",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users", response_model=list[User])
async def get_users():
    """Get all users"""
    return [...]

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user"""
    return {...}
```

---

## Summary

Bhai, REST aur GraphQL dono apne scenarios mein best hain:

1. **REST** - Simple, standard, HTTP caching, easy to understand
2. **GraphQL** - Flexible, no over/under-fetching, great for complex UIs
3. **tRPC** - Type-safe without GraphQL complexity (2026 trend)
4. **gRPC** - Best for microservice-to-microservice communication

Choose based on:
- Team expertise
- Client requirements
- API complexity
- Caching needs
- Performance requirements

---

*Previous: [Express and FastAPI](./Express_and_FastAPI.md) | Next: [Backend Architecture](./Backend_Architecture.md)*
