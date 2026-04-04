# 3. Rule-driven games

Examples:

* puzzle games
* turn-based tactics
* card games
* match-3
* tile roguelikes
* board-like games

Their main challenge is **correct state transition and testability**.

---

## 1. Package dependencies

### Good default dependencies

* minimal renderer: Canvas, Pixi, or even DOM/SVG for some card/board games
* store libs like **zustand** or a custom reducer architecture
* schema validation libraries for content/data
* maybe pathfinding/search libraries
* animation helper libs for polish only

### Avoid by default

* full ECS
* heavy physics engines
* too many game-framework abstractions
* premature multiplayer packages

### Why

This category often benefits from simplicity and pure logic.

---

## 2. Code design and WASM trade-offs

## Recommended code design

This category is ideal for:

* **pure state transition functions**
* **command pattern**
* **event log / replay**
* immutable-ish snapshots where practical

Example shape:

* `GameState`
* `applyCommand(state, command) -> nextState`
* `deriveViewModel(state)`

This makes:

* undo
* replay
* AI search
* testing
  much easier.

## WASM?

Usually not needed.

### Use WASM only if

* your AI search is deep and expensive
* procedural generation is algorithmically heavy
* you have complex solver logic already in native code

Otherwise JS is usually excellent here.

---

## 3. System design

## Engine / core

The "engine" is often very small:

* turn controller
* rules executor
* animation scheduler
* replay/undo manager

## Rules module

This is the heart:

* move validation
* effect resolution
* win/loss checks
* RNG handling
* turn progression

Keep it independent of renderer and sound.

## Render

Can be simple:

* grid/board view
* unit/card widgets
* move previews
* transitions

## Effects

Mostly presentation:

* card transitions
* grid highlights
* impact flashes
* resolve timing animations

## Audio

Simple and event-driven:

* move
* confirm
* damage
* victory/defeat
* ambience/music if needed

## Asset pipeline

Usually lighter than RPG or sim:

* board tiles
* card art
* icons
* small animation sets

## Save

Often extremely valuable:

* turn replay
* match snapshots
* undo
* puzzle progress

Because state is compact, save logic is usually easier.

## AI module

Can be separate and optionally workerized:

* minimax
* heuristics
* puzzle solving
* hint generation

---

## 4. Browser technology: needed vs not needed

## Needed

* Canvas or DOM/SVG depending on style
* localStorage or IndexedDB
* standard input APIs

## Sometimes useful

* Web Workers for AI/hints
* OffscreenCanvas if visuals are surprisingly dense

## Usually not needed

* WASM
* physics
* Web Audio complexity beyond basic use
* SharedArrayBuffer
* WebRTC unless multiplayer
