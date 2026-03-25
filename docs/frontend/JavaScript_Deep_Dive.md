# 📜 JavaScript Deep Dive — The Runtime Internals (Expert Guide)
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master every engine part from Call Stack to Event Loop, Memory Management, and Modern APIs.

---

## 📋 Table of Contents: The JS Core

| Pillar | Topic | What you'll learn? |
|--------|-------|--------------------|
| **1. Mechanics**| Execution Context & Scopes | How JS runs your code line by line. |
| **2. Engines** | Call Stack, Heap & V8 | Inside Chrome/Node's brain. |
| **3. Async** | Event Loop, Macro vs Micro tasks | Why `setTimeout` is not 100% accurate. |
| **4. Prototypes**| Prototypal Inheritance | Creating objects without classes (The OG way). |
| **5. Patterns** | Closures & Higher-Order Functions| Encapsulation and pure functions. |
| **6. Modern** | ES6 to ES2024 (ESNext) | Destructuring, Proxies, Symbols, Nullish coalescing. |

---

## 1. 🏗️ Execution Context: How JS Starts

Har JS code pehle ek **Global Execution Context** mein jata hai. Context ke do parts hote hain:
1. **Memory Component (Variable Environment):** Jahan saare variables `undefined` stored hote hain (Hoisting).
2. **Code Component (Thread of Execution):** Jahan code line-by-line run hota hai.

> 💡 **Mnemonic:** **H-E-C** (Hoisting, Execution, Context). Hoisting memory mein variables pehle hi book kar leta hai.

---

## 2. 🧠 V8 Engine: Call Stack & Heap

Chrome ka **V8 Engine** JS ko machine code mein badalta hai (JIT - Just In Time).
- **Call Stack:** Jahan current functions execute hote hain (LIFO order).
- **Memory Heap:** Jahan bade objects aur arrays store hote hain (Memory storage).
- **Stack Overflow:** Jab recursion bina limit ke chale aur stack bhar jaye.

---

## 🔄 3. The Event Loop: Async Secrets

JS single-threaded hai. Toh hum database calls ya timers kaise handle karte hain? Using **Web APIs** and the **Event Loop**.

### The Hierarchy of Tasks:
1. **Call Stack:** Primary focus.
2. **Micro-task Queue:** `.then()`, `async/await`, `mutationObserver`. (High priority).
3. **Macro-task Queue:** `setTimeout`, `setInterval`, `UI Rendering`. (Low priority).

> 🧩 **Deep Logic:** Event loop sirf tabhi Micro-task ya Macro-task uthaega jab **Call Stack khali** hoga.

---

## 🎯 4. Closures & Scope Chain

Ek function ke andar doosra function apni **Lexical Environment** yaad rakhta hai, chahe woh bahar run ho raha ho.
- **Use Case:** Private variables banana jise koi bahar se change na kar sake.

```javascript
function counter() {
  let count = 0;
  return function() {
    count++;
    console.log(count);
  };
}
const myCounter = counter();
myCounter(); // 1
myCounter(); // 2
```

---

## 🧬 5. Prototypes: Classes are just Sugar

JS mein everything is an **Object**. Har object ka ek `[[Prototype]]` hota hai. Jab aap kisi property ko call karte ho, JS use pehle object mein, phir uske prototype mein, aur phir pure chain up to `null` search karta hai.

---

## 🚀 6. Modern Javascript (The Pro Level)

Aapko latest JS pata honi chahiye production ke liye:
- **Nullish Coalescing (`??`):** `0` ya `""` ko `null` na maanna.
- **Optional Chaining (`?.`):** `data?.user?.id` (No crashes).
- **Proxies:** Objects ke get/set handler ko intercept karna.
- **Async/Await:** Promises ko readable sync style mein likhna.

---

## 🧪 Quick Test — JS Interview Master Class!

### Q1: `undefined` vs `not defined` vs `null`?
- **undefined:** Memory allocated hai par value nahi di (`let a;`).
- **not defined:** variable declare hi nahi kiya (`console.log(x);`).
- **null:** Humne intentionally value khali set ki hai.

### Q2: Why is `typeof null` an object?
**Answer:** Ye JS language ka ek purana "Bug" hai jo ab legacy support ke liye change nahi kiya gaya.

---

## 🔗 Resources
- [You Don't Know JS (Book Series)](https://github.com/getify/You-Dont-Know-JS)
- [Namaste JavaScript (Akshay Saini)](https://www.youtube.com/playlist?list=PLLasX_NVZKNWcXp_ndHmxid9IduKox9k2)
- [MDN Web Docs - JS Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

---

## 🏆 Summary Checklist
- [ ] Call Stack overflow kaise hota hai?
- [ ] Micro-task queue vs Macro-task queue priority.
- [ ] Closure memory leaks se kaise bachein?
- [ ] 'this' keyword different contexts mein kaise react karta hai?

> **JS Expert Tip:** Engine ko samajho, syntax toh GPT bhi likh lega. Agar internals pata hain, toh debugging 10x fast hogi.
