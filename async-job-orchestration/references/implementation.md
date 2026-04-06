# Async Job Orchestration - implementation references

## Category boundary

- Category: `async-job-orchestration`
- Family: `architecture-workflow-integration`
- Tier: `Tier 2`
- Boundary: Application-owned async workflow execution; excludes queue infrastructure operations.

## Beneficiary matrix

| business_category | benefit_rationale |
|---|---|
| ops-control-center | Alert fanout, escalation timers, and delayed compensation jobs |
| facility-ops | Scheduled maintenance reminders and async vendor updates |
| field-service | Post-visit sync jobs and offline reconciliation |
| route-planner | Batch route recomputation and delayed optimization tasks |
| booking-engine | Expiry cleanup and hold-release jobs |
| subscription-billing | Renewal cycles, dunning workflows, and retry orchestration |
| returns-portal | Reverse-logistics status sync and refund follow-up jobs |
| customer-support | SLA breach timers and auto-assignment workflows |
| applicant-tracking | Interview reminder and stage timeout workflows |
| event-ticketing | Reservation timeout and release pipelines |
| telehealth-portal | Appointment reminder jobs and async record processing |
| warehouse-console | Batch pick-wave generation and reconciliation tasks |

## Overlap review

| sibling_category | shared_decision_axes_count | unique_boundary_statement | verdict | note |
|---|---:|---|---|---|
| domain-event-pubsub | 2 | This category owns execution lifecycle/retries; pub/sub owns event transport contracts. | pass | Complementary with clear transport/runtime split. |
| object-storage-pipeline | 1 | Storage pipeline can trigger jobs, but orchestration policy remains here. | pass | Trigger source differs from orchestration ownership. |
| auth-social-sso | 1 | Auth may enqueue side effects, but callback/session flows are not orchestrator responsibilities. | pass | Non-overlapping core boundary. |

## Source audit

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://docs.celeryq.dev/en/stable/userguide/tasks.html) | Retry and task idempotency guidance | Durable job handler design |
| Official docs | [source](https://docs.bullmq.io/guide/retrying-failing-jobs) | Retry/backoff and failed-job handling | Queue-level retry semantics |
| Official docs | [source](https://temporal.io/blog/idempotency-and-durable-execution) | Durable execution + idempotency concepts | Compensation-safe orchestration patterns |
| Official docs | [source](https://cloud.google.com/architecture/patterns-for-running-reliable-services) | Reliability and backoff patterns | Failure isolation and retry boundaries |

## Smoke validation

Tier 2 category. Smoke validation evidence is optional and not required by policy.
