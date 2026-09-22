# Changelog

## [Unreleased]

- **Routing eval in CI**: new `scripts/eval.py` + `scripts/golden.tsv` (24 golden prompts, zh + en) — deterministic keyword scoring (ASCII 2x, CJK bigrams) over each skill's frontmatter, router row, and filenames; asserts unique top-1 routing per prompt plus full skill coverage (a new skill without a golden prompt fails). Wired into CI and `sync.sh`.
- **Validator completeness**: root routing table must list every discovered skill (nothing ships unrouted); `allowlist.tsv` ↔ `skills/` verified bidirectionally; relative Markdown links now hard-fail on the router surface (SKILL.md / skill-root docs) while `references/` prose links aggregate to advisory warnings (upstream archive targets that are not mirrored; code samples and placeholder targets like `](url)` are ignored, two-base resolution).
- **Size guard cleared**: `seo-geo-suite` 10.2KB → 6.7KB (intent-router matrix + nine pitfalls verbatim → `references/`) and `sync-lark-wiki` 10.2KB → 8.1KB (OAuth staging, permission-boundary, and pitfall prose consolidated into `references/`); both now under the 8KiB advisory line with zero size warnings.
- **Link hygiene**: repaired 31 import-era intra-document links across `messaging-bots-suite`, `system-watchdog-suite`, and `seo-geo-suite` (bundle import prefixed filenames without rewriting relative targets; fixed on the canonical side and re-mirrored — suffix-unique match with own-stem disambiguation, self-verified). Advisory link warnings dropped 11 → 4; the residue is genuinely unmirrored upstream targets (`evals/eval_triggers.json`, `references/client-site-gsc-verification.md`, `references/your-app-seo-loop.md`).

## [1.0.0] — 2026-09-23

- **Catalog accuracy**: flagship count corrected from 9 to 10 across both READMEs (badge, intro, bash example, catalog heading); `plugin.json` version now aligns with this CHANGELOG as the single repo-level version source.
- **Merge PR #1**: add `sync-lark-wiki` (automation) — staged-scope Lark Wiki Markdown sync with preview, read-back, and permission troubleshooting; cataloged under a new Standalone Skills section.
- **Catalog `labangram-agent`**: moved to `skills/plugin/`, added to `allowlist.tsv`, and mirrored from canonical `~/.hermes/skills/labangram-agent/`; root `plugin.json` / `mcp.json` (agent-plugins.org manifest for the public Labangram MCP endpoints) documented as intentionally paired with this skill.
- **Validator hardening**: `scan.py` placeholder hints now match against the matched secret itself instead of the whole line (fewer false negatives). New checks: frontmatter `name` must match the directory name, cited `references/` files/dirs must exist, SKILL.md token budget (advisory warn 8 KiB / hard fail 10 KiB), README relative links, `plugin.json` / `mcp.json` JSON validity, and the two-level `skills/<category>/<name>/` layout.
- **seo-geo-suite v2.1.0 slimming**: `SKILL.md` cut from 33.8 KB to ~10 KB as a pure intent router (four-track table, compact GEOFlow summary, intent matrix, module/pipeline one-liners, pitfall list, Taiwan one-liner, folder-level references map). Detail moved verbatim into new `references/` files: `geoflow-operating-model.md`, `modules-and-pipelines.md`, `pitfalls.md`, `taiwan-localization.md`, plus a full-file `INDEX.md` for two-stage lookup. `sanitize.py` now rewrites mirror-only filename mentions so the references map never dangles.
- **Repo metadata**: GitHub description and topics (`ai-agents`, `agent-skills`, `llm`, `mcp`, `seo`, `geo`, `claude-code`, `codex`, `cloudflare-workers`, `skills`) added.
- **Distribution fix**: the README-recommended `npx skills add lunkerchen/skills` was broken (registry lookup miss). Both READMEs now use the git-URL form, verified locally: the skills CLI installs the repo as one unit and only discovers a root-level `SKILL.md`, so a repo-native umbrella router `SKILL.md` (12-row routing table → suite → `references/`) ships at the repo root. `scan.py` validates its frontmatter and every routed path.

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
