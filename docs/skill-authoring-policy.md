# Skill authoring policy (release 1 taxonomy)

## Scope

This policy governs release-1 expansion for web coding skills.

## Mandatory rules

1. Category names must be narrow product-type categories (not umbrella buckets).
2. Skill frontmatter name must be `web-coding-skills-<category>` with `category` <= 3 slugs.
3. Examples are limited to TypeScript and Python.
4. Every shipped category requires `SKILL.md`.
5. Tier 2/3 categories require `references/implementation.md` using source-audit table format.

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

## Source audit format

Every curated reference doc must include:

- Source type
- URL
- Code/example anchor
- Rationale link (which recommendation the source supports)

## Tier policy

- Tier 1: SKILL.md only
- Tier 2: SKILL.md + references/implementation.md
- Tier 3: Tier 2 + smoke validation evidence (via scripts/smoke)

## Deterministic tier allocation

- Tier 2 = first two categories in each family (12 total)
- Tier 3 = first category of each family from Tier 2 (6 total)
