---
name: web-coding-skills-domain-event-pubsub
description: Used when building domain-event pub/sub modules for web applications with versioned contracts and idempotent consumers.
---

# Domain Event Pub/Sub playbook

## Purpose / category boundary

Application-domain event pub/sub module for producer/consumer decoupling, event contract versioning, and idempotent event consumption.

## When to use

- You need asynchronous business-event fanout across modules/services.
- Multiple products share the same event-driven integration pattern.
- You need explicit event schema evolution strategy.

## When not to use

- You need only synchronous request-response orchestration.
- You are solving broker cluster operations and platform-level routing.
- You cannot define stable domain events yet.

## Baseline stack

| Layer | Opinionated default |
|---|---|
| Event contract | Versioned JSON schema + event envelope |
| Backend (Python) | FastAPI/Flask publisher + consumer handlers |
| Backend (JS) | Hono/Express publisher + consumer handlers |
| Broker | Application adapter over Kafka/NATS/SNS/SQS semantics |
| Data | Outbox table + consumer dedupe ledger |
| Observability | Event lineage IDs + consumer lag metrics |

## Module split

- `events/` - event envelope and schema contracts
- `publishers/` - domain event emission rules
- `consumers/` - idempotent handler adapters
- `outbox/` - durable publish handoff
- `registry/` - schema version mapping
- `audit/` - event traceability and replay notes

## Data / workflow model

`domain-change -> outbox-write -> publish -> consume -> dedupe-check -> side-effect -> audit`.

Core entities:

- `outbox_event`
- `published_event`
- `consumer_offset`
- `consumer_dedupe_key`
- `event_contract_version`

## Strong opinions / defaults

- Publish from outbox, not directly from mutable request handlers.
- Treat consumers as at-least-once: idempotency is mandatory.
- Break schema compatibility intentionally with explicit version bump and migration note.

## Overengineering warnings

- Avoid event-driven everything; use events where decoupling is needed.
- Do not let transport details leak into domain contract names.
- Avoid speculative schema versions with no consumer rollout plan.

## TS/Python example note

Use TypeScript/Python only.

```ts
type DomainEvent = { type: string; version: number; id: string };
const key = (e: DomainEvent) => `${e.type}:v${e.version}:${e.id}`;
```

```python
def dedupe_key(event_type: str, version: int, event_id: str) -> str:
    return f"{event_type}:v{version}:{event_id}"
```

## References / local reference links

- [Implementation references](references/implementation.md)
- See `docs/taxonomy-manifest.yaml` for manifest proof pointers.
