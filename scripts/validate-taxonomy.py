from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys

try:
    import yaml
except ModuleNotFoundError:
    print("[FAIL] Missing dependency: PyYAML. Install with: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = {"2d-game", "3d-game", "video-streaming"}
IGNORE = {".git", ".codex", ".omx", "node_modules", "docs", "scripts"}

BASELINE_FAMILY_KEYS = [
    "operations-admin",
    "field-scheduling",
    "commerce-finance",
    "support-collaboration",
    "people-learning-engagement",
    "vertical-operations",
]
BASELINE_FAMILY_CATEGORIES = {
    "operations-admin": [
        "ops-control-center",
        "facility-ops",
        "incident-console",
        "property-portal",
        "tenant-portal",
        "procurement-portal",
    ],
    "field-scheduling": [
        "field-service",
        "dispatch-board",
        "route-planner",
        "booking-engine",
        "appointment-scheduler",
        "queue-management",
    ],
    "commerce-finance": [
        "invoice-ops",
        "subscription-billing",
        "expense-management",
        "ecommerce-admin",
        "marketplace-seller",
        "returns-portal",
    ],
    "support-collaboration": [
        "customer-support",
        "live-chat",
        "knowledge-base",
        "community-forum",
        "crm-workspace",
        "document-signing",
    ],
    "people-learning-engagement": [
        "job-board",
        "applicant-tracking",
        "learning-platform",
        "exam-proctoring",
        "event-ticketing",
        "donation-platform",
    ],
    "vertical-operations": [
        "telehealth-portal",
        "patient-intake",
        "restaurant-ordering",
        "kitchen-display",
        "inventory-control",
        "warehouse-console",
    ],
}

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
REQUIRED_ARCH_IMPL_SECTIONS = [
    "Category boundary",
    "Beneficiary matrix",
    "Overlap review",
    "Source audit",
]

SOURCE_AUDIT_HEADER = "| Source type | URL | Code/example anchor | Rationale link |"
BENEFICIARY_HEADER = "| business_category | benefit_rationale |"
OVERLAP_REQUIRED_TOKENS = [
    "sibling_category",
    "shared_decision_axes_count",
    "unique_boundary_statement",
    "verdict",
    "note",
]

BUSINESS_REQUIRED_FIELDS = {
    "category",
    "family",
    "artifact_tier",
    "distinct_implementation_drives",
    "nearest_sibling",
    "overlap_note",
    "smoke_validation_eligibility",
}
ARCH_REQUIRED_FIELDS = {
    "category",
    "family",
    "axis",
    "artifact_tier",
    "distinct_implementation_drives",
    "architecture_boundary",
    "proof",
    "artifacts",
}
ARCH_REQUIRED_PROOF_FIELDS = {
    "beneficiary_matrix_ref",
    "beneficiary_min_categories",
    "overlap_review_ref",
    "overlap_required_siblings",
    "source_audit_min_rows",
}
ARCH_REQUIRED_ARTIFACT_FIELDS = {"skill_md", "implementation_ref", "smoke_required"}


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def count_markdown_table_rows(section_text: str, header: str) -> int:
    lines = [line.strip() for line in section_text.splitlines()]
    try:
        header_idx = lines.index(header)
    except ValueError:
        return 0
    rows = 0
    for line in lines[header_idx + 2 :]:
        if not line.startswith("|"):
            break
        if re.match(r"^\|\s*-+\s*(\|\s*-+\s*)+\|?$", line):
            continue
        rows += 1
    return rows


def section_text(doc: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$"
    m = re.search(pattern, doc, re.MULTILINE)
    if not m:
        return ""
    start = m.end()
    n = re.search(r"^##\s+.+$", doc[start:], re.MULTILINE)
    end = start + n.start() if n else len(doc)
    return doc[start:end].strip()


def main() -> None:
    top_dirs = [p for p in ROOT.iterdir() if p.is_dir() and p.name not in IGNORE and not p.name.startswith(".")]
    category_dirs = [p for p in top_dirs if p.name not in ORIGINAL]
    if len(category_dirs) < 36:
        fail(f"category directory count {len(category_dirs)} < expected baseline 36")
    print(f"[OK] category directory count: {len(category_dirs)}")

    for c in category_dirs:
        skill_path = c / "SKILL.md"
        if not skill_path.exists():
            fail(f"missing SKILL.md in {c.name}")
    print("[OK] every category has SKILL.md")

    for c in category_dirs:
        text = (c / "SKILL.md").read_text()
        m = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
        if not m:
            fail(f"missing frontmatter name in {c.name}")
        name = m.group(1).strip()
        if not name.startswith("web-coding-skills-"):
            fail(f"bad prefix in {c.name}: {name}")
        suffix = name.removeprefix("web-coding-skills-")
        if len([s for s in suffix.split("-") if s]) > 3:
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
    families = manifest.get("families", [])
    if len(families) < len(BASELINE_FAMILY_KEYS):
        fail("manifest has fewer than baseline business families")

    baseline_keys = [f.get("key") for f in families[: len(BASELINE_FAMILY_KEYS)]]
    if baseline_keys != BASELINE_FAMILY_KEYS:
        fail(f"baseline family keys changed: {baseline_keys}")

    business_rows = []
    for fam in families[: len(BASELINE_FAMILY_KEYS)]:
        key = fam["key"]
        categories = fam.get("categories", [])
        got_names = [c.get("category") for c in categories]
        expected_names = BASELINE_FAMILY_CATEGORIES[key]
        if got_names != expected_names:
            fail(f"baseline category order changed for {key}: {got_names}")
        if len(categories) != 6:
            fail(f"baseline family {key} expected 6 categories, got {len(categories)}")
        for idx, row in enumerate(categories):
            missing = BUSINESS_REQUIRED_FIELDS - set(row.keys())
            if missing:
                fail(f"business row missing fields for {row.get('category')}: {sorted(missing)}")
            expected_tier = "tier3" if idx == 0 else "tier2" if idx == 1 else "tier1"
            if row["artifact_tier"] != expected_tier:
                fail(f"business tier changed for {row['category']}: expected {expected_tier}, got {row['artifact_tier']}")
            expected_smoke = idx == 0
            if bool(row["smoke_validation_eligibility"]) != expected_smoke:
                fail(f"business smoke flag mismatch for {row['category']}")
            business_rows.append(row)
    if len(business_rows) != 36:
        fail(f"business baseline category count expected 36, got {len(business_rows)}")
    print("[OK] business-axis append-only baseline preserved")

    arch_families = families[len(BASELINE_FAMILY_KEYS) :]
    if not arch_families:
        fail("no appended architecture families found")

    architecture_rows = []
    for fam in arch_families:
        if fam.get("axis") != "architecture":
            fail(f"appended family missing axis=architecture: {fam.get('key')}")
        for row in fam.get("categories", []):
            missing = ARCH_REQUIRED_FIELDS - set(row.keys())
            if missing:
                fail(f"architecture row missing fields for {row.get('category')}: {sorted(missing)}")
            if row["axis"] != "architecture":
                fail(f"architecture row axis mismatch for {row['category']}")
            if row["family"] != fam.get("key"):
                fail(f"architecture family mismatch for {row['category']}")
            if row["artifact_tier"] not in {"tier1", "tier2", "tier3"}:
                fail(f"invalid architecture tier for {row['category']}: {row['artifact_tier']}")

            proof = row.get("proof")
            artifacts = row.get("artifacts")
            if not isinstance(proof, dict):
                fail(f"proof block must be a map for {row['category']}")
            if not isinstance(artifacts, dict):
                fail(f"artifacts block must be a map for {row['category']}")
            missing_proof = ARCH_REQUIRED_PROOF_FIELDS - set(proof.keys())
            if missing_proof:
                fail(f"proof block missing keys for {row['category']}: {sorted(missing_proof)}")
            missing_artifacts = ARCH_REQUIRED_ARTIFACT_FIELDS - set(artifacts.keys())
            if missing_artifacts:
                fail(f"artifacts block missing keys for {row['category']}: {sorted(missing_artifacts)}")

            if artifacts["skill_md"] is not True or artifacts["implementation_ref"] is not True:
                fail(f"artifacts booleans must be true for {row['category']}")
            if not isinstance(artifacts["smoke_required"], bool):
                fail(f"artifacts.smoke_required must be bool for {row['category']}")

            beneficiary_min = proof["beneficiary_min_categories"]
            siblings_required = proof["overlap_required_siblings"]
            source_min_rows = proof["source_audit_min_rows"]
            if not isinstance(beneficiary_min, int) or beneficiary_min < 10:
                fail(f"beneficiary_min_categories must be int >=10 for {row['category']}")
            if siblings_required not in {2, 3}:
                fail(f"overlap_required_siblings must be 2 or 3 for {row['category']}")
            if not isinstance(source_min_rows, int) or source_min_rows < 1:
                fail(f"source_audit_min_rows must be int >=1 for {row['category']}")
            if row["artifact_tier"] in {"tier2", "tier3"} and source_min_rows < 3:
                fail(f"tier2/tier3 category {row['category']} must set source_audit_min_rows >= 3")
            if row["artifact_tier"] == "tier3" and artifacts["smoke_required"] is not True:
                fail(f"tier3 category {row['category']} must set smoke_required=true")
            if row["artifact_tier"] != "tier3" and artifacts["smoke_required"] is True:
                fail(f"non-tier3 category {row['category']} cannot set smoke_required=true")

            expected_prefix = f"{row['category']}/references/implementation.md#"
            if not str(proof["beneficiary_matrix_ref"]).startswith(expected_prefix):
                fail(f"beneficiary_matrix_ref must point to implementation.md anchor for {row['category']}")
            if not str(proof["overlap_review_ref"]).startswith(expected_prefix):
                fail(f"overlap_review_ref must point to implementation.md anchor for {row['category']}")

            architecture_rows.append(row)

    if not architecture_rows:
        fail("no architecture categories found in appended families")
    print(f"[OK] architecture manifest rows validated ({len(architecture_rows)} categories)")

    all_rows = []
    for fam in families:
        all_rows.extend(fam.get("categories", []))

    dir_category_names = {p.name for p in category_dirs}
    manifest_category_names = {r.get("category") for r in all_rows}
    if dir_category_names != manifest_category_names:
        missing_in_manifest = sorted(dir_category_names - manifest_category_names)
        missing_in_dirs = sorted(manifest_category_names - dir_category_names)
        fail(f"category dir/manifest mismatch; missing_in_manifest={missing_in_manifest}, missing_in_dirs={missing_in_dirs}")
    print("[OK] category directories and manifest rows are aligned")

    for row in architecture_rows:
        category = row["category"]
        impl = ROOT / category / "references" / "implementation.md"
        if not impl.exists():
            fail(f"missing references/implementation.md for architecture category {category}")
        text = impl.read_text()

        section_positions = []
        for heading in REQUIRED_ARCH_IMPL_SECTIONS:
            token = f"## {heading}"
            idx = text.find(token)
            if idx < 0:
                fail(f"missing required section '{token}' in {category}/references/implementation.md")
            section_positions.append(idx)
        if section_positions != sorted(section_positions):
            fail(f"required sections out of order in {category}/references/implementation.md")

        if SOURCE_AUDIT_HEADER not in text:
            fail(f"missing source-audit header in {category}/references/implementation.md")

        beneficiary = section_text(text, "Beneficiary matrix")
        overlap = section_text(text, "Overlap review")
        source_audit = section_text(text, "Source audit")
        smoke = section_text(text, "Smoke validation")
        if not beneficiary:
            fail(f"missing beneficiary matrix section body in {category}/references/implementation.md")
        if not overlap:
            fail(f"missing overlap review section body in {category}/references/implementation.md")
        if not source_audit:
            fail(f"missing source audit section body in {category}/references/implementation.md")
        if row["artifact_tier"] == "tier3" and not smoke:
            fail(f"tier3 architecture category missing smoke validation section: {category}")

        beneficiary_rows = count_markdown_table_rows(beneficiary, BENEFICIARY_HEADER)
        min_beneficiary = row["proof"]["beneficiary_min_categories"]
        if beneficiary_rows < min_beneficiary:
            fail(f"{category} beneficiary matrix has {beneficiary_rows} rows, needs >= {min_beneficiary}")

        overlap_header_found = all(token in overlap for token in OVERLAP_REQUIRED_TOKENS)
        if not overlap_header_found:
            fail(f"{category} overlap review missing required fields {OVERLAP_REQUIRED_TOKENS}")
        overlap_rows = 0
        for line in overlap.splitlines():
            s = line.strip()
            if s.startswith("|") and "sibling_category" not in s and not re.match(r"^\|\s*-+\s*(\|\s*-+\s*)+\|?$", s):
                overlap_rows += 1
        if overlap_rows < row["proof"]["overlap_required_siblings"]:
            fail(f"{category} overlap review rows {overlap_rows} < required {row['proof']['overlap_required_siblings']}")

        source_rows = count_markdown_table_rows(source_audit, SOURCE_AUDIT_HEADER)
        min_source_rows = row["proof"]["source_audit_min_rows"]
        if source_rows < min_source_rows:
            fail(f"{category} source-audit rows {source_rows} < required {min_source_rows}")
    print("[OK] architecture implementation evidence validated")

    tier3_categories = [r["category"] for r in all_rows if r.get("artifact_tier") == "tier3"]
    for c in tier3_categories:
        if not (ROOT / "scripts" / "smoke" / f"{c}.mjs").exists():
            fail(f"missing smoke script for tier3 category {c}")
    print(f"[OK] tier3 smoke scripts present ({len(tier3_categories)})")

    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        fail("missing README.md")
    readme = readme_path.read_text()
    for c in category_dirs:
        token = f"web-coding-skills-{c.name}"
        if token not in readme:
            fail(f"README missing {token}")
    print("[OK] README includes every category skill token")

    for row in architecture_rows:
        if row["artifact_tier"] in {"tier2", "tier3"}:
            token = f"web-coding-skills-{row['category']}"
            if token not in readme:
                fail(f"tier2/tier3 architecture category must be explicitly mentioned in README: {row['category']}")
    print("[OK] README coverage for architecture tier2/tier3 categories passed")

    print("[PASS] taxonomy validation complete")


if __name__ == "__main__":
    main()
