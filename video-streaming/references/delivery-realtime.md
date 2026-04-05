# Delivery & Real-time Reference

## HLS adaptive player (TypeScript + hls.js)

hls.js handles ABR rung selection automatically. Always attach network and fatal error handlers; on a fatal media error, attempt one recovery before destroying the instance.

```typescript
import Hls, { Events, ErrorTypes, ErrorDetails } from 'hls.js';

function mountPlayer(videoEl: HTMLVideoElement, manifestUrl: string): Hls | null {
  if (!Hls.isSupported()) {
    // Safari has native HLS — just point src directly
    videoEl.src = manifestUrl;
    return null;
  }

  const hls = new Hls({
    lowLatencyMode: true,       // enable LL-HLS for sub-3-second latency
    maxBufferLength: 10,        // seconds of forward buffer
    backBufferLength: 30,       // seconds of back-buffer for DVR scrubbing
    enableWorker: true,
  });

  hls.loadSource(manifestUrl);
  hls.attachMedia(videoEl);

  hls.on(Events.MANIFEST_PARSED, () => {
    videoEl.play().catch(() => {
      // Autoplay blocked — surface a play button to the user
    });
  });

  let recoveryAttempted = false;

  hls.on(Events.ERROR, (_, data) => {
    if (!data.fatal) return;

    if (data.type === ErrorTypes.MEDIA_ERROR && !recoveryAttempted) {
      recoveryAttempted = true;
      hls.recoverMediaError();
    } else {
      hls.destroy();
      // Re-mount after a back-off to handle transient CDN issues
      setTimeout(() => mountPlayer(videoEl, manifestUrl), 5_000);
    }
  });

  return hls;
}
```

## Real-time chat server (Node.js / TypeScript + Socket.IO + Redis)

Fan-out is handled by Redis pub/sub. Each socket server process subscribes to the same channel, so a message sent to one pod is broadcast to viewers connected to any pod.

```typescript
import { Server } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';
import http from 'http';
import { verifyToken } from './auth';

const RATE_LIMIT_MAX = 3;   // messages per window
const RATE_LIMIT_WINDOW = 2_000; // ms

interface MessagePayload {
  text: string;
  streamId: string;
}

async function startChatServer(httpServer: http.Server) {
  const pubClient = createClient({ url: process.env.REDIS_URL });
  const subClient = pubClient.duplicate();
  await Promise.all([pubClient.connect(), subClient.connect()]);

  const io = new Server(httpServer, { cors: { origin: '*' } });
  io.adapter(createAdapter(pubClient, subClient));

  io.use(async (socket, next) => {
    const token = socket.handshake.auth.token as string;
    const user = await verifyToken(token);
    if (!user) return next(new Error('Unauthorized'));
    socket.data.user = user;
    next();
  });

  io.on('connection', (socket) => {
    const { user } = socket.data;

    // Per-socket rate limiter: sliding bucket
    let bucket = RATE_LIMIT_MAX;
    const refill = setInterval(() => { bucket = RATE_LIMIT_MAX; }, RATE_LIMIT_WINDOW);

    socket.on('join', (streamId: string) => {
      socket.join(`stream:${streamId}`);
    });

    socket.on('chat:message', (payload: MessagePayload) => {
      if (bucket <= 0) {
        socket.emit('chat:error', { code: 'RATE_LIMITED' });
        return;
      }
      bucket--;

      const message = {
        id: crypto.randomUUID(),
        text: payload.text.slice(0, 300), // hard-truncate; never trust client length
        userId: user.id,
        displayName: user.displayName,
        timestamp: Date.now(),
      };

      io.to(`stream:${payload.streamId}`).emit('chat:message', message);
    });

    socket.on('disconnect', () => clearInterval(refill));
  });
}
```

## Viewer count (Redis + TypeScript)

Track live viewer counts using a Redis sorted set keyed by stream ID. Expire entries when the socket disconnects.

```typescript
import { RedisClientType } from 'redis';

const VIEWER_KEY = 'stream:viewers';
const PRESENCE_TTL = 30; // seconds

async function onViewerJoin(redis: RedisClientType, streamId: string, userId: string) {
  await redis.zAdd(VIEWER_KEY, { score: Date.now(), value: `${streamId}:${userId}` });
  // Broadcast updated count to all in the room
  const count = await redis.zCount(VIEWER_KEY, Date.now() - PRESENCE_TTL * 1000, '+inf');
  return count;
}

async function onViewerLeave(redis: RedisClientType, streamId: string, userId: string) {
  await redis.zRem(VIEWER_KEY, `${streamId}:${userId}`);
}

// Run periodically to prune stale entries (clients that disconnected without cleanup)
async function pruneStaleViewers(redis: RedisClientType) {
  const cutoff = Date.now() - PRESENCE_TTL * 1000;
  await redis.zRemRangeByScore(VIEWER_KEY, '-inf', cutoff);
}
```

## WebRTC broadcaster capture (TypeScript, browser)

For ultra-low latency (<500 ms) use cases. Capture and send via WHIP (WebRTC HTTP Ingest Protocol) to a media server like mediasoup or Cloudflare Stream.

```typescript
async function startBroadcast(whipEndpoint: string, streamToken: string): Promise<RTCPeerConnection> {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });

  const pc = new RTCPeerConnection({
    iceServers: [{ urls: 'stun:stun.cloudflare.com:3478' }],
  });

  for (const track of stream.getTracks()) {
    pc.addTrack(track, stream);
  }

  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);

  // WHIP: POST the SDP offer, receive the SDP answer
  const res = await fetch(whipEndpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/sdp',
      Authorization: `Bearer ${streamToken}`,
    },
    body: offer.sdp,
  });

  if (!res.ok) throw new Error(`WHIP failed: ${res.status}`);

  const answerSdp = await res.text();
  await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });

  return pc;
}
```
