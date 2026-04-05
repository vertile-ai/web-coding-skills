---
name: web-coding-skills-field-service
description: Used when building field service software on the web. Field service platform for technician assignment, visit execution, checklists, and completion evidence.
---

# Field Service playbook

## Purpose / category boundary

Field service platform for technician assignment, visit execution, checklists, and completion evidence.

## When to use

- You need a dedicated product workflow for **field service**, not a generic SaaS shell.
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

- PostgreSQL + geospatial index
- Optimization worker
- Map routing API integration

## Module split

- `api/` - typed endpoints, auth checks, request validation
- `domain/` - business rules, state transitions, invariants
- `workflow/` - orchestration for long-running or compensating actions
- `repo/` - persistence adapters and query objects
- `realtime/` - websocket or event fanout where applicable
- `jobs/` - async processors for notifications, reconciliation, and exports
- `audit/` - immutable activity trail and trace correlation

## Data / workflow model

Demand intake -> capacity lookup -> slot/route optimization -> confirmation -> exception handling.

Recommended entity backbone:

- `tenant`
- `field_service_record`
- `workflow_state`
- `activity_event`
- `integration_event`

## Strong opinions / defaults

- Separate optimization from booking writes; compute candidate plans in workers, commit minimal final state.
- Prefer idempotent command handlers (`command_id` with unique constraint) for all externally triggered actions.
- Model lifecycle states as enums plus guarded transition functions; reject invalid transitions early.

## Overengineering warnings

- Avoid synchronous routing/optimization in request handlers.
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
