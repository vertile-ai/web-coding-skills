# Applicant Tracking - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://www.postgresql.org/docs/current/textsearch-intro.html) | Full-text search intro and query operators | Job/candidate/course discovery needs ranked textual search |
| Official docs | [source](https://www.postgresql.org/docs/current/gin.html) | GIN indexing strategy | Search-heavy portals need proper inverted indexes |
| Official docs | [source](https://docs.temporal.io/workflows) | Workflow orchestration model | Multi-stage applicant/learning lifecycles fit durable workflows |
| OSS repo | [source](https://github.com/calcom/cal.com) | Scheduling and lifecycle orchestration patterns | Interview/training/event scheduling shares queueing/availability constraints |

## Category-specific notes

- Category: `applicant-tracking`
- Family: `people-learning-engagement`
- Tier: `Tier 2`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
