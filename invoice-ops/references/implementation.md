# Invoice Ops - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://docs.stripe.com/billing/subscriptions/overview) | Subscription lifecycle + webhook recommendations | Billing states and retries should follow provider lifecycle semantics |
| Official docs | [source](https://docs.stripe.com/billing/subscriptions/subscription-schedules/use-cases) | Schedule phase examples | Planned upgrades/downgrades are first-class in subscription systems |
| Official docs | [source](https://docs.stripe.com/webhooks?lang=node) | Node webhook signature verification | Financial events must be verified and idempotent |
| OSS repo | [source](https://github.com/saleor/saleor) | Headless commerce architecture in production OSS | Admin/seller workflows need explicit domain boundaries |

## Category-specific notes

- Category: `invoice-ops`
- Family: `commerce-finance`
- Tier: `Tier 3`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
