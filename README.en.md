[![English](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)
[![Traditional Chinese](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-39-blue)](https://github.com/lunkerchen/skills/tree/main/skills)
[![AI Agent](https://img.shields.io/badge/AI-Agent%20Ready-brightgreen)](https://github.com/lunkerchen/skills)

# Practical Enterprise AI Skills

> A curated collection of Agent Skills used daily by a Forward-Deployed Engineer (FDE) — distilled from real client engagements, production systems, and high-concurrency workflows, not vibe coding or trivial prompts.

## What is this?

As an FDE helping enterprises and independent brands adopt AI, every skill in this repository represents a Battle-Tested Standard Operating Procedure (SOP) originally executed on production environments. They have been refined into **lean, modular, dependency-free, and agent-agnostic packages**.

These skills are compatible with any modern LLM and CLI Agent framework (Hermes, Claude Code, OpenAI Codex, Cursor, etc.), designed from the ground up to be adopted or customized for your exact workflows.

## Why these skills exist

Most AI Agent execution failures trace back to three root causes. These skills encode the solutions directly into verifiable contracts:

| Failure Mode | Root Cause | Solution & Mechanism | Representative Skills |
|---|---|---|---|
| **Ambiguous Context** | Agent lacks understanding of real business constraints, implicit boundaries, and acceptance criteria | Align before execution: Structured interview, QA scenario design, and FDE delivery loops | `deep-interview`, `qa-scenario-design`, `fde-framework` |
| **Missing Feedback Loops** | Submissions made without objective quality assertions and verification gates | Pre-ship automated assertions, multi-layer static audits, and active red-teaming | `typescript-project-verify`, `static-html-polish`, `personal-red-team` |
| **Over-Engineered Frameworks** | Bloated rituals and fragile scaffolding that destroy developer productivity | Occam's razor: lean, composable, zero external overhead, and grounded evidence | Core philosophy across all skills |

---

## 🌟 Flagship Spotlight: `seo-geo-suite` (SEO × GEO × AEO × Agent-Readiness)

In 2026, search visibility is no longer just about Google's traditional blue link rankings. We have consolidated 12 previously fragmented skills into one unified flagship package: **[`seo-geo-suite`](skills/seo-geo/seo-geo-suite/SKILL.md)**, defining the complete **Four-Track Modern Search & Agentic Ecosystem**:

1. **SEO (Search Engine Optimization)**: Google/Bing rankings, Topic Clusters, Core Web Vitals, and backlink topology.
2. **GEO (Generative Engine Optimization)**: Brand consensus (Share of Voice) and deep anti-summarization content across ChatGPT, Claude, DeepSeek, and Gemini.
3. **AEO (Answer Engine Optimization)**: Direct answer card extraction for Perplexity and Google AIO via inverted-pyramid 40–60 character top conclusions.
4. **Agent-Readiness**: Full compliance with **Is-Agentic 100-Point Audit** and **Cloudflare Level 0–5 Standards** (No-JS SSR, Markdown Content Negotiation with `Vary: Accept`, standardized `llms.txt`, Agent-Friendly 404 recovery, RFC 9457 structured errors, and MCP Server Cards).

---

## Installation & Usage

| Tool / Environment | Installation Command / Method |
|---|---|
| **npx skills CLI** (Recommended) | `npx skills add lunkerchen/skills` |
| **Hermes Agent** | Copy or symlink directories into `~/.hermes/skills/` |
| **Claude Code** | Copy into `~/.claude/skills/` |
| **OpenAI Codex** | Copy into `~/.codex/skills/` |
| **Manual / Custom Agent** | Copy specific skill directories directly into your agent's workspace |

> **Note**: Each skill is 100% self-contained with zero cross-skill dependencies. Pick and install only the categories or skills you need.

### Downloading a Single Skill

Every skill in the catalog links directly to its source directory in this repo:

```bash
# Example: Download only the flagship seo-geo-suite
git clone --depth 1 https://github.com/lunkerchen/skills.git
cp -r skills/seo-geo/seo-geo-suite ~/.hermes/skills/
```

---

## Catalog (39 Production-Ready Skills)

### seo-geo — Search, Generative Engines & Agent Readiness

Flagship workspace covering traditional search, AI model citations, direct answer extraction, and Agentic API contracts.

| Skill | Description |
|---|---|
| [seo-geo-suite](skills/seo-geo/seo-geo-suite/SKILL.md) | **SEO × GEO × AEO × Agent-Readiness Flagship Workspace**: All-in-one four-track search system, Is-Agentic 100-pt audit, Cloudflare L0–L5, full-site reconnaissance, AEO content restructuring, and 6 CI/CD quality gates |

### ai-adoption — Enterprise AI Adoption & Delivery

Playbooks for organizational AI adoption, stakeholder alignment, and field delivery.

| Skill | Description |
|---|---|
| [enterprise-ai-adoption](skills/ai-adoption/enterprise-ai-adoption/SKILL.md) | Organizational AI adoption: demonstrating measurable business value, mitigating fear, and creating peer champions |
| [fde-framework](skills/ai-adoption/fde-framework/SKILL.md) | Forward-Deployed Engineer playbook: PSF framework, MVD delivery, shadow methodology, and value pricing |
| [deep-interview](skills/ai-adoption/deep-interview/SKILL.md) | Structured requirements interview: one question at a time until goals, constraints, and success criteria are 100% clear |
| [qa-scenario-design](skills/ai-adoption/qa-scenario-design/SKILL.md) | Quality evidence design: formulate test scenarios, edge cases, and failure modes before writing code |
| [subagent-efficiency](skills/ai-adoption/subagent-efficiency/SKILL.md) | Subagent orchestration decision matrix: identifying parallelizable tasks while preventing token waste |

### automation — System & Workflow Automation

Pipelines connecting messaging apps, cloud services, and local development environments.

| Skill | Description |
|---|---|
| [lark-bot-development](skills/automation/lark-bot-development/SKILL.md) | Feishu/Lark bot engineering: event subscriptions, interactive cards, and two-way Bitable integration |
| [line-messaging-api](skills/automation/line-messaging-api/SKILL.md) | LINE Messaging API push: automated form/order notifications and customer support group alerts |
| [cloudflare-email-service](skills/automation/cloudflare-email-service/SKILL.md) | Transactional email delivery and inbound handling with Cloudflare Email Routing + Workers |
| [turnstile-spin](skills/automation/turnstile-spin/SKILL.md) | End-to-end Cloudflare Turnstile integration and bot protection pipeline |
| [gmail-inbox-organizer](skills/automation/gmail-inbox-organizer/SKILL.md) | AI-powered Gmail triage, label routing, and automated inbox summaries |
| [obsidian-cli](skills/automation/obsidian-cli/SKILL.md) | Obsidian terminal automation: note management, search, and wikilink graph creation |
| [gas-form-backend](skills/automation/gas-form-backend/SKILL.md) | Serverless Google Apps Script backends and Google Sheets synchronization for static web forms |
| [web-monitor](skills/automation/web-monitor/SKILL.md) | Lightweight hash-based web page change monitoring and silent watchdog alerts |
| [scan-automation](skills/automation/scan-automation/SKILL.md) | Automated system and dependency scanning with structured findings and remediation advice |
| [coupang-partners-api](skills/automation/coupang-partners-api/SKILL.md) | Coupang Partners Taiwan affiliate API integration with HMAC signatures and product discovery |
| [personal-red-team](skills/automation/personal-red-team/SKILL.md) | Personal and team red team audit: auditing scheduled crons, hidden operational risks, and security gaps |

### content — Content Engineering & Multimedia

High-fidelity copywriting, neural TTS generation, and video transcript extraction.

| Skill | Description |
|---|---|
| [stop-slop](skills/content/stop-slop/SKILL.md) | Remove AI writing patterns: eliminate cliché phrases, boilerplate padding, and restore authentic human voice |
| [writing-humanizer](skills/content/writing-humanizer/SKILL.md) | Humanized copy polishing: preserve factual depth while enhancing cadence and conversational flow |
| [s2t-taiwan](skills/content/s2t-taiwan/SKILL.md) | Simplified to Traditional Chinese localization tailored for Taiwan terminology and phrasing |
| [html-article-author](skills/content/html-article-author/SKILL.md) | Single-file polished HTML article publishing with typography, RWD, and SEO metadata |
| [vocus-article-writing-sop](skills/content/vocus-article-writing-sop/SKILL.md) | Vocus long-form tech journalism SOP: tech reporter perspective, executive summaries, and structured analyses |
| [markdown-to-podcast](skills/content/markdown-to-podcast/SKILL.md) | Markdown to Podcast audio conversion via Edge Neural TTS with multi-voice dialogues |
| [youtube-content](skills/content/youtube-content/SKILL.md) | YouTube transcript extraction, chaptering, and multi-format content repurposing |
| [ig-video-breakdown](skills/content/ig-video-breakdown/SKILL.md) | Instagram Reels transcript extraction and viral shot-by-shot script breakdown |

### design — UI & Visual Design

Dark-mode aesthetics, strict mobile RWD guidelines, and accessibility hardening.

| Skill | Description |
|---|---|
| [night-sky-design](skills/design/night-sky-design/SKILL.md) | Night sky single-file HTML styling: dark canvas, glassmorphism, and brand gradients |
| [rwd-mobile-rules](skills/design/rwd-mobile-rules/SKILL.md) | Strict mobile RWD rules: 44px touch targets, viewport overflow prevention, and zero layout shift |
| [static-html-polish](skills/design/static-html-polish/SKILL.md) | Static HTML modernization: retrofitting RWD, semantic markup, a11y, and modern CSS |
| [popular-web-designs](skills/design/popular-web-designs/SKILL.md) | Modern tech brand aesthetic guidelines: Stripe, Linear, and Vercel minimalist patterns |

### engineering — Software Engineering & Verification

Development environment hygiene, TypeScript assertions, and code review gates.

| Skill | Description |
|---|---|
| [typescript-project-verify](skills/engineering/typescript-project-verify/SKILL.md) | 5-gate TypeScript verification: type-checking, dependency compliance, and runtime sanity |
| [github-code-review](skills/engineering/github-code-review/SKILL.md) | Rigorous pre-landing code review: security scans, quality gates, architectural feedback, and actionable diffs |
| [linter-configuration](skills/engineering/linter-configuration/SKILL.md) | Automated linter configuration: one-click setup for Biome, Prettier, and ESLint |
| [static-html-biome-audit](skills/engineering/static-html-biome-audit/SKILL.md) | Biome static analysis for single-file HTML: CSS, syntax, and accessibility checks |
| [npm-global-upgrade](skills/engineering/npm-global-upgrade/SKILL.md) | Global npm package maintenance: handling symlinks, allow-scripts, and dependency conflicts |
| [local-dev-server-startup](skills/engineering/local-dev-server-startup/SKILL.md) | Local dev server management: resolving port conflicts and coexistence with macOS background services |
| [hono-workers-testing](skills/engineering/hono-workers-testing/SKILL.md) | Hono on Cloudflare Workers test suite: Vitest, D1 mocks, and execution context simulation |
| [mcp-worker-deploy](skills/engineering/mcp-worker-deploy/SKILL.md) | Deploy stateless Model Context Protocol (MCP) servers to Cloudflare Workers |

### security — Cybersecurity

| Skill | Description |
|---|---|
| [website-security-owasp-cve](skills/security/website-security-owasp-cve/SKILL.md) | Website vulnerability scanning: OWASP Top 10 compliance and CVE dependency auditing |

### note-taking — Second Brain & Knowledge Management

| Skill | Description |
|---|---|
| [obsidian-vault-organizer](skills/note-taking/obsidian-vault-organizer/SKILL.md) | Obsidian vault organization: PARA hierarchy, broken wikilink repair, and index creation |

---

## License

Released under the [MIT License](LICENSE).
