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
    "local-dev-server-startup": [
        ("omniroute-dev-conflict.md", "port-conflict-example"),
        ("OmniRoute", "your dev tool"),
    ],
    "npm-global-upgrade": [
        ("see `omniroute-maintenance` skill", "see its maintenance skill"),
        ("see `omniroute-maintenance`", "see its maintenance"),
        ("omniroute", "your-tool"),
        ("OmniRoute", "your-tool"),
    ],
    "geo-article-friendly": [
        ("Laban 客製版", "customized"),
        ("（Laban）", ""),
        ("Laban 的語氣", "the user's voice"),
        ("Laban 版", "custom"),
        ("Laban 專屬", "user-specific"),
        ("Laban", "the user"),
    ],
    "webapp-geo-optimization": [
        ("author: Laban", "author: community"),
        ("Laban 版", "custom"),
        ("Laban", "the user"),
    ],
    "seo-geo-suite": [
        ("author: Laban", "author: community"),
        ("Laban 版", "custom"),
        ("Laban", "the user"),
    ],
    "site-seo-geo-audit": [
        ("labangram.kamera-ichi.com", "your-app.example.com"),
    ],
    "enterprise-ai-adoption": [
        ("Laban 的專案", "使用者的專案"),
    ],
    "coupang-partners-api": [
        ("f0366df97500", "YOUR_CRON_JOB_ID"),
        ("咖啡, 泡麵, 零食, 衛生紙, 洗衣精", "咖啡, 泡麵, 零食"),
    ],
    "personal-red-team": [
        ("usagi", "content-profile"),
        ("Laban", "使用者"),
    ],
    "scan-automation": [
        ("bumblebee", "your-scanner"),
    ],
    "gmail-inbox-organizer": [
        ("/opt/homebrew/bin/gws", "gws"),
    ],
    "s2t-taiwan": [
        ("/Users/lunker/Documents/FDE_IG自動貼文發布/素材/xiaohongshu-<id>/", "$IG_SOURCE_DIR/素材/xiaohongshu-<id>/"),
    ],
    "content-writing-suite": [
        ("Laban's", "the user's"),
        ("this user (Laban)", "this user"),
        ("Laban 客製版", "customized"),
        ("（Laban）", ""),
        ("Laban 的語氣", "the user's voice"),
        ("Laban 版", "custom"),
        ("Laban 專屬", "user-specific"),
        ("Laban", "the user"),
        ("/Users/lunker/Documents/FDE_IG自動貼文發布/素材/xiaohongshu-<id>/", "$IG_SOURCE_DIR/素材/xiaohongshu-<id>/"),
        ("$HOME/Documents/FDE_IG自動貼文發布/素材/xiaohongshu-<id>/", "$IG_SOURCE_DIR/素材/xiaohongshu-<id>/"),
    ],
    "cloud-workers-suite": [
        ("Kamera-ichi", "your-project"),
        ("kamera-ichi.com", "your-app.example.com"),
    ],
    "web-monitor": [
        ("momo-gift", "monitored-site"),
    ],
    "static-site-geo": [
        ("Cheng Jung Chen / Laban", "the site owner"),
        ("known as Laban and", "known as"),
        ("['Laban', '@labangram']", "['@your-brand']"),
        (" / Laban:", ":"),
        (" / Laban", ""),
    ],
}

# Applied to every sanitized skill after SPECIFIC_RULES.
GLOBAL_RULES: list[tuple[str, str]] = [
    ("author: Laban", "author: community"),
    ("/Users/lunker/", "$HOME/"),
    ("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Laban/", "$OBSIDIAN_VAULT/"),
    ("$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Laban/", "$OBSIDIAN_VAULT/"),
    ("~/Developer/Projects/", "$DEV_PROJECTS/"),
    ("~/.hermes/", "$HERMES_HOME/"),
    ("Cheng Jung Chen", "the site owner"),
    ("Labangram", "YourBrand"),
    ("labangram.com", "your-brand.example.com"),
    ("labangram", "your-brand"),
    ("kamera-ichi.com", "your-app.example.com"),
    ("kamera-ichi", "your-app"),
    ("Kamera-ichi", "your-project"),
    ("camera-market.tw", "your-marketplace.example.com"),
    ("camera-market", "your-marketplace"),
    ("器材市集", "your-marketplace"),
    ("fde-proposal.pages.dev", "your-proposal.pages.dev"),
    ("course-landing-yongtai.vercel.app", "your-landing.vercel.app"),
    ("course-landing-yongtai", "your-course-landing"),
    ("report-with-photos.vercel.app", "your-demo.vercel.app"),
    ("report-with-photos", "your-demo"),
    ("github.com/lunker", "github.com/your-handle"),
    ("lunkertw", "your-handle"),
    ("coupang-affiliate-bot", "your-affiliate-bot"),
    ("nail-booking", "your-booking-app"),
    ("yongzhi-course-landing", "your-course-landing"),
]

# Files/dirs removed from the mirrored copy (never from canonical).
DELETE_PATHS: dict[str, list[str]] = {
    "youtube-content": ["scripts/__pycache__"],
    "mcp-worker-deploy": ["references/tavily-worker.md"],
    "local-dev-server-startup": ["references/omniroute-dev-conflict.md"],
    "web-monitor": ["references/momo-gift-monitor.md"],
}

# Files renamed in the mirrored copy (content rules cannot touch filenames).
RENAME_PATHS: dict[str, list[tuple[str, str]]] = {
    "spa-geo-crawlability": [
        ("references/kamera-ichi-cloudflare-implementation.md", "references/your-app-cloudflare-implementation.md"),
    ],
    "geo-content-reformatting": [
        ("references/report-with-photos-implementation.md", "references/your-demo-implementation.md"),
    ],
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
    for src_rel, dst_rel in RENAME_PATHS.get(name, []):
        src = target / src_rel
        dst = target / dst_rel
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dst)
            print(f"sanitize: renamed {src_rel} -> {dst_rel}")
    print(f"sanitize: {name} — {changed} file(s) rewritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
