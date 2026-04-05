# Returns Portal - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://shopify.dev/docs/api/admin-rest/latest/resources/return) | Return object lifecycle and status transitions | RMA portals need explicit eligibility and lifecycle states for return authorization |
| Official docs | [source](https://docs.stripe.com/refunds) | Refund lifecycle, partial refunds, and failure handling | Reverse-logistics closure must align with payment refund reconciliation semantics |
| Official docs | [source](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks) | Signature validation, retries, and idempotent consumers | Return/refund integrations should be replay-safe and operationally observable |
| OSS repo | [source](https://github.com/saleor/saleor) | Order return/refund related domain modules in commerce core | Returns workflows need clear order, fulfillment, and payment boundary handling |

## Category-specific notes

- Category: `returns-portal`
- Family: `commerce-finance`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
