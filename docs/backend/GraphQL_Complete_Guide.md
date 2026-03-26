# 📊 GraphQL Complete Guide
> **Level:** Intermediate | **Language:** Hinglish | **Goal:** Master GraphQL with Apollo

---

## 🧭 Core Concepts (Concept-First)

- GraphQL Basics: Query, Mutation, Subscription
- Schema Definition
- Resolvers
- Apollo Server

---

## 1. 🔍 GraphQL Basics

```typescript
// Schema
type Query {
  users: [User!]!
  user(id: ID!): User
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}

type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}
```

---

## 2. 🎯 Resolvers

```typescript
const resolvers = {
  Query: {
    users: () => db.users.findAll(),
    user: (_, { id }) => db.users.findById(id),
  },
  Mutation: {
    createUser: (_, { input }) => db.users.create(input),
  },
  User: {
    posts: (parent) => db.posts.findByUserId(parent.id),
  },
};
```

---

## 3. 🚀 Apollo Server Setup

```typescript
import { ApolloServer, gql } from '@apollo/server';

const typeDefs = gql`
  type Query {
    hello: String
  }
`;

const resolvers = {
  Query: {
    hello: () => 'Hello World!',
  },
};

const server = new ApolloServer({ typeDefs, resolvers });
await server.start();
```

---

## ✅ Checklist

- [ ] GraphQL schema define kar sakte ho
- [ ] Resolvers implement kar sakte ho
- [ ] Apollo Server setup kar sakte ho