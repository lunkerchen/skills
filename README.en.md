[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.md)
[![English](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-44-blue)](https://github.com/lunkerchen/skills/tree/main/skills)
[![AI Agent](https://img.shields.io/badge/AI-Agent%20Ready-brightgreen)](https://github.com/lunkerchen/skills)

# Skills for AI Adoption

> Agent skills I use every day as a forward-deployed engineer (FDE) — born from real client projects and production workflows, not vibe coding.

## What this is

I help businesses adopt AI as a forward-deployed engineer. Every skill in this repo started as a workflow I actually ran for a client, a customer, or my own production system — then got distilled into something **small, composable, and installable by any agent**.

These skills work with any model and any agent (Hermes, Claude Code, Codex…). They are designed to be hacked on and made your own.

## Why these skills exist

Most agent failure comes from three causes. These skills encode the fixes:

| Failure mode | The fix encoded | Representative skills |
|---|---|---|
| **Missing context** — the agent doesn't understand your goals, constraints, or success criteria | Align before executing: structured interviews, QA scenario design | `deep-interview`, `qa-scenario-design`, `fde-framework` |
| **Missing feedback loops** — ship and stop, no verification gates | Static checks, verification gates, audit before publish | `typescript-project-verify`, `static-html-polish`, `scan-automation`, `personal-red-team` |
| **Process that owns you** — frameworks eat your productivity | Discipline over ceremony: small composable skills, never process frameworks | The shared design principle of every skill here |

## Installation

| Method | Command / Path |
|---|---|
| **npx skills CLI** (recommended) | `npx skills add lunkerchen/skills` |
| **Hermes** | Copy `skills/<category>/<name>/` to `~/.hermes/skills/` (or symlink) |
| **Claude Code** | Copy to `~/.claude/skills/` |
| **Codex** | Copy to `~/.codex/skills/` |
| **Manual** | Copy the skill directories you need into your agent's skills path |

**You don't need to install everything.** Skills have zero dependencies on each other — pick the categories you need.

### Downloading a single skill

Every skill name in the catalog below is clickable — it links to that skill's directory in this repo:

1. Click the skill name (e.g. [`personal-red-team`](skills/automation/personal-red-team/SKILL.md))
2. Download `SKILL.md` (plus its `references/` directory if present)
3. Drop it into your agent's skills path (see the install table above)

Or clone the whole repo and copy just what you need:

```bash
git clone --depth 1 https://github.com/lunkerchen/skills.git
cp -r skills/automation/personal-red-team ~/.hermes/skills/
```

## Quick start

1. **Pick a skill** — browse the categories below for the workflow you need
2. **Install it** — any method in the table above
3. **Describe the task in plain words** — your agent auto-loads the matching skill (e.g. say "connect this form to LINE notifications" and the agent loads `line-messaging-api`)

## What's inside (44 skills)

### ai-adoption

Enterprise AI adoption for real businesses — change management without resistance, FDE delivery frameworks.

| Skill | Description |
|---|---|
| [enterprise-ai-adoption](skills/ai-adoption/enterprise-ai-adoption/SKILL.md) | frictionless enterprise AI adoption: prove value, reduce fear, let peers lead |
| [fde-framework](skills/ai-adoption/fde-framework/SKILL.md) | FDE playbook: PSF, MVD, shadow work, outcome pricing, career path |
| [deep-interview](skills/ai-adoption/deep-interview/SKILL.md) | one question at a time until goals, constraints, and success criteria are clear |
| [qa-scenario-design](skills/ai-adoption/qa-scenario-design/SKILL.md) | design QA scenarios and failure modes before implementing, with evidence grading |
| [subagent-efficiency](skills/ai-adoption/subagent-efficiency/SKILL.md) | know when direct execution beats spawning a subagent — and when it doesn't |

### automation

Forms, notifications, and integrations that run businesses.

| Skill | Description |
|---|---|
| [gas-form-backend](skills/automation/gas-form-backend/SKILL.md) | free Google Apps Script backend for static forms: Sheets, email, LINE push |
| [lark-bot-development](skills/automation/lark-bot-development/SKILL.md) | build Lark/Feishu bots: app lifecycle, event subscription (WebSocket/webhook), messaging, cards, SDKs |
| [line-messaging-api](skills/automation/line-messaging-api/SKILL.md) | push form submissions to LINE official accounts or support groups via Messaging API |
| [cloudflare-email-service](skills/automation/cloudflare-email-service/SKILL.md) | send and route transactional email with Cloudflare Email Service and Workers |
| [turnstile-spin](skills/automation/turnstile-spin/SKILL.md) | end-to-end Cloudflare Turnstile bot protection: widget, siteverify, validation, framework guides |
| [coupang-partners-api](skills/automation/coupang-partners-api/SKILL.md) | Coupang Partners Taiwan affiliate API: HMAC signing, search, deeplinks, reports |
| [gmail-inbox-organizer](skills/automation/gmail-inbox-organizer/SKILL.md) | automated Gmail triage: label emails by sender and subject, archive promotions |
| [web-monitor](skills/automation/web-monitor/SKILL.md) | cron-based web page change monitoring with fingerprinting and silent-when-unchanged alerts |
| [scan-automation](skills/automation/scan-automation/SKILL.md) | automate system dependency scans, parse NDJSON, log trends, debug hangs |
| [personal-red-team](skills/automation/personal-red-team/SKILL.md) | evidence-first audit of your whole setup: crons, skills, projects → safe fixes + decision briefs |
| [obsidian-cli](skills/automation/obsidian-cli/SKILL.md) | drive Obsidian from the CLI: notes, tasks, search, plugin and theme development |

### note-taking

Knowledge systems and note-vault maintenance.

| Skill | Description |
|---|---|
| [obsidian-vault-organizer](skills/note-taking/obsidian-vault-organizer/SKILL.md) | audit and restructure an Obsidian vault safely: classification, linking, templates, approval gates, and verification |

### content

Writing and publishing workflows with an anti-AI-slop core.

| Skill | Description |
|---|---|
| [stop-slop](skills/content/stop-slop/SKILL.md) | strip AI clichés and robotic cadence from your writing before publishing |
| [writing-humanizer](skills/content/writing-humanizer/SKILL.md) | audit and rewrite AI-sounding text into natural, human voice |
| [s2t-taiwan](skills/content/s2t-taiwan/SKILL.md) | convert Simplified Chinese to Taiwan Traditional Chinese with proper terminology |
| [html-article-author](skills/content/html-article-author/SKILL.md) | convert markdown to standalone dark-themed HTML articles with CJK fonts |
| [vocus-article-writing-sop](skills/content/vocus-article-writing-sop/SKILL.md) | turn AI-tool briefings into polished long-form tech journalism for vocus |
| [markdown-to-podcast](skills/content/markdown-to-podcast/SKILL.md) | turn markdown articles into podcast WAVs with neural TTS and piano intro |
| [youtube-content](skills/content/youtube-content/SKILL.md) | fetch YouTube transcripts and convert them into summaries, threads, and blogs |
| [ig-video-breakdown](skills/content/ig-video-breakdown/SKILL.md) | Instagram video breakdown workflow: download, transcribe, analyze content |

### design

Distinctive single-file HTML design systems.

| Skill | Description |
|---|---|
| [night-sky-design](skills/design/night-sky-design/SKILL.md) | dark night-sky single-file HTML theme with brand gradient accents for decks and pages |
| [rwd-mobile-rules](skills/design/rwd-mobile-rules/SKILL.md) | mandatory mobile RWD rules for every HTML artifact: viewport, grids, touch targets, nav |
| [static-html-polish](skills/design/static-html-polish/SKILL.md) | audit-harden-verify pipeline adding RWD, SEO/GEO, and a11y to static HTML pages |
| [popular-web-designs](skills/design/popular-web-designs/SKILL.md) | 54 real-world design systems (Stripe, Linear, Vercel…) with ready-to-use CSS tokens |

### engineering

Cloud and infrastructure workflows, hardened by production use.

| Skill | Description |
|---|---|
| [mcp-worker-deploy](skills/engineering/mcp-worker-deploy/SKILL.md) | deploy stateless MCP servers to Cloudflare Workers, auth-first |
| [hono-workers-testing](skills/engineering/hono-workers-testing/SKILL.md) | test Hono/Workers backends: vitest, D1 mocks, fake executionCtx patterns |
| [github-code-review](skills/engineering/github-code-review/SKILL.md) | full code-review pipeline: pre-push review, PR comments, security scan |
| [linter-configuration](skills/engineering/linter-configuration/SKILL.md) | emit Biome/Prettier configs matching existing project style, zero churn |
| [static-html-biome-audit](skills/engineering/static-html-biome-audit/SKILL.md) | lint standalone HTML with Biome; fix CSS, a11y, semantics |
| [typescript-project-verify](skills/engineering/typescript-project-verify/SKILL.md) | five verification gates for TypeScript projects: tsc, vitest, build, format, smoke |
| [npm-global-upgrade](skills/engineering/npm-global-upgrade/SKILL.md) | upgrade global npm packages safely: allow-scripts, symlinks, OSV triage |
| [local-dev-server-startup](skills/engineering/local-dev-server-startup/SKILL.md) | start dev servers safely beside launchd/brew-managed services; fix port conflicts |

### seo-geo

Search + generative engine optimization for real websites.

| Skill | Description |
|---|---|
| [modern-seo-strategy](skills/seo-geo/modern-seo-strategy/SKILL.md) | integrated SEO+GEO strategy: semantic maps, EEAT, AI citation optimization, five-phase plan |
| [static-site-geo](skills/seo-geo/static-site-geo/SKILL.md) | GEO/SEO patterns for static sites: JSON-LD, sitemaps, OG images, llms.txt, build verification |
| [spa-geo-crawlability](skills/seo-geo/spa-geo-crawlability/SKILL.md) | fill SPA shells with prerendered content via Edge Functions so AI crawlers see text |
| [geo-content-reformatting](skills/seo-geo/geo-content-reformatting/SKILL.md) | rewrite H2/H3 headings into question form for AI-search visibility, zero design change |
| [geo-article-friendly](skills/seo-geo/geo-article-friendly/SKILL.md) | refit existing articles for AI search: evidence, structure, semantics — preserving the author's voice |
| [site-seo-geo-audit](skills/seo-geo/site-seo-geo-audit/SKILL.md) | whole-site SEO+GEO audit workflow: reconnaissance, schema checks, content gaps, priority matrix |
| [webapp-geo-optimization](skills/seo-geo/webapp-geo-optimization/SKILL.md) | invisible GEO optimization for web apps: structured data, JSON-LD, sitemaps, OG images |

## Example requests

```text
幫我把這個靜態表單接上 LINE 通知 + Google Sheets 存檔
```

→ the agent loads `gas-form-backend` + `line-messaging-api` and ships the backend, then `turnstile-spin` for spam protection.

```text
我的網站 AI 搜尋（ChatGPT/Gemini）都找不到內容
```

→ run `site-seo-geo-audit` first to find the gaps, then `static-site-geo` (static sites) or `spa-geo-crawlability` (SPAs) to implement.

```text
我感覺整個系統哪裡在漏，幫我全面檢查一遍
```

→ `personal-red-team` runs an evidence-first audit of your whole setup (crons / skills / projects): safe fixes + decision briefs.

```text
把這篇文章的 AI 味去掉
```

→ `stop-slop` strips the template junk, `writing-humanizer` finishes the job to natural human voice.

## Repository layout

```
skills/<category>/<skill-name>/SKILL.md   ← the skills (+ optional references/)
scripts/                                  ← sync + scan + sanitize tooling
docs/CONTRIBUTING.md                      ← contribution guide
.out-of-scope/                            ← why some skills are NOT here (trust statement)
```

**Why are some skills not here?** See `.out-of-scope/` — every exclusion decision is documented: client project data, commercial toolkits, personal research collections, retired skills. This public repo only ships workflows that are valuable after generalization; anything with client names, real paths, or credentials is sanitized or excluded.

## Contributing

Want to share a workflow? See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). Everything passes a secret scan and sanitize gate before publish — no client data in the public repo.

## License

MIT — hack around with them, make them your own.
