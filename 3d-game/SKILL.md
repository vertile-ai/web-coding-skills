---
name: coding-skills-web-3d-game
description: Used when developing web based 3D game. Covers renderer selection, scene graph design, asset pipeline, memory management, shader strategy, physics integration, and browser API trade-offs across six 3D game drives: render, control, system, content, physics, and network. Use when designing or building any browser-based 3D game, choosing between Three.js and Babylon.js, planning camera rigs, handling GLTF assets, managing GPU memory, or deciding on physics libs and multiplayer architecture.
---

# Web 3D game playbook

## Shared baseline for almost all web 3D games

The 3D baseline is heavier than 2D. Extra concerns from the start:

* **GPU memory lifecycle**: geometry, materials, and textures must be explicitly disposed — not just garbage collected.
* **Draw call budget**: browsers are sensitive to thousands of draw calls. Design for batching from day one.
* **Asset pipeline**: GLTF/GLB + Draco compression + KTX2 textures is the standard. Raw OBJ or uncompressed PNG at scale is a warning sign.

## Core baseline stack

Usually:

* **TypeScript**
* **Vite** or similar fast bundler
* **Three.js** (default) or **Babylon.js** (if you want a full engine, strong editor, or better mobile GPU support)
* **@react-three/fiber** + **@react-three/drei** only when the game is heavily component-tree structured and teams are React-fluent — not by default
* **Howler.js** or Web Audio API positional audio for spatial sound
* **Rapier** (WASM, via `@dimforge/rapier3d-compat`) or **Cannon-es** for physics if needed
* **zustand** or a custom event bus for game state outside the Three.js scene graph
* **IndexedDB** for non-trivial saves or world data
* **Web Workers** for expensive simulation, AI, or world generation tasks

## Base module split

* `core/` — loop, timing, events, IDs, random
* `game/` — game rules and simulation
* `render/` — renderer, camera, scene, lights, post-processing, shaders
* `memory/` — geometry pools, texture caches, disposal tracking
* `audio/` — spatial sound, music, SFX mixer, ambient zones
* `assets/` — GLTF loaders, Draco/KTX2 decoders, texture cache, manifests
* `input/` — keyboard, mouse, Pointer Lock, gamepad, touch
* `physics/` — physics world, body lifecycle, constraints, raycasts
* `ui/` — HUD, menus, overlays (often DOM/React over canvas)
* `save/` — serialization, versioning, storage
* `net/` — if multiplayer
* `tools/` — debug overlays, stats, physics wireframes, profilers

## Good general rule

Do **not** start with React Three Fiber + Rapier + custom GLSL shaders + ECS + multiplayer simultaneously. Each adds real complexity. Pick the minimum per-category and expand only when clearly needed.

The single most common 3D web game mistake is **GPU memory leaks**: Three.js objects are not automatically freed. Always call `.dispose()` on geometry, materials, and textures when removing objects from the scene.

## Category references

Pick the one that matches the game's dominant challenge:

| Drive | Main challenge | Reference |
|-------|----------------|-----------|
| Render | Visual quality, PBR materials, post-processing, large static scenes | [render-driven.md](references/render-driven.md) |
| Control | Camera rig, collision response, animation blending, input feel | [control-driven.md](references/control-driven.md) |
| System | Scale, instancing, LOD, chunk streaming, background simulation | [system-driven.md](references/system-driven.md) |
| Content | Asset streaming, large worlds, data-driven NPCs and items, save versioning | [content-driven.md](references/content-driven.md) |
| Physics | Stable simulation, rigid bodies, constraints, visual feedback | [physics-driven.md](references/physics-driven.md) |
| Network | Authority, 3D state sync, transform interpolation, prediction | [network-driven.md](references/network-driven.md) |

For renderer selection, memory management rules, shadow cost, draw call budget, WebGPU readiness, and starter architectures per category, see [cross-category.md](references/cross-category.md).
