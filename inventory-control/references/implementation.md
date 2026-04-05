# Inventory Control - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://shopify.dev/docs/api/admin-rest/latest/resources/inventorylevel) | Inventory level adjust/connect endpoints | Stock ledgers need explicit increment/decrement semantics with location scoping |
| Official docs | [source](https://www.postgresql.org/docs/current/transaction-iso.html) | Transaction isolation behavior and anomalies | Inventory movement handlers must be designed to avoid lost updates under concurrency |
| OSS repo | [source](https://github.com/odoo/odoo) | `addons/stock/models/stock_quant.py` on-hand quantity domain logic | Per-location quant models are foundational for cycle count and reservation correctness |
| OSS repo | [source](https://github.com/frappe/erpnext) | `erpnext/stock/doctype/stock_ledger_entry` ledger-driven stock history | Inventory systems benefit from append-only stock movement history for reconciliation |

## Category-specific notes

- Category: `inventory-control`
- Family: `vertical-operations`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
