#!/usr/bin/env python3
"""Repo-owned validator for the skills portfolio.

Checks (exit 0 = clean):
  1. Every skills/**/SKILL.md exists with name + description frontmatter.
  2. No secret patterns in any tracked file under skills/.
  3. No absolute personal paths (/Users/...) in skill payloads.
  4. No stray files that shouldn't be mirrored (.env, *.pem, *.key).
  5. Frontmatter name matches the directory name (lowercase-hyphens).
  6. `references/...` paths cited in SKILL.md resolve to real files.
  7. SKILL.md token budget: advisory warn at 8 KiB, hard fail at 10 KiB.
  8. README relative links, plugin.json, and mcp.json stay valid.
  9. Repo-root SKILL.md router: frontmatter present; every routed path exists.
 10. Router completeness: every skills/<category>/<name> is listed in the
     root SKILL.md routing table (nothing ships unrouted).
 11. allowlist.tsv ↔ skills/ directory agree in both directions.
 12. Relative Markdown links: hard-fail outside `references/` (router surface),
     advisory warn inside `references/` prose (upstream archive links); code
     samples and placeholder targets ignored; two-base resolution.
     (--strict is accepted for compatibility; findings are always fatal.)

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
PERSONAL_NAME_PATTERNS = (
    re.compile(r"\bLaban\b"),
    re.compile(r"\blunker\b"),
    re.compile(r"\blabanchen\b"),
    re.compile(r"\bCheng Jung Chen\b"),
)
CLIENT_NAME_PATTERNS = (
    re.compile(r"星創網絡"),
    re.compile(r"star-chase"),
    re.compile(r"Star Chase"),
)
FORBIDDEN_FILES = {".env", ".env.*", "*.pem", "*.key", "*.p12", "*.jks"}
# Lines containing these markers are placeholder assignments (YOUR_..., EXAMPLE...),
# not real secrets — skip them.
PLACEHOLDER_HINTS = (
    "YOUR_",
    "YOUR-",
    "EXAMPLE",
    "example.com",
    "<your",
    "CHANGE_ME",
    "placeholder",
    "TODO",
)
FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*[\"']?([^\"'\n]+)")
FRONTMATTER_DESC = re.compile(r"(?m)^description:\s*(.*)$")
NAME_FORMAT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_PATH = re.compile(r"`(references/[A-Za-z0-9_./-]+\.md)`")
REF_DIR = re.compile(r"`(references/[A-Za-z0-9_./-]+/)`")
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
WARN_BYTES = 8 * 1024
FAIL_BYTES = 10 * 1024
SKILL_TREE_REF = re.compile(r"`(skills/[A-Za-z0-9_./-]+/SKILL\.md)`")


FENCED_CODE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def link_findings(md_file: Path, skills_root: Path) -> tuple[list[str], list[str]]:
    """Relative-link check for one markdown file.

    Returns (hard_findings, soft_targets). Code fences and inline code are
    stripped first so documentation samples like `](url)` are not mistaken for
    links. Targets resolve against both the file's directory and the owning
    skill root (reference docs often cite paths from the skill-root
    perspective). Targets without a file extension (placeholders such as `url`
    or `<root>`) are ignored. Links outside `references/` are the router
    surface and fail hard; links inside `references/` prose point at upstream
    archives that may not ship in this mirror, so they are returned as soft
    targets for the caller to aggregate into advisory warnings.
    """
    body = md_file.read_text(encoding="utf-8", errors="replace")
    body = INLINE_CODE.sub(" ", FENCED_CODE.sub(" ", body))
    rel_parts = md_file.relative_to(skills_root).parts
    skill_root = (
        skills_root.joinpath(*rel_parts[:2]) if len(rel_parts) >= 2 else md_file.parent
    )
    hard: list[str] = []
    soft: list[str] = []
    bucket = soft if "references" in rel_parts else hard
    for target in MD_LINK.findall(body):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "${" in target:
            continue
        rel = target.split("#", 1)[0].split("?", 1)[0]
        if not rel:
            continue
        leaf = rel.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]
        if "." not in leaf:
            continue  # placeholder word, not a file path
        if (md_file.parent / rel).exists() or (skill_root / rel).exists():
            continue
        bucket.append(target)
    return [f"broken link ({t})" for t in hard], soft


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return [f"{path}: unreadable"]
    for i, line in enumerate(text.splitlines(), 1):
        for pat in SECRET_PATTERNS:
            match = pat.search(line)
            if match and not any(h in match.group(0) for h in PLACEHOLDER_HINTS):
                findings.append(f"{path}:{i}: secret pattern {pat.pattern[:30]}...")
                break
        for pat in PRIVATE_PATH_PATTERNS:
            if pat.search(line):
                findings.append(f"{path}:{i}: absolute personal path")
                break
        for pat in PERSONAL_NAME_PATTERNS:
            if pat.search(line):
                findings.append(f"{path}:{i}: personal name")
                break
        for pat in CLIENT_NAME_PATTERNS:
            if pat.search(line):
                findings.append(f"{path}:{i}: client name")
                break
    return findings


def validate_skill(skill_dir: Path, warnings: list[str]) -> list[str]:
    findings: list[str] = []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return [f"{skill_dir}: missing SKILL.md"]
    text = md.read_text(encoding="utf-8", errors="replace")
    m_name = FRONTMATTER_NAME.search(text)
    if not m_name:
        findings.append(f"{md}: missing frontmatter name")
    else:
        name = m_name.group(1).strip()
        if not NAME_FORMAT.match(name):
            findings.append(f"{md}: invalid name '{name}' (lowercase-hyphens expected)")
        if name != skill_dir.name:
            findings.append(f"{md}: frontmatter name '{name}' != directory '{skill_dir.name}'")
    if not FRONTMATTER_DESC.search(text):
        findings.append(f"{md}: missing frontmatter description")
    size = md.stat().st_size
    if size > FAIL_BYTES:
        findings.append(f"{md}: {size} bytes exceeds {FAIL_BYTES}-byte token budget")
    elif size > WARN_BYTES:
        warnings.append(f"{md}: {size} bytes over {WARN_BYTES}-byte advisory budget")
    for ref in REF_PATH.findall(text):
        if not (skill_dir / ref).is_file():
            findings.append(f"{md}: broken reference {ref}")
    for ref_dir in REF_DIR.findall(text):
        if not (skill_dir / ref_dir).is_dir():
            findings.append(f"{md}: broken reference dir {ref_dir}")
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
    warnings: list[str] = []
    discovered: set[str] = set()
    for md in skills_root.rglob("SKILL.md"):
        rel = md.parent.relative_to(skills_root)
        if len(rel.parts) != 2:
            findings.append(
                f"{md}: expected skills/<category>/<name>/SKILL.md, found {len(rel.parts)} level(s)"
            )
        else:
            discovered.add(f"skills/{rel.parts[0]}/{rel.parts[1]}")
        findings.extend(validate_skill(md.parent, warnings))
    allow_expected: set[str] = set()
    allow_path = repo / "scripts" / "allowlist.tsv"
    if allow_path.is_file():
        for line in allow_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) >= 2 and fields[0] and fields[1]:
                allow_expected.add(f"skills/{fields[1]}/{Path(fields[0]).name}")
        for path in sorted(allow_expected - discovered):
            findings.append(f"{path}: allowlist entry not present under skills/")
        for path in sorted(discovered - allow_expected):
            findings.append(f"{path}: missing from scripts/allowlist.tsv")
    for f in skills_root.rglob("*"):
        if f.is_file() and any(f.match(g) for g in FORBIDDEN_FILES):
            findings.append(f"{f}: forbidden file type")
    for readme in (repo / "README.md", repo / "README.en.md"):
        if not readme.is_file():
            continue
        for target in MD_LINK.findall(readme.read_text(encoding="utf-8", errors="replace")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            rel = target.split("#", 1)[0]
            if rel and not (repo / rel).exists():
                findings.append(f"{readme}: broken link ({target})")
    for manifest in (repo / "plugin.json", repo / "mcp.json"):
        if manifest.is_file():
            try:
                json.loads(manifest.read_text(encoding="utf-8"))
            except Exception as exc:
                findings.append(f"{manifest}: invalid JSON ({exc})")
    soft_by_file: dict[Path, list[str]] = {}
    for md_file in sorted(skills_root.rglob("*.md")):
        hard, soft = link_findings(md_file, skills_root)
        findings.extend(f"{md_file}: {h}" for h in hard)
        if soft:
            soft_by_file[md_file] = soft
    for f, targets in soft_by_file.items():
        sample = ", ".join(targets[:3]) + ("…" if len(targets) > 3 else "")
        warnings.append(
            f"{f}: {len(targets)} unresolved reference-prose link(s): {sample}"
        )
    root_md = repo / "SKILL.md"
    if root_md.is_file():
        rtext = root_md.read_text(encoding="utf-8", errors="replace")
        rm_name = FRONTMATTER_NAME.search(rtext)
        if not rm_name or not FRONTMATTER_DESC.search(rtext):
            findings.append(f"{root_md}: missing frontmatter name/description")
        elif not NAME_FORMAT.match(rm_name.group(1).strip()):
            findings.append(f"{root_md}: invalid frontmatter name")
        routed = set(SKILL_TREE_REF.findall(rtext))
        for ref in routed:
            if not (repo / ref).is_file():
                findings.append(f"{root_md}: broken routed path {ref}")
        for path in sorted(
            f"{d}/SKILL.md" for d in discovered if f"{d}/SKILL.md" not in routed
        ):
            findings.append(f"{root_md}: skill not listed in routing table: {path}")
    for w in warnings:
        print(f"WARN {w}")
    if findings:
        for line in findings:
            print(f"FAIL {line}")
        print(f"scan: {len(findings)} finding(s)")
        return 1
    print(f"scan: OK ({sum(1 for _ in skills_root.rglob('SKILL.md'))} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
