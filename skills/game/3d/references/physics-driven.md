# 5. Physics-driven games

Examples:

* vehicle and racing simulations
* destruction and demolition sandboxes
* physics puzzle games
* ragdoll and cloth games
* soft-body and fluid toy experiences
* Kerbal-style building and flight games

Their main challenge is **stable 3D physics simulation, object lifecycle management, visual-physical synchronization, and performance under many active bodies**.

---

## 1. Package dependencies

### Good default dependencies

**Rapier** (`@dimforge/rapier3d-compat`) — strong default choice:

* WASM-based, significantly faster than pure-JS options
* good API design: shapes, joints, character controller, raycasts
* actively maintained, good browser support
* deterministic (same seed → same result)

**Cannon-es** — the pure-JS alternative:

* easier to debug (plain JS, readable stack traces)
* slower under many bodies
* good for games where physics is present but not the core stress test

**Ammo.js** / **Jolt Physics WASM** — for advanced scenarios:

* Ammo.js: Bullet physics port — huge feature set, complex API
* Jolt: newer, excellent performance, growing adoption
* both have steeper integration cost
* use only if Rapier's features are genuinely insufficient

### Avoid by default

* Cannon.js (original, unmaintained) — use Cannon-es instead
* building a custom physics solver for general-purpose 3D — the math complexity is extreme
* running physics and render in the same tight loop without interpolation — visual jitter is the result

### Physics lib trade-off summary

| Library | Speed | API Quality | Debuggability | Best Use |
|---------|-------|-------------|----------------|----------|
| Rapier | Excellent | Good | Moderate (WASM) | Default for most games |
| Cannon-es | Fair | Good | Easy (pure JS) | Small-scale, simpler games |
| Ammo.js | Good | Complex | Hard (WASM) | Feature-heavy simulation |
| Jolt | Excellent | Good | Moderate (WASM) | Heavy load, vehicle sims |

### Avoid by default (usage patterns)

* mixing two physics systems — they have separate worlds and time steps, reconciling them is painful
* using physics for objects that do not need it (static scenery, UI elements, particle effects)

---

## 2. Code design and WASM trade-offs

## Recommended code design

The physics world is the runtime authority for object positions.

Canonical flow per frame:

1. **Pre-step**: apply player/game commands as forces, impulses, or velocity mutations
2. **Physics step**: `world.step()` at fixed timestep
3. **Post-step**: read body positions and rotations, apply to Three.js meshes
4. **Render**: Three.js render

```ts
// Per frame:
world.step(); // Rapier steps internally at fixed rate

for (const [rigidBody, mesh] of syncPairs) {
  const pos = rigidBody.translation();
  const rot = rigidBody.rotation();
  mesh.position.set(pos.x, pos.y, pos.z);
  mesh.quaternion.set(rot.x, rot.y, rot.z, rot.w);
}
```

This means Three.js meshes are **driven by physics**, not the other way around.

### Interpolation

Fixed-timestep physics can render at a different FPS. Without interpolation, visual jitter appears.

Pattern: store previous and current physics state, interpolate mesh positions by the fractional elapsed time:

```ts
const alpha = accumulatedTime / fixedStep;
mesh.position.lerpVectors(prevPos, currPos, alpha);
```

Rapier's fixed-step accumulator handles this internally; check its docs for the recommended pattern.

### Body lifecycle

The most common mistake after correctness: **not removing unused physics bodies**.

Every vehicle, debris chunk, and ragdoll that is created must be explicitly removed:

```ts
world.removeRigidBody(body);
world.removeCollider(collider);
```

In addition, the corresponding Three.js mesh must be disposed:

```ts
mesh.geometry.dispose();
mesh.material.dispose();
scene.remove(mesh);
```

Track active physics bodies. Implement a pool or cap for destruction debris — do not spawn unlimited bodies.

### Joints and constraints

Use Rapier's joint API for vehicles (axles), hinges (doors), ropes, and chains:

* `RevoluteJoint` — single-axis rotation (wheels, hinges)
* `PrismaticJoint` — linear slide (suspension)
* `SphericalJoint` — ball socket (ragdoll joints)
* `FixedJoint` — rigid weld between bodies

Tune damping and stiffness parameters. Joints with no damping will oscillate and explode.

## WASM considerations

Rapier is already WASM. You are already there.

Custom WASM beyond Rapier is rarely needed. Exceptions:

* custom fluid simulation
* soft-body physics not covered by the chosen lib
* massive multi-body constraint solving beyond what the lib provides

---

## 3. System design

## Engine / loop

Absolutely needs:

* fixed timestep step (e.g., 1/60s or 1/120s) with accumulator and interpolation
* deterministic seeding if you need replay
* pause and slow-motion support — expose a time scale multiplier applied to the step size
* physics wireframe debug view during development — Rapier has a debug renderer

## Physics module

* `PhysicsWorld` — wraps `Rapier.World`, owns all bodies and colliders
* body registry — map from game entity ID to `RigidBodyHandle`
* shape definitions — centralize common shapes (sphere, box, capsule) for reuse
* event callback — Rapier's event queue for collision start/end events
* sleeping — let Rapier put idle bodies to sleep; do not force-awaken everything each tick

## Gameplay layer

Issues commands to physics; does not mutate positions directly:

* apply impulse on hit
* apply torque on input
* spawn debris as new bodies
* read collision outcomes → trigger sound, score, visual FX

## Visual layer

* read rigid body transforms each frame → update mesh transforms
* interpolation buffer for smooth rendering
* destruction: pre-fractured meshes swapped in and spawned as separate bodies on impact
* particle effects triggered by collision event intensity

## Audio

Physics-responsive audio is what makes this category feel real:

* collision intensity (relative velocity magnitude) → volume and pitch variant selection
* material-aware: metal vs wood vs glass collision sounds
* rolling/sliding loops with volume tied to contact speed
* vehicle engine pitch tied to wheel angular velocity

## Vehicle simulation

If the game has vehicles, Rapier's vehicle controller or a joint-based approach:

* chassis rigid body + wheel colliders
* suspension: `PrismaticJoint` with spring parameters
* steering: apply torque or directly set wheel angle
* engine force: apply force to chassis in forward direction

Avoid trying to simulate vehicles purely with impulses on a single body — the results are unrealistic and hard to tune.

## Asset pipeline

* rigid body shapes defined in GLTF extras metadata or a separate JSON config
* pre-fractured destruction meshes — each piece has its own GLTF mesh and a corresponding physics shape definition
* shape simplification: convex hulls for irregular objects, compound shapes for complex geometry — exact mesh colliders are expensive

## Save

Depends on game type:

* puzzle-level games: save level state (positions and rotations if needed), progress flags
* sandbox games: can be expensive — serialize all active body transforms and types

For sandbox saves: limit what is serialized; do not attempt to save fluid simulation or large debris fields.

---

## 4. Browser technology: needed vs not needed

## Needed

* **WebGL2** (Three.js default)
* **WASM** — Rapier is WASM; this is not optional
* **requestAnimationFrame** with fixed-step accumulator
* **Web Audio API** for physics-responsive sound

## Often useful

* **Web Workers** for physics simulation if you want to offload from main thread (complex with Rapier but possible via WASM worker)
* **SharedArrayBuffer** for zero-copy data exchange between physics worker and render thread
* **OffscreenCanvas** if render is also moved to worker

## Usually not needed

* React or DOM-heavy rendering for the in-world view
* complex content management systems (this is about physics, not story)
* IndexedDB unless the sandbox or puzzle save state is large
* WebGPU unless you need GPU-side physics (not common for browser games yet)
