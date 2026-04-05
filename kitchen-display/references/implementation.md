# Kitchen Display - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://hl7.org/fhir/R4/patient.html) | FHIR Patient resource definitions | Healthcare workflow categories need standards-based data modeling |
| OSS repo | [source](https://github.com/medplum/medplum) | FHIR-native healthcare platform architecture | Telehealth/intake systems benefit from proven FHIR-first patterns |
| Official docs | [source](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) | RLS policy examples | Sensitive vertical data requires per-tenant/per-role data isolation |
| Official docs | [source](https://docs.temporal.io/workflows) | Workflow durability and retries | Inventory/fulfillment/clinical intake flows need durable orchestration |

## Category-specific notes

- Category: `kitchen-display`
- Family: `vertical-operations`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
