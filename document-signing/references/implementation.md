# Document Signing - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://developers.docusign.com/docs/esign-rest-api/how-to/request-signature-in-app/) | Envelope creation and signature request flow | Signing systems need explicit envelope lifecycle and signer orchestration |
| Official docs | [source](https://developers.docusign.com/docs/esign-rest-api/esign101/concepts/recipients/) | Recipient roles and routing order | Signer order and role modeling must be first-class workflow constraints |
| Official docs | [source](https://www.rfc-editor.org/rfc/rfc3161) | Trusted timestamp protocol semantics | Tamper-evident signing requires timestamp-aware evidence packaging |
| OSS repo | [source](https://github.com/docusealco/docuseal) | Open-source e-signature service architecture | Signature products benefit from clear audit trail and envelope domain boundaries |

## Category-specific notes

- Category: `document-signing`
- Family: `support-collaboration`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
