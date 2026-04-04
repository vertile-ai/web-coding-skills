# 6. Network-driven games

Examples:

* realtime PvP
* co-op action
* MMO-lite 2D games
* shared social spaces
* async multiplayer tactics/card games

Their main challenge is **authority, synchronization, latency, and cheating risk**.

---

## 1. Package dependencies

### Good default dependencies

Frontend:

* rendering lib: Pixi/Phaser/Canvas
* socket library
* binary serializer if needed
* store/event system

Backend:

* WebSocket stack
* session/room manager
* persistence layer
* matchmaking or room discovery if needed
* metrics/logging

### Avoid by default

* shipping singleplayer-first architecture and bolting networking on later
* huge REST-first design for realtime sync
* direct client-authoritative state in competitive games

### Why

Networked games are shaped by authority model from day one.

---

## 2. Code design and WASM trade-offs

## Recommended code design

Split clearly:

* local predicted state
* authoritative state
* presentation state

You often need:

* command/input messages
* snapshot updates
* reconciliation layer
* interpolation/extrapolation
* disconnect/rejoin flow

For async turn-based, a much simpler model works:

* command submission
* authoritative turn resolution
* state fetch / event log replay

## WASM?

Usually not the first concern.

Use it only if:

* simulation validation on server is heavy
* shared native simulation exists
* compression or specialized compute is a bottleneck

Most network game pain is not CPU. It is:

* protocol design
* consistency
* race conditions
* anti-cheat
* session lifecycle

---

## 3. System design

## Frontend modules

### Input

* command generation
* local buffering
* prediction hooks

### Net client

* connection lifecycle
* heartbeat/reconnect
* message decoding
* reliability strategy where needed

### Simulation/presentation

For realtime:

* local prediction
* server reconciliation
* remote interpolation

For async:

* simpler authoritative state rendering

### Render/effects/audio

Should tolerate rollback/reconciliation where applicable.
Do not make game truth depend on effect timing.

## Backend modules

### Session/room server

* room lifecycle
* player join/leave
* match state

### Authority/simulation

* validates inputs
* steps game state
* sends snapshots or events

### Persistence

* player progress
* match history
* reconnect state
* inventory/account state if needed

### Matchmaking/social

* lobbies
* friend presence
* invites
* rankings if needed

### Observability

Very important:

* ping
* packet loss
* room count
* desync rate
* reconnect failures

## Save

Depends on model:

* async games: very important
* realtime matches: usually per-match state + account progression

---

## 4. Browser technology: needed vs not needed

## Needed

* **WebSocket** almost always for realtime
* standard rendering stack
* IndexedDB/local storage for cached state and settings
* visibility/focus handling for reconnect/pause UX

## Sometimes useful

* **WebRTC** for voice or selective peer scenarios, but not required for most authoritative multiplayer game state
* **Service workers** for patching/cache
* **Web Workers** for client-side prediction or heavy decode paths
* **Gamepad API** if relevant

## Usually not needed

* WASM early
* SharedArrayBuffer unless highly specialized performance architecture
* peer-to-peer authority for competitive games
