---
name: web-coding-skills-video-streaming
description: Used when designing or building a web-based video streaming platform. Covers ingest protocols, transcoding pipelines, adaptive delivery (HLS/DASH), real-time chat, CDN distribution, storage strategy, auth, and scalability. Use when architecting a live or on-demand streaming service, choosing ingest vs delivery protocols, designing a transcoding pipeline, planning CDN/storage, or building a real-time interaction layer (chat, notifications).
---

# Web video streaming platform playbook

## Core mental model

A streaming platform has three distinct data planes that must never be conflated:

* **Ingest plane** — raw, high-bitrate media arrives from the broadcaster (RTMP, SRT, WebRTC WHIP)
* **Processing plane** — raw media is transcoded into multiple quality rungs and packaged into segments (FFmpeg + packager)
* **Delivery plane** — packaged segments are served at scale through a CDN to many concurrent viewers (HLS / DASH)

Real-time interactions (chat, reactions, notifications) ride a completely separate signaling plane (WebSocket) and should never touch the media pipeline.

## Stack baseline

| Layer | Recommended defaults |
|-------|---------------------|
| Ingest protocol | RTMP (universal broadcaster support) or SRT (low-latency, loss-resilient) |
| Transcoding | FFmpeg, AWS MediaLive, or GCP Live Stream API |
| Packaging | HLS (.m3u8 + .ts segments) for broadest compatibility; DASH (.mpd) for DRM-heavy use cases |
| Media player | hls.js (web), ExoPlayer (Android), AVPlayer (iOS) |
| Real-time chat | WebSocket via Socket.IO or native `ws`, backed by Redis pub/sub |
| Auth | OAuth 2.0 / OIDC; short-lived signed tokens for stream URLs |
| CDN | AWS CloudFront, Cloudflare Stream, or Akamai |
| Object storage | AWS S3 or GCS for VOD recordings |
| Database | PostgreSQL for users/metadata; Redis for ephemeral state (viewer counts, chat) |
| Notification push | Firebase Cloud Messaging (FCM) or APNS |

## Architecture components

### Client side

* **Broadcaster app** — captures camera/mic, sends via RTMP or WebRTC WHIP to the ingest edge.
* **Viewer app** — runs an adaptive bitrate (ABR) player that fetches HLS/DASH segments from the CDN.
* Both apps share an auth token issued by the Authentication Service.

### Server side

```text
Broadcaster → [Ingest Edge / RTMP endpoint]
                    ↓
             [Transcoding Worker]  ←── FFmpeg, multiple quality rungs
                    ↓
             [Packager]            ←── Produces HLS/DASH segments
                    ↓
             [Origin Storage]      ←── S3 / GCS bucket (segments + manifests)
                    ↓
                  [CDN]            ←── Edge pops worldwide
                    ↓
               Viewer browser      ←── hls.js / native player

Viewer browser ←→ [WebSocket / Chat Server] ←→ [Redis pub/sub]
```

### Quality rungs (typical ABR ladder)

| Rung | Resolution | Bitrate |
|------|-----------|---------|
| 1080p | 1920×1080 | 4–6 Mbps |
| 720p | 1280×720 | 2–3 Mbps |
| 480p | 854×480 | 1–1.5 Mbps |
| 360p | 640×360 | 600–800 Kbps |
| 240p | 426×240 | 300 Kbps (mobile fallback) |

The player selects the rung automatically based on measured bandwidth.

## Latency tiers

| Mode | Typical delay | Protocol | Use case |
|------|--------------|----------|----------|
| Standard live | 15–30 s | RTMP → HLS (6-s segments) | Sports, concerts |
| Low-latency | 2–5 s | RTMP → LHLS / LL-DASH (1-s chunks) | Live Q&A, gaming |
| Ultra-low | < 500 ms | WebRTC | One-to-one, interactive |

Avoid over-engineering toward ultra-low latency unless the product truly requires it — it multiplies infrastructure cost significantly.

## Module split (server side)

* `ingest/` — RTMP/SRT receiver, stream key validation, rate limiting
* `transcode/` — FFmpeg job queue, quality ladder config, thumbnail extraction
* `package/` — HLS/DASH segment writer, manifest updater, S3 uploader
* `chat/` — WebSocket hub, message fan-out, Redis pub/sub adapter
* `auth/` — token issuance, stream key management, RBAC
* `notify/` — FCM/APNS push, email/webhook fanout
* `api/` — REST/GraphQL gateway for stream metadata, user profiles, subscriptions
* `vod/` — on-demand playback index, recording lifecycle management

## Good general rules

* **Separate ingest from delivery origins** — never let viewer traffic hit the transcoding server.
* **Idempotent segment uploads** — re-uploading a segment to S3 must be safe (use the sequence number as the key).
* **Back-pressure on the transcode queue** — if the queue depth grows, drop quality rungs rather than delay the live edge.
* **Signed CDN URLs** — protect premium streams with short-lived signed tokens; never expose raw S3 bucket URLs.
* **Chat rate-limiting per connection** — always enforce server-side; never trust the client.

## Category references

| Concern | Reference |
|---------|-----------|
| Ingest pipeline & transcoding code | [ingest-transcode.md](references/ingest-transcode.md) |
| HLS delivery, ABR player setup, WebRTC | [delivery-realtime.md](references/delivery-realtime.md) |
| CDN, load balancing, auth, and scalability | [scalability.md](references/scalability.md) |
