[![English](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.zh-TW.md)

# AI 導入實戰 Skills

我每天在用的 Agent skills — 作為 forward-deployed engineer（FDE），全部從真實客戶專案與生產環境淬煉而來，不是 vibe coding。

我幫企業導入 AI（星創網絡 / Star Chase）。這個 repo 裡的每個 skill，原本都是我在客戶、或自己的生產系統上跑過的工作流 — 然後被濃縮成小、可組合、任何 agent 都能安裝的 skill。

這些 skills 相容任何模型、任何 agent，設計上就是拿來改造成你自己的。

## 安裝

```bash
npx skills add lunkerchen/skills
```

選擇你要的 skills，以及要安裝到哪些 agent。

## 為什麼有這些 skills

Agent 失敗大多來自：缺少上下文、缺少回饋迴圈、流程反過來控制你。這些 skills 把解法編碼進去：

- **先對齊再執行** — 盤問式訪談、QA 情境設計、結構化目標澄清
- **回饋迴圈** — 靜態檢查、驗證關卡、發布前審計
- **紀律大於儀式** — 小而可組合的 skill，拒絕反客為主的流程框架

## 內容

### ai-adoption — 企業 AI 導入

- `enterprise-ai-adoption` — 企業 AI 導入的組織採用戰役
- `deep-interview` — 結構化目標澄清：模糊需求 → 一次一問 → 三個維度全 clear
- `multi-agent-debate` — 多代理辯論：對抗式討論收斂到更好結論
- `qa-scenario-design` — 品質證據設計：implement 前先設計 QA scenarios

### engineering — 工程

- `cloudflare-deploy` — 一鍵 commit + deploy Cloudflare Workers/Pages/D1
- `mcp-worker-deploy` — 部署 MCP stateless servers 到 CF Workers
- `hono-workers-testing` — Hono/Workers backend 測試
- `static-html-biome-audit` — Biome lint for single HTML files

### content — 內容

- `stop-slop` — 去除 AI 寫作味
- `s2t-taiwan` — 簡體轉台灣繁體
- `gzh-design` — 微信公眾號文章排版引擎
- `vocus-article-writing-sop` — 方格子深度文章寫作風格固化

### seo-geo — 搜尋與 GEO

- `geolook-tw` — GeoLook GEO analysis for Taiwan market
- `static-site-geo` — SEO/GEO implementation patterns for static HTML sites
- `spa-geo-crawlability` — Fill SPA empty HTML via Edge Functions for AI crawlers
- `geo-content-reformatting` — Reformat H2/H3 into GEO-friendly QA headings

### automation — 自動化

- `gas-form-backend` — 靜態表單接 Google Apps Script 後端
- `line-messaging-api` — 表單資料自動送 LINE 官方帳號
- `turnstile-spin` — Cloudflare Turnstile end-to-end
- `cloudflare-email-service` — Transactional email with Cloudflare Email

## 範例請求

```text
幫我把這個靜態表單接上 LINE 通知 + Google Sheets 存檔
```

→ agent 載入 `gas-form-backend` + `line-messaging-api` 直接建後端，再用 `turnstile-spin` 加防垃圾。

## Repo 結構

```
skills/<category>/<skill-name>/SKILL.md   ← skills 本體
scripts/                                  ← sync + scan 工具
registry/skills.json                      ← 機器可讀清單
docs/                                     ← 貢獻指引
.out-of-scope/                            ← 為什麼有些 skill 不在這裡
```

## 需求

- 任何支援 skills 的 agent（Hermes、Claude Code、Codex…）
- 安裝器需要 `npx`

## 授權

MIT — 拿去改造，變成你自己的。
