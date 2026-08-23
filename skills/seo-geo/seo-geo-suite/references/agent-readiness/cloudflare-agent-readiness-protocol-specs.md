# Cloudflare Agent-Readiness Protocol Specs & Boilerplate (Level 5 Agent-Native)

本規範收錄 Cloudflare Agent Readiness（`isitagentready.com` 檢測體系）及 Vercel / Ora `is-agentic.com` 標準中，**Level 5 Agent-Native 一次到位**的完整協議規格、端點 JSON 範本與跨框架實作代碼。

---

## 1. 10 大必備協議端點規格（一覽表）

| 端點路徑 | 支援協議 / 標準 | Content-Type | 關鍵欄位與驗證要點 |
|---|---|---|---|
| `/.well-known/agent-skills/index.json` | Agent Skills Discovery RFC v0.2.0 | `application/json` | `$schema`, `skills[]` 且各技能需有真實 `sha256:{hex}` 雜湊 |
| `/.well-known/mcp/server-card.json` | MCP Server Card (SEP-1649) | `application/json` | `serverInfo`, `transport.endpoint`, `capabilities`, `tools[]` |
| `/.well-known/agent-card.json` | A2A (Agent-to-Agent) Protocol | `application/json` | `name`, `version`, `supportedInterfaces[]`, `capabilities`, `skills[]` |
| `/.well-known/ai-catalog.json` | ARD 1.0 (Agent Resource Discovery) | `application/json` | `specVersion: "1.0"`, `host`, `entries[]` (含 `urn:air:...` 識別碼) |
| `/auth.md` | Auth.md Agent Registration | `text/markdown; charset=utf-8` | H1 需包含 `# auth.md`，內嵌 `agent_auth` YAML 與各存取模式 |
| `/.well-known/api-catalog` | RFC 9727 API Catalog | `application/linkset+json; charset=utf-8` | `linkset[]` 包含 `anchor`, `service-desc`, `service-doc`, `status` |
| `/.well-known/oauth-protected-resource` | RFC 9728 Protected Resource Metadata | `application/json; charset=utf-8` | `resource`, `authorization_servers[]`, `scopes_supported[]` |
| `/.well-known/oauth-authorization-server` | RFC 8414 + Agent Auth Extension | `application/json; charset=utf-8` | `issuer`, `agent_auth`（含 `register_uri`, `claim_uri`, 認證模式） |
| `/.well-known/openid-configuration` | OpenID Connect Discovery 1.0 | `application/json; charset=utf-8` | `issuer`, `authorization_endpoint`, `token_endpoint`, `jwks_uri` |
| `/.well-known/http-message-signatures-directory` | Web Bot Auth JWKS Directory | `application/json; charset=utf-8` | `keys[]` 包含至少一組可用於簽名驗證之 JWK 公鑰 |

---

## 2. 10 大協議端點 JSON / Markdown 範本

### (1) `public/.well-known/agent-skills/index.json` (RFC v0.2.0)
```json
{
  "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
  "skills": [
    {
      "name": "search-cases",
      "type": "skill-md",
      "description": "搜尋品牌案例庫與實戰成效數據。",
      "url": "/.well-known/agent-skills/search-cases/SKILL.md",
      "digest": "sha256:ab1e69bc2420d89978a3d893a7f6b41ac21c443b773f006d37cf44622f3da424"
    },
    {
      "name": "service-guide",
      "type": "skill-md",
      "description": "查閱核心服務方案、範圍與交付物標準。",
      "url": "/.well-known/agent-skills/service-guide/SKILL.md",
      "digest": "sha256:c98ff11b0ab587abd24221eaa6cf0473f01782c0c1c70c9bbdf54453caad68c6"
    },
    {
      "name": "consultation-booking",
      "type": "skill-md",
      "description": "獲取預約諮詢流程、官方通訊管道與聯絡方式。",
      "url": "/.well-known/agent-skills/consultation-booking/SKILL.md",
      "digest": "sha256:778646ed1b372d6cf0a13ac55a4de9d2704325d0022454322654cb9ca291381f"
    }
  ]
}
```
*(注意：別忘了複製或建立 legacy 路徑別名 `/.well-known/skills/index.json`)*

---

### (2) `public/.well-known/mcp/server-card.json` (SEP-1649)
*(同源別名：`public/.well-known/mcp.json`)*
```json
{
  "$schema": "https://json.schemastore.org/mcp-server-card.json",
  "serverInfo": {
    "name": "brand-official",
    "version": "2.0.0",
    "title": "Brand Official Agent Services",
    "description": "MCP endpoint for brand services, case studies, and consultation booking"
  },
  "transport": {
    "type": "http",
    "endpoint": "https://www.yourdomain.com/api/mcp"
  },
  "capabilities": {
    "tools": { "list": true },
    "resources": { "list": true },
    "prompts": { "list": true }
  },
  "tools": [
    {
      "name": "search_cases",
      "description": "搜尋品牌客戶案例與成效數據",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": { "type": "string", "description": "搜尋關鍵字" }
        }
      }
    },
    {
      "name": "get_service_info",
      "description": "獲取核心服務方案與交付物說明",
      "inputSchema": {
        "type": "object",
        "properties": {
          "service": { "type": "string" }
        },
        "required": ["service"]
      }
    },
    {
      "name": "get_company_info",
      "description": "獲取公司簡介、官方聯絡管道與預約諮詢資訊",
      "inputSchema": {
        "type": "object",
        "properties": {}
      }
    }
  ]
}
```

---

### (3) `public/.well-known/agent-card.json` (A2A Agent Card)
```json
{
  "$schema": "https://a2a-protocol.org/latest/schema.json",
  "name": "brand-agent",
  "version": "1.0.0",
  "description": "Brand 官方 AI Agent — 提供業務諮詢、案例檢索與服務說明",
  "url": "https://www.yourdomain.com",
  "supportedInterfaces": [
    {
      "url": "https://www.yourdomain.com/api/a2a",
      "protocol": "HTTP+JSON",
      "transport": "HTTP"
    }
  ],
  "capabilities": {
    "informationRetrieval": true,
    "caseSearch": true,
    "consultationBooking": true
  },
  "skills": [
    {
      "id": "search-cases",
      "name": "Search Case Studies",
      "description": "搜尋跨產業客戶案例與實務成效數據。"
    },
    {
      "id": "service-guide",
      "name": "Service Guide",
      "description": "查閱核心服務方案、範圍與交付物。"
    },
    {
      "id": "consultation-booking",
      "name": "Consultation Booking",
      "description": "獲取預約諮詢流程與官方聯絡管道。"
    }
  ]
}
```

---

### (4) `public/.well-known/ai-catalog.json` (ARD 1.0 Manifest)
```json
{
  "$schema": "https://json.schemastore.org/ai-catalog.json",
  "specVersion": "1.0",
  "host": {
    "displayName": "Brand Official",
    "identifier": "yourdomain.com"
  },
  "entries": [
    {
      "identifier": "urn:air:yourdomain.com:context:llms-txt",
      "displayName": "Brand LLM Context",
      "type": "text/plain",
      "url": "https://www.yourdomain.com/llms.txt",
      "description": "Lightweight LLM directory and guidance"
    },
    {
      "identifier": "urn:air:yourdomain.com:context:llms-full-txt",
      "displayName": "Brand Full LLM Context",
      "type": "text/plain",
      "url": "https://www.yourdomain.com/llms-full.txt",
      "description": "Full LLM context and knowledge base"
    },
    {
      "identifier": "urn:air:yourdomain.com:api:catalog",
      "displayName": "Brand API Catalog",
      "type": "application/linkset+json",
      "url": "https://www.yourdomain.com/.well-known/api-catalog",
      "description": "RFC 9727 API Catalog listing public endpoints"
    },
    {
      "identifier": "urn:air:yourdomain.com:mcp:server-card",
      "displayName": "Brand MCP Server Card",
      "type": "application/mcp-server-card+json",
      "url": "https://www.yourdomain.com/.well-known/mcp/server-card.json",
      "description": "MCP Server Card for tools and services"
    },
    {
      "identifier": "urn:air:yourdomain.com:a2a:agent-card",
      "displayName": "Brand A2A Agent Card",
      "type": "application/a2a-agent-card+json",
      "url": "https://www.yourdomain.com/.well-known/agent-card.json",
      "description": "A2A Agent Card for agent-to-agent discovery"
    },
    {
      "identifier": "urn:air:yourdomain.com:skills:index",
      "displayName": "Brand Agent Skills Index",
      "type": "application/agent-skills+json",
      "url": "https://www.yourdomain.com/.well-known/agent-skills/index.json",
      "description": "Agent Skills Discovery RFC v0.2.0 index"
    }
  ]
}
```

---

### (5) `public/auth.md` (Auth.md)
*(重要：標題必須帶 `# auth.md`，內嵌 `agent_auth` 區塊，且 URL 避免包裹行內 backticks 以免掃描器 Regex 抓錯)*
```markdown
# Brand auth.md — Agent Registration & Access Policy

## Overview
Brand provides open, machine-readable access for AI agents to discover services, search case studies, and read public documentation without mandatory credentials.

## Agent Registration & Auth Flow

```yaml
agent_auth:
  skill: "https://www.yourdomain.com/auth.md"
  register_uri: "https://www.yourdomain.com/consult/"
  claim_uri: "https://www.yourdomain.com/consult/"
  claim_endpoint: "https://www.yourdomain.com/consult/"
  identity_endpoint: "https://www.yourdomain.com/api/lead"
  identity_types_supported:
    - "anonymous"
    - "identity_assertion"
  anonymous:
    credential_types_supported:
      - "none"
    claim_uri: "https://www.yourdomain.com/consult/"
  identity_assertion:
    assertion_types_supported:
      - "verified_email"
      - "urn:ietf:params:oauth:token-type:id-jag"
    credential_types_supported:
      - "bearer"
    claim_uri: "https://www.yourdomain.com/consult/"
```

## Supported Access Modes

### 1. Anonymous Read Access (Default)
- **Scope**: `public:read`
- **Authentication**: None required.
- **Claim URI**: https://www.yourdomain.com/consult/
- **Endpoints**:
  - Homepage & Markdown Twins (`Accept: text/markdown` or `/*.md`)
  - LLM Context Directory: https://www.yourdomain.com/llms.txt, https://www.yourdomain.com/llms-full.txt
  - Agent Skills: https://www.yourdomain.com/.well-known/agent-skills/index.json
  - API Catalog: https://www.yourdomain.com/.well-known/api-catalog
  - MCP Server Card: https://www.yourdomain.com/.well-known/mcp/server-card.json
  - A2A Agent Card: https://www.yourdomain.com/.well-known/agent-card.json
- **Rate Limit**: 60 requests / minute per IP.

### 2. Lead & Consultation Submission
- **Scope**: `lead:submit`
- **Authentication**: Anonymous or Client-Identified (`X-Agent-ID` header optional).
- **Claim URI**: https://www.yourdomain.com/consult/
- **Endpoint**: https://www.yourdomain.com/api/lead (POST) or web form at https://www.yourdomain.com/consult/.

## OAuth & Protected Resource Metadata
- **Protected Resource Metadata (RFC 9728)**: https://www.yourdomain.com/.well-known/oauth-protected-resource
- **Authorization Server Metadata (RFC 8414)**: https://www.yourdomain.com/.well-known/oauth-authorization-server
- **OpenID Configuration**: https://www.yourdomain.com/.well-known/openid-configuration
- **JWKS Endpoint**: https://www.yourdomain.com/.well-known/jwks.json
- **Scopes Supported**: `["public:read", "lead:submit"]`
- **Bearer Methods**: `["header"]`

## Contact & Security
- **Security & Tech Inquiries**: info@yourdomain.com
- **Website**: https://www.yourdomain.com
```

---

### (6) `public/.well-known/api-catalog` (RFC 9727)
*(註：同時輸出 `public/.well-known/api-catalog.json`)*
```json
{
  "linkset": [
    {
      "anchor": "https://www.yourdomain.com/api",
      "service-desc": [
        {
          "href": "https://www.yourdomain.com/openapi.json",
          "type": "application/vnd.oai.openapi+json;version=3.0"
        }
      ],
      "service-doc": [
        {
          "href": "https://www.yourdomain.com/llms.txt",
          "type": "text/plain"
        }
      ],
      "status": [
        {
          "href": "https://www.yourdomain.com/api/health",
          "type": "application/json"
        }
      ]
    }
  ]
}
```

---

### (7) `public/.well-known/oauth-protected-resource` (RFC 9728)
*(同時輸出 `public/.well-known/oauth-protected-resource.json`)*
```json
{
  "resource": "https://www.yourdomain.com",
  "authorization_servers": [
    "https://www.yourdomain.com"
  ],
  "scopes_supported": [
    "public:read",
    "lead:submit"
  ],
  "bearer_methods_supported": [
    "header"
  ]
}
```

---

### (8) `public/.well-known/oauth-authorization-server` & `openid-configuration`
```json
{
  "issuer": "https://www.yourdomain.com",
  "authorization_endpoint": "https://www.yourdomain.com/oauth/authorize",
  "token_endpoint": "https://www.yourdomain.com/oauth/token",
  "jwks_uri": "https://www.yourdomain.com/.well-known/jwks.json",
  "response_types_supported": [
    "code",
    "token"
  ],
  "grant_types_supported": [
    "authorization_code",
    "client_credentials"
  ],
  "scopes_supported": [
    "public:read",
    "lead:submit"
  ],
  "agent_auth": {
    "skill": "https://www.yourdomain.com/auth.md",
    "register_uri": "https://www.yourdomain.com/consult/",
    "claim_uri": "https://www.yourdomain.com/consult/",
    "claim_endpoint": "https://www.yourdomain.com/consult/",
    "identity_endpoint": "https://www.yourdomain.com/api/lead",
    "identity_types_supported": [
      "anonymous",
      "identity_assertion"
    ],
    "anonymous": {
      "credential_types_supported": [
        "none"
      ],
      "claim_uri": "https://www.yourdomain.com/consult/"
    },
    "identity_assertion": {
      "assertion_types_supported": [
        "verified_email",
        "urn:ietf:params:oauth:token-type:id-jag"
      ],
      "credential_types_supported": [
        "bearer"
      ],
      "claim_uri": "https://www.yourdomain.com/consult/"
    }
  }
}
```

---

### (9) `public/.well-known/http-message-signatures-directory` & `jwks.json` (Web Bot Auth)
```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "kid": "brand-bot-key-2026",
      "x": "11qYAYKxCrfVS_7TyWQHOg7hcvPapiMlrwIaaPcHURo",
      "use": "sig",
      "alg": "EdDSA"
    }
  ]
}
```

---

### (10) 前端 WebMCP 工具註冊 (HTML `<head>` / Layout)
```html
<script is:inline>
  if (typeof navigator !== 'undefined' && 'modelContext' in navigator && navigator.modelContext?.registerTool) {
    try {
      navigator.modelContext.registerTool({
        name: 'getBrandInfo',
        description: '獲取品牌公司簡介、核心服務與聯絡資訊',
        inputSchema: { type: 'object', properties: {} },
        execute: async () => ({
          company: 'Brand Official',
          website: 'https://www.yourdomain.com',
          services: ['服務A', '服務B', '服務C'],
          llms_txt: 'https://www.yourdomain.com/llms.txt',
          contact: { email: 'info@yourdomain.com', line: 'https://page.line.me/brand' }
        })
      });
    } catch (_) {}
  }
</script>
```

---

## 3. DNS-AID (DNS for AI Discovery) 設定指引

若要在 Cloudflare DNS 達成 DNS-AID 檢驗 100% 打勾，於 Cloudflare Dashboard > DNS > Records 新增：

```text
Type: HTTPS
Name: _index._agents
Value: 1 yourdomain.com. alpn="h2,h3" port=443

Type: HTTPS
Name: _mcp._agents
Value: 1 yourdomain.com. alpn="h2,h3" port=443

Type: HTTPS
Name: _a2a._agents
Value: 1 yourdomain.com. alpn="h2,h3" port=443
```
