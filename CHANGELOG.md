# Changelog

## [1.0.0] — 2026-09-23

- **Catalog accuracy**: flagship count corrected from 9 to 10 across both READMEs (badge, intro, bash example, catalog heading); `plugin.json` version now aligns with this CHANGELOG as the single repo-level version source.
- **Merge PR #1**: add `sync-lark-wiki` (automation) — staged-scope Lark Wiki Markdown sync with preview, read-back, and permission troubleshooting; cataloged under a new Standalone Skills section.
- **Catalog `labangram-agent`**: moved to `skills/plugin/`, added to `allowlist.tsv`, and mirrored from canonical `~/.hermes/skills/labangram-agent/`; root `plugin.json` / `mcp.json` (agent-plugins.org manifest for the public Labangram MCP endpoints) documented as intentionally paired with this skill.
- **Validator hardening**: `scan.py` placeholder hints now match against the matched secret itself instead of the whole line (fewer false negatives). New checks: frontmatter `name` must match the directory name, cited `references/` files/dirs must exist, SKILL.md token budget (advisory warn 8 KiB / hard fail 10 KiB), README relative links, `plugin.json` / `mcp.json` JSON validity, and the two-level `skills/<category>/<name>/` layout.
- **seo-geo-suite v2.1.0 slimming**: `SKILL.md` cut from 33.8 KB to ~10 KB as a pure intent router (four-track table, compact GEOFlow summary, intent matrix, module/pipeline one-liners, pitfall list, Taiwan one-liner, folder-level references map). Detail moved verbatim into new `references/` files: `geoflow-operating-model.md`, `modules-and-pipelines.md`, `pitfalls.md`, `taiwan-localization.md`, plus a full-file `INDEX.md` for two-stage lookup. `sanitize.py` now rewrites mirror-only filename mentions so the references map never dangles.
- **Repo metadata**: GitHub description and topics (`ai-agents`, `agent-skills`, `llm`, `mcp`, `seo`, `geo`, `claude-code`, `codex`, `cloudflare-workers`, `skills`) added.

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
