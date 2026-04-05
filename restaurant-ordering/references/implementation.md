# Restaurant Ordering - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://developer.squareup.com/docs/orders-api/overview) | Order lifecycle and line-item examples | Restaurant ordering needs explicit order state transitions and fulfillment semantics |
| Official docs | [source](https://developer.squareup.com/docs/catalog-api/what-it-does) | Catalog object model for items/modifiers | Menu modeling should be normalized for item options and modifier combinations |
| Official docs | [source](https://docs.stripe.com/refunds) | Refund lifecycle and partial refund behavior | Cancellation/refund flows need provider-backed reconciliation semantics |
| OSS repo | [source](https://github.com/medusajs/medusa) | `packages/modules/order` domain services and workflow patterns | Ordering systems benefit from modular order domain boundaries and extensible workflows |

## Category-specific notes

- Category: `restaurant-ordering`
- Family: `vertical-operations`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
