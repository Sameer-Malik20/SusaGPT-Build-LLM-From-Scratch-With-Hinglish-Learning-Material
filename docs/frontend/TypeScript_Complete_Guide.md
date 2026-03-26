# 💻 TypeScript Complete Guide
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master TypeScript from basics to advanced

---

## 🧭 Core Concepts (Concept-First)

- Types: Primitive, arrays, objects
- Interfaces & Types: Differences
- Generics: Reusable code
- Utility Types
- Advanced Patterns

---

## 1. 📝 Basic Types

```typescript
// Primitives
let name: string = "John";
let age: number = 25;
let isActive: boolean = true;

// Arrays
let numbers: number[] = [1, 2, 3];
let names: Array<string> = ["a", "b"];

// Objects
interface User {
  id: number;
  name: string;
  email?: string; // optional
}

const user: User = { id: 1, name: "John" };
```

---

## 2. 🔧 Interfaces vs Types

```typescript
// Interface - for objects
interface User {
  name: string;
  age: number;
}

// Type - for unions, primitives
type Status = "active" | "inactive";
type ID = string | number;
```

---

## 3. 🎯 Generics

```typescript
function identity<T>(arg: T): T {
  return arg;
}

// Generic interface
interface Container<T> {
  value: T;
  getValue(): T;
}

// Generic constraints
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(item: T): number {
  return item.length;
}
```

---

## 4. 🛠️ Utility Types

```typescript
// Partial - all optional
type PartialUser = Partial<User>;

// Required - all required
type RequiredUser = Required<User>;

// Pick - select fields
type UserPreview = Pick<User, "id" | "name">;

// Omit - exclude fields
type UserWithoutEmail = Omit<User, "email">;

// Record
type UserMap = Record<string, User>;
```

---

## 5. 🔒 Advanced Patterns

```typescript
// Union types
function process(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toString();
}

// Type guards
function isString(val: unknown): val is string {
  return typeof val === "string";
}

// Mapped types
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
```

---

## ✅ Checklist

- [ ] Basic types use kar sakte ho
- [ ] Interfaces vs Types distinguish kar sakte ho
- [ ] Generics implement kar sakte ho
- [ ] Utility types apply kar sakte ho