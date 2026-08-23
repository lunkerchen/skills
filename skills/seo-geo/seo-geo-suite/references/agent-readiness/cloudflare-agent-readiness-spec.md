---
name: cloudflare-agent-readiness
description: "Use when making a website compliant with Cloudflare Agent-Readiness (isitagentready.com Level 0-5) standards: Markdown content negotiation, MCP server card, Agent Skills v0.2.0, A2A agent card, ARD ai-catalog, RFC 9727 API catalog, Auth.md, and Content Signals."
author: Hermes Agent
license: MIT
version: 1.0.0
metadata:
  hermes:
    tags: [seo, aeo, geo, cloudflare, agent-readiness, isitagentready, mcp, a2a, llms-txt]
---

# Cloudflare Agent-Readiness (Level 0–5)

Implementation methodology for making any website compliant with Cloudflare's Agent Readiness specifications (validated against `isitagentready.com` and Cloudflare Radar) and Vercel Labs / Ora's `is-agentic.com` standard.

## When to Use

- User asks to make a site "符合 CF 的 agent-readiness" / "提升 Agent 就緒度" / "通過 isitagentready.com 檢測".
- Implementing or upgrading `Accept: text/markdown` content negotiation.
- Publishing `/.well-known/agent-skills/`, `/.well-known/mcp/server-card.json`, `/.well-known/agent-card.json`, or `/.well-known/ai-catalog.json`.
- Configuring RFC 9309 `robots.txt` AI rules and `Content-Signal` headers.

## Agentic Evaluation Standards

- **Is-Agentic (Vercel Labs / Ora)**:
  - **Essential (80 pts)**: No-JS SSR (H1 + 500+ chars), Non-blocked AI crawlers (ora-agent, ClaudeBot, GPTBot, DeepSeekBot), Real 404 with markdown guidance, Real 301/302 redirects, Markdown Content Negotiation with `Vary: Accept, Accept-Encoding`, OpenAPI spec & RFC 9457 JSON errors.
  - **Recommended (20 pts)**: `## When to use this site` in `llms.txt`, Sitemap exists, Content efficiency >= 5%, Rich JSON-LD identity, Trust anchor pages (/about, /contact, /privacy), RateLimit headers (`RateLimit`, `Retry-After`), MCP Server card (`/.well-known/mcp/server-card.json`), 100% native controls & accessible names.
  - **Bonus (+5 pts)**: MCP Apps (`ui://`), Generative UI, A2UI, a11y injection safety.

## Level Architecture

- **Level 1 (Basic)**: `robots.txt` (RFC 9309), `sitemap.xml`, RFC 8288 `Link` response headers.
- **Level 2 (Bot-Aware)**: AI Crawler directives (`GPTBot`, `ClaudeBot`, etc.) + `Content-Signal: ai-train=yes, search=yes, ai-input=yes`.
- **Level 3 (Agent-Readable)**: Dynamic `Accept: text/markdown` content negotiation returning clean markdown with `Vary`, `Content-Signal`, and `X-Markdown-Tokens`.
- **Level 4 (Agent-Integrated)**: `MCP Server Card` (`/.well-known/mcp/server-card.json`), `A2A Agent Card` (`/.well-known/agent-card.json`), `Agent Skills Index v0.2.0` (`/.well-known/agent-skills/index.json`), `RFC 9727 API Catalog` (`/.well-known/api-catalog`).
- **Level 5 (Agent-Native)**: Web Bot Auth (`/.well-known/http-message-signatures-directory`), ARD (`/.well-known/ai-catalog.json`), Auth metadata (`/auth.md` & `/.well-known/oauth-protected-resource`).

## Extended References

- [Implementation Guide](references/guide.md): Code examples across Next.js, Cloudflare Workers, and static sites.
- [Protocol Specifications](references/protocol-specs.md): JSON schemas and header definitions for all 22 checks.
