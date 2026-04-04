# 6. Network-driven games

Examples:

* realtime 3D PvP (deathmatch, battle royale lite)
* 3D co-op action games
* shared 3D social spaces and virtual worlds
* MMO-lite 3D games
* async turn-based 3D tactics

Their main challenge is **authoritative state, 3D transform synchronization, prediction/reconciliation in 3D space, and latency concealment under the extra cost of rendering a 3D scene**.

---

## 1. Package dependencies

### Good default dependencies

Frontend:

* **Three.js** for rendering
* **WebSocket** client — native or **socket.io-client**
* binary serialization: **msgpack-lite** or a custom schema with `DataView` — JSON is too verbose for per-frame transforms
* store/event system for local state

Backend:

* **Node.js** + **ws** (WebSocket) or **uWebSockets.js** for high-throughput rooms
* room/session manager — can be simple in-memory for small scale
* authoritative simulation — ideally the same physics lib as the client (Rapier has a WASM Node.js build)
* persistence layer for accounts and progression
* metrics and logging from day one

### Avoid by default

* peer-to-peer authority for any competitive or progression-affecting game
* shipping singleplayer 3D architecture and bolting on networking — 3D state is much harder to retrofit than 2D
* WebRTC data channels as the primary game state transport (fine for voice; complex for game state)
* socket.io rooms for high-frequency 3D state messages — the overhead is acceptable for low-frequency events but not for per-frame position updates

### Why

Networking in 3D is harder than 2D for two reasons:

1. **State size**: 3D positions have three floats; rotations need quaternions (four floats) or compressed Euler. Per-entity bandwidth is larger.
2. **Physics reconciliation**: correcting a mispredicted 3D physics body is visually jarring — rubber-banding in 3D is worse than in 2D.

---

## 2. Code design and WASM trade-offs

## Recommended code design

Three clear state layers:

* **Authoritative state** — owned by server, source of truth
* **Predicted state** — client-side prediction of local player actions before server confirmation
* **Presentation state** — smoothed, interpolated, visually consumed

### Transform interpolation

The core challenge in 3D networking.

For remote entities, do not snap to the received transform. Instead, buffer received snapshots with timestamps and interpolate between them with a small delay:

```ts
// On snapshot receive:
entityBuffer[id].push({ position, quaternion, timestamp });

// On render:
const renderTime = Date.now() - INTERPOLATION_DELAY;
const { from, to } = findInterpolationPair(entityBuffer[id], renderTime);
const alpha = (renderTime - from.timestamp) / (to.timestamp - from.timestamp);
mesh.position.lerpVectors(from.position, to.position, alpha);
mesh.quaternion.slerpQuaternions(from.quaternion, to.quaternion, alpha);
```

Quaternion slerp is required for rotation — lerp between Euler angles causes gimbal lock artifacts.

### Client-side prediction

For the local player:

* apply input immediately on client (no waiting for server)
* server sends authoritative corrections
* client reconciles: rewind to the divergence point, replay inputs from that point forward
* if the correction is small (< threshold), blend visually rather than snap

Bad pattern: waiting for server acknowledgment before moving the local player — the game will feel broken at any latency above 50ms.

### Snapshot vs event model

For realtime:

* **Snapshot**: server sends full entity state every N ms; client interpolates between them
* more bandwidth but simpler to implement and resilient to message loss
* good default

For async or turn-based:

* **Event/command log**: server sends deltas (actions taken); client replays
* very low bandwidth but requires deterministic replay

### Compression

3D state is verbose. Optimize:

* positions: 16-bit fixed-point per axis with known world bounds is often sufficient
* rotations: quantized quaternion (smallest-three encoding) — compress 4 floats to 3 half-floats
* send only dirty entities each tick
* delta snapshots for world state if stable

## WASM considerations

Usually not the first concern.

The real pain in networked 3D games:

* protocol design and message schema
* reconciliation correctness in 3D
* race conditions in session lifecycle
* anti-cheat if progression is at stake
* 3D collision authority on server vs client

Use WASM if:

* you share a physics simulation between client and server (Rapier has Node.js WASM build — run the same sim on both sides for deterministic validation)
* compression/decompression is a bottleneck on high-player-count servers

---

## 3. System design

## Frontend modules

### Input

* generate input commands with timestamps
* local buffering for prediction
* do not send raw key states — send semantic commands: `{ type: 'move', direction: [0, 0, 1], timestamp }`

### Net client

* WebSocket connection lifecycle with reconnect
* heartbeat / ping measurement
* message framing and binary deserialization
* jitter buffer for snapshot interpolation

### Prediction and reconciliation

* apply input locally and record in pending input queue
* on server correction: diff against predicted state
* if significant divergence: rollback to correction, re-simulate pending inputs
* visual smoothing to hide small corrections

### Render / effects / audio

* must tolerate rollback without leaving orphaned particles or sounds
* do not tie game truth to effect timing
* interpolation buffer per remote entity

## Backend modules

### Session / room server

* room lifecycle: create, join, start, end
* player join/leave with grace period for reconnect
* tick scheduler

### Authoritative simulation

* receives client input commands
* validates them (rate limits, bounds, legality checks)
* steps simulation state
* broadcasts snapshots or events to all clients in room
* run the same physics lib as client (Rapier) for reliable server-side validation

### Persistence

* player account and progression
* match history
* reconnect state buffer (last known world state for rejoining players)

### Anti-cheat

* server is authoritative: never trust client-reported positions or damage values
* validate inputs: max speed, position delta, fire rate
* anomaly detection: sudden position jumps, impossible damage rates

### Observability

Essential from day one:

* average RTT per player
* packet loss rate
* snapshot delivery rate
* desync rate (how often clients diverge significantly from server state)
* room lifecycle events (abnormal exits, reconnect success rate)

---

## 4. Browser technology: needed vs not needed

## Needed

* **WebSocket** — near-universal for realtime game state
* **WebGL2** (Three.js default)
* **Web Audio** with 3D spatial positioning
* **Visibility / focus events** — pause and reconnect gracefully when tab is hidden
* **localStorage / IndexedDB** for cached session token and offline progression

## Sometimes useful

* **WebRTC** for voice chat between players — separate from game state transport
* **Web Workers** for client-side snapshot decompression or heavy decode paths
* **Service workers** for patching and asset cache versioning across game updates
* **Gamepad API** if supporting controllers

## Usually not needed

* WASM for client game logic (use it only if sharing a Rapier sim with server)
* SharedArrayBuffer unless very specialized parallel decode architecture
* Peer-to-peer authority for competitive game state
* WebGPU — rendering is not the bottleneck in networked games; sync correctness is
