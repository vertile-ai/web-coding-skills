---
name: web-coding-skills-async-job-orchestration
description: Used when building async job orchestration modules for web applications with retries, idempotency, and compensation-safe workflows.
---

# Async Job Orchestration playbook

## Purpose / category boundary

Application-layer background job orchestration module for durable async workflows, retry control, dead-letter handling, and compensation-safe side effects.

## When to use

- You need cron/queue-triggered workflows reused across multiple products.
- Business flows require retry, timeout, or compensation semantics.
- You need deterministic job identity and idempotency guarantees.

## When not to use

- Work is immediate and request-bound with no async boundary.
- You are solving queue-cluster operations or infra deployment concerns.
- You only need fire-and-forget notifications with no workflow state.

## Baseline stack

| Layer | Opinionated default |
|---|---|
| Backend (Python) | FastAPI/Flask + Celery/RQ-style adapter boundary |
| Backend (JS) | Hono/Express + BullMQ/worker adapter boundary |
| Queue | Redis/SQS-backed queue abstraction |
| Data | PostgreSQL workflow state + dedupe keys |
| Scheduler | Cron-triggered enqueue via app-owned scheduler module |
| Observability | Job metrics + structured failure logs + trace IDs |

## Module split

- `commands/` - enqueue contracts and idempotency keys
- `workers/` - job handlers and side-effect boundaries
- `workflow/` - retry/backoff and compensation policy
- `state/` - job status persistence and replay markers
- `scheduler/` - time-based triggers (cron-like)
- `audit/` - execution attempts and failure trail

## Data / workflow model

`enqueue -> reserve -> execute -> commit/compensate -> finalize -> audit`.

Core entities:

- `job_command`
- `job_execution`
- `job_retry_state`
- `dead_letter_entry`
- `workflow_compensation`

## Strong opinions / defaults

- Every handler must be idempotent with explicit dedupe key.
- Retry policy belongs to workflow module, not sprinkled inside handlers.
- Dead-letter entries must include replay instructions.

## Overengineering warnings

- Avoid distributed workflow engines before queue-based orchestration is saturated.
- Do not mix domain logic and transport code inside workers.
- Avoid unbounded retries without terminal state and operator visibility.

## TS/Python example note

Use TypeScript/Python only.

```ts
type Job = { jobId: string; type: string };
function dedupeKey(job: Job): string {
  return `${job.type}:${job.jobId}`;
}
```

```python
def dedupe_key(job_type: str, job_id: str) -> str:
    return f"{job_type}:{job_id}"
```

## References / local reference links

- [Implementation references](references/implementation.md)
- See `docs/skill-authoring-policy.md` for architecture tier obligations.
