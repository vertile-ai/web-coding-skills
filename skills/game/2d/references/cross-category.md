# Cross-category summary: what to use where

Here's the condensed decision view.

## Control-driven

Best fit:

* Pixi or Phaser
* fixed loop
* small ECS/component system
* minimal worker use
* minimal WASM use

Use browser tech:

* Canvas/WebGL, Web Audio, input APIs

Do not prioritize:

* WASM, heavy backend, giant content systems

---

## System-driven

Best fit:

* custom sim core
* workers
* IndexedDB
* snapshot/diff architecture
* maybe WASM later

Use browser tech:

* Workers, IndexedDB, Canvas/WebGL, maybe OffscreenCanvas

Do not prioritize:

* rich character animation systems before sim correctness

---

## Rule-driven

Best fit:

* reducer/command pattern
* pure state transitions
* optional DOM/SVG
* very testable architecture

Use browser tech:

* basic canvas or DOM, local save, maybe workers for AI

Do not prioritize:

* ECS, physics, WASM

---

## Content-driven

Best fit:

* data-driven runtime
* strong content schema
* save versioning
* dialogue/quest tools
* Canvas + DOM hybrid

Use browser tech:

* IndexedDB, Web Audio, maybe service worker, maybe worker for prep tasks

Do not prioritize:

* WASM, multicore compute, massive physics stack

---

## Physics-driven

Best fit:

* physics-first loop
* fixed timestep
* careful object lifecycle
* JS physics first, WASM later if proven needed

Use browser tech:

* Canvas/WebGL, Web Audio, maybe worker/WASM

Do not prioritize:

* DOM-heavy in-world UI
* overcomplicated network architecture unless multiplayer

---

## Network-driven

Best fit:

* authority-first design
* WebSocket
* prediction/reconciliation for realtime
* room/session backend
* robust observability

Use browser tech:

* WebSocket, rendering stack, local cache, maybe worker

Do not prioritize:

* WASM before sync model is correct
* P2P authority in competitive games

---

# A practical module recommendation by category

## Engine module

* **Control-driven**: strong loop/timing/input ownership
* **System-driven**: tick scheduler and world systems runner
* **Rule-driven**: turn/rules executor, minimal engine
* **Content-driven**: scene/progression/script runtime
* **Physics-driven**: physics-step orchestrator
* **Network-driven**: client prediction + authoritative sync interface

## Audio module

* **Control-driven**: fast low-latency SFX
* **System-driven**: ambience and alerts
* **Rule-driven**: event cues
* **Content-driven**: music/dialogue/progression-aware
* **Physics-driven**: collision-responsive
* **Network-driven**: effect-safe under reconciliation

## Asset module

* **Control-driven**: atlases and animation sheets
* **System-driven**: tiles/chunks/icons/data defs
* **Rule-driven**: board/card/icon assets
* **Content-driven**: large content DB + localization assets
* **Physics-driven**: shape and joint config + debris/effects
* **Network-driven**: normal assets, but patching/version consistency matters more

## Visual/effects module

* **Control-driven**: very important for feel
* **System-driven**: mostly state visualization and overlays
* **Rule-driven**: readability first
* **Content-driven**: scene and UI presentation first
* **Physics-driven**: impact/destruction feedback
* **Network-driven**: must survive correction/interpolation

---

# When browser technology is overkill

A lot of teams overuse browser APIs. Here are common mistakes:

## Don't reach for WASM when

* the game is mostly UI/content/rules
* performance bottlenecks haven't been measured
* the real issue is asset/render inefficiency

## Don't use Workers when

* work is small and communication overhead dominates
* core realtime loop needs main-thread immediacy
* you are adding architecture complexity without measurable gain

## Don't use WebGL/WebGPU when

* simple Canvas 2D is already enough
* your game is board/UI-heavy
* your problem is content complexity, not rendering throughput

## Don't use IndexedDB-heavy architecture when

* the save is tiny and localStorage is enough
* the game session is short and disposable

## Don't use React for world rendering when

* the scene updates every frame
* entity count is non-trivial
* animation must be tightly synced to simulation

But React/DOM is still great for:

* menus
* inventory
* overlays
* settings
* social UI
* debug tools

---

# Best "starter architecture" for each category

## Control-driven

* TS + Vite + Pixi/Phaser + Howler
* fixed timestep
* component/system gameplay
* local save
* no WASM, no worker at first

## System-driven

* TS + Vite + Pixi
* sim in Worker
* IndexedDB
* snapshot/diff updates
* consider WASM only after profiling

## Rule-driven

* TS + reducer/command core
* Canvas or DOM/SVG
* replay/undo
* pure logic tests
* optional AI worker

## Content-driven

* TS + Pixi/Phaser + React UI
* data-driven content pipeline
* IndexedDB
* localization and content validation
* maybe service worker for asset caching

## Physics-driven

* TS + Pixi + Matter/Planck
* fixed timestep
* tuned body lifecycle
* no WASM initially unless physics is genuinely huge

## Network-driven

* TS + Pixi/Phaser + WebSocket client
* authoritative backend
* prediction/reconciliation if realtime
* metrics and reconnect handling from the start
