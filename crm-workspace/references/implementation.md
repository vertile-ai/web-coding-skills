# CRM Workspace - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://developers.hubspot.com/docs/api/crm/contacts) | Contact object CRUD and association patterns | CRM systems require robust contact/account lifecycle modeling |
| Official docs | [source](https://developers.hubspot.com/docs/api/crm/deals) | Deal stage and pipeline APIs | Opportunity progression should follow explicit stage transitions |
| Official docs | [source](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks) | Signature verification, retries, idempotent consumers | CRM activity ingestion from external systems must be replay-safe and observable |
| OSS repo | [source](https://github.com/espocrm/espocrm) | CRM entity and pipeline domain modules in production OSS | CRM workspace boundaries should separate contacts, activities, and opportunity pipelines |

## Category-specific notes

- Category: `crm-workspace`
- Family: `support-collaboration`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
