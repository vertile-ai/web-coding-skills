---
name: web-coding-skills-2d-game
description: Used when developing web based 2D game. Covers dependencies, code patterns, module design, WASM/Worker/WebGL trade-offs, and browser APIs for all six web 2D game drives: control, system, rule, content, physics, and network. Use when designing or building any browser-based 2D game, choosing a renderer, planning a sim or netcode architecture, or deciding on saves, assets, and tooling.
---

# Web 2D game playbook

## Shared baseline for almost all web 2D games

Before category-specific advice, most web 2D games share this baseline.

## Core baseline stack

Usually:

* **TypeScript**
* **Vite** or similar fast bundler
* **Canvas 2D** or **WebGL/WebGPU-backed framework**
* **Howler.js** or direct Web Audio API for sound
* **zustand / custom store / event bus** for game state coordination
* **IndexedDB** for save/cache if the game stores non-trivial data
* **Web Workers** only when there is real heavy background work

## Base module split

A good universal split is:

* `core/` — loop, timing, random, IDs, events
* `game/` — game rules/simulation
* `render/` — renderer, camera, animation, particles
* `audio/` — music, SFX, mixer, audio state
* `assets/` — loading, caching, atlases, manifests
* `input/` — keyboard, mouse, gamepad, touch
* `ui/` — menus, HUD, overlays
* `save/` — serialization, versioning, storage
* `net/` — if multiplayer
* `tools/` — debug tools, editors, profilers, replay tools

## Good general rule

Do **not** start with WASM, ECS, Workers, WebGL custom pipelines, or multiplayer infra unless the category truly needs them.

A lot of web games get worse because they over-adopt architecture meant for a different class of game.

## Category references

Pick the one that matches the game's dominant challenge:

| Drive | Main challenge | Reference |
|-------|---------------|-----------|
| Control | Tight input, frame consistency, collision, game feel | [control-driven.md](references/control-driven.md) |
| System | Scale of simulation, many agents, background compute | [system-driven.md](references/system-driven.md) |
| Rule | Correct state transitions, testability, undo/replay | [rule-driven.md](references/rule-driven.md) |
| Content | Content scale, persistence, authoring pipelines | [content-driven.md](references/content-driven.md) |
| Physics | Stable simulation, performance under many bodies | [physics-driven.md](references/physics-driven.md) |
| Network | Authority, synchronization, latency, cheating risk | [network-driven.md](references/network-driven.md) |

For cross-category comparisons, module recommendations, browser API overkill rules, and starter architectures, see [cross-category.md](references/cross-category.md).
