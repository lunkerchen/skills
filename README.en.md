[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.md)
[![English](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-43-blue)](https://github.com/lunkerchen/skills/tree/main/skills)
[![AI Agent](https://img.shields.io/badge/AI-Agent%20Ready-brightgreen)](https://github.com/lunkerchen/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-43-blue)](https://github.com/lunkerchen/skills/tree/main/skills)
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

## Quick start

1. **Pick a skill** — browse the categories below for the workflow you need
2. **Install it** — any method in the table above
3. **Describe the task in plain words** — your agent auto-loads the matching skill (e.g. say "connect this form to LINE notifications" and the agent loads `line-messaging-api`)

## What's inside (43 skills)

### ai-adoption

Enterprise AI adoption for real businesses — change management without resistance, FDE delivery frameworks.

- `enterprise-ai-adoption` — frictionless enterprise AI adoption: prove value, reduce fear, let peers lead
- `fde-framework` — FDE playbook: PSF, MVD, shadow work, outcome pricing, career path
- `deep-interview` — one question at a time until goals, constraints, and success criteria are clear
- `qa-scenario-design` — design QA scenarios and failure modes before implementing, with evidence grading
- `subagent-efficiency` — know when direct execution beats spawning a subagent — and when it doesn't

### automation

Forms, notifications, and integrations that run businesses.

- `gas-form-backend` — free Google Apps Script backend for static forms: Sheets, email, LINE push
- `lark-bot-development` — build Lark/Feishu bots: app lifecycle, event subscription (WebSocket/webhook), messaging, cards, SDKs
- `line-messaging-api` — push form submissions to LINE official accounts or support groups via Messaging API
- `cloudflare-email-service` — send and route transactional email with Cloudflare Email Service and Workers
- `turnstile-spin` — end-to-end Cloudflare Turnstile bot protection: widget, siteverify, validation, framework guides
- `coupang-partners-api` — Coupang Partners Taiwan affiliate API: HMAC signing, search, deeplinks, reports
- `gmail-inbox-organizer` — automated Gmail triage: label emails by sender and subject, archive promotions
- `web-monitor` — cron-based web page change monitoring with fingerprinting and silent-when-unchanged alerts
- `scan-automation` — automate system dependency scans, parse NDJSON, log trends, debug hangs
- `personal-red-team` — evidence-first audit of your whole setup: crons, skills, projects → safe fixes + decision briefs
- `obsidian-cli` — drive Obsidian from the CLI: notes, tasks, search, plugin and theme development

### note-taking

Knowledge systems and note-vault maintenance.

- `obsidian-vault-organizer` — audit and restructure an Obsidian vault safely: classification, linking, templates, approval gates, and verification

### content

Writing and publishing workflows with an anti-AI-slop core.

- `stop-slop` — strip AI clichés and robotic cadence from your writing before publishing
- `writing-humanizer` — audit and rewrite AI-sounding text into natural, human voice
- `s2t-taiwan` — convert Simplified Chinese to Taiwan Traditional Chinese with proper terminology
- `html-article-author` — convert markdown to standalone dark-themed HTML articles with CJK fonts
- `vocus-article-writing-sop` — turn AI-tool briefings into polished long-form tech journalism for vocus
- `markdown-to-podcast` — turn markdown articles into podcast WAVs with neural TTS and piano intro
- `youtube-content` — fetch YouTube transcripts and convert them into summaries, threads, and blogs

### design

Distinctive single-file HTML design systems.

- `night-sky-design` — dark night-sky single-file HTML theme with brand gradient accents for decks and pages
- `rwd-mobile-rules` — mandatory mobile RWD rules for every HTML artifact: viewport, grids, touch targets, nav
- `static-html-polish` — audit-harden-verify pipeline adding RWD, SEO/GEO, and a11y to static HTML pages
- `popular-web-designs` — 54 real-world design systems (Stripe, Linear, Vercel…) with ready-to-use CSS tokens

### engineering

Cloud and infrastructure workflows, hardened by production use.

- `mcp-worker-deploy` — deploy stateless MCP servers to Cloudflare Workers, auth-first
- `hono-workers-testing` — test Hono/Workers backends: vitest, D1 mocks, fake executionCtx patterns
- `github-code-review` — full code-review pipeline: pre-push review, PR comments, security scan
- `linter-configuration` — emit Biome/Prettier configs matching existing project style, zero churn
- `static-html-biome-audit` — lint standalone HTML with Biome; fix CSS, a11y, semantics
- `typescript-project-verify` — five verification gates for TypeScript projects: tsc, vitest, build, format, smoke
- `npm-global-upgrade` — upgrade global npm packages safely: allow-scripts, symlinks, OSV triage
- `local-dev-server-startup` — start dev servers safely beside launchd/brew-managed services; fix port conflicts

### seo-geo

Search + generative engine optimization for real websites.

- `modern-seo-strategy` — integrated SEO+GEO strategy: semantic maps, EEAT, AI citation optimization, five-phase plan
- `static-site-geo` — GEO/SEO patterns for static sites: JSON-LD, sitemaps, OG images, llms.txt, build verification
- `spa-geo-crawlability` — fill SPA shells with prerendered content via Edge Functions so AI crawlers see text
- `geo-content-reformatting` — rewrite H2/H3 headings into question form for AI-search visibility, zero design change
- `geo-article-friendly` — refit existing articles for AI search: evidence, structure, semantics — preserving the author's voice
- `site-seo-geo-audit` — whole-site SEO+GEO audit workflow: reconnaissance, schema checks, content gaps, priority matrix
- `webapp-geo-optimization` — invisible GEO optimization for web apps: structured data, JSON-LD, sitemaps, OG images

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
