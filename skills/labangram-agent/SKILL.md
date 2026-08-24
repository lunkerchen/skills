---
name: labangram-agent
description: Use Labangram's public MCP and API surfaces for portfolio discovery, service fit, pricing, and human-confirmed inquiry preparation.
---

# Labangram Agent Skill

Use the canonical Labangram endpoints for machine-readable portfolio, services, pricing, and product inquiry preparation.

## Routes

- Documentation MCP: `https://labangram.kamera-ichi.com/api/mcp`
- Product action MCP: `https://labangram.kamera-ichi.com/api/product-mcp`
- REST contract: `https://labangram.kamera-ichi.com/openapi.json`
- No-auth sandbox: `https://labangram.kamera-ichi.com/api/sandbox/v1/projects`
- Pricing: `https://labangram.kamera-ichi.com/pricing.md`

## Rules

1. Read live `tools/list` and `/pricing.md` before making a claim.
2. Use the sandbox for integration tests; do not write production data during validation.
3. `submit_inquiry` prepares a draft only and requires human confirmation before any outbound action.
4. Never invent prices, project facts, client identities, ratings, or availability.

