# 2. Control-driven games

Examples:

* first-person shooters (FPS)
* third-person action and platformers
* racing / driving games
* stealth and combat action
* character-controller exploration games

Their main challenge is **camera rig correctness, collision response, animation blending, and input feel**.

---

## 1. Package dependencies

### Good default dependencies

* **Three.js** — direct, not via R3F, for tighter control of update order
* **Rapier** (`@dimforge/rapier3d-compat`) for character physics — provides a character controller with slope handling, step-up, and coyote-time-friendly queries
* **Cannon-es** as the lighter alternative if the physics are simpler
* **@yomotsu/camera-controls** for third-person camera — handles collision avoidance, orbit smoothing
* **Howler.js** or positional Web Audio for spatial footstep, gunshot, and ambient audio
* small math utilities if needed — Three.js already provides `Vector3`, `Quaternion`, `Euler`

### Avoid by default

* Matter.js or planck.js — these are 2D physics; never the right fit here
* PointerLockControls from Three.js examples for anything beyond a prototype — they provide no physics interaction; build a proper character controller instead
* React Three Fiber for the hot gameplay loop — per-frame scene mutations work against React's batching model
* full ECS architecture from day one for a small action game — the overhead is not justified until entity counts grow

### Why

Control-driven 3D games need:

* deterministic per-frame update order (input → physics → animation → camera → render)
* tight camera-collision interplay
* minimal overhead in the hot path

---

## 2. Code design and WASM trade-offs

## Recommended code design

Separate phases strictly:

1. **Input sampling** — read keyboard, mouse delta, gamepad axes
2. **Character simulation** — apply velocity, call Rapier character controller move, resolve contacts
3. **Animation state machine** — transition based on velocity, grounded state, action flags
4. **Camera update** — follow character, resolve against scene geometry, apply smoothing
5. **Render** — Three.js render call

Do not blend these phases. Do not update the camera inside the physics step.

Example structure:

* `InputMap` — raw device state → normalized action values
* `CharacterController` — wraps Rapier kinematic controller, owns velocity and state
* `AnimationGraph` — state machine with blend trees (idle, walk, run, jump, fall, attack)
* `CameraRig` — springarm-style follow camera with raycast collision
* `CombatSystem` — hitbox raycasts, damage events, hit effects

### Camera rig design

The most underestimated module in this category.

A springarm camera (common in TPS):

```ts
// Every frame:
const desiredPos = character.position.clone()
  .add(offset.applyQuaternion(character.quaternion));
const hit = raycaster.intersectObjects(scene.collidables);
const finalPos = hit.length ? hit[0].point : desiredPos;
camera.position.lerpTo(finalPos, dt * cameraSpeed);
camera.lookAt(character.head);
```

Bad pattern: directly parenting the camera to the character mesh without collision — it will clip into walls.

### Animation blending

Use `THREE.AnimationMixer` with `CrossFadeTo` for transitions.

Common mistakes:

* playing animations without setting a weight — every active `AnimationAction` contributes
* not calling `mixer.update(delta)` — easy to forget when refactoring the loop
* running animation state in response to render, not simulation state — animation should follow physics truth, not drive it

### WASM?

Rapier is already WASM. The question is whether your own game logic needs WASM.

Usually not. The real bottlenecks are:

* raycast volume per frame (broad collision queries)
* skinned mesh with many bones on mid-tier hardware
* large numbers of animated NPC characters simultaneously

Profile before adding custom WASM. JS physics with Rapier handles most single-character or small-cast games fine.

---

## 3. System design

## Engine / core

Needs:

* fixed timestep for physics, variable timestep for render interpolation
* pause support that suspends physics, not just the render loop
* frame profiler — know your physics step time vs render time separately

## Input

* keyboard, mouse delta (Pointer Lock for FPS), gamepad axes
* dead-zone normalization for sticks
* action mapping — `jump`, `attack`, `interact` — not raw key checks scattered everywhere
* distinguish "pressed this frame" vs "held" vs "released"

For FPS:

* request Pointer Lock on canvas click; handle `pointerlockchange` to detect user exit
* accumulate mouse delta across events in the same frame — do not use only the last event

## Character controller

Prefer a **kinematic character controller** (like Rapier's) over a dynamic rigid body for player characters. Dynamic bodies fight against you when you need deterministic step-up, slope limits, and coyote time.

Pattern:

* compute desired velocity from input + gravity
* call `characterController.computeColliderMovement(collider, desiredMovement)`
* apply the corrected movement to the kinematic body

## Collision and raycasting

* keep a list of raycast targets rather than querying the whole scene — `raycaster.intersectObjects(targets)` is O(n) per call
* for weapon hitscan: single raycast per shot, not per frame
* for projectiles: physics body, not frame-by-frame raycasting

## Animation

* one `AnimationMixer` per character
* state machine with explicit transitions — not ad-hoc `if` chains scattered across update
* blend tree for direction-aware locomotion if the game shows character from behind

## Audio

* positional audio is important: `THREE.PositionalAudio` via `THREE.AudioListener` on camera
* footstep audio tied to ground contact events from physics, not to a timer
* preload all short-duration sounds — do not load on demand during combat

## Asset pipeline

* character meshes: GLTF/GLB with skeletal rig and embedded animations
* environment: Draco-compressed static geometry, merged where possible
* texture atlases for environment to reduce draw calls
* LOD meshes for NPCs and background characters if counts grow

## Save

Usually simpler:

* player position and rotation at checkpoint
* progression flags
* inventory if applicable
* settings (keybindings, sensitivity, FOV)

---

## 4. Browser technology: needed vs not needed

## Needed

* **WebGL2** (Three.js default)
* **Pointer Lock API** for FPS mouse input
* **Gamepad API** for controller support
* **requestAnimationFrame** loop
* **Web Audio API** for spatial sound
* **Rapier WASM** for physics

## Sometimes needed

* **Web Workers** for NPC AI pathfinding when many agents are active
* **OffscreenCanvas** for auxiliary render targets (minimaps, portals)
* **Fullscreen API**
* **Vibration API** on mobile
* **IndexedDB** if save data is complex

## Usually not needed

* React Three Fiber — its overhead matters in the hot gameplay loop
* SharedArrayBuffer unless doing very advanced parallel simulation
* WebGPU — Three.js WebGL2 path is sufficient for this category for now
* WASM for game logic (Rapier is already the WASM physics provider)
