[![English](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.zh-TW.md)

# Skills for AI Adoption

Agent skills I use every day as a forward-deployed engineer (FDE) — born from real client projects and production workflows, not vibe coding.

I help businesses adopt AI (星創網絡 / Star Chase). Every skill in this repo started as a workflow I ran for a client, a customer, or my own production system — then got distilled into something small, composable, and installable by any agent.

These skills work with any model and any agent. They are designed to be hacked on and made your own.

## Installation

```bash
npx skills add lunkerchen/skills
```

Pick the skills you want, and which agents to install them on.

## Why these skills exist

Most agent failure comes from missing context, missing feedback loops, and process that owns you instead of you owning it. These skills encode the fixes:

- **Alignment before execution** — grilling sessions, QA scenario design, structured interviews
- **Feedback loops** — static checks, verification gates, audit-before-publish
- **Discipline over ceremony** — small skills that compose, never process frameworks that take over

## What's inside

### ai-adoption

Enterprise AI adoption for real businesses — change management without resistance, FDE delivery frameworks.

- `enterprise-ai-adoption` — 企業 AI 導入的組織採用戰役
- `deep-interview` — 結構化目標澄清：模糊需求 → 一次一問 → 三個維度全 clear
- `multi-agent-debate` — 多代理辯論：對抗式討論收斂到更好結論
- `qa-scenario-design` — 品質證據設計：implement 前先設計 QA scenarios

### engineering

Cloud and infrastructure workflows, hardened by production use.

- `cloudflare-deploy` — 一鍵 commit + deploy Cloudflare Workers/Pages/D1
- `mcp-worker-deploy` — 部署 MCP stateless servers 到 CF Workers
- `hono-workers-testing` — Hono/Workers backend 測試
- `static-html-biome-audit` — Biome lint for single HTML files

### content

Writing and publishing workflows with an anti-AI-slop core.

- `stop-slop` — 去除 AI 寫作味
- `s2t-taiwan` — 簡體轉台灣繁體
- `gzh-design` — 微信公眾號文章排版引擎
- `vocus-article-writing-sop` — 方格子深度文章寫作風格固化

### seo-geo

Search + generative engine optimization for real websites.

- `geolook-tw` — GeoLook GEO analysis for Taiwan market
- `static-site-geo` — SEO/GEO implementation patterns for static HTML sites
- `spa-geo-crawlability` — Fill SPA empty HTML via Edge Functions for AI crawlers
- `geo-content-reformatting` — Reformat H2/H3 into GEO-friendly QA headings

### automation

Forms, notifications, and API integrations that run businesses.

- `gas-form-backend` — 靜態表單接 Google Apps Script 後端
- `line-messaging-api` — 表單資料自動送 LINE 官方帳號
- `turnstile-spin` — Cloudflare Turnstile end-to-end
- `cloudflare-email-service` — Transactional email with Cloudflare Email

## Example request

```text
幫我把這個靜態表單接上 LINE 通知 + Google Sheets 存檔
```

→ the agent loads `gas-form-backend` + `line-messaging-api` and ships the backend, then `turnstile-spin` for spam protection.

## Repository layout

```
skills/<category>/<skill-name>/SKILL.md   ← the skills
scripts/                                  ← sync + scan tooling
registry/skills.json                      ← machine-readable inventory
docs/                                     ← contribution guide
.out-of-scope/                            ← why some skills are NOT here
```

## Requirements

- Any agent that supports skills (Hermes, Claude Code, Codex, etc.)
- `npx` for the installer

## License

MIT — hack around with them, make them your own.
