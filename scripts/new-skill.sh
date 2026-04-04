#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOMAIN="${1:-}"
SKILL="${2:-}"

if [[ -z "$DOMAIN" || -z "$SKILL" ]]; then
  echo "Usage: $0 <domain-kebab> <skill-kebab>" >&2
  echo "Example: $0 debugging race-condition-triage" >&2
  exit 1
fi

DOMAIN_DIR="$ROOT/domains/$DOMAIN"
TARGET="$DOMAIN_DIR/$SKILL"
if [[ -e "$TARGET" ]]; then
  echo "Already exists: $TARGET" >&2
  exit 1
fi

mkdir -p "$DOMAIN_DIR"
cd "$DOMAIN_DIR"
npx --yes skills init "$SKILL"
echo >&2
echo "Created: domains/$DOMAIN/$SKILL/SKILL.md" >&2
echo "Next: edit name/description in frontmatter and fill in instructions." >&2
