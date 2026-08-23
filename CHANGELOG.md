# Changelog

## [0.4.0] — 2026-08-24

- **Mega-Skill Consolidation**: Consolidate 12 fragmented SEO/GEO/AEO skills into a single flagship umbrella skill: `seo-geo-suite` (v2.0.0).
- **Four-Track Search & Agentic Ecosystem**: Integrate traditional search (SEO), generative engine optimization (GEO: ChatGPT/Claude/DeepSeek), answer engine optimization (AEO: Perplexity/AIO), and autonomous agent readiness (Is-Agentic & Cloudflare L0–L5).
- **Agentic Standards & Protocol Alignment**:
  - Integrate Vercel Labs / Ora `is-agentic.com` 100-point audit framework (Essential 80 + Recommended 20 + Bonus 5).
  - Enforce RFC 9110 (HTTP Semantics & Content Negotiation with `Vary: Accept, Accept-Encoding`).
  - Enforce RFC 9457 (`application/problem+json`) structured error contracts.
  - Enforce RFC 9727 API Catalog and Cloudflare L0–L5 readiness.
  - Mandatory `## When to use this site (Agent instructions)` in `llms.txt`.
  - Standardized Agent-friendly 404 recovery pages with markdown indices.
- **Cleanups & Catalog Refinement**: Catalog refined to 39 high-impact production skills; verified by `scripts/scan.py` (0 warnings).

## [0.3.0] — 2026-08-09

- Dual-source sync: `sync.sh` falls back to `~/.agents/skills` when a skill is missing from the canonical `~/.hermes/skills` tree.
- `sync.sh` now strips `__pycache__` from every mirrored skill.
- Add `ig-video-breakdown` (content) — Instagram video breakdown workflow.
- Fix leaks: `s2t-taiwan` and `lark-bot-development` examples sanitized.
- READMEs: fix duplicated badge block, catalog counts updated.

## [0.2.1] — 2026-08-08

- Chinese-primary landing: `README.md` is now 繁體中文; English moved to `README.en.md`.
- Fully linked skill catalog linking directly to in-repo files.
