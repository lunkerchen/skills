[![English](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)
[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-43-blue)](https://github.com/lunkerchen/skills/tree/main/skills)
[![AI Agent](https://img.shields.io/badge/AI-Agent%20Ready-brightgreen)](https://github.com/lunkerchen/skills)

# AI 導入實戰 Skills

> 一個 forward-deployed engineer（FDE）每天在用的 agent skills — 全部從真實客戶專案與生產工作流淬煉而來，不是 vibe coding。

## 這是什麼

我以 FDE 身分幫企業導入 AI。這個 repo 裡的每個 skill，原本都是我在客戶、或自己的生產系統上實際跑過的工作流 — 然後被濃縮成**小、可組合、任何 agent 都能安裝**的 skill。

這些 skills 相容任何模型、任何 agent（Hermes、Claude Code、Codex…），設計上就是拿來改造成你自己的。

## 為什麼有這些 skills

Agent 失敗大多來自三個原因，這些 skills 把解法直接編碼進去：

| 失敗模式 | 對應修復 | 代表 skills |
|---|---|---|
| **缺少上下文** — agent 不了解你的目標、限制、成功標準 | 先對齊再執行：結構化訪談、QA 情境設計 | `deep-interview`、`qa-scenario-design`、`fde-framework` |
| **缺少回饋迴圈** — 做完就交付，沒有驗證關卡 | 靜態檢查、驗證閘門、發布前審計 | `typescript-project-verify`、`static-html-polish`、`scan-automation`、`personal-red-team` |
| **流程反客為主** — 框架吃掉你的生產力 | 紀律大於儀式：小而可組合，拒絕流程框架 | 所有 skills 的共同設計原則 |

## 安裝

| 方法 | 指令 / 路徑 |
|---|---|
| **npx skills CLI**（推薦） | `npx skills add lunkerchen/skills` |
| **Hermes** | 複製 `skills/<category>/<name>/` 到 `~/.hermes/skills/`（或 symlink） |
| **Claude Code** | 複製到 `~/.claude/skills/` |
| **Codex** | 複製到 `~/.codex/skills/` |
| **手動** | 直接複製你需要的 skill 目錄到 agent 的 skills 路徑 |

**不需要全裝。** skill 之間零相依，挑你需要的分類複製即可。

### 下載單一 skill

分類清單裡的每個 skill 名稱都可點擊 — 直接連到 repo 內對應的 skill 目錄：

1. 點 skill 名稱（例：[`personal-red-team`](skills/automation/personal-red-team/SKILL.md)）
2. 下載 `SKILL.md`（如有 `references/` 目錄一併下載）
3. 放到你 agent 的 skills 路徑（見上方安裝表）

或 clone 整個 repo 只取需要的目錄：

```bash
git clone --depth 1 https://github.com/lunkerchen/skills.git
cp -r skills/automation/personal-red-team ~/.hermes/skills/
```

## 快速開始

1. **挑一個 skill** — 從下面的分類找你要的工作流
2. **安裝** — 用上表任一方法
3. **用平常的話描述需求** — agent 會自動載入對應 skill（例：說「幫我把這個表單接上 LINE 通知」，agent 就會載入 `line-messaging-api`）

## 內容一覽（43 個 skills）

### ai-adoption — 企業 AI 導入

企業 AI 導入的實戰打法 — 無阻力變革管理、FDE 交付框架。

- [enterprise-ai-adoption](skills/ai-adoption/enterprise-ai-adoption/SKILL.md) — 企業 AI 導入的組織採用戰役：證明價值、降低恐懼、讓同儕帶頭
- [fde-framework](skills/ai-adoption/fde-framework/SKILL.md) — FDE playbook：PSF、MVD、影子工作法、成果計價、轉職路線
- [deep-interview](skills/ai-adoption/deep-interview/SKILL.md) — 一次一問直到目標、限制、成功標準全 clear
- [qa-scenario-design](skills/ai-adoption/qa-scenario-design/SKILL.md) — implement 前先設計 QA scenarios 與 failure modes，附證據分級
- [subagent-efficiency](skills/ai-adoption/subagent-efficiency/SKILL.md) — 知道何時直接執行勝過 spawn subagent — 以及何時相反

### automation — 自動化

表單、通知、整合 — 幫你「跑生意」的自動化。

- [gas-form-backend](skills/automation/gas-form-backend/SKILL.md) — 免費 GAS 後端：靜態表單接 Sheets + Email + LINE push
- [lark-bot-development](skills/automation/lark-bot-development/SKILL.md) — 開發 Lark/飛書 BOT：應用生命週期、事件訂閱（WebSocket/webhook）、訊息、卡片、SDK
- [line-messaging-api](skills/automation/line-messaging-api/SKILL.md) — 表單資料自動送 LINE 官方帳號或客服群組（Messaging API push）
- [cloudflare-email-service](skills/automation/cloudflare-email-service/SKILL.md) — Cloudflare Email Service + Workers 發送與路由交易信
- [turnstile-spin](skills/automation/turnstile-spin/SKILL.md) — Cloudflare Turnstile 端到端防機器人：widget、siteverify、驗證、框架指南
- [coupang-partners-api](skills/automation/coupang-partners-api/SKILL.md) — 酷澎台灣分潤 API：HMAC 簽章、搜尋、deeplinks、報表
- [gmail-inbox-organizer](skills/automation/gmail-inbox-organizer/SKILL.md) — Gmail 自動分類：依寄件人/主旨標籤、封存促銷信
- [web-monitor](skills/automation/web-monitor/SKILL.md) — cron 網頁變更監控：指紋比對、無變化時靜默
- [scan-automation](skills/automation/scan-automation/SKILL.md) — 自動化系統相依掃描、解析 NDJSON、記錄趨勢、debug 卡住
- [personal-red-team](skills/automation/personal-red-team/SKILL.md) — 證據優先的全系統紅隊審計：cron、skills、專案盤點 → 安全修復 + 決策簡報
- [obsidian-cli](skills/automation/obsidian-cli/SKILL.md) — 用 CLI 驅動 Obsidian：筆記、任務、搜尋、plugin/theme 開發

### note-taking — 筆記

知識系統與筆記庫維護。

- [obsidian-vault-organizer](skills/note-taking/obsidian-vault-organizer/SKILL.md) — 安全盤點與重整 Obsidian vault：分類、連結、模板、批准閘門與驗證

### content — 內容

寫作與發布工作流，核心是反 AI 味（anti-slop）。

- [stop-slop](skills/content/stop-slop/SKILL.md) — 去除 AI 寫作味：砍掉模板化廢話與機器節奏
- [writing-humanizer](skills/content/writing-humanizer/SKILL.md) — 審計並改寫 AI 味文字，回到自然人聲
- [s2t-taiwan](skills/content/s2t-taiwan/SKILL.md) — 簡體轉台灣繁體，含正確術語表
- [html-article-author](skills/content/html-article-author/SKILL.md) — markdown 轉深色主題 HTML 文章（CJK 字型）
- [vocus-article-writing-sop](skills/content/vocus-article-writing-sop/SKILL.md) — AI 工具簡報改寫為方格子深度長文
- [markdown-to-podcast](skills/content/markdown-to-podcast/SKILL.md) — markdown 文章轉 podcast WAV（神經 TTS + 鋼琴 intro）
- [youtube-content](skills/content/youtube-content/SKILL.md) — YouTube 逐字稿轉摘要、Threads、部落格

### design — 設計

有辨識度的單檔 HTML 設計系統。

- [night-sky-design](skills/design/night-sky-design/SKILL.md) — 深色星空單檔 HTML 主題，品牌漸層點綴，簡報/網頁通用
- [rwd-mobile-rules](skills/design/rwd-mobile-rules/SKILL.md) — 每次產出 HTML 的強制行動版規則：viewport、grid、觸控目標、導覽
- [static-html-polish](skills/design/static-html-polish/SKILL.md) — audit→harden→verify 管線：靜態 HTML 補 RWD/SEO-GEO/a11y
- [popular-web-designs](skills/design/popular-web-designs/SKILL.md) — 54 套真實設計系統（Stripe、Linear、Vercel…）現成 CSS tokens

### engineering — 工程

雲端與基礎設施工作流，生產環境驗證過。

- [mcp-worker-deploy](skills/engineering/mcp-worker-deploy/SKILL.md) — 部署無狀態 MCP server 到 Cloudflare Workers，auth-first
- [hono-workers-testing](skills/engineering/hono-workers-testing/SKILL.md) — Hono/Workers 後端測試：vitest、D1 mocks、fake executionCtx
- [github-code-review](skills/engineering/github-code-review/SKILL.md) — 完整 code review 管線：push 前檢查、PR 評論、安全掃描
- [linter-configuration](skills/engineering/linter-configuration/SKILL.md) — 產出符合專案風格的 Biome/Prettier 設定，零 churn
- [static-html-biome-audit](skills/engineering/static-html-biome-audit/SKILL.md) — Biome lint 單檔 HTML；修 CSS、a11y、語意
- [typescript-project-verify](skills/engineering/typescript-project-verify/SKILL.md) — TypeScript 五道驗證閘門：tsc、vitest、build、format、smoke
- [npm-global-upgrade](skills/engineering/npm-global-upgrade/SKILL.md) — 安全升級全域 npm 套件：allow-scripts、symlinks、OSV 判讀
- [local-dev-server-startup](skills/engineering/local-dev-server-startup/SKILL.md) — 在 launchd/brew 管理的服務旁安全啟動 dev server；修 port 衝突

### seo-geo — SEO + GEO

搜尋引擎 + 生成式引擎優化（AI 搜尋可見度）。

- [modern-seo-strategy](skills/seo-geo/modern-seo-strategy/SKILL.md) — SEO+GEO 整合策略：語意地圖、EEAT、AI 引用優化、五階段計畫
- [static-site-geo](skills/seo-geo/static-site-geo/SKILL.md) — 靜態網站 GEO/SEO 模式：JSON-LD、sitemap、OG 圖、llms.txt、建置驗證
- [spa-geo-crawlability](skills/seo-geo/spa-geo-crawlability/SKILL.md) — 用 Edge Functions 預渲染 SPA 空殼，讓 AI 爬蟲看得到內容
- [geo-content-reformatting](skills/seo-geo/geo-content-reformatting/SKILL.md) — 把 H2/H3 改寫成問句形式提升 AI 搜尋可見度，零設計變更
- [geo-article-friendly](skills/seo-geo/geo-article-friendly/SKILL.md) — 既有文章改造為 AI 搜尋友好：證據強化、結構重構、語意優化，保留作者語氣
- [site-seo-geo-audit](skills/seo-geo/site-seo-geo-audit/SKILL.md) — 全站 SEO+GEO 審計工作流：偵察、Schema 診斷、內容缺口、優先序矩陣
- [webapp-geo-optimization](skills/seo-geo/webapp-geo-optimization/SKILL.md) — Web App 隱形 GEO 優化：結構化資料、JSON-LD、sitemap、OG 圖

## 實際用法（組合範例）

```text
「幫我把這個靜態表單接上 LINE 通知 + Google Sheets 存檔」
```

→ agent 載入 `gas-form-backend` + `line-messaging-api` 建後端，再用 `turnstile-spin` 加防機器人。

```text
「我的網站 AI 搜尋（ChatGPT/Gemini）都找不到內容」
```

→ 先跑 `site-seo-geo-audit` 找出缺口，再用 `static-site-geo`（靜態站）或 `spa-geo-crawlability`（SPA）落地。

```text
「我感覺整個系統哪裡在漏，幫我全面檢查一遍」
```

→ `personal-red-team` 會做證據優先的全系統盤點（cron / skills / 專案），安全修復 + 決策簡報。

```text
「把這篇文章的 AI 味去掉」
```

→ `stop-slop` 砍模板化廢話，`writing-humanizer` 收尾到自然人聲。

## Repository 結構

```
skills/<category>/<skill-name>/SKILL.md   ← 技能本體（+ 選擇性 references/）
scripts/                                  ← sync + scan + sanitize 工具
docs/CONTRIBUTING.md                      ← 貢獻指南
.out-of-scope/                            ← 為什麼某些 skills 不在這裡（信任聲明）
```

**為什麼有些 skills 不在這裡？** 見 `.out-of-scope/` — 每個排除決定都有紀錄：客戶專案資料、商業工具、個人研究收藏、過時技能。公開 repo 只收「通用化之後仍有價值」的工作流；涉及客戶名、真實路徑、金鑰的內容一律 sanitize 或排除。

## 貢獻

想分享自己的工作流？見 [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)。發布前會通過秘密掃描與 sanitize 關卡 — 公開 repo 不留客戶資料。

## License

MIT — hack around with them, make them your own.
