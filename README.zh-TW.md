[![English](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.zh-TW.md)

# AI 導入實戰 Skills

我每天在用的 Agent skills — 作為 forward-deployed engineer（FDE），全部從真實客戶專案與生產環境淬煉而來，不是 vibe coding。

我以 forward-deployed engineer（FDE）身分幫企業導入 AI。這個 repo 裡的每個 skill，原本都是我在客戶、或自己的生產系統上跑過的工作流 — 然後被濃縮成小、可組合、任何 agent 都能安裝的 skill。

這些 skills 相容任何模型、任何 agent，設計上就是拿來改造成你自己的。

## 安裝

```bash
npx skills add lunkerchen/skills
```

選擇你要的 skills，以及要安裝到哪些 agent。

## 為什麼有這些 skills

Agent 失敗大多來自：缺少上下文、缺少回饋迴圈、流程反過來控制你。這些 skills 把解法編碼進去：

- **先對齊再執行** — 結構化訪談、QA 情境設計、領域模型
- **回饋迴圈** — 靜態檢查、驗證關卡、發布前審計
- **紀律大於儀式** — 小而可組合的 skill，拒絕反客為主的流程框架

## 內容

### ai-adoption — 企業 AI 導入

- `enterprise-ai-adoption` — 企業 AI 導入的組織採用戰役：證明價值、降低恐懼、讓同儕帶頭
- `fde-framework` — FDE playbook：PSF、MVD、影子工作法、成果計價、轉職路線
- `deep-interview` — 一次一問直到目標、限制、成功標準全 clear
- `qa-scenario-design` — implement 前先設計 QA scenarios 與 failure modes，附證據分級
- `subagent-efficiency` — 知道何時直接執行勝過 spawn subagent — 以及何時相反

### automation — 自動化

- `gas-form-backend` — 免費 GAS 後端：靜態表單接 Sheets + Email + LINE push
- `lark-bot-development` — 開發 Lark/飛書 BOT：應用生命週期、事件訂閱（WebSocket/webhook）、訊息、卡片、SDK
- `line-messaging-api` — 表單資料自動送 LINE 官方帳號或客服群組（Messaging API push）
- `cloudflare-email-service` — Cloudflare Email Service + Workers 發送與路由交易信
- `turnstile-spin` — Cloudflare Turnstile 端到端防機器人：widget、siteverify、驗證、框架指南
- `coupang-partners-api` — 酷澎台灣分潤 API：HMAC 簽章、搜尋、deeplinks、報表
- `gmail-inbox-organizer` — Gmail 自動分類：依寄件人/主旨標籤、封存促銷信
- `web-monitor` — cron 網頁變更監控：指紋比對、無變化時靜默
- `scan-automation` — 自動化系統相依掃描、解析 NDJSON、記錄趨勢、debug 卡住
- `obsidian-cli` — 用 CLI 驅動 Obsidian：筆記、任務、搜尋、plugin/theme 開發

### content — 內容

- `stop-slop` — 去除 AI 寫作味：砍掉模板化廢話與機器節奏
- `writing-humanizer` — 審計並改寫 AI 味文字，回到自然人聲
- `s2t-taiwan` — 簡體轉台灣繁體，含正確術語表
- `html-article-author` — markdown 轉深色主題 HTML 文章（CJK 字型）
- `vocus-article-writing-sop` — AI 工具簡報改寫為方格子深度長文
- `markdown-to-podcast` — markdown 文章轉 podcast WAV（神經 TTS + 鋼琴 intro）
- `youtube-content` — YouTube 逐字稿轉摘要、Threads、部落格

### design — 設計

- `night-sky-design` — 深色星空單檔 HTML 主題，品牌漸層點綴，簡報/網頁通用
- `rwd-mobile-rules` — 每次產出 HTML 的強制行動版規則：viewport、grid、觸控目標、導覽
- `static-html-polish` — audit→harden→verify 管線：靜態 HTML 補 RWD/SEO-GEO/a11y
- `popular-web-designs` — 54 套真實設計系統（Stripe、Linear、Vercel…）現成 CSS tokens

### engineering — 工程

- `mcp-worker-deploy` — 部署 MCP 2026-07-28 stateless servers 到 CF Workers，auth-first
- `hono-workers-testing` — 測試 Hono/Workers backend：vitest、D1 mock、fake executionCtx
- `github-code-review` — 完整 code review 管線：push 前審查、PR 行內評論、安全掃描
- `linter-configuration` — 依專案既有風格輸出 Biome/Prettier 設定，零噪音
- `static-html-biome-audit` — Biome lint 單檔 HTML：修 CSS、a11y、語意
- `typescript-project-verify` — TypeScript monorepo 五道驗證關卡：tsc、vitest、build、format、smoke
- `npm-global-upgrade` — 安全升級全域 npm 套件：allow-scripts、symlinks、OSV 判讀
- `local-dev-server-startup` — 在 launchd/brew 管理的服務旁安全啟動 dev server；解 port 衝突

### seo-geo — 搜尋與 GEO

- `modern-seo-strategy` — SEO+GEO 整合策略：語意地圖、EEAT、AI 引用優化、五階段計畫
- `static-site-geo` — 靜態站 GEO/SEO 模式：JSON-LD、sitemap、OG 圖、llms.txt、建置驗證
- `spa-geo-crawlability` — Edge Functions 預渲染 SPA 空殼，讓 AI crawler 看得到文字
- `geo-content-reformatting` — H2/H3 改寫為問句形式，提升 AI 搜尋可見度，零設計變更
- `geo-article-friendly` — 現有文章改造為 GEO 友好：證據、結構、語意 — 保留作者語氣
- `site-seo-geo-audit` — 全站 SEO+GEO 審計：偵察、Schema 診斷、內容缺口、優先矩陣
- `webapp-geo-optimization` — Web App 隱形 GEO 優化：structured data、JSON-LD、sitemap、OG 圖

## 範例請求

```text
幫我把這個靜態表單接上 LINE 通知 + Google Sheets 存檔
```

→ agent 載入 `gas-form-backend` + `line-messaging-api` 直接建後端，再用 `turnstile-spin` 加防垃圾。

## Repo 結構

```
skills/<category>/<skill-name>/SKILL.md   ← skills 本體
scripts/                                  ← sync + scan + sanitize 工具
docs/                                     ← 貢獻指引
.out-of-scope/                            ← 為什麼有些 skill 不在這裡
```

## 需求

- 任何支援 skills 的 agent（Hermes、Claude Code、Codex…）
- 安裝器需要 `npx`

## 授權

MIT — 拿去改造，變成你自己的。
