# Domain Event Pub/Sub - implementation references

## Category boundary

- Category: `domain-event-pubsub`
- Family: `architecture-workflow-integration`
- Tier: `Tier 1`
- Boundary: Domain event publication/consumption design with versioned contracts and idempotent handlers.

## Beneficiary matrix

| business_category | benefit_rationale |
|---|---|
| ops-control-center | Incident lifecycle events to notify downstream workflows |
| facility-ops | Facility status change fanout to related modules |
| dispatch-board | Dispatch assignment events consumed by analytics/notifications |
| queue-management | Queue transition events for SLA and reporting modules |
| invoice-ops | Invoice lifecycle events for reconciliation and notifications |
| marketplace-seller | Order/payout/dispute event fanout to seller tooling |
| community-forum | Moderation and reputation events to async processors |
| crm-workspace | Contact/activity events for downstream automation |
| learning-platform | Enrollment/progress events for reporting and nudges |
| donation-platform | Donation events for receipts and impact ledgers |
| inventory-control | Stock movement events for replenishment and alerts |
| warehouse-console | Fulfillment events for status sync across channels |

## Overlap review

| sibling_category | shared_decision_axes_count | unique_boundary_statement | verdict | note |
|---|---:|---|---|---|
| async-job-orchestration | 2 | This category governs event contract and delivery semantics, not retry/workflow runtime control. | pass | Runtime and transport separated. |
| object-storage-pipeline | 1 | Storage changes can emit events, but storage ingest/retrieval policy remains outside this category. | pass | No direct storage ownership overlap. |
| tenant-rbac-policy | 1 | RBAC policy may emit events but policy evaluation remains external. | pass | Emission only, no policy-engine overlap. |

## Source audit

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://microservices.io/patterns/data/transactional-outbox.html) | Transactional outbox pattern | Publish reliability from domain transactions |
| Official docs | [source](https://www.enterpriseintegrationpatterns.com/patterns/messaging/IdempotentReceiver.html) | Idempotent receiver pattern | Consumer duplicate-handling strategy |
| Official docs | [source](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) | Outbox implementation details | Cloud-practical outbox operation notes |

## Smoke validation

Tier 1 category. Smoke validation evidence is optional and not required by policy.
