# Kitchen Display - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://socket.io/docs/v4/rooms/) | Room join/leave and targeted broadcast patterns | KDS requires station-specific realtime ticket fanout and acknowledgement events |
| Official docs | [source](https://developer.squareup.com/docs/orders-api/fulfillments) | Fulfillment state updates and kitchen-facing order progress | Kitchen ticket routing should follow explicit prep/ready/handoff progression |
| OSS repo | [source](https://github.com/odoo/odoo) | `addons/pos_restaurant` POS restaurant workflow modules | Restaurant station flows need bounded states for prep, bump, and completion |
| Official docs | [source](https://www.postgresql.org/docs/current/sql-notify.html) | LISTEN/NOTIFY event delivery semantics | KDS projections can use lightweight DB-driven event fanout for operator consoles |

## Category-specific notes

- Category: `kitchen-display`
- Family: `vertical-operations`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
