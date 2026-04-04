# 1. Render-driven games and experiences

Examples:

* WebGL demos and interactive art
* product configurators and architectural visualizations
* walking simulators and experience-first games
* museum / gallery experiences
* shader-heavy tech demos
* procedurally generated world showcases

Their main challenge is **visual fidelity, material quality, and GPU performance at scale**.

---

## 1. Package dependencies

### Good default dependencies

* **Three.js** directly — no additional abstraction needed unless team is React-native
* **@react-three/fiber** + **@react-three/drei** if the scene is component-tree-friendly and team knows React deeply
* **three/examples/jsm/postprocessing/EffectComposer** or **postprocessing** (npm) for effect pipelines
* **@dimforge/rapier3d-compat** only if interactive physics is involved
* **leva** for runtime shader/scene parameter tweaking during development
* **stats.js** for FPS/memory debug overlay
* GLTF tools: **GLTFLoader**, **DRACOLoader**, **KTX2Loader** — use all three if asset sizes matter

### Avoid by default

* Babylon.js unless you genuinely need its editor or PG (Playground) ecosystem — it is heavier than Three.js for custom pipelines
* React Three Fiber if the scene is fully imperative and animation-heavy with many direct mutations per frame
* Excessive post-processing effects stacked without GPU profiling — bloom + SSAO + depth of field + motion blur together will destroy mobile and mid-tier GPUs

### Why

This category lives or dies on:

* material and lighting correctness (PBR workflow)
* asset pipeline quality (compressed geometry and textures)
* GPU budget awareness

---

## 2. Code design and shader trade-offs

## Recommended code design

Organize around the **scene state**, not the render loop:

* `SceneBuilder` — loads GLTF, places objects, sets lighting
* `MaterialLibrary` — canonical materials, shared across instances
* `AnimationMixer` — centralized, updated each frame from one place
* `PostStack` — effect composer configuration
* `CameraRig` — handles transitions, cinematic paths, orbit vs free

Avoid:

* mutating `mesh.position` from everywhere in the codebase
* creating new `THREE.Vector3()` inside the render loop (allocation = GC pressure)
* cloning materials per object when sharing is possible

### Shader design

PBR first. Custom GLSL second.

Use `THREE.MeshStandardMaterial` or `THREE.MeshPhysicalMaterial` before writing custom shaders. The built-in PBR is solid.

When you need custom behavior, prefer:

* `onBeforeCompile` injection over fully custom `ShaderMaterial` — lets you extend the standard shader without rewriting lighting

```ts
material.onBeforeCompile = (shader) => {
  shader.uniforms.myUniform = { value: 0 };
  shader.fragmentShader = shader.fragmentShader.replace(
    '#include <output_fragment>',
    myInjection + '\n#include <output_fragment>'
  );
};
```

Use full `THREE.ShaderMaterial` only when:

* you need a completely non-standard render path
* you are writing a fullscreen effect
* standard material injection isn't sufficient

### Bad pattern: over-shading

Writing custom shaders for everything, including objects that could use PBR, creates a maintenance and portability burden. PBR materials also receive Three.js lighting improvements for free. Custom shaders do not.

---

## 3. System design

## Renderer / core

* one `WebGLRenderer` instance, shared across everything
* `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` — not unlimited; high-DPI screens kill performance on mobile
* `renderer.shadowMap.enabled` only if you have shadow-casting lights; shadow maps are expensive
* use `renderer.info` to track draw calls and triangle counts during development

## Scene graph

* keep the scene graph shallow where possible
* use `THREE.Group` for logical grouping but not deep hierarchy for performance
* large static geometry: merge with `BufferGeometryUtils.mergeGeometries()` to reduce draw calls
* repeated objects: use `THREE.InstancedMesh` — not separate meshes

## Lighting

The biggest quality vs cost lever:

* **Baked lighting** (lightmaps via Blender or Bakery): zero runtime cost, highest quality for static scenes
* **Environment maps** (HDR PMREM): cheap and high quality for reflection/ambient
* **DirectionalLight + shadow map**: one is often enough for a primary sun
* **PointLight / SpotLight**: expensive in Three.js due to per-light draw pass overhead; use sparingly

Avoid:

* many shadow-casting lights
* `RectAreaLight` without understanding it needs a special material
* dynamic GI unless you have a WebGPU path

## Post-processing

Standard stack for a high-quality experience:

1. `RenderPass`
2. `SSAOPass` (optional, expensive)
3. `UnrealBloomPass` or `SelectiveBloomPass`
4. `SMAAPass` or `FXAAPass` for anti-aliasing
5. `OutputPass` for tone mapping and gamma

Check GPU time for each pass. Drop anything that doesn't contribute visually. SSAO + bloom together should be conditional on device capability.

## Asset pipeline

This is critical:

* all geometry: GLTF/GLB + Draco compression (`draco_encoder` CLI or Blender exporter)
* all textures: KTX2 with Basis Universal compression — significant VRAM and download savings
* environment maps: HDR loaded via `RGBELoader`, converted to PMREM via `PMREMGenerator`
* lazy-load assets by scene or area — do not load everything upfront

## Memory management

The most common footgun in this category:

* every `BufferGeometry`, `Material`, and `Texture` must be `.dispose()`d when removed
* track all disposables, especially in scenes that load/unload content
* `renderer.dispose()` does not cascade — you must dispose individually
* use `renderer.info.memory` to watch texture and geometry counts in dev

---

## 4. Browser technology: needed vs not needed

## Needed

* **WebGL2** — baseline; Three.js r163+ defaults to WebGL2
* **requestAnimationFrame**
* **Pointer Events / Pointer Lock** if interactive
* GLTF + Draco + KTX2 toolchain

## Often useful

* **WebGPU** — future; opt-in via `THREE.WebGPURenderer` for compute shaders or mesh shaders, but not production-ready for all targets as of 2025
* **OffscreenCanvas** for rendering in worker if main thread is congested
* **SharedArrayBuffer** if Draco or Basis decode must happen in a worker with transferable output

## Usually not needed

* WASM for gameplay logic (rendering bottlenecks are GPU, not CPU)
* full physics engine unless the experience is interactive
* IndexedDB unless assets or user data need to persist across sessions
* Web Workers for rendering — Three.js render calls must stay on main thread with WebGL
