# Cross-category summary: what to use where

Here is the condensed decision view for 3D web games.

## Render-driven

Best fit:

* Three.js direct (or R3F if team is React-native)
* PBR materials, baked lighting, HDR environment
* EffectComposer post-processing stack
* Draco + KTX2 asset pipeline
* strict geometry/texture disposal

Use browser tech:

* WebGL2, postprocessing lib, GLTF toolchain

Do not prioritize:

* full physics engine, multiplayer, heavy simulation

---

## Control-driven

Best fit:

* Three.js direct (not R3F in the hot loop)
* Rapier kinematic character controller
* custom camera springarm with raycast wall avoidance
* fixed timestep + render interpolation
* AnimationMixer with state machine

Use browser tech:

* Pointer Lock API, Gamepad API, Web Audio positional, Rapier WASM

Do not prioritize:

* React Three Fiber for gameplay loop, InstancedMesh for single-player characters, WebGPU

---

## System-driven

Best fit:

* InstancedMesh per unit type — non-negotiable at scale
* simulation in Web Worker
* snapshot / diff architecture for render bridge
* LOD per instance group
* IndexedDB world saves
* maybe WASM after profiling

Use browser tech:

* Workers, SharedArrayBuffer/transferables, IndexedDB, InstancedMesh

Do not prioritize:

* React Three Fiber for live world, full physics for agent movement, WebGPU until GPU-side compute is genuinely needed

---

## Content-driven

Best fit:

* Three.js + React DOM hybrid (world in canvas, UI in DOM)
* chunk streaming with hard dispose-on-unload discipline
* data-driven content (JSON-defined items, quests, NPCs)
* save versioning with migration system
* KTX2 + Draco everywhere

Use browser tech:

* IndexedDB, Service Worker for caching, Workers for GLTF parse and background tasks

Do not prioritize:

* WASM, heavy post-processing, full physics unless hybrid gameplay needs it

---

## Physics-driven

Best fit:

* Rapier (default) or Cannon-es (simpler games)
* fixed timestep with interpolation
* physics world as position authority
* per-frame sync from bodies to meshes
* strict body disposal

Use browser tech:

* WASM (Rapier), Web Audio for collision sounds, Workers for physics if offloading is needed

Do not prioritize:

* DOM-heavy in-world UI, complex content management, networking before physics stability is solid

---

## Network-driven

Best fit:

* authority-first design from day one
* WebSocket + binary protocol
* client-side prediction + server reconciliation
* snapshot interpolation with quaternion slerp for remote entities
* authoritative server running same physics lib (Rapier Node.js)
* observability metrics from day one

Use browser tech:

* WebSocket, Web Audio spatial, Visibility API for reconnect, WebRTC for voice only

Do not prioritize:

* WASM before sync model is correct, WebGPU, P2P authority for competitive games

---

# Renderer selection guide

## Three.js

* Default choice for custom pipelines, custom shaders, tight control
* Largest community, most examples, best ecosystem
* Direct API — not framework-opinionated
* Requires explicit memory management

## Babylon.js

* Full engine with inspector, PBR, GUI, and animation editor
* Better out-of-box mobile GPU support on some hardware
* Built-in Node Material Editor for shader authoring
* Choose if: you want an editor-driven workflow, or your team found Three.js debugging painful

## @react-three/fiber (R3F)

* React abstraction over Three.js — the same objects underneath
* Excellent for component-tree-organized scenes
* **Do not use for games with many mutations per frame** — React reconciler adds overhead
* Best for: configuration-heavy visualizations, product configurators, scenes driven by React state
* Bad for: action games with physics hot loops, simulation games with per-frame instancing updates

## Raw WebGL

* Only if: you need a custom renderer that Three.js cannot express
* Very rare; almost always premature

## WebGPU (THREE.WebGPURenderer)

* Available as opt-in in Three.js r163+
* Not yet production-ready across all browser/GPU targets (as of 2025)
* Compute shaders open new possibilities (GPU-side particle systems, path tracing, agent simulation)
* Worth experimenting in render-driven or system-driven contexts
* Do not ship as primary renderer until Safari support is solid

---

# Memory management: the universal 3D footgun

Every Three.js resource that allocates GPU memory must be explicitly disposed.

## What needs disposal

| Object | Method | When |
|--------|--------|------|
| `BufferGeometry` | `.dispose()` | When mesh is removed |
| `Material` | `.dispose()` | When mesh is removed; once per shared material |
| `Texture` | `.dispose()` | When material is disposed or texture replaced |
| `RenderTarget` | `.dispose()` | When pass is removed from effect composer |
| `WebGLRenderer` | `.dispose()` | When renderer is destroyed |

## What does NOT auto-dispose

* Removing a mesh from the scene does not dispose its geometry, material, or textures.
* Replacing `mesh.material` does not dispose the old material.
* `renderer.dispose()` does not cascade to scene objects.

## Tracking pattern

```ts
class DisposableTracker {
  private items: { dispose(): void }[] = [];
  track<T extends { dispose(): void }>(item: T): T {
    this.items.push(item);
    return item;
  }
  disposeAll() {
    this.items.forEach(i => i.dispose());
    this.items = [];
  }
}
```

Attach one tracker per scene chunk, NPC, or loaded GLTF group. Call `disposeAll()` when unloading.

## Monitoring in dev

```ts
console.log(renderer.info.memory);
// { geometries: N, textures: N }
```

Watch these numbers as scenes load and unload. A monotonically increasing count means leaks.

---

# Draw call budget

3D games can tank frame rate with too many draw calls before GPU cost is even the bottleneck.

## Rules of thumb

* 100–500 draw calls: generally fine across all target hardware
* 500–1000: acceptable on desktop, watch on mobile
* 1000+: audit your batching strategy

## Techniques to reduce draw calls

| Problem | Solution |
|---------|----------|
| Many identical meshes | `THREE.InstancedMesh` |
| Many static objects | `BufferGeometryUtils.mergeGeometries()` |
| Many small textures | texture atlas |
| Many small transparent objects | sort and batch manually or use sprite systems |

## Shadow maps multiply draw calls

Each shadow-casting light adds a full render pass. Three directional lights with shadows = 3× the scene rendered just for shadows. Use sparingly.

---

# Lighting strategy: baked vs dynamic

| Approach | Cost | Quality | Dynamism | When to use |
|----------|------|---------|----------|-------------|
| Baked lightmaps | ~0 runtime | Highest | None (static) | Static scenes, experiences, open world backgrounds |
| Environment map (HDR PMREM) | Very low | High for reflections | Can swap per zone | Almost always should be used |
| Single directional + shadow | Low-medium | Good | Yes | Outdoor scenes, day/night |
| Multiple point/spot lights | High | Good | Yes | Only where locally needed |
| Dynamic GI | Very high | Best | Yes | WebGPU path only; not for most games |

Recommendation for most games: baked lightmaps for static geometry + one directional with shadow + HDR environment map. This delivers high quality at low runtime cost.

---

# When browser APIs are overkill

## Do not reach for WebGPU when

* the game works well in WebGL2
* you are not doing compute shaders or mesh shaders
* target platforms include Safari (limited WebGPU support as of 2025)

## Do not use Workers for Three.js rendering

* WebGL rendering must happen on the main thread (or the OffscreenCanvas worker it was initialized on)
* Workers are for simulation, AI, physics, and asset processing

## Do not use InstancedMesh for low counts

* Below ~50–100 objects, the API overhead may not be worth it
* Regular meshes are simpler and fine at small counts

## Do not use React Three Fiber for physics hot loops

* Each frame-driven mutation triggers React reconciliation overhead
* For physics-heavy or high-entity-count games, direct Three.js mutation is more efficient

## Do not use shared physics for purely visual animations

* Physics bodies are expensive; CSS-like spring animations or GSAP are better for UI effects
* Reserve physics for objects that actually interact with the game world

---

# Starter architecture by category

## Render-driven

* TS + Vite + Three.js
* GLTFLoader + DRACOLoader + KTX2Loader
* EffectComposer with 2–3 passes max
* DisposableTracker per loaded scene
* PMREMGenerator for environment maps
* No physics, no network, no WASM

## Control-driven

* TS + Vite + Three.js
* Rapier (`@dimforge/rapier3d-compat`)
* Fixed timestep loop + render interpolation
* AnimationMixer + state machine
* Custom camera springarm
* Pointer Lock for FPS or OrbitControls-derived for TPS

## System-driven

* TS + Vite + Three.js
* Worker for simulation tick
* InstancedMesh per unit type
* IndexedDB via Dexie for world saves
* React DOM for UI panel overlay
* Consider WASM only after profiling

## Content-driven

* TS + Vite + Three.js + React DOM
* Chunk streaming with strict dispose discipline
* Draco + KTX2 everywhere
* JSON content schema validated at build time
* IndexedDB + versioned save migrations
* Service worker for visited chunk caching

## Physics-driven

* TS + Vite + Three.js + Rapier
* Fixed timestep with mesh interpolation
* Physics world as position authority
* Body + mesh disposal lifecycle paired together
* Web Audio collision-intensity audio system

## Network-driven

* TS + Vite + Three.js + WebSocket
* Binary protocol (msgpack or custom DataView)
* Authoritative Node.js server with Rapier WASM
* Client prediction + snapshot interpolation with quaternion slerp
* Observability (RTT, desync rate) from day one
