#! /usr/bin/env bash
# Mirror selected skills from the canonical source (~/.hermes/skills) into this repo.
#
# Reads scripts/allowlist.tsv — lines: <canonical-relative-path>\t<category>[\tsanitize]
# Lines starting with # are comments. Skills flagged `sanitize` get personal
# paths rewritten by scripts/sanitize.py after the copy. Runs the repo
# scanner afterwards.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CANON="$HOME/.hermes/skills"
ALT_CANON="$HOME/.agents/skills"   # cross-agent shared store — fallback when canonical is missing
ALLOWLIST="$ROOT/scripts/allowlist.tsv"

[[ -f "$ALLOWLIST" ]] || { echo "sync: missing $ALLOWLIST"; exit 1; }

copied=0
while IFS=$'\t' read -r src cat flag; do
  [[ -z "$src" || "$src" == \#* ]] && continue
  if [[ -d "$CANON/$src" ]]; then
    src_dir="$CANON/$src"
  elif [[ -d "$ALT_CANON/$src" ]]; then
    src_dir="$ALT_CANON/$src"
    echo "sync: fallback (agents) $src"
  else
    echo "sync: SKIP (missing) $CANON/$src"
    continue
  fi
  name="$(basename "$src")"
  dest="$ROOT/skills/$cat/$name"
  rm -rf "$dest"
  mkdir -p "$dest"
  cp -R "$src_dir/." "$dest/"
  # Never ship bytecode — .pyc embeds machine-specific source paths.
  find "$dest" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
  echo "sync: $src -> skills/$cat/$name"
  if [[ "${flag:-}" == "sanitize" ]]; then
    python3 "$ROOT/scripts/sanitize.py" "$name" --repo "$ROOT" || exit 1
  fi
  copied=$((copied + 1))
done < "$ALLOWLIST"

echo "sync: $copied skill(s) mirrored"
python3 "$ROOT/scripts/scan.py" --repo "$ROOT" --strict
