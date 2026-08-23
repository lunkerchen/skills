# Cloudflare Agent-Readiness Protocol Specs & Boilerplate (Level 5)

本手冊提供新專案實作 Level 5 Agent-Native 的完整範本與代碼。

---

## 1. Next.js 內容協商與 Middleware 樣板 (`proxy.ts`)

```ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const accept = request.headers.get("accept") || "";

  // 1. 攔截 AI Agent 的 Markdown 內容協商請求
  if (
    accept.includes("text/markdown") &&
    !pathname.startsWith("/api") &&
    !pathname.startsWith("/_next") &&
    !pathname.startsWith("/admin") &&
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

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|images|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|avif|webm|mp4)$).*)",
  ],
};
```

---

## 2. Next.js 全域標頭與重寫 (`next.config.ts`)

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async headers() {
    return [
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
      {
        source: "/.well-known/:path*",
        headers: [
          { key: "Access-Control-Allow-Origin", value: "*" },
          { key: "Access-Control-Allow-Methods", value: "GET, OPTIONS" },
          { key: "Content-Signal", value: "ai-train=yes, search=yes, ai-input=yes" },
        ],
      },
    ];
  },
  async rewrites() {
    return [
      { source: "/.well-known/llms.txt", destination: "/llms.txt" },
      { source: "/.well-known/llms-full.txt", destination: "/llms-full.txt" },
      { source: "/.well-known/sitemap.md", destination: "/sitemap.md" },
      { source: "/.well-known/mcp.json", destination: "/.well-known/mcp/server-card.json" },
      { source: "/.well-known/agent-skills", destination: "/.well-known/agent-skills/index.json" },
      { source: "/.well-known/auth.md", destination: "/auth.md" },
    ];
  },
};

export default nextConfig;
```

---

## 3. 全套 10 大協議端點 JSON 範本

### (1) `public/.well-known/agent-skills/index.json` (RFC v0.2.0)
```json
{
  "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
  "skills": [
    {
      "name": "consultation-inquiry",
      "type": "skill-md",
      "description": "Submit business inquiry and requirements",
      "url": "/.well-known/agent-skills/consultation-inquiry/SKILL.md",
      "digest": "sha256:..."
    }
  ]
}
```

### (2) `public/.well-known/mcp/server-card.json` (MCP Server Card)
```json
{
  "$schema": "https://modelcontextprotocol.io/schemas/server-card.json",
  "name": "brand-agent-service",
  "title": "Brand AI Agent Service",
  "displayName": "Brand AI Agent Service",
  "description": "Official AI Agent and service discovery interface.",
  "version": "1.0.0",
  "homepage": "https://domain.com",
  "websiteUrl": "https://domain.com",
  "repository": "https://github.com/org/repo",
  "icons": [{ "src": "https://domain.com/icon.png", "mimeType": "image/png" }],
  "transportTypes": ["streamable-http", "http-post"],
  "remotes": [{ "type": "streamable-http", "url": "https://domain.com/api/lead" }],
  "capabilities": { "tools": true, "resources": true, "prompts": true },
  "tools": [ ... ],
  "resources": [ ... ]
}
```

### (3) `public/.well-known/agent-card.json` (A2A Agent Card)
```json
{
  "name": "brand-agent",
  "displayName": "Brand AI Agent",
  "version": "1.0.0",
  "description": "Official A2A Agent.",
  "provider": { "organization": "Brand Inc.", "url": "https://domain.com" },
  "providerName": "Brand Inc.",
  "supportedInterfaces": [{ "url": "https://domain.com/api/lead", "transport": "HTTP-POST", "protocol": "A2A/1.0" }],
  "transportProtocols": ["HTTP-POST"],
  "inputModes": ["text"],
  "outputModes": ["text"],
  "hasSecurity": true,
  "security": [{ "type": "http", "scheme": "bearer" }],
  "capabilities": { "pushNotifications": false, "streaming": false, "extensions": [{ "id": "ap2", "version": "1.0.0" }] },
  "skills": [ ... ]
}
```

### (4) `public/.well-known/ai-catalog.json` (ARD Manifest v1.0)
```json
{
  "specVersion": "1.0",
  "host": { "displayName": "Brand Inc.", "identifier": "did:web:domain.com" },
  "entries": [
    {
      "identifier": "urn:air:domain.com:mcp:service",
      "displayName": "Brand MCP Server",
      "type": "application/mcp-server-card+json",
      "url": "https://domain.com/.well-known/mcp/server-card.json",
      "representativeQueries": ["服務諮詢與報價", "核心業務方案"]
    }
  ]
}
```

### (5) `public/auth.md` (Auth.md)
```markdown
# auth.md — Brand Agent Registration & Authentication

## Audience
This document is for autonomous AI agents and automated systems.

## Agent Registration Endpoints
- **Registration Endpoint**: `POST https://domain.com/api/lead`
- **Registration Method**: Anonymous / Identity Assertion
- **Claim Endpoint**: `https://domain.com/api/lead`
- **Supported Identity Types**: `anonymous`, `identity_assertion`

## Machine-Readable Metadata
- **OAuth Protected Resource**: `https://domain.com/.well-known/oauth-protected-resource`
- **OAuth Authorization Server**: `https://domain.com/.well-known/oauth-authorization-server`
- **Agent Skills Index**: `https://domain.com/.well-known/agent-skills/index.json`
- **MCP Server Card**: `https://domain.com/.well-known/mcp/server-card.json`
- **API Catalog**: `https://domain.com/.well-known/api-catalog`
```

### (6) `app/.well-known/api-catalog/route.ts` (RFC 9727 API Catalog)
輸出 `Content-Type: application/linkset+json; charset=utf-8`。

### (7) `public/.well-known/oauth-protected-resource` (RFC 9728)
```json
{
  "resource": "https://domain.com",
  "authorization_servers": ["https://domain.com"],
  "scopes_supported": ["read:content", "write:lead", "read:catalog"],
  "bearer_methods_supported": ["header"],
  "resource_documentation": "https://domain.com/auth.md"
}
```

### (8) `public/.well-known/oauth-authorization-server` (OAuth Discovery + Agent Auth)
```json
{
  "issuer": "https://domain.com",
  "authorization_endpoint": "https://domain.com/admin/login",
  "token_endpoint": "https://domain.com/api/admin/login",
  "jwks_uri": "https://domain.com/.well-known/jwks.json",
  "response_types_supported": ["code", "token"],
  "grant_types_supported": ["client_credentials", "authorization_code"],
  "scopes_supported": ["read:content", "write:lead", "read:catalog"],
  "bearer_methods_supported": ["header"],
  "agent_auth": {
    "skill": "https://domain.com/.well-known/agent-skills/consultation-inquiry/SKILL.md",
    "register_uri": "https://domain.com/api/lead",
    "identity_types_supported": ["anonymous", "identity_assertion"],
    "anonymous": {
      "credential_types_supported": ["bearer_token"],
      "claim_uri": "https://domain.com/api/lead"
    },
    "identity_assertion": {
      "assertion_types_supported": ["urn:ietf:params:oauth:token-type:id-jag", "verified_email"],
      "credential_types_supported": ["bearer_token"],
      "claim_uri": "https://domain.com/api/lead",
      "revocation_uri": "https://domain.com/api/lead",
      "events_supported": ["revocation"]
    }
  }
}
```

### (9) `public/.well-known/http-message-signatures-directory` & `jwks.json` (Web Bot Auth)
```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "kid": "brand-sig-key-1",
      "x": "11qYAYKxCrfVS_7TyWQHOg7hcvPapiMlrGwHEP1CmlA",
      "use": "sig"
    }
  ]
}
```

### (10) `app/layout.tsx` WebMCP 註冊
```tsx
<Script id="webmcp-tools" strategy="afterInteractive">
  {`if(typeof window!=="undefined"&&window.navigator&&"modelContext"in window.navigator&&typeof window.navigator.modelContext?.registerTool==="function"){try{window.navigator.modelContext.registerTool({name:"inquire_consultation",description:"Submit business inquiry",inputSchema:{type:"object",properties:{name:{type:"string"},email:{type:"string"},need:{type:"string"}},required:["name","email","need"]},execute:async(args)=>{const r=await fetch("/api/lead",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(args)});return await r.json();}});}catch(e){}}`}
</Script>
```

---

## 4. DNS for AI Discovery (DNS-AID) 探索記錄

### BIND 格式（適用於專案 DNS 配置手冊）
```dns
; DNS-AID Entrypoint & Index Records
_index._agents.domain.com.    3600 IN HTTPS 1 domain.com. alpn="h2,h3" port=443 mandatory=alpn,port
_index._agents.domain.com.    3600 IN TXT   "url=https://domain.com/.well-known/ai-catalog.json"
_catalog._agents.domain.com.  3600 IN TXT   "url=https://domain.com/.well-known/ai-catalog.json"

; Protocol Service Bindings
_a2a._agents.domain.com.      3600 IN SVCB  1 domain.com. alpn="a2a" port=443 mandatory=alpn,port
_mcp._agents.domain.com.      3600 IN SVCB  1 domain.com. alpn="mcp" port=443 mandatory=alpn,port
```

### Cloudflare Dashboard 設定清單
| 記錄類型 | 名稱（Name） | 內容 / 參數（Content / Value） | 說明 |
|---|---|---|---|
| **HTTPS** | `_index._agents` | `1 . alpn=h2,h3 port=443 mandatory=alpn,port` | HTTPS 探索端點 |
| **TXT** | `_index._agents` | `url=https://domain.com/.well-known/ai-catalog.json` | 索引入口指向 |
| **TXT** | `_catalog._agents` | `url=https://domain.com/.well-known/ai-catalog.json` | AI Catalog 指向 |
| **SVCB** | `_a2a._agents` | `1 . alpn=a2a port=443 mandatory=alpn,port` | A2A 服務綁定 |
| **SVCB** | `_mcp._agents` | `1 . alpn=mcp port=443 mandatory=alpn,port` | MCP 服務綁定 |
| **DNSSEC** | `domain.com` | 在 Cloudflare DNS 設定啟用 DNSSEC 簽名 | 防止 DNS 欺騙與滿足驗證 |
