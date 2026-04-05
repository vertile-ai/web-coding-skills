# 3. System-driven games

Examples:

* 3D city builders and town planners
* real-time strategy (RTS) in 3D
* large colony / management simulations
* factory and logistics games
* grand strategy with 3D map
* large agent field simulations

Their main challenge is **rendering scale, instancing, LOD, chunk streaming, and background simulation correctness**.

---

## 1. Package dependencies

### Good default dependencies

* **Three.js** with `InstancedMesh` — this is non-negotiable at scale; separate meshes per unit will destroy draw call budget
* custom tick-driven simulation core — not an off-the-shelf game engine, because you need explicit tick control
* **Comlink** for comfortable worker communication
* **Dexie** or direct IndexedDB for world saves that exceed memory
* octree or grid spatial index — either hand-rolled or a small lib — for efficient selection and queries
* `@dimforge/rapier3d-compat` only if physical simulation of units is actually needed; most RTS/city builder logic does not need a full physics world

### Avoid by default

* separate `THREE.Mesh` per unit at scale — even 1000 separate meshes will hurt
* scene graph as the source of truth for simulation state — the scene should be a projection of simulation state, not its owner
* React Three Fiber for the live 3D world — R3F's reconciler is not designed for scenes that change every simulation tick
* Babylon.js GUI system for heavy simulation UI — use React DOM overlaying the canvas instead

### Why

This category wants:

* batched rendering via instancing
* explicit simulation ticks, not per-frame computation
* clear split between simulation state and render state
* background compute through workers

---

## 2. Code design and WASM trade-offs

## Recommended code design

The core data shape:

* flat typed arrays or object pools — not deep object graphs per entity
* all unit/building/resource data kept in compact arrays: `positions: Float32Array`, `health: Int32Array`, etc.
* simulation runs headlessly on these arrays
* render reads arrays to update `InstancedMesh` instance matrices and colors

Example system split:

* `AgentSystem` — movement, pathfinding, behavior states
* `EconomySystem` — resource production and consumption
* `BuildingSystem` — construction, job allocation
* `MapSystem` — terrain, zones, road graph
* `RenderBridge` — reads simulation arrays → writes to `InstancedMesh` attributes per frame

### Worker pattern

Main thread handles:

* input
* camera
* Three.js render
* React DOM UI

Worker handles:

* simulation tick
* pathfinding
* AI decisions

Communication: transferable `SharedArrayBuffer` or structured-clone of diff snapshots.

Bad pattern: running simulation on main thread and wondering why frame rate drops under load. The simulation and render budget compete directly on main thread.

### InstancedMesh usage

```ts
const mesh = new THREE.InstancedMesh(geometry, material, MAX_UNITS);
scene.add(mesh);

// per frame:
for (let i = 0; i < activeCount; i++) {
  dummy.position.set(units.x[i], units.y[i], units.z[i]);
  dummy.updateMatrix();
  mesh.setMatrixAt(i, dummy.matrix);
}
mesh.instanceMatrix.needsUpdate = true;
```

Never create a separate mesh per unit. `InstancedMesh` is the right tool the moment you have more than ~50 identical repeated objects.

### LOD

`THREE.LOD` provides automatic distance-based mesh switching:

```ts
const lod = new THREE.LOD();
lod.addLevel(highDetailMesh, 0);
lod.addLevel(medDetailMesh, 50);
lod.addLevel(lowDetailMesh, 200);
lod.addLevel(iconMesh, 500);
```

At large scale, combine LOD with instancing per LOD level.

## WASM?

This category benefits from WASM more than most others in 3D.

### Use WASM when

* pathfinding grid is large and A* calls are numerous per tick
* agent count exceeds a few thousand with complex behavior
* world generation uses heavy noise/erosion algorithms
* simulation hot loops are proven CPU-bound after profiling

### Do not start with WASM blindly

Workers + typed arrays in JS can sustain surprising scale. Profile first.

Trade-off: WASM adds build complexity, slower iteration, and trickier debugging. Earn it with profiler evidence.

---

## 3. System design

## Engine / core

Tick-driven, not frame-driven:

* `SimulationClock` — fixed tick rate (e.g., 10Hz or 20Hz), independent of render FPS
* `CommandQueue` — player actions buffered and applied at tick boundary
* `WorldState` — canonical simulation state
* `SystemsRunner` — ordered list of simulation systems that run per tick
* `RenderBridge` — reads WorldState, updates Three.js scene objects

## Simulation

* keep simulation systems decoupled and individually testable without a renderer
* pathfinding: use a pre-baked navigation mesh (NavMesh) where possible; Recast.js can generate one
* spatial queries: octree or grid lookup for "which units are in this area" — do not iterate all units
* time scaling: simulation should support 1x/2x/4x/8x tick rates; render always runs at full FPS

## Render

* `InstancedMesh` per unit type per LOD level
* terrain: tiled chunks, each chunk a single merged `BufferGeometry` — do not render every tile as its own mesh
* selection highlight: `InstancedMesh` supports per-instance color via `setColorAt`; use this for selection, not separate objects
* map overlays (zone colors, road heat, population density): custom shader on the terrain mesh reading a texture updated from the simulation

## UI

Very important:

* inspectors, stat panels, production chains, resource counters
* this is where DOM/React is the right choice — not WebGL text
* React components reading from a shared store that the simulation writes to
* avoid putting all UI in Three.js `Sprite` text — it is hard to style and maintain

## Audio

* ambience tracks per zone type
* event cues: construction complete, resource depleted, alert
* less latency-sensitive than action games

## Asset pipeline

* building meshes: GLTF/GLB per building type, shared geometry across instances
* terrain: procedurally generated BufferGeometry or tiled heightmap
* icons and UI: sprite sheets or SVG — not 3D objects in the DOM

## Save

A top priority:

* world snapshots — serializing all agent and building state
* versioned migration (world saves outlive patches)
* autosave at tick boundaries, not mid-tick
* chunked saves for very large worlds — save active area + lazy-load distant chunks from IndexedDB

## Tools

Greatly accelerate development:

* simulation speed control (pause, 1x, 4x)
* debug inspector for individual agents
* overlays for pathfinding, heat maps, zone assignments
* tick counter and system timing breakdown

---

## 4. Browser technology: needed vs not needed

## Needed

* **Web Workers** — simulation must run off main thread at scale
* **SharedArrayBuffer** or **transferable typed arrays** for simulation→render data exchange
* **IndexedDB** for world saves
* **Three.js InstancedMesh** — not a browser API but the critical rendering pattern
* **requestAnimationFrame** for render loop

## Often useful

* **OffscreenCanvas** if render needs to move to a worker (unusual but possible)
* **WASM** for pathfinding or agent AI after profiling
* **Comlink** for clean worker communication
* **CompressionStream** for large world save compression

## Usually not needed

* full physics engine (agents are usually moved by simulation logic, not physics)
* React Three Fiber — the reconciler overhead is a problem in high-tick scenes
* WebGPU — useful for GPU-driven compute of agent positions or large terrain, but premature for most projects
* ultra-low-latency input systems — the game operates on ticks, not frames
