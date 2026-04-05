# 4. Content-driven games

Examples:

* 3D open-world RPGs and action-RPGs
* narrative adventure games with 3D environments
* 3D visual novel hybrids
* collectible or exploration games with large world maps
* dialogue-heavy games with 3D scenes

Their main challenge is **asset streaming, large world management, data-driven content pipelines, and save versioning**.

---

## 1. Package dependencies

### Good default dependencies

* **Three.js** for the 3D world view
* **React** + DOM for menus, inventory, dialogue, character sheets, maps — not WebGL
* **GLTFLoader** + **DRACOLoader** + **KTX2Loader** — the standard asset pipeline triad
* **Dexie** or direct IndexedDB for large save data and chunk caches
* schema validation lib (Zod, Ajv) for content definitions — catch schema drift early
* localization tooling if multi-language
* optional: a scripting runtime for dialogue/quests — can be a simple JSON command interpreter

### Avoid by default

* giant inheritance hierarchies for NPCs (`class Merchant extends ShopNPC extends TalkableNPC`) — data-driven composition handles this better
* hardcoding any content (item stats, quest flags, dialogue) in TypeScript code
* loading all GLTF assets upfront — a large open world cannot fit in memory or tolerate long initial loads
* Babylon.js unless you actively need its scene serializer or PG ecosystem

### Why

This category lives or dies on:

* tooling and content pipeline quality
* how robustly saves survive version changes
* how well assets stream in without stalls

---

## 2. Code design and WASM trade-offs

## Recommended code design

All content as data:

* items: JSON definitions → runtime entity composed from definition + save state
* quests: state machine definitions loaded from data, not hardcoded transitions
* NPCs: behavior config, dialogue graph ref, loot table — not subclasses
* dialogue: graph structure with conditions referencing quest/inventory state
* skills/effects: effect handler registry keyed by string — `"deal_damage"`, `"apply_buff"`, `"spawn_object"`

For the world:

* chunk the world into grid cells, each chunk a GLTF file with its geometry and object placement metadata
* stream in chunks based on player proximity, stream out and dispose distant ones
* chunk streaming: load assets async, track reference counts, dispose geometry + textures on unload

### Dispose-on-unload pattern

This category has the most memory leak risk. Establish a pattern early:

```ts
function unloadChunk(chunk: Chunk) {
  for (const obj of chunk.objects) {
    obj.geometry.dispose();
    if (Array.isArray(obj.material)) {
      obj.material.forEach(m => {
        m.map?.dispose();
        m.normalMap?.dispose();
        m.dispose();
      });
    } else {
      obj.material.map?.dispose();
      obj.material.dispose();
    }
    chunk.scene.remove(obj);
  }
}
```

Without this, every chunk load permanently increases GPU VRAM usage.

## WASM?

Low priority.

### When WASM can help

* procedural generation for terrain or dungeon layout
* advanced pathfinding in a large world graph
* heavy simulation inside a minigame

For most content-driven games, the real bottlenecks are:

* save loading / parsing speed
* asset decompression latency
* UI interaction complexity
* localization string processing

Not CPU arithmetic.

---

## 3. System design

## Engine / runtime

Should support:

* scene transitions between outdoor areas, dungeons, towns
* trigger zones that activate quests, music, NPC states
* cutscene / scripted sequence system
* save checkpoints with snapshot semantics
* time-of-day cycle (if present)

## Content layer

The most important module:

* item database — validate at build time, not runtime
* quest database — each quest a state machine with condition references
* NPC definitions — dialogue graph ID, faction, schedule
* world map metadata — chunk boundaries, streaming hints, area names
* skill / effect definitions
* localization strings

Validate content against schemas as a CI step. A content bug shipped to players is expensive.

## Scripting

For quests and dialogue:

* simplest acceptable approach: JSON arrays of `{ type, args }` commands executed by a runtime
* avoid embedding a full scripting language unless the team has dedicated narrative designers who author it
* common command types: `SetFlag`, `GiveItem`, `ShowDialogue`, `TriggerCutscene`, `PlaySound`, `MoveNPC`

## Chunk streaming

* player position → set of desired chunk IDs
* desired vs loaded → queue load/unload
* each chunk: async GLTF load → parse → add to scene
* unload: remove from scene → dispose all geometry/materials/textures
* monitor `renderer.info.memory` to verify chunks are actually being freed

## Render

* world view: Three.js, chunks of static geometry, instanced foliage and props
* NPCs: GLTF skeletal meshes with LOD by distance
* camera: third-person spring arm or fixed cinematic depending on scene type
* UI: React DOM overlaying the canvas for all menus and inventory

## Audio

* music state machine: explore track → combat track → cutscene track
* ambience zones per area chunk
* NPC voice hooks (event-triggered) if audio is dubbed
* footstep material detection via physics raycast down

## Asset pipeline

Major module:

* all meshes: GLTF/GLB + Draco
* all textures: KTX2 basis for VRAM compression
* streaming manifest: JSON listing which assets belong to which chunk
* asset reference checker: build-time tool that catches broken asset paths before release

## Save system

One of the most important and risky modules:

* save slots with timestamps and preview data
* serialized: quest flags, inventory, player position, time of day, NPC states
* versioned migrations — every save format change needs a migration path
* auto-save at safe points (not mid-combat, not mid-cutscene)
* consider event log replay for debugging corrupt saves

## Tools

Essential:

* dialogue previewer that runs without the 3D world
* quest flag inspector and state visualizer
* save format explorer
* content validator CLI
* asset manifest checker

---

## 4. Browser technology: needed vs not needed

## Needed

* **IndexedDB** for chunk caches and large save data
* **GLTFLoader + DRACOLoader + KTX2Loader** pipeline
* **WebGL2** for Three.js
* **Web Audio API** for spatial audio and music system

## Often useful

* **Service Worker** for asset caching — large worlds benefit from caching previously visited chunks
* **Web Workers** for GLTF parsing, localization preprocessing, background save serialization
* **File System Access API** for developer tools (local content editing, not player-facing)
* **CompressionStream** for save data compression

## Usually not needed

* WASM for content-layer logic
* heavy GPU features (WebGPU, SSAO, complex post-processing) — this category's bottleneck is content, not rendering
* SharedArrayBuffer unless parallel asset decode pipelines are needed
* full physics stack unless the gameplay genuinely requires it
