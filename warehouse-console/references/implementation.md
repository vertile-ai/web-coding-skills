# Warehouse Console - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://www.postgresql.org/docs/current/explicit-locking.html) | Row/table lock modes and conflict behavior | Pick-pack-ship workflows need deterministic reservation and lock strategy under concurrency |
| Official docs | [source](https://techdocs.zebra.com/datawedge/latest/guide/api/tutorials/) | DataWedge API tutorials for barcode scan intents | Warehouse consoles depend on reliable scan-event ingestion from handheld devices |
| OSS repo | [source](https://github.com/odoo/odoo) | `addons/stock/models/stock_picking.py` picking/transfer workflow logic | Receiving, transfer, and shipment state machines need explicit transition rules |
| OSS repo | [source](https://github.com/frappe/erpnext) | `erpnext/stock/doctype/stock_entry/stock_entry.py` stock movement handling | Warehouse operations benefit from auditable inventory movement transactions |

## Category-specific notes

- Category: `warehouse-console`
- Family: `vertical-operations`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
