# Auth Social SSO - implementation references

## Category boundary

- Category: `auth-social-sso`
- Family: `architecture-identity-access`
- Tier: `Tier 2`
- Boundary: Google/GitHub social SSO, account linking, and session lifecycle at application layer.

## Beneficiary matrix

| business_category | benefit_rationale |
|---|---|
| ops-control-center | Shared operator authentication and secure callback handling |
| facility-ops | Staff/contractor login consistency with account-linking safeguards |
| field-service | Technician login and token refresh reliability on mobile/web clients |
| booking-engine | End-user social login onboarding with replay-safe callback flow |
| appointment-scheduler | User identity continuity for reschedule/cancel workflows |
| tenant-portal | Tenant self-service account access with deterministic provider mapping |
| customer-support | Agent/customer auth session hardening and auditability |
| live-chat | Session continuity for chat identity and room authorization |
| learning-platform | Student/instructor social login with stable identity links |
| event-ticketing | Buyer login path and account reconciliation after external callback |
| telehealth-portal | Clinician/patient session protection and auth event trails |
| donation-platform | Donor account login without generic auth sprawl |

## Overlap review

| sibling_category | shared_decision_axes_count | unique_boundary_statement | verdict | note |
|---|---:|---|---|---|
| tenant-rbac-policy | 2 | This category owns provider callback + account-linking flow, not permission evaluation rules. | pass | Boundaries are complementary. |
| async-job-orchestration | 1 | This category focuses synchronous auth lifecycle; async jobs are supporting side effects only. | pass | No orchestration ownership conflict. |
| domain-event-pubsub | 1 | Auth emits events but does not define event bus contract policy. | pass | Event transport remains separate. |

## Source audit

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://developers.google.com/identity/openid-connect/openid-connect) | OIDC ID token validation guidance | Provider callback and token claims validation |
| Official docs | [source](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps) | OAuth app authorization flow | GitHub callback and authorization-code handling |
| Official docs | [source](https://datatracker.ietf.org/doc/html/rfc7636) | PKCE protocol sections 4-7 | Replay-safe auth-code exchange design |
| Official docs | [source](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) | Authentication controls checklist | Session hardening and abuse-resistance defaults |

## Smoke validation

Tier 2 category. Smoke validation evidence is optional and not required by policy.
