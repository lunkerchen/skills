---
name: google-search-console-api
description: Use when pulling Google Search Console (GSC) data via API. Query searchAnalytics and properties. Exclude generic SEO theory or keyword planning without API access.
author: Hermes Agent
license: MIT
version: 1.1.0
metadata:
  hermes:
    tags: [seo, gsc, google-search-console, api, search-analytics]
    related_skills: [site-seo-geo-audit, static-site-geo, modern-seo-strategy]
---

# Google Search Console API — Data Access

Retrieve real GSC search analytics (clicks, impressions, CTR, position), site properties, and URL inspection data via official REST endpoints.

## When to Use

- SEO workflows requiring real GSC performance metrics (queries, pages, devices, dates).
- Inspecting verified property lists or indexing status.
- Testing local GSC OAuth tokens and API scopes.
- **Do not trigger** for general SEO brainstorming without API integration.

## API Surface

- **Base URL**: `https://www.googleapis.com/webmasters/v3`
- **List Sites**: `GET /sites` → Returns verified properties.
- **Query Search Analytics**: `POST /sites/{siteUrl}/searchAnalytics/query`
  - Body: `{startDate, endDate, dimensions?, dimensionFilterGroups?, rowLimit?, dataState?}`
  - Output: `rows[]: {keys: string[], clicks, impressions, ctr, position}`
  - Note: `siteUrl` must be URL-encoded (e.g. `sc-domain%3Ayour-app.example.com`).
- **URL Inspection**: `POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect`
- **OAuth Scope**: `https://www.googleapis.com/auth/webmasters.readonly` (or `webmasters` for sitemap submission write operations).

## Local Credential Architecture

- **Primary Token**: `$HERMES_HOME/google_token.json` (Verify `scopes` includes `webmasters` before calling; returns 401 if scope is missing).
- **Dedicated Project Tokens**: e.g., `$HERMES_HOME/google_token_starchase.json` for verified brand properties.
- **Client Library**: Reference tested TypeScript client at `$DEV_PROJECTS/SEO/open-seo/src/server/lib/gscClient.ts`.

## Core Verification Flow

1. **Check Token Scopes**: Run `scripts/probe_gsc.py` or inspect token JSON before initiating API requests.
2. **Execute Query**: Send authenticated request with required dimensions (`query`, `page`, `date`).
3. **Handle Permission Errors**: 401/403 indicate missing OAuth scopes or disabled GCP Search Console API rather than payload syntax errors.

## Extended References & Runbooks

- [OAuth & Loopback Re-Auth Guide](references/oauth-loopback-flow.md): Step-by-step local OAuth re-authentication and GCP setup.
- [Client Site Verification Runbook](references/client-site-gsc-verification.md): Verification via HTML meta tag when API access is unavailable.
- [your-project SEO Loop](references/your-app-seo-loop.md): Practical production analytics loop.
- [Trigger Evals](evals/eval_triggers.json): Automated test fixtures.
