from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys

try:
    import yaml
except ModuleNotFoundError:
    print('[FAIL] Missing dependency: PyYAML. Install with: pip install pyyaml')
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = {"2d-game", "3d-game", "video-streaming"}
IGNORE = {".git", ".codex", ".omx", "node_modules", "docs", "scripts"}


REQUIRED_SKILL_HEADERS = [
    "## Purpose / category boundary",
    "## When to use",
    "## When not to use",
    "## Baseline stack",
    "## Module split",
    "## Data / workflow model",
    "## Strong opinions / defaults",
    "## Overengineering warnings",
    "## TS/Python example note",
    "## References / local reference links",
]

SOURCE_AUDIT_HEADER = "| Source type | URL | Code/example anchor | Rationale link |"


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def main() -> None:
    top_dirs = [p for p in ROOT.iterdir() if p.is_dir() and p.name not in IGNORE and not p.name.startswith('.')]
    new_categories = [p for p in top_dirs if p.name not in ORIGINAL]

    if len(new_categories) < 30:
        fail(f"new category count {len(new_categories)} < 30")
    print(f"[OK] new category count: {len(new_categories)}")

    for c in new_categories:
        if not (c / "SKILL.md").exists():
            fail(f"missing SKILL.md in {c.name}")
    print("[OK] every new category has SKILL.md")

    for c in new_categories:
        text = (c / "SKILL.md").read_text()
        m = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
        if not m:
            fail(f"missing frontmatter name in {c.name}")
        name = m.group(1).strip()
        if not name.startswith("web-coding-skills-"):
            fail(f"bad prefix in {c.name}: {name}")
        suffix = name.removeprefix("web-coding-skills-")
        if len([s for s in suffix.split('-') if s]) > 3:
            fail(f"more than 3 slugs in {c.name}: {name}")

        missing_headers = [h for h in REQUIRED_SKILL_HEADERS if h not in text]
        if missing_headers:
            fail(f"missing required SKILL headers in {c.name}: {missing_headers}")

        langs = re.findall(r"```([A-Za-z0-9_-]+)", text)
        bad_langs = [x for x in langs if x.lower() not in {"ts", "typescript", "python"}]
        if bad_langs:
            fail(f"non TS/Python fenced languages in {c.name}: {bad_langs}")

    print("[OK] naming and language constraints passed")

    manifest_path = ROOT / "docs" / "taxonomy-manifest.yaml"
    if not manifest_path.exists():
        fail("missing docs/taxonomy-manifest.yaml")
    manifest = yaml.safe_load(manifest_path.read_text())

    rows = []
    for fam in manifest.get("families", []):
        for cat in fam.get("categories", []):
            rows.append(cat)

    if len(rows) != len(new_categories):
        fail(f"manifest category count {len(rows)} != new category count {len(new_categories)}")

    required_fields = {
        "category",
        "family",
        "artifact_tier",
        "distinct_implementation_drives",
        "nearest_sibling",
        "overlap_note",
        "smoke_validation_eligibility",
    }
    for row in rows:
        missing = required_fields - set(row.keys())
        if missing:
            fail(f"manifest row missing fields for {row.get('category')}: {sorted(missing)}")

    tiers = Counter(r["artifact_tier"] for r in rows)
    if tiers.get("tier3", 0) != 6:
        fail(f"tier3 count expected 6, got {tiers.get('tier3', 0)}")

    tier2_plus = [r["category"] for r in rows if r["artifact_tier"] in {"tier2", "tier3"}]
    if len(tier2_plus) != 12:
        fail(f"tier2+tier3 expected 12, got {len(tier2_plus)}")

    for c in tier2_plus:
        ref = ROOT / c / "references" / "implementation.md"
        if not ref.exists():
            fail(f"missing references/implementation.md for {c}")
        ref_text = ref.read_text()
        if SOURCE_AUDIT_HEADER not in ref_text:
            fail(f"missing source-audit header table in {c}/references/implementation.md")
        expected_note = f"- Category: `{c}`"
        if expected_note not in ref_text:
            fail(f"category-specific note mismatch in {c}/references/implementation.md")

    tier3 = [r["category"] for r in rows if r["artifact_tier"] == "tier3"]
    for c in tier3:
        if not (ROOT / "scripts" / "smoke" / f"{c}.mjs").exists():
            fail(f"missing smoke script for tier3 category {c}")

    print(f"[OK] tier policy passed (tier3={len(tier3)}, tier2+tier3={len(tier2_plus)})")

    readme = (ROOT / "README.md").read_text()
    for c in new_categories:
        token = f"web-coding-skills-{c.name}"
        if token not in readme:
            fail(f"README missing {token}")
    print("[OK] README includes every new category")

    print("[PASS] taxonomy validation complete")


if __name__ == "__main__":
    main()
