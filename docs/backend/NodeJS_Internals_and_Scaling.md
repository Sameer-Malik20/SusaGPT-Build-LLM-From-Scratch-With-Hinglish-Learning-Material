# ⚙️ Node.js Internals & Scaling — The Event Loop Deep Dive
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master Node.js Lifecycle, Libuv, Streams, Buffers, Cluster, Worker Threads, and High-Throughput performance.

---

## 📋 Table of Contents: Node's Brain

| Layer | Topic | Why? |
|-------|-------|------|
| **1. Runtime** | V8 + Libuv Architecture | JS ko machine code aur I/O mein badalne ka raaz. |
| **2. Event Loop** | Phases (Timers, I/O, Poll, Check) | 10,000 requests per second handle karna. |
| **3. Memory** | Buffers & Streams | Heavy data (Movies/PDFs) bina RAM crash khupaye padhna. |
| **4. Concurrency** | Cluster & Worker Threads | Multi-core CPU ka poora fayda uthana. |
| **5. Caching** | Module Caching & Node Cache | बार-बार computation se bachna. |
| **6. Micro-Services**| Event-Driven (EventEmitter) | Services ka internal talk logic. |

---

## 🏗️ 1. Node.js Anatomy (The Stack)

Node.js sirf JS nahi hai, woh 3 cheezon se milkar bana hai:
1. **V8 (Chrome Engine):** JS code ko optimize machine code mein badalta hai.
2. **Libuv (C++ Library):** Ye asynchronous I/O (File, Network, Database) handle karta hai. (Event Loop isi mein hai).
3. **C++ Bindings:** V8 aur Libuv ko JS ke saath jodne wala bridge.

---

## 🔄 2. The 6 Phases of Event Loop (Interview Most Asked)

Agar aapko lagta hai `setTimeout` or `setImmediate` same hain, toh aap galat ho.

1. **Timers:** `setTimeout` aur `setInterval` ke callbacks execute hote hain.
2. **Pending Callbacks:** System notifications (I/O errors).
3. **Idle, Prepare:** Internally used for cleanup.
4. **Poll (DIL):** Jahan database requests, network responses read hoti hain. Node yahan "Insaani" wait karta hai responses milne tak.
5. **Check:** `setImmediate` ke callbacks yahan run hote hain.
6. **Close Callbacks:** `socket.on('close')`, etc.

---

## 🛤️ 3. Streams & Buffers (Heavy Data)

- **Buffer:** Ek finite memory space jo raw data bytes mein store karta hai.
- **Streams:** Data ko chote-chote chunks mein padhna aur bhejnah. (Best for 1GB File upload/download).
  - Types: Readable, Writable, Duplex, Transform (e.g., Zlib for compression).

```javascript
// Stream example (Memory efficient)
const fs = require('fs');
const readable = fs.createReadStream('./big_file.mp4');
const writable = fs.createWriteStream('./copy.mp4');
readable.pipe(writable); // 8GB file copy on 512MB RAM!
```

---

## 🚀 4. Scaling: Cluster vs Worker Threads

Nodejs default single threaded hai.
- **Cluster Module:** Ye OS ke **Multiple CPU Cores** par app ke clones (Child Processes) banata hai.
  - Usage: Incoming HTTP requests ko parallelly handle karne ke liye.
- **Worker Threads:** Ek hi process ke andar naya thread/worker banana heavy calculation (e.g. AI logic, Math) ke liye.

---

## 🛡️ 5. Memory Management: Garbage Collection

Node memory limits par chalta hai (`--max-old-space-size`).
- **Memory Leaks:** Jab aap global variables mein data dhalte jate ho aur woh kabhi khali nahi hote. (Heap out of memory).
- **Heap Snapshot:** Chrome DevTools se Node process ko "Inspect" karke leaks dhundna.

---

## 🧪 Quick Test — Node Senior Backend Level!

### Q1: `nextTick` vs `setImmediate`?
- **process.nextTick:** Current phase ke turant baad (Priority 1).
- **setImmediate:** Agle Event Loop (Check phase) mein (Priority 2).

### Q2: Why Node over Go/Java for I/O?
**Answer:** Node ki asynchronous nature (I/O non-blocking) I/O tasks (e.g., API requests) mein faster response deti hai kam resources (RAM) par compared to thread-per-request model of old Java/PHP.

---

## 🏆 Final Summary Checklist
- [ ] Libuv event loop phases ka order kya hai?
- [ ] Streams memory leak se kaise bachate hain?
- [ ] Cluster module multi-core CPU handle kaise karta hai?
- [ ] Buffer `slice` vs `copy` (Optimization).

> **Node Tip:** Never block the main thread. Agar loop mein 1 Million calculations karoge, toh poori app down ho jayegi. Calculation ke liye Workers use karo!
