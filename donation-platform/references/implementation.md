# Donation Platform - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://docs.stripe.com/payments/checkout/accept-a-payment) | Checkout payment session flow | Donation checkout should use a resilient provider-backed payment initiation flow |
| Official docs | [source](https://docs.stripe.com/billing/subscriptions/overview) | Subscription lifecycle for recurring charges | Recurring pledges should model retries and lifecycle transitions explicitly |
| Official docs | [source](https://docs.stripe.com/webhooks) | Signature verification and retry behavior | Donation payment events must be authenticated and idempotently processed |
| OSS repo | [source](https://github.com/opencollective/opencollective) | Collective contribution and payout domain modeling | Donation platforms need transparent contribution, allocation, and reporting boundaries |

## Category-specific notes

- Category: `donation-platform`
- Family: `people-learning-engagement`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
