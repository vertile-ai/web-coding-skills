# 4. Content-driven games

Examples:

* RPGs
* visual novels
* adventure games
* farming/life sims
* dialogue-heavy games
* collectible-heavy progression games

Their main challenge is **content scale, persistence, and authoring pipelines**.

---

## 1. Package dependencies

### Good default dependencies

* renderer: Phaser or Pixi for world view
* React/DOM UI for menus, inventory, dialogue, meta screens
* schema validation for content definitions
* text/layout tools
* audio package
* IndexedDB wrapper
* localization tooling
* maybe scripting/interpreter tools

### Avoid by default

* giant inheritance hierarchies
* hardcoded content in code
* engine plugins that lock content flow into opaque editor formats unless that editor is central to your workflow

### Why

These games live or die on data quality and tooling.

---

## 2. Code design and WASM trade-offs

## Recommended code design

Use:

* **data-driven domain models**
* content definitions in JSON/YAML/DB-like format
* event-driven progression updates
* scriptable dialogue/cutscene systems
* runtime entities composed from content + state

For example:

* items as data + effect handlers
* quests as state machines
* dialogue as graph definitions
* enemies as templates + behavior config

Do not build everything as subclasses.

## WASM?

Usually low priority.

### When WASM helps

* very heavy procgen
* simulation-heavy subgames
* native engine reuse

But for most RPG/adventure/VN style games, the real problems are:

* content management
* save versioning
* UI flow
* localization
* patching

Not arithmetic throughput.

---

## 3. System design

## Engine / runtime

Should support:

* scene changes
* triggers
* cutscene/dialogue flow
* quest state
* save checkpoints
* inventory/progression

## Content layer

This is crucial:

* item database
* quest database
* NPC definitions
* map metadata
* dialogue trees
* skill/effect definitions
* localization strings

This should be validated before runtime.

## Scripting

Often helpful:

* dialogue conditions
* quest triggers
* cutscene actions
* scripted encounters

Can be:

* simple custom DSL
* JSON actions
* embedded scripting
* command/event chain system

## Render

Depends on subtype:

* top-down map
* side-view adventure scenes
* VN layering
* UI-heavy menus

## Audio

* music state system
* ambience zones
* dialogue beep/voice hooks
* event themes

## Asset pipeline

This is a major module:

* character portraits/sprites
* maps/tilesets
* dialogue portraits
* localization assets
* item icons
* audio banks

## Save

One of the most important modules.
Needs:

* compact serialization
* migration/versioning
* quest flags
* inventory
* map state
* checkpoints
* maybe rollback/replay for debugging

## Tooling

Very valuable:

* dialogue previewer
* quest debugger
* save inspector
* content validator
* asset reference checker

---

## 4. Browser technology: needed vs not needed

## Needed

* IndexedDB
* Canvas/WebGL if world view exists
* DOM/React often very useful for UI-heavy layers
* Web Audio API

## Often useful

* File System Access API for internal dev tools or local editors, not for all players
* Service worker for asset caching if the game is large
* Web Workers for localization preprocessing, procgen, or background data prep

## Usually not needed

* WASM early on
* advanced GPU features
* SharedArrayBuffer
* heavy physics stack unless hybrid gameplay needs it
