# Cloudflare Agent Readiness Implementation Guide

## 1. Next.js 16 Implementation

### Middleware / Proxy (`proxy.ts` or `middleware.ts`)
```ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const accept = request.headers.get("accept") || "";

  if (
    accept.includes("text/markdown") &&
    !pathname.startsWith("/api") &&
    !pathname.startsWith("/_next") &&
    !pathname.endsWith(".txt") &&
    !pathname.endsWith(".md") &&
    !pathname.endsWith(".xml") &&
    !pathname.endsWith(".json")
  ) {
    const target = pathname.includes("sitemap") ? "/sitemap.md" : "/llms.txt";
    const response = NextResponse.rewrite(new URL(target, request.url));
    response.headers.set("Content-Type", "text/markdown; charset=utf-8");
    response.headers.set("Vary", "Accept, Accept-Encoding");
    response.headers.set("Content-Signal", "ai-train=yes, search=yes, ai-input=yes");
    return response;
  }

  return NextResponse.next();
}
```

### Global Headers (`next.config.ts`)
```ts
headers: [
  {
    source: "/:path*",
    headers: [
      { key: "Vary", value: "Accept, Accept-Encoding" },
      { key: "Content-Signal", value: "ai-train=yes, search=yes, ai-input=yes" },
      {
        key: "Link",
        value: [
          '</llms.txt>; rel="describedby"; type="text/markdown"',
          '</sitemap.xml>; rel="sitemap"; type="application/xml"',
          '</sitemap.md>; rel="alternate"; type="text/markdown"',
          '</.well-known/agent-skills/index.json>; rel="agent-skills"; type="application/json"',
          '</.well-known/api-catalog>; rel="api-catalog"',
          '</.well-known/mcp/server-card.json>; rel="mcp-server-card"; type="application/json"',
        ].join(", "),
      },
    ],
  },
]
```

## 2. Robots.txt Configuration
```txt
User-agent: *
Allow: /

Sitemap: https://domain.com/sitemap.xml
Agentmap: https://domain.com/.well-known/ai-catalog.json
Content-Signal: ai-train=yes, search=yes, ai-input=yes

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Amazonbot
Allow: /
```
