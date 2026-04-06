---
name: web-coding-skills-auth-social-sso
description: Used when building a web auth module focused on Google/GitHub social SSO, account linking, and session hardening.
---

# Auth Social SSO playbook

## Purpose / category boundary

Application-layer auth module for Google/GitHub social sign-in, account linking, token/session lifecycle, and tenant-safe identity mapping.

## When to use

- You need production-grade social sign-in (Google + GitHub) with deterministic account-linking rules.
- You need one auth module reused across multiple product categories.
- You need clear boundaries between provider adapters, identity core, and session policy.

## When not to use

- You need enterprise SAML/OIDC federation as the primary scope.
- You are solving infrastructure IdP provisioning or deployment topology.
- You need a generic “all auth topics” category with no provider boundary.

## Baseline stack

| Layer | Opinionated default |
|---|---|
| Frontend | React + TypeScript + PKCE flow helpers |
| Backend (Python) | FastAPI/Flask with explicit auth adapter boundary |
| Backend (JS) | Hono/Express with typed auth middleware and callback guards |
| Data | PostgreSQL for identity/account linkage state |
| Cache | Redis for short-lived OAuth state + replay protection |
| Security | Signed/rotating tokens + audit events |

## Module split

- `providers/` - Google/GitHub OAuth adapters and callback validation
- `identity/` - account mapping, dedupe, and linking rules
- `session/` - token/session issuance, refresh, revocation
- `api/` - login/callback/logout endpoints and DTO boundaries
- `audit/` - auth lifecycle events and suspicious-flow tracking

## Data / workflow model

`start-login -> provider-callback -> identity-resolve -> session-issue -> audit-append`.

Core entities:

- `identity_provider_account`
- `user_identity_link`
- `auth_session`
- `auth_event`

## Strong opinions / defaults

- Treat provider payloads as untrusted until signature/nonce/state checks pass.
- Keep account-linking explicit and rule-driven; never auto-link by email without policy.
- Make callback handlers idempotent with replay-safe state keys.

## Overengineering warnings

- Do not introduce service mesh or multi-service split before callback/security invariants are stable.
- Avoid “provider plug-in architecture” until a third provider is real, not hypothetical.
- Do not couple authorization policy logic into callback handlers.

## TS/Python example note

Use TypeScript/Python only. Keep provider logic in adapters and identity logic in domain code.

```ts
type Provider = 'google' | 'github';
function providerToIssuer(provider: Provider): string {
  return provider === 'google' ? 'https://accounts.google.com' : 'https://github.com';
}
```

```python
def provider_to_issuer(provider: str) -> str:
    return "https://accounts.google.com" if provider == "google" else "https://github.com"
```

## References / local reference links

- [Implementation references](references/implementation.md)
- For taxonomy rules, see `docs/skill-authoring-policy.md` and `docs/taxonomy-manifest.yaml`.
