# Tenant RBAC Policy - implementation references

## Category boundary

- Category: `tenant-rbac-policy`
- Family: `architecture-identity-access`
- Tier: `Tier 1`
- Boundary: Tenant-scoped application authorization and policy lifecycle; excludes infrastructure IAM provisioning.

## Beneficiary matrix

| business_category | benefit_rationale |
|---|---|
| ops-control-center | Operator privilege boundaries by tenant and workflow state |
| facility-ops | Site-level access controls for maintenance and contractor actions |
| dispatch-board | Dispatcher/manager role separation in allocation actions |
| procurement-portal | Approval rights for requisition and PO transitions |
| invoice-ops | Finance permission boundaries for draft/finalize/void actions |
| subscription-billing | Plan-change and refund permission controls |
| customer-support | Agent escalation rights and tenant-safe ticket operations |
| document-signing | Sender/signer/admin capabilities with auditable policy change |
| applicant-tracking | Recruiter/interviewer role partitioning |
| telehealth-portal | Clinician/staff/patient action permissions |
| inventory-control | Stock adjustment permissions and approval escalation |
| warehouse-console | Pick/pack/ship action authorization controls |

## Overlap review

| sibling_category | shared_decision_axes_count | unique_boundary_statement | verdict | note |
|---|---:|---|---|---|
| auth-social-sso | 2 | This category decides authorization policy, not identity-provider callback/session issuance. | pass | Clear ownership split. |
| domain-event-pubsub | 1 | Policy events may be published, but bus contract/version strategy is out of scope here. | pass | No bus-governance duplication. |
| async-job-orchestration | 1 | Policy re-evaluation jobs can exist, but orchestration runtime semantics are external. | pass | Only integrates with orchestrator. |

## Source audit

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://authzed.com/docs/spicedb/concepts/schema) | Authorization schema modeling concepts | Role/permission graph boundary guidance |
| Official docs | [source](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) | Row-level security policy examples | Tenant-scope safety and data boundary enforcement |
| Official docs | [source](https://casbin.org/docs/overview/) | Policy model and enforcement concepts | Practical policy evaluation architecture |

## Smoke validation

Tier 1 category. Smoke validation evidence is optional and not required by policy.
