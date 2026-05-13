# Real-Time Backend - WebSockets, SSE, and Live Updates

Bhai, real-time features ajkal har application mein chahiye hote hain - chat apps, live notifications, collaborative editing, stock prices, aur bhi bahut kuch. Chalo detail mein samajhte hain ki real-time kaise implement karte hain!

---

## 1. Beginner-Friendly Hinglish Explanation

### Real-Time Kya Hai?

Soch jab tum WhatsApp pe message bhejte ho:
- Message jaldi se jaldi对面的 ko deliver hota hai
- Tumhein turant "Delivered" dikhta hai
- Jab对面 ne padha, "Seen" dikhta hai
- Ye sab real-time hai!

Real-time matlab ** turant communication** - jab kuch hota hai, turant sabko pata chal jata hai (without refreshing page).

### Traditional vs Real-Time

```
TRADITIONAL (Request-Response):
┌─────────┐         REQUEST          ┌─────────┐
│ Browser │ ───────────────────────> │ Server  │
│         │                            │         │
│         │ <─────────────────────── │         │
│         │          RESPONSE         │         │
└─────────┘                            └─────────┘
         │
         │ (User waits... no updates)
         │
         v
    User refreshes page for new data


REAL-TIME (Persistent Connection):
┌─────────┐         ┌─────────┐
│ Browser │ <══════>│ Server  │
│         │  WebSocket │         │
│         │  Connection │         │
│         │ <──────────│         │
│         │   LIVE DATA   │         │
│         │ <──────────│         │
│         │   LIVE DATA   │         │
└─────────┘            └─────────┘
     │
     │ Connection stays open
     │ Server can push anytime
     │
     v
   No page refresh needed!
```

### Real-Time Technologies

| Technology | Use Case | Pros | Cons |
|------------|----------|------|------|
| **WebSockets** | Chat, Gaming, Live Feeds | Full duplex, low latency | Complex, persistent connections |
| **Server-Sent Events (SSE)** | Notifications, Live Updates | Simple, automatic reconnection | One-way only |
| **Long Polling** | Fallback option | Works everywhere | Inefficient |
| **WebRTC** | Video/Audio calls | P2P possible | Complex setup |

---

## 2. Deep Technical Explanation

### WebSocket Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      WEBSOCKET ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    WEBSOCKET HANDSHAKE                       │   │
│  │                                                              │   │
│  │   Client                                              Server  │   │
│  │   ────                                              ───────   │   │
│  │   GET /ws                                              │       │   │
│  │   Upgrade: websocket                          │              │   │
│  │   Connection: Upgrade        ────────────────────────────────>│   │
│  │   Sec-WebSocket-Key: xxx     │              │              │   │
│  │                               │              │  101 Switch │   │
│  │                               │              │  Protocols   │   │
│  │                               │              │  ───────────>│   │
│  │   Connection: Upgrade         ────────────────────────────────│   │
│  │   (WebSocket established!)    │                              │   │
│  │                               │                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   WEBSOCKET FRAME FORMAT                      │   │
│  │                                                              │   │
│  │   ┌─────────────────────────────────────────────────────┐   │   │
│  │   │                 FIN | RSV1-3 | OPCODE | MASK        │   │   │
│  │   │                   1 byte                             │   │   │
│  │   ├─────────────────────────────────────────────────────┤   │   │
│  │   │                    MASK | LENGTH                    │   │   │
│  │   │                   1 byte                             │   │   │
│  │   ├─────────────────────────────────────────────────────┤   │   │
│  │   │                  EXTENDED LENGTH (if needed)        │   │   │
│  │   │                  0, 4, or 8 bytes                    │   │   │
│  │   ├─────────────────────────────────────────────────────┤   │   │
│  │   │                      MASKING KEY                    │   │   │
│  │   │                   4 bytes (if MASK=1)                │   │   │
│  │   ├─────────────────────────────────────────────────────┤   │   │
│  │   │                      PAYLOAD DATA                   │   │   │
│  │   │                   Up to 2^63 bytes                  │   │   │
│  │   └─────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │   OPCODE: 0x0=continuation, 0x1=text, 0x2=binary,          │   │
│  │           0x8=close, 0x9=ping, 0xA=pong                     │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Connection Management

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONNECTION MANAGEMENT                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐  │
│  │   Client 1  │         │   Client 2  │         │   Client 3  │  │
│  │  (User A)   │         │  (User B)   │         │  (User C)   │  │
│  └──────┬──────┘         └──────┬──────┘         └──────┬──────┘  │
│         │                       │                       │          │
│         └───────────────────────┼───────────────────────┘          │
│                                 │                                  │
│                    ┌────────────┴────────────┐                     │
│                    │     WebSocket Server    │                     │
│                    │                         │                     │
│                    │  ┌─────────────────┐   │                     │
│                    │  │ Connection Pool │   │                     │
│                    │  │                 │   │                     │
│                    │  │ ws:123 (User A) │   │                     │
│                    │  │ ws:124 (User B) │   │                     │
│                    │  │ ws:125 (User C) │   │                     │
│                    │  └─────────────────┘   │                     │
│                    │                         │                     │
│                    │  ┌─────────────────┐   │                     │
│                    │  │   Room Manager  │   │                     │
│                    │  │                 │   │                     │
│                    │  │ chat-room:1 -> [A, B]   │                     │
│                    │  │ chat-room:2 -> [A, C]   │                     │
│                    │  │ notification -> [A, B, C] │                │
│                    │  └─────────────────┘   │                     │
│                    └─────────────────────────┘                     │
│                                 │                                  │
│                    ┌────────────┴────────────┐                     │
│                    │       Message Router   │                     │
│                    │                        │                     │
│                    │  Broadcast to room    │                     │
│                    │  Direct message       │                     │
│                    │  System events        │                     │
│                    └────────────────────────┘                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Implementation

### Socket.IO Server Implementation

```javascript
// File: realtime/server.js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const jwt = require('jsonwebtoken');

const app = express();
const server = http.createServer(app);

// Socket.IO with full configuration
const io = new Server(server, {
  cors: {
    origin: ['http://localhost:3000', 'https://myapp.com'],
    methods: ['GET', 'POST'],
    credentials: true,
  },
  pingTimeout: 60000,      // Time to wait for pong
  pingInterval: 25000,     // Send ping every 25 seconds
  transports: ['websocket', 'polling'],  // Prefer websocket, fallback to polling
  allowEIO3: true,         // Support Engine.IO v3 clients
});

// Store connected users
const users = new Map();
const rooms = new Map();

// Authentication middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  
  if (!token) {
    return next(new Error('Authentication required'));
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.user = decoded;
    next();
  } catch (error) {
    next(new Error('Invalid token'));
  }
});

// File: realtime/connectionHandlers.js
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.user.id} (${socket.id})`);
  
  // Store user connection
  users.set(socket.user.id, {
    socketId: socket.id,
    userId: socket.user.id,
    username: socket.user.username,
    joinedAt: new Date(),
  });

  // Join user to their personal room
  socket.join(`user:${socket.user.id}`);

  // ──────────────────────────────────────────────
  // SOCKET EVENT HANDLERS
  // ──────────────────────────────────────────────

  // Handle joining chat rooms
  socket.on('join-room', async (roomId) => {
    // Verify user has access to room
    const hasAccess = await checkRoomAccess(socket.user.id, roomId);
    
    if (!hasAccess) {
      socket.emit('error', { message: 'Access denied to this room' });
      return;
    }

    // Leave previous rooms if any
    socket.rooms.forEach((room) => {
      if (room !== socket.id) {
        socket.leave(room);
      }
    });

    // Join new room
    socket.join(roomId);
    
    // Track room membership
    if (!rooms.has(roomId)) {
      rooms.set(roomId, new Set());
    }
    rooms.get(roomId).add(socket.user.id);

    // Notify room members
    socket.to(roomId).emit('user-joined', {
      userId: socket.user.id,
      username: socket.user.username,
      roomId,
      members: Array.from(rooms.get(roomId)),
    });

    // Send room info to joining user
    const roomMessages = await getRecentMessages(roomId, 50);
    socket.emit('room-history', {
      roomId,
      messages: roomMessages,
      members: Array.from(rooms.get(roomId)),
    });

    console.log(`User ${socket.user.username} joined room ${roomId}`);
  });

  // Handle leaving room
  socket.on('leave-room', (roomId) => {
    socket.leave(roomId);
    
    if (rooms.has(roomId)) {
      rooms.get(roomId).delete(socket.user.id);
    }

    socket.to(roomId).emit('user-left', {
      userId: socket.user.id,
      username: socket.user.username,
    });
  });

  // Handle chat messages
  socket.on('chat-message', async (data) => {
    const { roomId, content, type = 'text', attachments = [] } = data;

    // Validate message
    if (!content?.trim() || content.length > 5000) {
      socket.emit('error', { message: 'Invalid message content' });
      return;
    }

    // Create message
    const message = await createMessage({
      roomId,
      senderId: socket.user.id,
      senderName: socket.user.username,
      content: content.trim(),
      type,
      attachments,
    });

    // Broadcast to room
    io.to(roomId).emit('new-message', message);

    // Store in Redis for persistence
    await redis.lpush(`room:${roomId}:messages`, JSON.stringify(message));
    await redis.ltrim(`room:${roomId}:messages`, 0, 999); // Keep last 1000 messages

    // Handle mentions
    const mentions = extractMentions(content);
    for (const mentionedUser of mentions) {
      // Send notification to mentioned user
      io.to(`user:${mentionedUser}`).emit('mention-notification', {
        from: socket.user.username,
        message: message,
      });
    }
  });

  // Handle typing indicator
  socket.on('typing-start', (roomId) => {
    socket.to(roomId).emit('user-typing', {
      userId: socket.user.id,
      username: socket.user.username,
    });
  });

  socket.on('typing-stop', (roomId) => {
    socket.to(roomId).emit('user-stopped-typing', {
      userId: socket.user.id,
    });
  });

  // Handle direct messages
  socket.on('direct-message', async (data) => {
    const { recipientId, content } = data;

    const message = await createDirectMessage({
      senderId: socket.user.id,
      recipientId,
      content,
    });

    // Send to recipient (if online)
    io.to(`user:${recipientId}`).emit('new-direct-message', message);
    
    // Send confirmation to sender
    socket.emit('message-sent', message);
  });

  // Handle presence updates
  socket.on('update-presence', (status) => {
    const user = users.get(socket.user.id);
    user.status = status;

    // Broadcast to all connected users
    io.emit('presence-update', {
      userId: socket.user.id,
      status,
    });
  });

  // ──────────────────────────────────────────────
  // DISCONNECTION HANDLER
  // ──────────────────────────────────────────────
  
  socket.on('disconnect', async (reason) => {
    console.log(`User disconnected: ${socket.user.id} (${reason})`);

    // Remove from users map
    users.delete(socket.user.id);

    // Remove from all rooms
    for (const [roomId, members] of rooms.entries()) {
      if (members.has(socket.user.id)) {
        members.delete(socket.user.id);
        
        // Notify room
        io.to(roomId).emit('user-left', {
          userId: socket.user.id,
          username: socket.user.username,
        });

        // Clean up empty rooms
        if (members.size === 0) {
          rooms.delete(roomId);
        }
      }
    }

    // Broadcast offline status
    io.emit('presence-update', {
      userId: socket.user.id,
      status: 'offline',
    });
  });
});

// ──────────────────────────────────────────────
// UTILITY FUNCTIONS
// ──────────────────────────────────────────────

async function checkRoomAccess(userId, roomId) {
  // Check if user has access to this room
  const membership = await prisma.roomMember.findUnique({
    where: {
      userId_roomId: { userId, roomId },
    },
  });
  return !!membership;
}

async function createMessage(data) {
  return prisma.message.create({
    data: {
      roomId: data.roomId,
      senderId: data.senderId,
      content: data.content,
      type: data.type || 'text',
    },
    include: {
      sender: {
        select: { id: true, username: true, avatar: true },
      },
    },
  });
}

async function getRecentMessages(roomId, limit = 50) {
  const messages = await redis.lrange(`room:${roomId}:messages`, 0, limit - 1);
  return messages.map(m => JSON.parse(m)).reverse();
}

function extractMentions(content) {
  const mentionRegex = /@(\w+)/g;
  const matches = content.match(mentionRegex);
  return matches ? matches.map(m => m.slice(1)) : [];
}

// ──────────────────────────────────────────────
// START SERVER
// ──────────────────────────────────────────────

const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
  console.log(`Real-time server running on port ${PORT}`);
});
```

### Socket.IO Client Implementation

```typescript
// File: client/src/socket/socketClient.ts
import { io, Socket } from 'socket.io-client';
import { store } from '../store';
import { addMessage, setTyping, updatePresence } from '../store/chatSlice';

class SocketClient {
  private socket: Socket | null = null;
  private typingTimers: Map<string, NodeJS.Timeout> = new Map();

  connect(token: string) {
    if (this.socket?.connected) {
      console.log('Socket already connected');
      return;
    }

    this.socket = io(process.env.REACT_APP_WS_URL || 'ws://localhost:3001', {
      auth: { token },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 10,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
    });

    this.setupEventListeners();
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  private setupEventListeners() {
    if (!this.socket) return;

    // Connection events
    this.socket.on('connect', () => {
      console.log('Socket connected:', this.socket?.id);
      store.dispatch({ type: 'socket/connected' });
    });

    this.socket.on('disconnect', (reason) => {
      console.log('Socket disconnected:', reason);
      store.dispatch({ type: 'socket/disconnected' });
    });

    this.socket.on('connect_error', (error) => {
      console.error('Connection error:', error.message);
      store.dispatch({ type: 'socket/error', payload: error.message });
    });

    // ──────────────────────────────────────────
    // MESSAGE EVENTS
    // ──────────────────────────────────────────

    this.socket.on('room-history', ({ roomId, messages, members }) => {
      store.dispatch({
        type: 'chat/loadHistory',
        payload: { roomId, messages, members },
      });
    });

    this.socket.on('new-message', (message) => {
      store.dispatch(addMessage(message));
      
      // Play notification sound if not in the room
      if (!store.getState().chat.currentRoom?.id === message.roomId) {
        this.playNotificationSound();
      }
    });

    this.socket.on('message-sent', (message) => {
      store.dispatch(addMessage({ ...message, status: 'sent' }));
    });

    // ──────────────────────────────────────────
    // PRESENCE EVENTS
    // ──────────────────────────────────────────

    this.socket.on('user-joined', ({ userId, username, members }) => {
      store.dispatch(updatePresence({ userId, status: 'online' }));
    });

    this.socket.on('user-left', ({ userId }) => {
      store.dispatch(updatePresence({ userId, status: 'offline' }));
    });

    this.socket.on('presence-update', ({ userId, status }) => {
      store.dispatch(updatePresence({ userId, status }));
    });

    // ──────────────────────────────────────────
    // TYPING EVENTS
    // ──────────────────────────────────────────

    this.socket.on('user-typing', ({ userId, username }) => {
      store.dispatch(setTyping({ userId, username, isTyping: true }));
    });

    this.socket.on('user-stopped-typing', ({ userId }) => {
      store.dispatch(setTyping({ userId, isTyping: false }));
    });

    // ──────────────────────────────────────────
    // NOTIFICATION EVENTS
    // ──────────────────────────────────────────

    this.socket.on('mention-notification', ({ from, message }) => {
      store.dispatch({
        type: 'notifications/add',
        payload: {
          id: Date.now(),
          type: 'mention',
          from,
          message: message.content,
          roomId: message.roomId,
          createdAt: new Date(),
        },
      });
      this.playNotificationSound();
    });

    this.socket.on('new-direct-message', (message) => {
      store.dispatch(addMessage(message));
      if (!store.getState().chat.currentRoom?.id === message.roomId) {
        this.showBrowserNotification('New Message', message.content);
      }
    });
  }

  // ──────────────────────────────────────────
  // PUBLIC METHODS
  // ──────────────────────────────────────────

  joinRoom(roomId: string) {
    this.socket?.emit('join-room', roomId);
  }

  leaveRoom(roomId: string) {
    this.socket?.emit('leave-room', roomId);
  }

  sendMessage(roomId: string, content: string, type = 'text', attachments: string[] = []) {
    this.socket?.emit('chat-message', { roomId, content, type, attachments });
  }

  sendDirectMessage(recipientId: string, content: string) {
    this.socket?.emit('direct-message', { recipientId, content });
  }

  startTyping(roomId: string) {
    this.socket?.emit('typing-start', roomId);
  }

  stopTyping(roomId: string) {
    this.socket?.emit('typing-stop', roomId);
  }

  // Debounced typing
  handleTyping(roomId: string, text: string) {
    this.startTyping(roomId);

    const existingTimer = this.typingTimers.get(roomId);
    if (existingTimer) {
      clearTimeout(existingTimer);
    }

    const timer = setTimeout(() => {
      this.stopTyping(roomId);
      this.typingTimers.delete(roomId);
    }, 2000);

    this.typingTimers.set(roomId, timer);
  }

  updatePresence(status: 'online' | 'away' | 'busy' | 'offline') {
    this.socket?.emit('update-presence', status);
  }

  // ──────────────────────────────────────────
  // UTILITIES
  // ──────────────────────────────────────────

  private playNotificationSound() {
    const audio = new Audio('/notification.mp3');
    audio.volume = 0.5;
    audio.play().catch(() => {});
  }

  private showBrowserNotification(title: string, body: string) {
    if (Notification.permission === 'granted') {
      new Notification(title, { body, icon: '/icon.png' });
    }
  }
}

export const socketClient = new SocketClient();
```

### Server-Sent Events Implementation

```javascript
// File: realtime/sse.js
const express = require('express');
const router = express.Router();

// Store SSE connections
const clients = new Map();

// GET /api/notifications/stream - SSE endpoint
router.get('/stream', authenticate, async (req, res) => {
  // Set headers for SSE
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no'); // Disable nginx buffering

  // Send initial connection message
  res.write(`data: ${JSON.stringify({ type: 'connected', timestamp: Date.now() })}\n\n`);

  // Keep connection alive with heartbeat
  const heartbeatInterval = setInterval(() => {
    res.write(`: heartbeat\n\n`);
  }, 30000);

  // Store client connection
  const clientId = req.user.id;
  clients.set(clientId, { res, heartbeatInterval });

  // Handle client disconnect
  req.on('close', () => {
    clearInterval(heartbeatInterval);
    clients.delete(clientId);
    console.log(`SSE client disconnected: ${clientId}`);
  });
});

// POST /api/notifications/broadcast - Broadcast to specific user
router.post('/send', authenticate, async (req, res) => {
  const { userId, event, data } = req.body;

  const client = clients.get(userId);
  if (client) {
    client.res.write(`data: ${JSON.stringify({ type: event, payload: data })}\n\n`);
  }

  res.json({ success: !!client });
});

// Broadcast to multiple users
router.post('/broadcast', authenticate, async (req, res) => {
  const { userIds, event, data } = req.body;

  let sent = 0;
  for (const userId of userIds) {
    const client = clients.get(userId);
    if (client) {
      client.res.write(`data: ${JSON.stringify({ type: event, payload: data })}\n\n`);
      sent++;
    }
  }

  res.json({ success: true, sent, total: userIds.length });
});

// Broadcast to all connected clients
function broadcastToAll(event, data) {
  for (const [clientId, client] of clients.entries()) {
    try {
      client.res.write(`data: ${JSON.stringify({ type: event, payload: data })}\n\n`);
    } catch (error) {
      console.error(`Failed to send to client ${clientId}:`, error);
      clients.delete(clientId);
    }
  }
}

// ──────────────────────────────────────────────
// SSE with specific streams
// ──────────────────────────────────────────────

const streams = new Map();

// GET /api/live/scores - Live sports scores
router.get('/scores', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const streamId = `scores:${Date.now()}`;
  const streamClients = streams.get('scores') || new Set();
  streamClients.add(res);
  streams.set('scores', streamClients);

  res.write(`data: ${JSON.stringify({ type: 'subscribed', stream: 'scores' })}\n\n`);

  req.on('close', () => {
    streamClients.delete(res);
  });
});

// Simulate live score updates
setInterval(() => {
  const scoreUpdate = {
    type: 'score-update',
    payload: {
      matchId: 'match-123',
      homeScore: Math.floor(Math.random() * 5),
      awayScore: Math.floor(Math.random() * 5),
      timestamp: Date.now(),
    },
  };

  const clients = streams.get('scores') || new Set();
  for (const res of clients) {
    try {
      res.write(`data: ${JSON.stringify(scoreUpdate)}\n\n`);
    } catch (error) {
      clients.delete(res);
    }
  }
}, 10000); // Update every 10 seconds

module.exports = router;
```

---

## 4. Frontend Integration

### React Hook for Real-Time

```typescript
// File: client/src/hooks/useSocket.ts
import { useEffect, useRef, useCallback } from 'react';
import { socketClient } from '../services/socket';
import { useDispatch, useSelector } from 'react-redux';

export function useSocket() {
  const dispatch = useDispatch();
  const { isConnected, user } = useSelector((state) => state.socket);
  const reconnectAttempts = useRef(0);

  useEffect(() => {
    // Connect when user is authenticated
    if (user?.token && !isConnected) {
      socketClient.connect(user.token);
    }

    // Disconnect on unmount
    return () => {
      socketClient.disconnect();
    };
  }, [user?.token, isConnected]);

  return {
    isConnected,
    joinRoom: socketClient.joinRoom.bind(socketClient),
    leaveRoom: socketClient.leaveRoom.bind(socketClient),
    sendMessage: socketClient.sendMessage.bind(socketClient),
    sendDirectMessage: socketClient.sendDirectMessage.bind(socketClient),
    handleTyping: socketClient.handleTyping.bind(socketClient),
    updatePresence: socketClient.updatePresence.bind(socketClient),
  };
}

// File: client/src/hooks/useRealtime.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { EventSourcePolyfill } from 'event-source-polyfill';

interface UseSSEOptions {
  url: string;
  token?: string;
  onMessage?: (data: any) => void;
  onError?: (error: Event) => void;
  enabled?: boolean;
}

export function useSSE({
  url,
  token,
  onMessage,
  onError,
  enabled = true,
}: UseSSEOptions) {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<Event | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!enabled || !url) return;

    const eventSource = new EventSourcePolyfill(url, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      heartbeatTimeout: 60000,
    });

    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      setIsConnected(true);
      setError(null);
    };

    eventSource.onmessage = (event) => {
      try {
        const parsedData = JSON.parse(event.data);
        setData(parsedData);
        onMessage?.(parsedData);
      } catch (e) {
        console.error('Failed to parse SSE data:', e);
      }
    };

    eventSource.onerror = (err) => {
      setError(err);
      setIsConnected(false);
      onError?.(err);

      // EventSource will auto-reconnect
    };

    return () => {
      eventSource.close();
      eventSourceRef.current = null;
    };
  }, [url, token, enabled]);

  const reconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      // The useEffect will reconnect
    }
  }, []);

  return { data, error, isConnected, reconnect };
}

// File: client/src/components/ChatRoom.tsx
import React, { useState, useEffect, useRef } from 'react';
import { useSocket } from '../hooks/useSocket';
import { useSelector, useDispatch } from 'react-redux';
import { sendMessage, setTyping } from '../store/chatSlice';

export function ChatRoom({ roomId }) {
  const dispatch = useDispatch();
  const { currentRoom, messages, typingUsers } = useSelector((state) => state.chat);
  const { joinRoom, leaveRoom, sendMessage, handleTyping } = useSocket();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const typingTimeoutRef = useRef<NodeJS.Timeout>();

  // Join room on mount
  useEffect(() => {
    if (roomId) {
      joinRoom(roomId);
    }
    return () => {
      if (roomId) {
        leaveRoom(roomId);
      }
    };
  }, [roomId]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle typing
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
    
    // Notify others that user is typing
    handleTyping(roomId, e.target.value);
  };

  // Send message
  const handleSend = () => {
    if (!input.trim()) return;
    
    sendMessage(roomId, input.trim());
    setInput('');
    
    // Stop typing indicator
    // Already handled by handleTyping timeout
  };

  // Handle Enter key
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-room">
      {/* Messages */}
      <div className="messages">
        {messages.map((message) => (
          <div key={message.id} className="message">
            <img src={message.sender.avatar} alt="" />
            <div className="message-content">
              <div className="message-header">
                <span className="sender">{message.sender.username}</span>
                <span className="time">{formatTime(message.createdAt)}</span>
              </div>
              <div className="text">{message.content}</div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Typing indicators */}
      {typingUsers.length > 0 && (
        <div className="typing-indicator">
          {typingUsers.map((u) => u.username).join(', ')} {typingUsers.length === 1 ? 'is' : 'are'} typing...
        </div>
      )}

      {/* Input */}
      <div className="message-input">
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Type a message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}
```

---

## 5. Real-World Production Examples

### Chat System Architecture

```javascript
// File: production/chatArchitecture.js
const chatSystemArchitecture = {
  components: {
    // WebSocket layer for real-time messaging
    websocketServer: {
      port: 3001,
      protocol: 'Socket.IO',
      features: ['rooms', 'namespaces', 'rooms'],
      maxConnections: 100000,
    },

    // SSE for notifications (simpler use case)
    sseServer: {
      port: 3002,
      protocol: 'SSE',
      features: ['single stream per user', 'reconnection'],
    },

    // Message broker for scalability
    messageBroker: {
      type: 'Redis Pub/Sub',
      channels: ['chat:*', 'notifications:*', 'presence:*'],
    },

    // Message storage
    messageStore: {
      type: 'PostgreSQL + Redis',
      hotStorage: 'Redis (recent messages)',
      coldStorage: 'PostgreSQL (older messages)',
    },

    // Presence management
    presenceService: {
      type: 'Redis',
      ttl: 60, // seconds
      updateInterval: 30, // seconds
    },
  },

  scalingStrategy: {
    // Horizontal scaling with Redis adapter
    socketIoAdapter: {
      type: 'Redis Adapter',
      setup: `
        const adapter = require('@socket.io/redis-adapter');
        const pubClient = createRedisClient();
        const subClient = createRedisClient();
        io.adapter(adapter(pubClient, subClient));
      `,
    },

    // Multiple WebSocket instances
    instances: [
      { id: 1, host: 'ws-1.internal', port: 3001 },
      { id: 2, host: 'ws-2.internal', port: 3001 },
      { id: 3, host: 'ws-3.internal', port: 3001 },
    ],

    // Load balancer
    loadBalancer: {
      type: 'HAProxy',
      algorithm: 'leastconn',
      healthCheck: '/health',
    },
  },
};
```

### Collaborative Editing (like Google Docs)

```javascript
// File: production/collaborativeEditor.js
const collaborativeEditor = {
  // WebSocket server for real-time sync
  websocketServer: {
    port: 3003,
    protocol: 'WebSocket',
    libraries: ['yjs', 'y-websocket', 'y-indexeddb'],
  },

  // CRDT (Conflict-free Replicated Data Type) for conflict resolution
  crdt: {
    library: 'Yjs',
    features: [
      'Automatic conflict resolution',
      'Offline support',
      'Efficient sync',
      'Awareness (cursor positions)',
    ],
  },

  // Document structure
  documentStructure: {
    // Main document content
    content: 'Y.Text',
    // Comments
    comments: 'Y.Map',
    // Presence awareness
    awareness: {
      user: 'string',
      cursor: 'number',
      color: 'string',
      name: 'string',
    },
  },

  // Sync strategy
  syncStrategy: {
    // Save interval
    saveInterval: 30000, // 30 seconds
    
    // Sync updates
    updateDebounce: 50, // ms
    
    // Awareness (cursor) update
    awarenessUpdateInterval: 100, // ms
    
    // Offline queue
    offlineQueue: true,
    maxOfflineTime: 86400000, // 24 hours
  },
};

// WebSocket handler for collaborative editing
const collaborativeSocketHandler = (socket) => {
  let doc = null;

  socket.on('document-open', async ({ documentId }) => {
    // Get or create document
    doc = await getOrCreateDocument(documentId);
    
    // Setup Yjs document
    const ydoc = new Y.Doc();
    
    // Connect to WebSocket provider
    const provider = new WebsocketProvider(
      'wss://yjs-server.example.com',
      documentId,
      ydoc
    );

    // Handle awareness (cursor, selection)
    const awareness = provider.awareness;
    
    awareness.setLocalStateField('user', {
      name: socket.user.username,
      color: getRandomColor(),
      cursor: null,
    });

    // Sync awareness to clients
    awareness.on('change', ({ added, updated, removed }) => {
      const users = Array.from(awareness.getStates().values());
      socket.emit('presence-update', { users });
    });

    // Handle document updates
    ydoc.on('update', (update, origin) => {
      if (origin !== socket.id) {
        socket.emit('document-update', { update: Y.encodeStateAsUpdate(ydoc) });
      }
    });

    // Apply pending updates
    socket.on('client-update', ({ update }) => {
      Y.applyUpdate(ydoc, new Uint8Array(update));
    });

    // Cleanup on disconnect
    socket.on('disconnect', () => {
      provider.disconnect();
      ydoc.destroy();
    });
  });
};
```

---

## 6. Failure Cases

### Common Real-Time Failures

```javascript
// FAILURE 1: Memory leaks from event listeners
// BAD - Not cleaning up listeners
function ChatRoom({ roomId }) {
  useEffect(() => {
    socket.on('message', handleMessage);
    socket.on('typing', handleTyping);
    socket.on('presence', handlePresence);
    // Listeners keep accumulating!
  }, []);

  return <div>...</div>;
}

// GOOD - Cleanup listeners
function ChatRoom({ roomId }) {
  useEffect(() => {
    const handleMessage = (msg) => { /* ... */ };
    const handleTyping = (data) => { /* ... */ };
    const handlePresence = (data) => { /* ... */ };

    socket.on('message', handleMessage);
    socket.on('typing', handleTyping);
    socket.on('presence', handlePresence);

    // Cleanup function
    return () => {
      socket.off('message', handleMessage);
      socket.off('typing', handleTyping);
      socket.off('presence', handlePresence);
    };
  }, [roomId]);

  return <div>...</div>;
}

// FAILURE 2: Connection storm on reconnect
// BAD - Too many reconnect attempts
socket.on('disconnect', () => {
  setInterval(() => {
    socket.connect(); // Flood of connections!
  }, 1000);
});

// GOOD - Exponential backoff
socket.on('disconnect', () => {
  let delay = 1000;
  const reconnect = () => {
    socket.connect();
    socket.once('connect_error', () => {
      delay = Math.min(delay * 2, 30000);
      setTimeout(reconnect, delay);
    });
  };
  reconnect();
});

// FAILURE 3: Missing heartbeat handling
// BAD - No ping/pong
const server = new Server(app);

// After some time, connection might be stale
// No way to detect!

// GOOD - Proper heartbeat
const server = new Server(app, {
  pingTimeout: 60000,
  pingInterval: 25000,
});

// Or manual heartbeat
const heartbeatInterval = setInterval(() => {
  if (socket.isActive) {
    socket.isActive = false;
    socket.emit('ping');
  } else {
    socket.disconnect();
  }
}, 30000);

socket.on('pong', () => {
  socket.isActive = true;
});

// FAILURE 4: Not handling offline state
// BAD - Assuming always online
socket.emit('message', data);
socket.emit('update', data);

// GOOD - Handle offline
async function sendWithFallback(data) {
  if (socket?.connected) {
    socket.emit('message', data);
  } else {
    // Store in local queue
    await localQueue.add(data);
  }
}
```

---

## 7. Debugging Guide

### WebSocket Debugging

```javascript
// File: debugging/socketDebug.js

// 1. Enable Socket.IO debug logging
// Start with: DEBUG=socket:* node server.js
const debug = require('debug');

const log = {
  connection: debug('socket:connection'),
  messages: debug('socket:messages'),
  errors: debug('socket:errors'),
  rooms: debug('socket:rooms'),
};

// 2. Connection logging
io.on('connection', (socket) => {
  log.connection(`New connection: ${socket.id} (${socket.handshake.address})`);
  log.connection(`Auth: ${JSON.stringify(socket.handshake.auth)}`);
  log.connection(`Query: ${JSON.stringify(socket.handshake.query)}`);

  socket.on('disconnect', (reason) => {
    log.connection(`Disconnected: ${socket.id} (${reason})`);
  });
});

// 3. Message logging middleware
io.use((socket, next) => {
  log.messages(`Incoming: ${socket.id}`, socket.handshake);
  next();
});

// 4. Event logging
socket.onAny((eventName, ...args) => {
  log.messages(`Event: ${eventName} from ${socket.id}`);
  log.messages(`Data: ${JSON.stringify(args)}`);
});

socket.on('new-message', (data) => {
  log.messages(`Message from ${socket.id}: ${data.content}`);
  
  // Log room info
  log.rooms(`Rooms: ${Array.from(socket.rooms)}`);
});

// 5. Error logging
socket.on('error', (error) => {
  log.errors(`Error for ${socket.id}: ${error.message}`);
  log.errors(error.stack);
});

// 6. Client-side debug
// In browser console:
/*
// Enable all Socket.IO debugging
localStorage.debug = '*';

// Or specific
localStorage.debug = 'socket.io-client:socket';

// Listen to all events
socket.on('new-message', (data) => {
  console.log('Message received:', data);
});
*/
```

### Performance Monitoring

```javascript
// File: debugging/performanceMonitor.js

// Track message latency
const messageLatency = new Map();

socket.on('chat-message', (data) => {
  const start = messageLatency.get(data.messageId);
  if (start) {
    const latency = Date.now() - start;
    console.log(`Message latency: ${latency}ms`);
    messageLatency.delete(data.messageId);
    
    // Alert if too slow
    if (latency > 1000) {
      console.warn(`Slow message delivery: ${latency}ms`);
    }
  }
});

// Track active connections
setInterval(() => {
  const stats = {
    totalConnections: io.engine.clientsCount,
    rooms: io.sockets.adapter.rooms.size,
    transport: Object.keys(io.engine.transport).length,
  };
  
  console.log('Server stats:', stats);
  
  // Alert if too many connections
  if (stats.totalConnections > 10000) {
    console.warn('High connection count!');
  }
}, 60000);

// Track message throughput
let messageCount = 0;
const startTime = Date.now();

setInterval(() => {
  const rate = messageCount / ((Date.now() - startTime) / 1000);
  console.log(`Messages per second: ${rate.toFixed(2)}`);
  messageCount = 0;
}, 1000);

socket.on('chat-message', () => {
  messageCount++;
});
```

---

## 8. Tradeoffs

### Real-Time Technology Comparison

| Feature | WebSockets | SSE | Long Polling | WebRTC |
|---------|------------|-----|--------------|--------|
| **Browser Support** | Excellent | Excellent | Universal | Good |
| **Server Complexity** | High | Low | Medium | Very High |
| **Connection Type** | Full Duplex | One-way | Half Duplex | P2P |
| **Firewall Friendly** | Sometimes | Yes | Yes | Sometimes |
| **Automatic Reconnect** | Manual | Built-in | Manual | Manual |
| **Binary Data** | Yes | No | Yes | Yes |
| **Scalability** | Complex | Easy | Medium | N/A |
| **Best For** | Chat, Games | Notifications | Fallback | Video |

### When to Use What

```javascript
// USE WEBSOCKETS when:
const websocketUseCases = [
  'Real-time chat applications',
  'Multiplayer games',
  'Collaborative editing (Google Docs)',
  'Live dashboards with frequent updates',
  'Trading platforms',
  'Video/audio calls',
];

// USE SSE when:
const sseUseCases = [
  'Live notifications',
  'News feeds',
  'Progress updates',
  'Simple real-time features',
  'When server needs to push to client only',
];

// USE POLLING when:
const pollingUseCases = [
  'Legacy browser support',
  'Simple features',
  'When WebSockets blocked',
  'Infrequent updates',
];

// USE WEBRTC when:
const webrtcUseCases = [
  'Video/audio calls',
  'P2P file sharing',
  'Real-time gaming',
  'Screen sharing',
];
```

---

## 9. Security Concerns

### WebSocket Security

```javascript
// File: security/websocketSecurity.js

// 1. Authentication
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  
  if (!token) {
    return next(new Error('Authentication error'));
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.user = decoded;
    next();
  } catch (err) {
    next(new Error('Authentication error'));
  }
});

// 2. Authorization per event
socket.on('join-room', async (roomId) => {
  const hasPermission = await checkRoomPermission(socket.user.id, roomId);
  
  if (!hasPermission) {
    socket.emit('error', { message: 'Unauthorized' });
    return;
  }
  
  socket.join(roomId);
});

// 3. Input validation
socket.on('chat-message', (data) => {
  // Validate message content
  if (typeof data.content !== 'string' || data.content.length > 5000) {
    socket.emit('error', { message: 'Invalid message' });
    return;
  }
  
  // Sanitize HTML
  data.content = sanitizeHtml(data.content);
  
  // Continue processing
});

// 4. Rate limiting per socket
const rateLimiter = new Map();

socket.on('chat-message', () => {
  const key = socket.user.id;
  const now = Date.now();
  
  if (!rateLimiter.has(key)) {
    rateLimiter.set(key, { count: 0, resetAt: now + 60000 });
  }
  
  const limiter = rateLimiter.get(key);
  
  if (now > limiter.resetAt) {
    limiter.count = 0;
    limiter.resetAt = now + 60000;
  }
  
  limiter.count++;
  
  if (limiter.count > 60) { // Max 60 messages per minute
    socket.emit('rate-limited', { retryAfter: limiter.resetAt - now });
    return;
  }
  
  // Continue processing
});

// 5. Secure WebSocket (WSS)
const server = https.createServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert'),
}, app);

const io = new Server(server, {
  // Force WebSocket Secure
  allowRequest: (req, callback) => {
    const isSecure = req.headers['x-forwarded-proto'] === 'https';
    callback(null, isSecure);
  },
});

// 6. CORS for Socket.IO
const io = new Server(server, {
  cors: {
    origin: 'https://myapp.com',
    methods: ['GET', 'POST'],
    credentials: true,
  },
});
```

---

## 10. Performance Optimization

### WebSocket Optimization

```javascript
// File: performance/websocketOptimize.js

// 1. Message batching
const messageBatcher = new Map();
const BATCH_INTERVAL = 100; // ms

function queueMessage(socketId, event, data) {
  if (!messageBatcher.has(socketId)) {
    messageBatcher.set(socketId, []);
  }
  
  messageBatcher.get(socketId).push({ event, data });
  
  // Schedule flush
  if (!messageBatcher.get(socketId).flushScheduled) {
    setTimeout(() => flushMessages(socketId), BATCH_INTERVAL);
    messageBatcher.get(socketId).flushScheduled = true;
  }
}

function flushMessages(socketId) {
  const messages = messageBatcher.get(socketId);
  if (!messages || messages.length === 0) return;
  
  const socket = io.sockets.sockets.get(socketId);
  if (socket) {
    socket.emit('batch', messages);
  }
  
  messageBatcher.delete(socketId);
}

// 2. Compression
const zlib = require('zlib');

socket.on('chat-message', (data) => {
  const compressed = zlib.deflateSync(JSON.stringify(data));
  
  // Send compressed to client
  socket.compress(true).emit('message', compressed);
});

// 3. Selective emit
// Only send to relevant sockets
io.to('room-123').except(socket.id).emit('message', data);

// 4. Room-based routing
// Instead of broadcasting to all
// Use rooms for targeted messaging
socket.join(`user:${socket.user.id}`); // Personal room
socket.join(`role:${socket.user.role}`); // Role-based room

// For admins only
io.to('role:admin').emit('alert', data);

// 5. Redis Adapter for horizontal scaling
const { createAdapter } = require('@socket.io/redis-adapter');
const pubClient = createClient({ host: 'redis-host', port: 6379 });
const subClient = pubClient.duplicate();

io.adapter(createAdapter(pubClient, subClient));
```

---

## 11. Scaling Challenges

### Horizontal Scaling

```javascript
// File: scaling/websocketScale.js

// 1. Redis Adapter for multiple instances
const { createAdapter } = require('@socket.io/redis-adapter');

const pubClient = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
});

const subClient = pubClient.duplicate();

io.adapter(createAdapter(pubClient, subClient));

// Now all Socket.IO instances share state
// Room membership, socket IDs, etc.

// 2. Sticky Sessions with Load Balancer
// Nginx config for sticky sessions
const nginxConfig = `
upstream websocket {
  ip_hash;
  server ws-1:3001;
  server ws-2:3001;
  server ws-3:3001;
}

server {
  location /socket.io/ {
    proxy_pass http://websocket;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
  }
}
`;

// 3. Presence service with Redis
class PresenceService {
  constructor(redis) {
    this.redis = redis;
  }

  async setOnline(userId) {
    await this.redis.setex(`presence:${userId}`, 60, 'online');
    await this.redis.sadd('online-users', userId);
  }

  async setOffline(userId) {
    await this.redis.del(`presence:${userId}`);
    await this.redis.srem('online-users', userId);
  }

  async isOnline(userId) {
    return (await this.redis.get(`presence:${userId}`)) === 'online';
  }

  async getOnlineUsers() {
    return this.redis.smembers('online-users');
  }
}

// 4. Message persistence before delivery
// Store in Redis first, then deliver
async function publishMessage(roomId, message) {
  // Store in Redis
  await redis.lpush(`room:${roomId}:messages`, JSON.stringify(message));
  await redis.ltrim(`room:${roomId}:messages`, 0, 999);
  
  // Deliver to connected clients
  io.to(roomId).emit('new-message', message);
  
  // Later: Sync to database
  queue.add('persist-messages', { roomId, message });
}
```

---

## 12. Best Practices

### Real-Time Best Practices

```markdown
# Real-Time Best Practices

## 1. Connection Management
- Always authenticate WebSocket connections
- Use secure WebSocket (WSS)
- Implement heartbeat/ping-pong
- Handle reconnection gracefully
- Clean up on disconnect

## 2. Message Design
- Use JSON for messages
- Include message IDs
- Include timestamps
- Version your messages
- Keep messages small

## 3. Scalability
- Use Redis adapter for multiple instances
- Implement sticky sessions
- Use rooms for targeted messaging
- Consider message persistence

## 4. Security
- Authenticate every connection
- Authorize every action
- Validate all input
- Rate limit messages
- Sanitize content

## 5. Performance
- Batch messages when possible
- Use compression
- Avoid broadcasting to all
- Use rooms efficiently
- Monitor connection count

## 6. User Experience
- Show connection status
- Show typing indicators
- Show online/offline status
- Queue messages when offline
- Graceful degradation
```

---

## 13. Common Mistakes

### Real-Time Mistakes

```javascript
// MISTAKE 1: Not handling reconnection
// BAD - Assume always connected
socket.emit('action', data);

// GOOD - Handle disconnection
function safeEmit(event, data) {
  if (socket?.connected) {
    socket.emit(event, data);
  } else {
    // Queue for later
    offlineQueue.push({ event, data });
  }
}

// MISTAKE 2: Too many event listeners
// BAD - Creating new listeners every render
useEffect(() => {
  socket.on('message', () => {/* ... */});
});

// GOOD - Single listener
useEffect(() => {
  const handler = () => {/* ... */};
  socket.on('message', handler);
  return () => socket.off('message', handler);
}, []);

// MISTAKE 3: Not optimizing message size
// BAD - Sending full objects
socket.emit('message', {
  id: '123',
  content: 'hello',
  user: {
    id: '456',
    name: 'John',
    avatar: 'https://example.com/big-image.jpg',
    bio: '...',
    // Lots of unnecessary data!
  },
  room: {
    id: '789',
    name: 'General',
    description: '...',
  },
});

// GOOD - Minimal payload
socket.emit('message', {
  id: '123',
  content: 'hello',
  userId: '456',
  userName: 'John',
  roomId: '789',
});
```

---

## 14. Interview Questions

### Real-Time Interview Q&A

```markdown
Q1: How do WebSockets differ from HTTP?
A: WebSockets provide full-duplex communication over a single TCP connection.
   HTTP is request-response based. WebSocket connection stays open,
   allowing both client and server to send data anytime.

Q2: What is the WebSocket handshake?
A: Client sends HTTP request with Upgrade header. Server responds with 101
   status (Switching Protocols). After this, connection becomes WebSocket.

Q3: How do you handle WebSocket disconnection?
A: Implement heartbeat/ping-pong for detection. On client: use reconnection
   library. On server: detect disconnect, cleanup, notify others.

Q4: What is long polling?
A: Client makes HTTP request, server holds it open until data available.
   When data arrives or timeout, response sent. Client immediately makes
   new request. Fallback for when WebSockets not available.

Q5: How do you scale WebSockets?
A: Use Redis adapter to share state between instances. Implement sticky
   sessions in load balancer. Consider message persistence. Use rooms
   for efficient broadcasting.

Q6: What are Server-Sent Events (SSE)?
A: One-way communication from server to client over HTTP. Auto-reconnection
   built-in. Simpler than WebSockets. Good for notifications, live feeds.

Q7: How do you secure WebSockets?
A: Authenticate during handshake. Use WSS (WebSocket Secure). Validate
   all messages. Rate limit. Authorize each action.
```

---

## 15. Latest 2026 Fullstack Engineering Patterns

### Modern Real-Time Patterns 2026

```typescript
// 1. Edge Functions for Real-Time (Cloudflare Workers)
export default {
  async fetch(request: Request): Promise<Response> {
    // Real-time at the edge!
    const url = new URL(request.url);
    
    if (url.pathname === '/ws') {
      // WebSocket handling at edge
      const pair = new WebSocketPair();
      handleWebSocket(pair[1]);
      return new Response(null, { status: 101, webSocket: pair[0] });
    }
    
    return new Response('Not Found', { status: 404 });
  },
};

// 2. GraphQL Subscriptions
// File: graphql/subscriptions.ts
import { gql } from 'graphql-tag';

const typeDefs = gql`
  type Subscription {
    messageAdded(roomId: ID!): Message!
    userPresenceUpdated: PresenceUpdate!
    typingStatusChanged(roomId: ID!): TypingStatus!
  }
`;

const resolvers = {
  Subscription: {
    messageAdded: {
      subscribe: async function* (_, { roomId }) {
        // Subscribe to Redis channel
        const pubsub = new PubSub();
        const iterator = pubsub.asyncIterator(`ROOM:${roomId}`);
        
        for await (const message of iterator) {
          yield { messageAdded: message };
        }
      },
    },
  },
};

// 3. Liveblocks for Collaborative Apps
// File: realtime/liveblocks.ts
import { createClient, LiveMap, LiveList } from '@liveblocks/client';
import { createRoomContext } from '@liveblocks/react';

const client = createClient({
  authEndpoint: '/api/auth/liveblocks',
});

const {
  RoomProvider,
  useRoom,
  useMyPresence,
  useOthers,
  useStorage,
} = createRoomContext(client);

// 4. Partykit for Multiplayer
// File: party/index.ts
import { Server } from 'partykit/server';

export default class ChatServer extends Server {
  onConnect(conn, room) {
    console.log(`Connected: ${conn.id} in ${room}`);
    
    // Broadcast to room
    this.room.broadcast(JSON.stringify({
      type: 'user-joined',
      userId: conn.id,
    }));
  }

  onMessage(message, sender) {
    // Parse and broadcast
    const data = JSON.parse(message);
    this.room.broadcast(JSON.stringify(data), [sender.id]);
  }

  onClose(conn) {
    this.room.broadcast(JSON.stringify({
      type: 'user-left',
      userId: conn.id,
    }));
  }
}

// 5. Supabase Realtime
// File: realtime/supabase.ts
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(url, key);

// Subscribe to database changes
supabase
  .channel('db-changes')
  .on('postgres_changes', {
    event: '*',
    schema: 'public',
    table: 'messages',
  }, (payload) => {
    console.log('New message:', payload.new);
  })
  .subscribe();

// Presence (online users)
supabase.channel('room-1')
  .on('presence', { event: 'sync' }, () => {
    const state = supabase.channel('room-1').presenceState();
    console.log('Online users:', state);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await supabase.channel('room-1').track({
        user_id: currentUser.id,
        online_at: new Date().toISOString(),
      });
    }
  });
```

---

## Summary

Bhai, real-time features implement karna challenging ho sakta hai, par kaafi's powerful feature hai:

1. **WebSockets** - Full duplex, complex, best for chat/gaming
2. **SSE** - Simple, one-way, best for notifications
3. **Socket.IO** - Abstraction over WebSocket, easy to use
4. **Redis Adapter** - For scaling WebSockets horizontally
5. **Security** - Always authenticate, validate, rate limit
6. **2026 Trends** - Edge WebSockets, GraphQL subscriptions, Partykit, Supabase Realtime

Remember:
- Connection management is key
- Handle offline gracefully
- Don't overuse real-time (polling might be enough)
- Scale with Redis adapter
- Always secure your connections

---

*Previous: [Caching and Queues](./Caching_and_Queues.md) | Next: [Backend Security](./Backend_Security.md)*
