# Crm Workspace - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://socket.io/docs/v4/rooms/) | Rooms join/leave + broadcast examples | Targeted fanout and tenant/user rooms are core chat primitives |
| Official docs | [source](https://www.twilio.com/docs/conversations) | Conversations SDK/API quickstarts | Omnichannel messaging patterns map to support/chat products |
| Official docs | [source](https://www.twilio.com/docs/usage/webhooks) | Webhook handshake and endpoint behavior | Inbound messaging/events must use verified webhook endpoints |
| OSS repo | [source](https://github.com/chatwoot/chatwoot) | Open-source support desk architecture | Support domain boundaries and operational concerns are proven in production |

## Category-specific notes

- Category: `crm-workspace`
- Family: `support-collaboration`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
