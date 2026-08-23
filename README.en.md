[![English](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)
[![Traditional Chinese](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-9%20Flagships-blue)](https://github.com/lunkerchen/skills/tree/main/skills)
[![AI Agent](https://img.shields.io/badge/AI-Agent%20Ready-brightgreen)](https://github.com/lunkerchen/skills)

# Practical Enterprise AI Agent Suites

> A curated collection of flagship Agent Suites used daily by a Forward-Deployed Engineer (FDE) — distilled from real client engagements, production systems, and high-concurrency workflows.

## What is this?

As an FDE helping enterprises and independent brands deploy AI, this repository consolidates 39+ previously fragmented skills into **9 Flagship Mega-Suites**. Each suite is **self-contained, dependency-free, and packaged with complete specifications and production playbooks**.

These skills are compatible with any modern LLM and CLI Agent framework (Hermes, Claude Code, OpenAI Codex, Cursor, etc.), engineered for immediate adoption and seamless extension.

## Why Flagship Mega-Suites?

Fragmented micro-skills cause agent routing indecision, tool mismatches, and unnecessary token consumption. Consolidating into Flagship Suites delivers three key advantages:

| Value | Mechanism & Highlights |
|---|---|
| **Single Closed-Loop Entrypoint** | Call 1 flagship suite per business domain; internal pipelines automatically chain multi-step workflows |
| **Context Window Optimization** | Eliminates loading multiple overlapping tools, drastically saving context space and tokens |
| **Enterprise-Grade Quality Gates** | Built-in compliance with 2026 standards (Is-Agentic 100-pt audit, Cloudflare L0–L5, RFC 9110 / RFC 9457 / RFC 9727, TypeScript 5-gate verification) |

---

## Installation & Usage

| Tool / Environment | Installation Command / Method |
|---|---|
| **npx skills CLI** (Recommended) | `npx skills add lunkerchen/skills` |
| **Hermes Agent** | Copy or symlink directories into `~/.hermes/skills/` |
| **Claude Code** | Copy into `~/.claude/skills/` |
| **OpenAI Codex** | Copy into `~/.codex/skills/` |
| **Manual / Custom Agent** | Copy specific suite directories directly into your agent workspace |

```bash
# Example: Download all 9 Flagship Mega-Suites
git clone --depth 1 https://github.com/lunkerchen/skills.git
cp -r skills/* ~/.hermes/skills/
```

---

## Catalog (9 Flagship Mega-Suites)

### 1. Search & Agent Readiness

| Flagship Suite | Capabilities & Modules |
|---|---|
| [seo-geo-suite](skills/seo-geo/seo-geo-suite/SKILL.md) | **SEO × GEO × AEO × Agent-Readiness Flagship Workspace**: Four-track search system, Is-Agentic 100-pt audit, Cloudflare L0–L5, full-site reconnaissance, AEO 40-60 character answer extraction, Markdown Twin content negotiation, and 6 CI/CD quality gates |

### 2. Enterprise AI Adoption & Delivery

| Flagship Suite | Capabilities & Modules |
|---|---|
| [fde-adoption-suite](skills/ai-adoption/fde-adoption-suite/SKILL.md) | **FDE Enterprise AI Adoption Flagship**: Structured requirements interview (deep-interview 1Q-at-a-time), QA scenario design, subagent delegation decision matrix (subagent-efficiency), PSF/MVD delivery framework, and peer-driven change management |

### 3. Content Engineering & Multimedia

| Flagship Suite | Capabilities & Modules |
|---|---|
| [content-writing-suite](skills/content/content-writing-suite/SKILL.md) | **Content Writing & Publishing Flagship**: AI cliché removal (stop-slop), humanized copywriting (writing-humanizer), Taiwan Traditional Chinese localization (s2t-taiwan), Vocus tech journalism SOP, and single-file polished HTML article authoring |
| [multimedia-repurpose-suite](skills/content/multimedia-repurpose-suite/SKILL.md) | **Multimedia & Video Repurposing Flagship**: YouTube transcript extraction and chaptering (youtube-content), Instagram Reels viral script breakdown (ig-video-breakdown), and Markdown to Podcast audio synthesis via Edge Neural TTS |

### 4. Frontend & Visual Design

| Flagship Suite | Capabilities & Modules |
|---|---|
| [frontend-design-suite](skills/design/frontend-design-suite/SKILL.md) | **Frontend Design & RWD Polish Flagship**: Night sky dark aesthetics (night-sky-design), Stripe/Linear/Vercel minimalist patterns, strict mobile RWD rules (44px touch targets, zero overflow, zero CLS), and static HTML modernization |

### 5. Software Engineering & Cloud Deployments

| Flagship Suite | Capabilities & Modules |
|---|---|
| [code-quality-suite](skills/engineering/code-quality-suite/SKILL.md) | **Code Quality & Verification Gates Flagship**: Rigorous GitHub pre-landing code review, 5-gate TypeScript verification (typescript-project-verify), automated linter setup (Biome/Prettier), single-file HTML Biome auditing, and npm global maintenance |
| [cloud-workers-suite](skills/engineering/cloud-workers-suite/SKILL.md) | **Cloudflare Workers & MCP Services Flagship**: Hono on Workers test suite (Vitest, D1 mocks, executionContext) and 2026 stateless Model Context Protocol (MCP) server deployment |

### 6. System Automation & Operations

| Flagship Suite | Capabilities & Modules |
|---|---|
| [messaging-bots-suite](skills/automation/messaging-bots-suite/SKILL.md) | **Enterprise Messaging & Notifications Flagship**: Feishu/Lark bots with Bitable sync, LINE Messaging API push alerts, Cloudflare transactional email routing, serverless Google Apps Script forms with Google Sheets, and Coupang Partners affiliate automation |
| [system-watchdog-suite](skills/automation/system-watchdog-suite/SKILL.md) | **System Watchdog & Red Team Flagship**: Personal and team red team audits (personal-red-team), automated vulnerability scans (scan-automation), hash-based web page change monitoring (web-monitor), OWASP & CVE defense, Cloudflare Turnstile anti-bot protection, Gmail AI triage, and Obsidian vault maintenance |

---

## License

Released under the [MIT License](LICENSE).
