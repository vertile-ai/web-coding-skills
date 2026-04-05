# Incident Console - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) | Section 5.9 SQL policy examples | Tenant-safe row access and role policy design |
| Official docs | [source](https://opentelemetry.io/docs/concepts/signals/traces/) | Traces model and span semantics | Operational workflows need traceable state transitions |
| Official docs | [source](https://docs.temporal.io/workflows) | Workflow execution and retries | Long-running ops tasks should be resumable and deterministic |
| Official docs | [source](https://docs.github.com/en/webhooks) | Webhook delivery model | Inbound system integrations must be idempotent and signed |

## Category-specific notes

- Category: `incident-console`
- Family: `operations-admin`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
