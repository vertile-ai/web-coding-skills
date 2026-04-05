# Expense Management - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://cloud.google.com/document-ai/docs/process-documents-ocr) | OCR document processing flow | Receipt capture pipelines should use robust document extraction instead of billing lifecycle examples |
| Official docs | [source](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks) | Delivery verification, retries, and idempotent consumers | Expense ingestion and approval events must be authenticated, replay-safe, and operationally observable |
| Official docs | [source](https://docs.camunda.org/manual/latest/reference/bpmn20/tasks/user-task/) | User task assignment and approval workflow modeling | Expense approvals need explicit human review states, assignees, and escalation-ready workflow semantics |
| OSS repo | [source](https://github.com/odoo/odoo) | `addons/hr_expense` module workflow and accounting integration | Expense systems benefit from auditable business workflows, policy enforcement hooks, and accounting integration patterns |

## Category-specific notes

- Category: `expense-management`
- Family: `commerce-finance`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
