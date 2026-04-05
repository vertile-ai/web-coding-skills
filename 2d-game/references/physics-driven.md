# 5. Physics-driven games

Examples:

* rope games
* destructible toys
* physics sandboxes
* vehicle/balance games
* projectile-emergent games

Their main challenge is **stable simulation and performance under many interacting bodies**.

---

## 1. Package dependencies

### Good default dependencies

* **matter-js**, **planck.js**, or another browser-suitable physics library
* renderer: Pixi or Canvas
* audio library
* maybe geometry utils

### Avoid by default

* mixing multiple physics systems
* forcing gameplay logic across both custom collision and full physics unless carefully separated
* huge general engine stack with hidden update ordering

### Why

Physics-driven games need very controlled timing and state ownership.

---

## 2. Code design and WASM trade-offs

## Recommended code design

The physics world is often the runtime center.

Pattern:

* gameplay issues commands
* physics world steps
* post-step gameplay resolves events
* render reads body transforms

Use:

* fixed timestep
* collision layers/masks
* separate physical state and visual FX state

## WASM?

This is a category where WASM can make sense, but still not always necessary.

### Use WASM if

* many bodies
* advanced constraints
* soft body or custom solver work
* existing native physics code

### Don't use it just for branding

JS physics libs are often enough for 2D web games if object counts are reasonable.

The first optimizations should be:

* reduce active body count
* sleeping bodies
* collision filtering
* chunk activation
* lower solver complexity

---

## 3. System design

## Engine / loop

Absolutely needs:

* fixed timestep
* careful update order
* deterministic-ish stepping
* pause / slow motion support

## Physics module

Heart of the game:

* world creation
* body lifecycle
* collision layers
* trigger callbacks
* constraints/joints
* raycasts if needed

## Gameplay layer

Should not directly hijack physics truth too freely.
It should:

* apply impulses/forces/commands
* read collision outcomes
* spawn effects
* update score/progression

## Visual layer

Often has:

* interpolation
* debris sprites
* trails
* impact bursts

## Audio

Physics-linked audio is important:

* collision intensity -> sound volume/variant
* rolling/sliding loops
* break/crash layers

## Asset pipeline

Moderate complexity:

* bodies/shapes config
* joint definitions
* destructible pieces
* effect atlases

## Save

Depends on game:

* level progress may be simple
* sandbox world saves can get large

If sandbox-heavy, save needs:

* object snapshots
* versioning
* compression

---

## 4. Browser technology: needed vs not needed

## Needed

* Canvas or WebGL
* requestAnimationFrame
* Web Audio
* local save storage

## Often useful

* Web Workers for level generation or background processing
* WASM if physics scale demands it
* OffscreenCanvas in advanced setups

## Usually not needed

* React for core in-world render
* complex DOM-heavy scene composition
* SharedArrayBuffer unless doing very advanced parallel simulation
