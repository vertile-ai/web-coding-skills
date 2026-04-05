---
name: web-coding-skills-live-chat
description: Used when building live chat software on the web. Live chat messaging system with tenant/user rooms, agent assignment, and transcript persistence.
---

# Live Chat playbook

## Purpose / category boundary

Live chat messaging system with tenant/user rooms, agent assignment, and transcript persistence.

## When to use

- You need a dedicated product workflow for **live chat**, not a generic SaaS shell.
- Success depends on deterministic state transitions and operator-visible auditability.
- You need opinionated defaults for modules, async boundaries, and failure handling.

## When not to use

- You only need CRUD around one table without workflow complexity.
- Your product is still an umbrella bucket (for example, all-in-one SaaS) with no narrow boundary.
- You cannot yet define category-specific invariants and lifecycle states.

## Baseline stack

| Layer | Opinionated default |
|---|---|
| Frontend | React + TypeScript + TanStack Query |
| Backend | Python FastAPI or Node/TypeScript service with typed DTO boundary |
| Data | PostgreSQL + Redis for ephemeral coordination |
| Async | Queue-backed jobs for side effects and long-running workflows |
| Auth | OIDC/OAuth2 + tenant-scoped RBAC |
| Observability | Structured logs + traces + domain metrics |

Additional category defaults:

- Realtime channel service
- Search index
- Background notification jobs

## Module split

- `api/` - typed endpoints, auth checks, request validation
- `domain/` - business rules, state transitions, invariants
- `workflow/` - orchestration for long-running or compensating actions
- `repo/` - persistence adapters and query objects
- `realtime/` - websocket or event fanout where applicable
- `jobs/` - async processors for notifications, reconciliation, and exports
- `audit/` - immutable activity trail and trace correlation

## Data / workflow model

Inbound message/content -> routing/moderation -> assignment/collaboration -> resolution/publication.

Recommended entity backbone:

- `tenant`
- `live_chat_record`
- `workflow_state`
- `activity_event`
- `integration_event`

## Strong opinions / defaults

- Persist commands first, then broadcast; realtime transport is a projection of durable state.
- Prefer idempotent command handlers (`command_id` with unique constraint) for all externally triggered actions.
- Model lifecycle states as enums plus guarded transition functions; reject invalid transitions early.

## Overengineering warnings

- Do not make websocket messages your source of truth.
- Do not add event sourcing or CQRS unless transition and audit requirements clearly demand it.
- Avoid premature multi-region writes before single-region correctness and replay tooling exist.

## TS/Python example note

Use only TypeScript or Python examples for this category. A minimal smoke baseline:

```ts
type Command = { commandId: string; tenantId: string; action: string };
function apply(command: Command) {
  // validate tenant scope + state transition, then persist event
  return { accepted: true, commandId: command.commandId };
}
```

```python
from dataclasses import dataclass

@dataclass
class Command:
    command_id: str
    tenant_id: str
    action: str

def apply(command: Command) -> dict:
    # validate tenant scope + state transition, then persist event
    return {"accepted": True, "command_id": command.command_id}
```

## References / local reference links

- [Implementation references](references/implementation.md)
- For source-audit and tier policy details, see `docs/skill-authoring-policy.md` and `docs/taxonomy-manifest.yaml`.
