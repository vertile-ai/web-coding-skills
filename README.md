## Why Coding Skills

Have you ever faced scenarios like these when working with AI-assisted code?

1. Spent too much time planning
2. Spent too much time requesting small modifications from various angles
3. Spent too much time understanding AI-generated code

If so, `coding-skills` might help. It is a collection of opinionated but battle-tested instructions at the implementation-detail level for different coding languages and frameworks. Sure, you can do spec-driven development — but what if you just want a quick start?

It covers the most common software requirements and provides a bottom-up strategy for AI to build modules. Whether it is a

- Video streaming platform
- 2D game
- 3D game
- Multi-tenant SaaS platform
- Instant messaging application
- ...

you name it! You should always be able to find a skill to start with. If not, we will strive to make it happen for you.

## 2 Major Principles

1. Every skill must be written and verified by a human. AI enhancement is acceptable, but no AI slop.
2. Every skill is battle-tested in a real-world environment.

## Why This Repo May Not Be for You

This repo is not the right fit if you want to pre-design the system architecture before writing any code.

## How It Works

Find the skill that suits your needs and install it using:

```bash
npx skills add https://github.com/vertile-ai/web-coding-skills --skills <replace-with-skill-name>
```

You can find the full list in the [Full List](#full-list) section below.

## Full List

| Skill | Name | Description |
|-------|------|-------------|
| `video-streaming` | Web Video Streaming Platform | Building a web-based video streaming platform. Covers ingest protocols, transcoding pipelines, adaptive delivery (HLS/DASH), real-time chat, CDN distribution, storage strategy, auth, and scalability. |
| `game/2d` | Web 2D Game | Developing a browser-based 2D game. Covers dependencies, code patterns, module design, WASM/Worker/WebGL trade-offs, and browser APIs for all six web 2D game drives: control, system, rule, content, physics, and network. |
| `game/3d` | Web 3D Game | Developing a browser-based 3D game. Covers renderer selection, scene graph design, asset pipeline, memory management, shader strategy, physics integration, and browser API trade-offs across six 3D game drives: render, control, system, content, physics, and network. |
