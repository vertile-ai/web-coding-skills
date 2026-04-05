# Field Service - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://developers.google.com/optimization/routing/vrptw) | VRPTW Python example | Dispatch/route categories need formal optimization primitives |
| Official docs | [source](https://docs.mapbox.com/api/navigation/directions/) | Directions API request/response examples | Route planning requires traffic-aware path computation |
| OSS repo | [source](https://github.com/calcom/cal.com) | Repository architecture and scheduling domain | Booking flows need battle-tested scheduling concepts |
| Official docs | [source](https://docs.temporal.io/workflows) | Workflow retries and compensation | Reschedule/reassignment flows benefit from workflow orchestration |

## Category-specific notes

- Category: `field-service`
- Family: `field-scheduling`
- Tier: `Tier 3`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
