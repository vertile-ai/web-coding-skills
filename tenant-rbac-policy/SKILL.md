---
name: web-coding-skills-tenant-rbac-policy
description: Used when building a tenant-scoped RBAC policy module for web applications with evolving role and permission rules.
---

# Tenant RBAC Policy playbook

## Purpose / category boundary

Application-level authorization module for tenant-scoped role/permission modeling, policy evaluation, and change-safe permission evolution.

## When to use

- You need role and permission checks reused across many business products.
- You need deterministic tenant boundaries in authorization decisions.
- You need auditable permission changes and policy rollouts.

## When not to use

- You only need a single static `is_admin` flag.
- You are designing infrastructure IAM for cloud control planes.
- You have not yet defined product actions/resources that require policy decisions.

## Baseline stack

| Layer | Opinionated default |
|---|---|
| Policy model | Role + permission grants with tenant overrides |
| Backend (Python) | FastAPI/Flask policy service module with cached evaluator |
| Backend (JS) | Hono/Express authorization middleware + policy adapter |
| Data | PostgreSQL with policy/version tables |
| Cache | Redis for policy snapshot caching |
| Audit | Immutable permission-change event log |

## Module split

- `policy-schema/` - action/resource taxonomy and role templates
- `policy-store/` - persistence and version snapshots
- `evaluator/` - runtime decision engine
- `middleware/` - request-scoped enforcement adapters
- `admin-api/` - role/grant mutation endpoints
- `audit/` - policy-change events and review trails

## Data / workflow model

`policy-change -> version-publish -> cache-refresh -> request-evaluate -> audit`.

Core entities:

- `role_template`
- `tenant_role_binding`
- `permission_grant`
- `policy_version`
- `policy_event`

## Strong opinions / defaults

- Keep policy evaluation pure and side-effect free.
- Version policy documents; never mutate policy in-place without history.
- Expose a “why denied” diagnostic path for operators.

## Overengineering warnings

- Avoid full policy DSL compilers before basic role-permission coverage is stable.
- Do not offload all checks to frontend; enforce server-side at every write boundary.
- Avoid multi-database policy sharding until tenant volume forces it.

## TS/Python example note

Use TypeScript/Python only.

```ts
type Decision = 'allow' | 'deny';
function evaluate(hasPermission: boolean): Decision {
  return hasPermission ? 'allow' : 'deny';
}
```

```python
def evaluate(has_permission: bool) -> str:
    return "allow" if has_permission else "deny"
```

## References / local reference links

- [Implementation references](references/implementation.md)
- For taxonomy and tier rules, see `docs/skill-authoring-policy.md`.
