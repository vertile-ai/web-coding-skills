# 1. Control-driven games

Examples:

* platformers
* shooters
* fighting games
* action roguelites
* twitch top-down action

Their main challenge is **tight input + frame consistency + collision + game feel**.

---

## 1. Package dependencies

### Good default dependencies

* **Phaser** or **PixiJS**

  * Phaser if you want batteries included
  * Pixi if you want more control over engine structure
* **Howler.js** for audio
* **matter-js** only if physics is simple and not core to game feel
* small utility libs only if needed:

  * animation helpers
  * object pooling utils
  * vector math helpers

### Avoid by default

* heavy React-driven in-game rendering
* large state-management frameworks for core frame simulation
* giant physics engines unless the game truly depends on them
* too many gameplay plugins

### Why

This category needs:

* predictable loop
* minimal overhead
* easy control of update order

The more framework abstraction you add, the harder it gets to tune feel.

---

## 2. Code design and WASM trade-offs

## Recommended code design

Use:

* **component-based game objects** or **small ECS**
* **fixed timestep simulation**
* **state machines** for characters and weapons
* explicit separation of:

  * input sampling
  * simulation update
  * collision resolution
  * render interpolation

A very common good structure:

* `InputSystem`
* `MovementSystem`
* `CollisionSystem`
* `CombatSystem`
* `AnimationSystem`
* `RenderSystem`

For smaller games, classic OOP can still work:

* `Player`
* `Enemy`
* `Projectile`
* `Pickup`

But once combat interactions grow, move toward systems rather than stuffing logic into classes.

## WASM?

Usually **not needed** at first.

### Use WASM only if

* you already have existing native code
* you need very high-performance pathfinding or geometry
* you have a custom collision/physics solver that is proven hot
* you are doing many AI agents or advanced simulation inside the action game

### Do not use WASM just because

* the game is "action"
* you think JS is automatically too slow

For most browser 2D action games, the real bottlenecks are:

* bad allocation patterns
* too many draw calls
* poor sprite batching
* bad collision broadphase
* too many objects alive at once

Not raw JS arithmetic.

---

## 3. System design

## Engine / core

Needs:

* fixed timestep loop
* pause / slow motion hooks
* deterministic-enough local update
* frame profiler / debug overlay

## Input

Very important:

* keyboard, mouse, touch, maybe gamepad
* input buffering
* action mapping, not raw key logic everywhere
* separate "pressed this frame" vs "held"

## Physics / collision

Usually:

* custom AABB / tile collision for platformers
* lightweight broadphase grid or quadtree
* custom hitbox/hurtbox logic for fighters/shooters
* avoid full general-purpose physics unless the game really needs emergent physics

## Visual / render

* sprite batching
* camera follow and shake
* layered rendering
* animation state synced to simulation state, not vice versa

## Effects

* particles
* trails
* flashes
* screen shake
* hit stop

These are crucial for feel, but should be **presentation-only**, not part of game truth.

## Audio

* low-latency SFX triggering
* ducking between music and SFX if needed
* preload frequently used short sounds

## Asset pipeline

* texture atlases
* sprite sheets
* animation metadata
* lazy-load levels if content is large

## Save

Usually simple:

* settings
* progression
* unlocked content
* maybe run history

Avoid serializing the entire runtime object graph unless needed.

---

## 4. Browser technology: needed vs not needed

## Needed

* **Canvas 2D** for simple games, **WebGL/Pixi/Phaser** for busier ones
* **requestAnimationFrame**
* **Web Audio API**
* **Pointer/Keyboard/Gamepad APIs**
* **localStorage** or **IndexedDB** for saves

## Sometimes needed

* **Web Workers** for level generation or expensive AI
* **OffscreenCanvas** if rendering architecture is advanced
* **Fullscreen API**
* **Vibration API** on supported mobile contexts

## Usually not needed

* Service worker beyond basic hosting/offline packaging
* WASM
* SharedArrayBuffer
* WebRTC
* WebGPU, unless you have lots of effects or massive sprite counts
