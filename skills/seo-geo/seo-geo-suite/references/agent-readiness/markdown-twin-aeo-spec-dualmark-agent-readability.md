# Spec（dualmark / agent-readability & Cloudflare Agent Readiness Standard）

- **請求端協商**：已知 AI bot UA（GPTBot/ClaudeBot/PerplexityBot/Claude-Web/anthropic-ai/DevinBot/ManusBot/FirecrawlAgent/OpenCode 等 ~44 個）→ markdown；`Accept: text/markdown` → markdown；`.md` URL（`/about.md`、`/` → `/index.md`）→ markdown；其餘 → HTML 帶 `Link rel="alternate"` 與 machine-readable discovery 宣告。
- **Response headers**：
  | Header | 值 | 說明 |
  |---|---|---|
  | Content-Type | `text/markdown; charset=utf-8` | charset 必帶 |
  | Content-Signal | `ai-train=yes, search=yes, ai-input=yes` | Cloudflare Agent & AI Crawl Control 權限聲明 |
  | Vary | `Accept, Accept-Encoding, User-Agent` | CDN 快取鍵，防快取錯格式，配合 Crawler Hints |
  | X-Markdown-Tokens | `Math.ceil(body.length / 4)` | agent context 預算預估 |
  | X-Robots-Tag | `noindex, nofollow` | twin 不進傳統搜尋索引，避免重複內容 |
  | Link | `<https://domain/index.md>; rel="alternate"; type="text/markdown", <https://domain/llms.txt>; rel="describedby"; type="text/plain", <https://domain/.well-known/mcp/manifest.json>; rel="service-desc"; type="application/json", <https://domain/openapi.json>; rel="service-desc"; type="application/json"` | RFC 8288 機器可讀端點聯網廣告 |
  | Cache-Control | `public, max-age=3600` | 靜態頁提供快取供 Crawler Hints / IndexNow |
- **HTML `<head>` 注入標記**：
  - `<meta name="ai-content-signal" content="ai-train=yes, search=yes, ai-input=yes" />`
  - `<link rel="alternate" type="text/markdown" href="/path.md" />`
  - `<link rel="describedby" type="text/plain" href="/llms.txt" />`
  - `<link rel="service-desc" type="application/json" href="/.well-known/mcp/manifest.json" />`
  - `<link rel="service-desc" type="application/json" href="/openapi.json" />`
- **未知路徑對 AI 請求**：回 markdown 404（agents 信任 status code，會丟棄 404 body）
- **AI 爬蟲白名單清單（robots.txt & User-Agent Matching）**：
  - OpenAI: `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`
  - Anthropic: `ClaudeBot`, `Claude-Web`, `Claude-SearchBot`, `anthropic-ai`
  - Google: `Google-Extended`, `GoogleOther`, `GoogleOther-Image`, `GoogleOther-Video`
  - Perplexity: `PerplexityBot`, `Perplexity-Search`
  - Apple: `Applebot`, `Applebot-Extended`
  - DeepSeek: `DeepSeekBot`
  - Meta: `meta-externalagent`, `Meta-ExternalFetcher`
  - Mistral: `MistralBot`
  - Cohere: `cohere-ai`, `cohere-training-data-crawler`
  - Autonomous / Coding Agents: `DevinBot`, `ManusBot`, `FirecrawlAgent`, `OpenCode`, `ora-agent`, `FriendlyCrawler`
  - Crawlers: `Amazonbot`, `Bytespider`, `Diffbot`, `DuckAssistBot`, `CCBot`, `YouBot`, `Barkrowler`, `Timpibot`, `ImagesiftBot`, `KangarooBot`, `Meltwater`, `Pinterestbot`, `Scrapy`, `Seekr`, `VelenPublicWebCrawler`, `YisouSpider`, `AI2Bot`
