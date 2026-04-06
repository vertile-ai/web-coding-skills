# Skill authoring policy (dual-axis taxonomy)

## Scope

This policy governs taxonomy and artifact authoring for web coding skills.

## Taxonomy model

The repository uses a **dual-axis taxonomy**:

1. **Business axis** — narrow product-type categories (for example, `ops-control-center`).
2. **Architecture axis** — reusable application-layer module categories (for example, `auth-social-sso`).

Both axes are represented in `docs/taxonomy-manifest.yaml`.

## Mandatory rules

1. Category names must remain specific and non-umbrella.
2. Skill frontmatter name must be `web-coding-skills-<category>` with `category` <= 3 slugs.
3. Examples are limited to TypeScript and Python.
4. Every shipped category requires `SKILL.md`.
5. Every architecture category requires `references/implementation.md`.
6. Architecture guidance must stay in application-layer coding design scope (no infra/deployment/IaC/topology runbooks).

## Required SKILL.md schema

1. Purpose / category boundary
2. When to use
3. When not to use
4. Baseline stack
5. Module split
6. Data / workflow model
7. Strong opinions / defaults
8. Overengineering warnings
9. TS/Python example note
10. References / local reference links

## Architecture evidence contract

Canonical evidence for architecture categories lives only in:

- `<category>/references/implementation.md`

Required sections (in order):

1. `## Category boundary`
2. `## Beneficiary matrix`
3. `## Overlap review`
4. `## Source audit`
5. `## Smoke validation` (required for Tier 3; optional otherwise)

`docs/taxonomy-manifest.yaml` stores only machine-readable pointers and thresholds for those proof sections.

## Source audit format

Every curated `references/implementation.md` must include:

- Source type
- URL
- Code/example anchor
- Rationale link (which recommendation the source supports)

Table header:

`| Source type | URL | Code/example anchor | Rationale link |`

## Axis-specific selection policy

### Business axis

- Keep release-1 narrow product-type boundary logic.
- Preserve existing business families/categories as append-only unless a dedicated migration is approved.

### Architecture axis

- Category admission must document beneficiary impact on **>=10 existing business categories**.
- Category overlap must be explicitly reviewed against nearest 2–3 architecture siblings.
- Manifest entries must include explicit `proof` refs/thresholds and `artifacts` requirements.

## Tier policy

### Business axis (existing release-1 rule)

- Tier 2 = first two categories in each business family.
- Tier 3 = first category of each business family from Tier 2.

### Architecture axis (explicit per-category assignment)

- **Tier 1**: `SKILL.md` + `references/implementation.md` with required beneficiary/overlap sections.
- **Tier 2**: Tier 1 + at least **3** source-audit rows + explicit README mention of shipped architecture category/family.
- **Tier 3**: Tier 2 + smoke validation evidence.

## Validation contract

`scripts/validate-taxonomy.py` must assert:

- business-axis append-only baseline preservation,
- manifest schema correctness for architecture rows (`axis`, `proof`, `artifacts`),
- artifact presence,
- beneficiary/overlap evidence presence and thresholds,
- README coverage for shipped categories,
- tier obligations including Tier 2 source-audit minimums and Tier 3 smoke requirements.
