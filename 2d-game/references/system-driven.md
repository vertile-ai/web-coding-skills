# 2. System-driven games

Examples:

* city builders
* colony sims
* management sims
* factory games
* large agent simulations

Their main challenge is **scale of simulation**, not twitch feel.

---

## 1. Package dependencies

### Good default dependencies

* **PixiJS** or custom Canvas/WebGL renderer
* pathfinding libs if appropriate, though many teams outgrow them
* maybe lightweight ECS or data-oriented utility libs
* **Dexie** or direct IndexedDB wrapper for saves
* worker communication helpers like **Comlink**
* compression libs for save data if worlds get large

### Avoid by default

* Phaser-style gameplay-first engine if the game is mostly simulation/UI-heavy
* rigid scene-tree engines for all logic
* React driving the entire simulation state directly

### Why

This category wants:

* explicit simulation ticks
* good chunking
* background compute
* clear data ownership

---

## 2. Code design and WASM trade-offs

## Recommended code design

Use:

* **data-oriented systems**
* large arrays/maps of entity data
* discrete simulation ticks
* clear split between:

  * simulation state
  * render state
  * player command queue

Often better than OOP here:

* `Citizens[]`
* `Jobs[]`
* `Buildings[]`
* `Resources[]`
* processors that sweep over them

instead of deep object networks.

### Good pattern

* main thread handles UI and render
* worker handles simulation tick
* main thread receives snapshots or diffs

## WASM?

This is one of the categories where WASM can make sense.

### WASM is useful when

* pathfinding is huge
* world simulation is large
* procedural generation is heavy
* many-agent AI is expensive
* you already have simulation code in Rust/C++

### But still, do not start there blindly

JS/TS + Workers can go very far.

Choose WASM after profiling shows:

* heavy hot loops
* memory locality matters
* worker compute is still too slow

### Trade-off

WASM makes debugging, iteration, and team onboarding slower.
So it is worth it only when the simulation pressure is real.

---

## 3. System design

## Engine / core

Core should be **tick-driven**, not frame-driven.

Split:

* `SimulationClock`
* `CommandQueue`
* `WorldState`
* `SystemsRunner`
* `SnapshotPublisher`

## Simulation

Modules often include:

* economy
* pathfinding
* job allocation
* agent needs
* map systems
* weather/time
* production chains

These should be isolated and testable headlessly.

## Render

Render is often just a projection of world state:

* map layers
* entity sprites/icons
* overlays
* debug heatmaps

Do not let rendering own truth.

## UI

Very important here:

* inspector panels
* charts
* overlays
* build menus
* alert feeds

This category often benefits from React or DOM UI around a canvas-rendered world.

## Audio

Less latency-sensitive than action games.
Focus on:

* ambience layers
* event cues
* scalable loop control

## Asset pipeline

* tile atlases
* map chunks
* large icon sets
* data-driven building/unit definitions

## Save

A big deal here:

* world snapshots
* versioned migrations
* partial chunk serialization
* autosave

Often use IndexedDB instead of localStorage.

## Tools

These games really benefit from:

* simulation speed controls
* debug inspector
* replay / event log
* graph views
* AI/path overlays

---

## 4. Browser technology: needed vs not needed

## Needed

* **Web Workers**
* **IndexedDB**
* **Canvas/WebGL**
* **structured clone / transferable objects**
* likely **requestIdleCallback** in some tooling/background tasks

## Often useful

* **OffscreenCanvas**
* **Comlink**
* **CompressionStream** or compression lib for saves
* **SharedArrayBuffer** only if you really need advanced high-frequency shared simulation data and can satisfy browser security requirements

## Sometimes useful

* **WASM**
* **WebGPU** if rendering huge maps/effects

## Usually not needed

* full physics engine
* ultra-low-latency input systems
* complex animation graph systems
