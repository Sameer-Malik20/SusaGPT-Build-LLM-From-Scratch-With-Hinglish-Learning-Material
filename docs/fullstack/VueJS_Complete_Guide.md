# 🖼️ Vue.js Complete Guide - Modern Frontend Framework

> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master Vue 3 with Composition API, Pinia, and real-world patterns.

---

## 🧭 Core Concepts (Concept-First)

- Vue 3 Fundamentals: Reactivity, components, templates
- Composition API: Script setup, refs, computed, watchers
- State Management: Pinia, stores, persistence
- Routing: Vue Router, navigation guards
- Component Patterns: Props, events, slots, provide/inject

---

## 📋 Complete Guide

### 1️⃣ Vue 3 Fundamentals

**Reactivity System:**
Vue 3 ka reactivity system ref aur reactive se kaam karta hai.
- `ref()` - Primitive values ke liye (numbers, strings)
- `reactive()` - Objects aur arrays ke liye
- `computed()` - Derived state ke liye

```javascript
import { ref, computed } from 'vue'

const count = ref(0)
const double = computed(() => count.value * 2)
```

**Template Syntax:**
- Directives: `v-if`, `v-for`, `v-bind`, `v-on`
- Event handling: `@click`, `@input`
- Two-way binding: `v-model`

### 2️⃣ Composition API Deep Dive

**Script Setup:**
```vue
<script setup>
import { ref, onMounted } from 'vue'

const name = ref('')
const items = ref([])

onMounted(() => {
  console.log('Component mounted!')
})
</script>
```

**Reusability with Composables:**
```javascript
// useMouse.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useMouse() {
  const x = ref(0)
  const y = ref(0)
  
  function update(e) {
    x.value = e.pageX
    y.value = e.pageY
  }
  
  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))
  
  return { x, y }
}
```

### 3️⃣ Pinia State Management

**Store Definition:**
```javascript
// stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: '',
    email: '',
    isLoggedIn: false
  }),
  getters: {
    displayName: (state) => state.name || 'Guest'
  },
  actions: {
    async login(credentials) {
      // API call here
      this.isLoggedIn = true
    },
    logout() {
      this.isLoggedIn = false
    }
  }
})
```

**Component me Use:**
```vue
<script setup>
import { useUserStore } from '@/stores/user'

const user = useUserStore()
</script>

<template>
  <h1>{{ user.displayName }}</h1>
</template>
```

### 4️⃣ Vue Router Patterns

**Route Configuration:**
```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    // Check auth
  }
  next()
})
```

### 5️⃣ Component Patterns

**Props Validation:**
```vue
<script setup>
defineProps({
  title: String,
  count: {
    type: Number,
    required: true,
    default: 0
  },
  items: {
    type: Array,
    default: () => []
  }
})
</script>
```

**Slots & Scoped Slots:**
```vue
<!-- BaseCard.vue -->
<template>
  <div class="card">
    <header>
      <slot name="header"></slot>
    </header>
    <main>
      <slot></slot>
    </main>
  </div>
</template>

<!-- Usage -->
<BaseCard>
  <template #header>My Title</template>
  Content here
</BaseCard>
```

### 6️⃣ Performance Optimization

- **Lazy Loading:** Route-based code splitting
- **v-memo:** Template re-rendering optimization
- **keep-alive:** Component caching
- **Teleport:** Portal components for modals

---

## 🎯 Best Practices Checklist

- [ ] Use `<script setup>` for clean syntax
- [ ] Prefer Composition API over Options API
- [ ] Use Pinia for global state management
- [ ] Implement proper TypeScript types
- [ ] Use lazy loading for routes
- [ ] Implement proper error boundaries

---

## 🔗 Related Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [Pinia](https://pinia.vuejs.org/)
- [VueUse](https://vueuse.core.io/) - Composition utilities

---

> 💡 **Tip:** Vue 3 ka ecosystem bohot mature hai. VueUse library use karo for common patterns!