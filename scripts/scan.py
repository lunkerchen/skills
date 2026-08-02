#!/usr/bin/env python3
"""Repo-owned validator for the skills portfolio.

Checks (exit 0 = clean):
  1. Every skills/**/SKILL.md exists with name + description frontmatter.
  2. No secret patterns in any tracked file under skills/.
  3. No absolute personal paths (/Users/...) in skill payloads.
  4. No stray files that shouldn't be mirrored (.env, *.pem, *.key).

Usage:
  python3 scripts/scan.py --repo . [--strict]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY"),
    re.compile(r"(?i)LINE_CHANNEL_TOKEN\s*=\s*\S+"),
    re.compile(r"(?i)LINE_GROUP_ID\s*=\s*\S+"),
    re.compile(r"(?i)TURNSTILE_SECRET\s*=\s*\S+"),
    re.compile(r"script\.google\.com/macros/s/[A-Za-z0-9_-]{30,}"),
)
PRIVATE_PATH_PATTERNS = (
    re.compile(r"/Users/[A-Za-z0-9_]+/"),
    re.compile(r"/home/[A-Za-z0-9_]+/"),
)
FORBIDDEN_FILES = {".env", ".env.*", "*.pem", "*.key", "*.p12", "*.jks"}
FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*[\"']?([^\"'\n]+)")
FRONTMATTER_DESC = re.compile(r"(?m)^description:\s*(.*)$")


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return [f"{path}: unreadable"]
    for i, line in enumerate(text.splitlines(), 1):
        for pat in SECRET_PATTERNS:
            if pat.search(line):
                findings.append(f"{path}:{i}: secret pattern {pat.pattern[:30]}...")
                break
        for pat in PRIVATE_PATH_PATTERNS:
            if pat.search(line):
                findings.append(f"{path}:{i}: absolute personal path")
                break
    return findings


def validate_skill(skill_dir: Path) -> list[str]:
    findings: list[str] = []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return [f"{skill_dir}: missing SKILL.md"]
    text = md.read_text(encoding="utf-8", errors="replace")
    if not FRONTMATTER_NAME.search(text):
        findings.append(f"{md}: missing frontmatter name")
    if not FRONTMATTER_DESC.search(text):
        findings.append(f"{md}: missing frontmatter description")
    for f in skill_dir.rglob("*"):
        if f.is_file():
            findings.extend(scan_file(f))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    repo = Path(args.repo)
    findings: list[str] = []
    skills_root = repo / "skills"
    if not skills_root.exists():
        print("scan: no skills/ directory — nothing to validate")
        return 0
    for md in skills_root.rglob("SKILL.md"):
        findings.extend(validate_skill(md.parent))
    for f in skills_root.rglob("*"):
        if f.is_file() and any(f.match(g) for g in FORBIDDEN_FILES):
            findings.append(f"{f}: forbidden file type")
    if findings:
        for line in findings:
            print(f"FAIL {line}")
        print(f"scan: {len(findings)} finding(s)")
        return 1
    print(f"scan: OK ({sum(1 for _ in skills_root.rglob('SKILL.md'))} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
