# 🎨 Frontend Engineering Lab: High-Performance UIs

Bhai, ye lab aapko ek basic React developer se ek **Frontend Architect** banne mein madad karegi. Har exercise production concepts par based hai.

---

## 🛠️ Exercise 1: The "Perf-First" Component
**Problem Statement:**
Ek aisi `HugeList` component banao jo 10,000 items render kare bina browser ko hang kiye.

**Tasks:**
1. Use `React.memo` properly.
2. Implement **Windowing** (Virtual Scrolling) using `react-window` or a custom implementation.
3. Profile the component using React DevTools.

---

## 🚀 Exercise 2: Next.js App Router Mastery
**Problem Statement:**
Ek "Product Dashboard" banao jo:
1. **Server Components** use kare data fetching ke liye.
2. **Streaming** (using `Suspense`) use kare skeletons dikhane ke liye jab data load ho raha ho.
3. **Server Actions** use kare product price update karne ke liye with optimistic UI.

---

## 📊 Exercise 3: State Management Showdown
**Problem Statement:**
Ek "Shopping Cart" banao.
1. Use **Zustand** for global cart state.
2. Use **React Query** for fetching product list and handling "Stale" data.
3. Compare the "Developer Experience" and bundle size.

---

## ♿ Exercise 4: Accessibility (a11y) Audit
**Problem Statement:**
Aapko ek "Login Form" diya gaya hai jisme sirf `<div onclick=...>` use hua hai buttons ke liye.
1. Use Semantic HTML (`<form>`, `<button>`, `<label>`).
2. Add `aria-labels` and `aria-live` regions for error messages.
3. Test using only your keyboard.

---

## 🎨 Exercise 5: CSS Mastery (Responsive & Glass)
**Problem Statement:**
Ek "Hero Section" design karo jo:
1. **Glassmorphism** effect use kare.
2. Fully responsive ho (Mobile, Tablet, Desktop) using **CSS Grid** (not just flex).
3. Smooth **Micro-animations** ho jab user buttons par hover kare.

---

## ❓ Interview Scenarios
1. "How would you optimize a Next.js app with a LCP (Largest Contentful Paint) of 5 seconds?"
2. "Explain the React Fiber reconciliation process in simple terms."
3. "Why would you choose Server Components over Client Components for a blog page?"

---
*Ready to build? Start coding in your local IDE!*
