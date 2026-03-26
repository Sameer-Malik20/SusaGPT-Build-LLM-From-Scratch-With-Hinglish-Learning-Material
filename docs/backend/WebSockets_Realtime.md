# 💬 WebSockets & Real-time Architecture
> **Level:** Intermediate | **Language:** Hinglish | **Goal:** Master real-time communication

---

## 🧭 Core Concepts (Concept-First)

- WebSocket Basics: Connection lifecycle
- Socket.io: Events, rooms
- Real-time patterns

---

## 1. 🔌 WebSocket Basics

```javascript
// Server - ws library
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('Client connected');
  
  ws.on('message', (message) => {
    console.log('Received:', message);
    ws.send('Hello from server!');
  });
  
  ws.send('Welcome!');
});
```

---

## 2. 📡 Socket.io

```javascript
// Server
const io = require('socket.io')(server);

io.on('connection', (socket) => {
  // Join room
  socket.join('room-1');
  
  // Send to room
  io.to('room-1').emit('event', data);
  
  // Send to client
  socket.emit('response', data);
  
  // Handle event
  socket.on('chat message', (msg) => {
    io.emit('chat message', msg);
  });
});
```

---

## ✅ Checklist

- [ ] WebSocket implement kar sakte ho
- [ ] Socket.io use kar sakte ho