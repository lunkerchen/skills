#!/usr/bin/env python3
"""Deterministic routing eval for the skills portfolio.

Every golden prompt (scripts/golden.tsv) is scored against each skill's
corpus — frontmatter name + description, the root router row, and every
relative filename inside the skill directory — using ASCII-token and
CJK-bigram overlap. A prompt passes only when its expected skill holds a
strictly unique top score, so routing regressions (description drift,
router blurb edits) fail CI without calling any LLM.

Also enforces coverage: every skills/<category>/<name> found in the repo
must be the expected target of at least one golden prompt, so adding a
skill forces adding routing tests for it.

Usage:
  python3 scripts/eval.py --repo .
Exit 0 = every prompt routes to its expected skill with full coverage.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GOLDEN = "scripts/golden.tsv"
ASCII_WORD = re.compile(r"[a-z0-9]+")
CJK_CHAR = re.compile(r"[㐀-䶿一-鿿]")
ROUTER_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|([^|]*)\|([^|]*)\|")
ASCII_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "for",
    "with", "is", "it", "as", "by", "from", "up", "this", "that", "be",
    "our", "my", "i", "we", "you", "do", "does", "did",
}
CJK_STOP = {"幫我", "一下", "這篇", "這個", "可以", "幫忙", "我想", "請問", "請幫"}


def tokens(text: str) -> set[str]:
    out: set[str] = set()
    text = text.lower()
    for word in ASCII_WORD.findall(text):
        if len(word) >= 2 and word not in ASCII_STOP:
            out.add(word)
    chars = CJK_CHAR.findall(text)
    for a, b in zip(chars, chars[1:]):
        bg = a + b
        if bg not in CJK_STOP:
            out.add(bg)
    return out


def weight(token: str) -> int:
    # ASCII keywords (skill names, module slugs, product names) are far more
    # discriminative than shared CJK bigrams, so weight them double.
    return 2 if token.isascii() else 1


def frontmatter(md: Path) -> str:
    lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return " ".join(ln.split(":", 1)[1] for ln in lines[1:i] if ":" in ln)
    return ""


def build_corpora(repo: Path) -> dict[str, set[str]]:
    rows: dict[str, str] = {}
    root_md = repo / "SKILL.md"
    if root_md.is_file():
        for line in root_md.read_text(encoding="utf-8", errors="replace").splitlines():
            m = ROUTER_ROW.match(line)
            if m:
                rows[m.group(1).strip()] = m.group(2) + " " + m.group(3)
    corpora: dict[str, set[str]] = {}
    skills_root = repo / "skills"
    if not skills_root.is_dir():
        return corpora
    for md in sorted(skills_root.rglob("SKILL.md")):
        rel = md.parent.relative_to(skills_root)
        if len(rel.parts) != 2:
            continue  # structure violations belong to scan.py
        key = f"skills/{rel.parts[0]}/{rel.parts[1]}/SKILL.md"
        text = frontmatter(md) + " " + rows.get(key, "")
        for f in sorted(md.parent.rglob("*")):
            if f.is_file():
                text += " " + str(f.relative_to(md.parent))
        corpora[key] = tokens(text)
    return corpora


def load_golden(repo: Path) -> list[tuple[str, str]]:
    path = repo / GOLDEN
    if not path.is_file():
        sys.exit(f"eval: missing {path}")
    cases: list[tuple[str, str]] = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
            sys.exit(f"eval: {path}:{i}: expected <prompt>\\t<skill path>")
        cases.append((parts[0].strip(), parts[1].strip()))
    if not cases:
        sys.exit(f"eval: {path}: no golden prompts")
    return cases


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    args = ap.parse_args()
    repo = Path(args.repo)
    corpora = build_corpora(repo)
    if not corpora:
        print("eval: no skills found — nothing to evaluate")
        return 0
    cases = load_golden(repo)

    failures: list[str] = []
    covered: set[str] = set()
    for prompt, expected in cases:
        if expected not in corpora:
            failures.append(f"{prompt!r}: expected path not in repo: {expected}")
            continue
        covered.add(expected)
        q = tokens(prompt)
        ranked = sorted(
            (
                (sum(weight(t) for t in q if t in corpus), key)
                for key, corpus in corpora.items()
            ),
            key=lambda kv: (-kv[0], kv[1]),
        )
        top_score, top_key = ranked[0]
        if top_key != expected:
            best = ", ".join(f"{k}={s}" for s, k in ranked[:3])
            failures.append(f"{prompt!r}: routed to {top_key}, want {expected} [{best}]")
        elif top_score == 0:
            failures.append(f"{prompt!r}: expected skill scored 0 — dead keywords")
        elif len(ranked) > 1 and ranked[1][0] == top_score:
            failures.append(f"{prompt!r}: tie at top with {ranked[1][1]} — ambiguous")
        else:
            print(f"PASS {prompt[:44]:<44} -> {expected} ({top_score})")

    for key in sorted(set(corpora) - covered):
        failures.append(f"coverage: no golden prompt routes to {key}")

    if failures:
        for line in failures:
            print(f"FAIL {line}")
        print(f"eval: {len(failures)} failure(s) over {len(cases)} prompt(s)")
        return 1
    print(f"eval: OK ({len(cases)} prompts, {len(corpora)} skills covered)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
