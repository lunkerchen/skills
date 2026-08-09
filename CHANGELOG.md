# Changelog

## [0.3.0] — 2026-08-09

- Dual-source sync: `sync.sh` falls back to `~/.agents/skills` when a skill is missing from the canonical `~/.hermes/skills` tree (4 skills live only in the shared store: `html-article-author`, `ig-video-breakdown`, `cloudflare-email-service`, `static-html-polish`).
- `sync.sh` now strips `__pycache__` from every mirrored skill (`.pyc` embeds machine-specific source paths).
- Add `ig-video-breakdown` (content) — Instagram video breakdown workflow.
- Fix leaks: `s2t-taiwan` now sanitized (personal IG source dir → `$IG_SOURCE_DIR` placeholder); `lark-bot-development` bitable token example → placeholder.
- READMEs: fix duplicated badge block in `README.en.md`, catalog + badge counts 43 → 44.

## [0.2.1] — 2026-08-08

- Chinese-primary landing: `README.md` is now 繁體中文 (GitHub main page); English moved to `README.en.md`; `README.zh-TW.md` removed.
- Skill catalog is now fully linked: every skill name links to its directory in-repo, with a "download a single skill" guide in both languages.

## [0.2.0] — 2026-08-08

- Top-level README overhaul (zh-TW primary): failure-mode table, per-agent installation table, quick start, 4 composed example requests, out-of-scope trust statement.
- Add `personal-red-team` skill (automation) with Chinese reference docs (evidence cheatsheet, brief/report templates, worked example).

## [0.1.0] — 2026-08-02

- Initial release candidate: 40 skills across 6 categories (ai-adoption, automation, content, design, engineering, seo-geo).
- Repo structure, bilingual README, MIT license, CI validator, sync + sanitize tooling.

## Unreleased

- v1 skill set (engineering / content / seo-geo / ai-adoption / automation).
