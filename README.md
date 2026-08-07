[![English](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.zh-TW.md)

# Skills for AI Adoption

Agent skills I use every day as a forward-deployed engineer (FDE) — born from real client projects and production workflows, not vibe coding.

I help businesses adopt AI as a forward-deployed engineer. Every skill in this repo started as a workflow I ran for a client, a customer, or my own production system — then got distilled into something small, composable, and installable by any agent.

These skills work with any model and any agent. They are designed to be hacked on and made your own.

## Installation

```bash
npx skills add lunkerchen/skills
```

Pick the skills you want, and which agents to install them on.

## Why these skills exist

Most agent failure comes from missing context, missing feedback loops, and process that owns you instead of you owning it. These skills encode the fixes:

- **Alignment before execution** — structured interviews, QA scenario design, domain models
- **Feedback loops** — static checks, verification gates, audit-before-publish
- **Discipline over ceremony** — small skills that compose, never process frameworks that take over

## What's inside

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

- `mcp-worker-deploy` — deploy stateless MCP 2026-07-28 servers to Cloudflare Workers, auth-first
- `hono-workers-testing` — test Hono/Workers backends: vitest, D1 mocks, fake executionCtx patterns
- `github-code-review` — full code-review pipeline: pre-push review, PR comments, security scan
- `linter-configuration` — emit Biome/Prettier configs matching existing project style, zero churn
- `static-html-biome-audit` — lint standalone HTML with Biome; fix CSS, a11y, semantics
- `typescript-project-verify` — five verification gates for TypeScript monorepos: tsc, vitest, build, format, smoke
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

## Example request

```text
幫我把這個靜態表單接上 LINE 通知 + Google Sheets 存檔
```

→ the agent loads `gas-form-backend` + `line-messaging-api` and ships the backend, then `turnstile-spin` for spam protection.

## Repository layout

```
skills/<category>/<skill-name>/SKILL.md   ← the skills
scripts/                                  ← sync + scan + sanitize tooling
docs/                                     ← contribution guide
.out-of-scope/                            ← why some skills are NOT here
```

## Requirements

- Any agent that supports skills (Hermes, Claude Code, Codex, etc.)
- `npx` for the installer

## License

MIT — hack around with them, make them your own.
