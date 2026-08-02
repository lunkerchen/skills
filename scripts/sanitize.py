#!/usr/bin/env python3
"""Idempotent sanitizer for mirrored skills.

sync.sh runs this on skills flagged `sanitize` in the allowlist. It rewrites
personal paths to portable placeholders and deletes stray build artifacts.
Rules are one-way and idempotent: placeholders never re-match source patterns.

Usage: python3 scripts/sanitize.py <skill-name> [--repo DIR]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Most-specific first; applied in order per file.
SPECIFIC_RULES: dict[str, list[tuple[str, str]]] = {
    "markdown-to-podcast": [
        ("/Users/lunker/Movies/專案/Realme 16 Pro/Audio/", "$VOICE_CLONE_AUDIO_DIR/"),
        ("~/Developer/BlueMagpie-TTS/", "$BLUEMAGPIE_TTS_DIR/"),
        ("Realme 16 Pro", "your reference recording"),
        ("（Laban）", "（user）"),
        ("偏好（Laban）", "偏好"),
        ("Laban ", "使用者"),
    ],
    "vocus-article-writing-sop": [
        ("Laban's", "the user's"),
    ],
    "youtube-content": [
        ("this user (Laban)", "this user"),
    ],
    "hono-workers-testing": [
        ("Kamera-ichi", "your-project"),
        ("kamera-ichi.com", "your-app.example.com"),
    ],
    "typescript-project-verify": [
        ("Kamera-ichi", "your-project"),
        ("camera-market", "your-marketplace"),
    ],
}

# Applied to every sanitized skill after SPECIFIC_RULES.
GLOBAL_RULES: list[tuple[str, str]] = [
    ("/Users/lunker/", "$HOME/"),
    ("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Laban/", "$OBSIDIAN_VAULT/"),
    ("$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Laban/", "$OBSIDIAN_VAULT/"),
    ("~/Developer/Projects/", "$DEV_PROJECTS/"),
    ("~/.hermes/", "$HERMES_HOME/"),
]

# Files/dirs removed from the mirrored copy (never from canonical).
DELETE_PATHS: dict[str, list[str]] = {
    "youtube-content": ["scripts/__pycache__"],
    "mcp-worker-deploy": ["references/tavily-worker.md"],
    "local-dev-server-startup": ["references/omniroute-dev-conflict.md"],
}

BINARY_SUFFIXES = {".pyc", ".pyo", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".woff", ".woff2"}


def sanitize_file(path: Path, rules: list[tuple[str, str]]) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False  # binary — leave as-is
    new = text
    for old, new_val in rules:
        new = new.replace(old, new_val)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_name")
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()

    name = args.skill_name
    root = Path(args.repo)
    skill_dir = root / "skills"
    target = None
    for cat_dir in skill_dir.iterdir():
        if (cat_dir / name).is_dir():
            target = cat_dir / name
            break
    if target is None:
        print(f"sanitize: skill '{name}' not found under {skill_dir}")
        return 1

    rules = list(SPECIFIC_RULES.get(name, [])) + list(GLOBAL_RULES)
    changed = 0
    for f in target.rglob("*"):
        if f.is_file() and f.suffix.lower() not in BINARY_SUFFIXES:
            if sanitize_file(f, rules):
                changed += 1
    for rel in DELETE_PATHS.get(name, []):
        p = target / rel
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            print(f"sanitize: deleted {rel}")
    print(f"sanitize: {name} — {changed} file(s) rewritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
