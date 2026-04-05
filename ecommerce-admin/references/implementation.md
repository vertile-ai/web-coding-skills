# Ecommerce Admin - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://shopify.dev/docs/api/admin-rest/latest/resources/product) | Product CRUD and publication flow examples | Catalog operations in admin consoles need explicit product lifecycle coverage |
| Official docs | [source](https://shopify.dev/docs/api/admin-rest/latest/resources/order) | Order status, line item, and edit examples | Admin order workflows should be grounded in concrete order-management primitives |
| Official docs | [source](https://docs.stripe.com/refunds) | Refund lifecycle and partial refund behavior | Refund operations should follow provider-backed finance and reconciliation semantics |
| OSS repo | [source](https://github.com/saleor/saleor) | Order, fulfillment, and dashboard domain boundaries in production OSS commerce | Admin workflows need explicit domain boundaries across catalog, order, and fulfillment operations |

## Category-specific notes

- Category: `ecommerce-admin`
- Family: `commerce-finance`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
