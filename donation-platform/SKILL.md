---
name: web-coding-skills-donation-platform
description: Used when building donation platform software on the web. Donation platform for campaign funding, recurring pledges, receipts, and impact reporting workflows.
---

# Donation Platform playbook

## Purpose / category boundary

Donation platform for campaign funding, recurring pledges, receipts, and impact reporting workflows.

## When to use

- You need a dedicated product workflow for **donation platform**, not a generic SaaS shell.
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

- Payment provider webhook verification pipeline
- Recurring pledge scheduler and retry jobs
- Fund allocation ledger with receipt and audit reporting

## Module split

- `api/` - typed endpoints, auth checks, request validation
- `domain/` - business rules, state transitions, invariants
- `workflow/` - orchestration for long-running or compensating actions
- `repo/` - persistence adapters and query objects
- `realtime/` - websocket or event fanout where applicable
- `jobs/` - async processors for notifications, reconciliation, and exports
- `audit/` - immutable activity trail and trace correlation

## Data / workflow model

Campaign created -> donor pledge/payment captured -> receipt issued -> allocation posted -> impact report generated.

Recommended entity backbone:

- `tenant`
- `donation_platform_record`
- `workflow_state`
- `activity_event`
- `integration_event`

## Strong opinions / defaults

- Model donation lifecycle states explicitly (pledged, authorized, captured, receipted, allocated, refunded) and disallow illegal transitions.
- Prefer idempotent command handlers (`command_id` with unique constraint) for all externally triggered actions.
- Model lifecycle states as enums plus guarded transition functions; reject invalid transitions early.

## Overengineering warnings

- Avoid mixing accounting allocation state with payment capture state in one status field.
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
