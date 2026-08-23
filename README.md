[![English](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)
[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-39-blue)](https://github.com/lunkerchen/skills/tree/main/skills)
[![AI Agent](https://img.shields.io/badge/AI-Agent%20Ready-brightgreen)](https://github.com/lunkerchen/skills)

# AI 導入實戰 Skills

> 一個 Forward-Deployed Engineer（FDE）每天在用的 Agent Skills 集合 — 全部從真實企業專案、生產環境與高併發工作流淬煉而來，不是概念玩具或 Prompt 堆砌。

## 這是什麼

我以 FDE 身分協助企業與自營品牌完成 AI 落地。這個 Repository 裡的每個 Skill，原本都是在客戶生產系統或自動化架構上實際運行的 SOP 與驗證腳本 — 經過高強度提煉，封裝成**小而獨立、零外部相依、任何 Agent 都能即插即用**的標準技能。

這些 Skills 相容於主流模型與 CLI Agent（Hermes、Claude Code、Codex、Cursor 等），採用開放規格設計，開箱即用且極易依據具體業務擴充。

## 為什麼需要這些 Skills

AI Agent 執行任務失敗通常歸咎於三大根本原因，這些 Skills 將最佳實踐直接編碼為防錯契約：

| 失敗模式 | 根本成因 | 技能解法與機制 | 代表 Skills |
|---|---|---|---|
| **上下文語意模糊** | Agent 不清楚真實業務邊界、隱性約束與驗收標準 | 先對齊再執行：結構化提問、QA 測試情境設計、FDE 交付閉環 | `deep-interview`、`qa-scenario-design`、`fde-framework` |
| **缺少驗證反饋迴圈** | 做完就草率交付，缺乏客觀的品質門戶（Quality Gates） | 發布前自動化斷言、多層次靜態審計、主動紅隊探測 | `typescript-project-verify`、`static-html-polish`、`personal-red-team` |
| **過度工程與流程浪費** | 繁瑣框架吞噬生產力，死碼與假訊號叢生 | 奧卡姆剃刀原則：小而自洽、代碼最簡化、真實證據優先 | 所有 Skills 的核心設計哲學 |

---

## 🌟 旗艦亮點：`seo-geo-suite` (SEO × GEO × AEO × Agent-Readiness)

在 2026 年，網站的可見度不再只是 Google 傳統藍色連結的 SEO 排名。我們將過去 12 個獨立子技能整合成全能旗艦包 **[`seo-geo-suite`](skills/seo-geo/seo-geo-suite/SKILL.md)**，構建了完整的**現代搜尋與 Agentic 四軌體系**：

1. **SEO（搜尋引擎優化）**：Google/Bing 關鍵字、主題地圖（Topic Clusters）、CWV 與反向連結。
2. **GEO（生成式引擎優化）**：ChatGPT、Claude、DeepSeek、Gemini 的品牌共識（SOV）與抗摘要深度內容。
3. **AEO（答案引擎優化）**：Perplexity、Google AIO 的直接答案卡抽取、倒金字塔 40–60 字結論置頂。
4. **Agent-Readiness（代理就緒）**：全面遵循 **Is-Agentic 100 分標準** 與 **Cloudflare Level 0–5 協定**（No-JS SSR、Markdown 內容協商、`Vary: Accept`、標準 `llms.txt`、Agent-Friendly 404 導航、RFC 9457 結構化錯誤與 MCP Server Card）。

---

## 安裝與使用

| 環境 / 工具 | 安裝指令 / 操作方式 |
|---|---|
| **npx skills CLI**（推薦） | `npx skills add lunkerchen/skills` |
| **Hermes Agent** | 複製或 Symlink 目錄至 `~/.hermes/skills/` |
| **Claude Code** | 複製至 `~/.claude/skills/` |
| **OpenAI Codex** | 複製至 `~/.codex/skills/` |
| **通用 / 手動安裝** | 直接將特定 Skill 目錄複製到您 Agent 的工作空間中 |

> **提示**：每個 Skill 均為完全自洽的獨立單元，無需安裝全部。依據業務需求挑選對應目錄即可。

### 下載單一 Skill

本清單中所有 Skill 名稱均附帶連結，可直接點擊查看原始碼與參考手冊：

```bash
# 範例：僅下載旗艦 seo-geo-suite
git clone --depth 1 https://github.com/lunkerchen/skills.git
cp -r skills/seo-geo/seo-geo-suite ~/.hermes/skills/
```

---

## 內容一覽（39 個精選實戰 Skills）

### seo-geo — 搜尋、生成式引擎與 Agent 就緒

涵蓋傳統搜尋、大模型引用、直接問答抽取與 Agentic API 規範的旗艦工作台。

| Skill | 說明 |
|---|---|
| [seo-geo-suite](skills/seo-geo/seo-geo-suite/SKILL.md) | **SEO × GEO × AEO × Agent-Readiness 全能旗艦工作台**：整合三軌搜尋、Is-Agentic 100分規範、Cloudflare L0–L5、全站審計、AEO 內容重構與 6 道建置驗證門戶 |

### ai-adoption — 企業 AI 導入與組織賦能

從商業諮詢、現場交付到團隊無阻力變革管理的實戰打法。

| Skill | 說明 |
|---|---|
| [enterprise-ai-adoption](skills/ai-adoption/enterprise-ai-adoption/SKILL.md) | 企業 AI 導入戰役：證明業務價值、降低員工恐懼、建立同儕示範槓桿 |
| [fde-framework](skills/ai-adoption/fde-framework/SKILL.md) | 前置部署工程師（FDE）實戰手冊：PSF 框架、MVD 交付、影子工作法、成果計價 |
| [deep-interview](skills/ai-adoption/deep-interview/SKILL.md) | 結構化深度訪談：一次一問直到目標、約束與驗收標準 100% 釐清 |
| [qa-scenario-design](skills/ai-adoption/qa-scenario-design/SKILL.md) | 品質證據設計：開發前先設計 QA Scenarios、極限邊界條件與失敗防護 |
| [subagent-efficiency](skills/ai-adoption/subagent-efficiency/SKILL.md) | 子代理調度決策矩陣：識別平行加速任務，避免過度派工浪費 Token |

### automation — 流程與系統自動化

串接通訊軟體、雲端服務與本機環境的高效自動化管線。

| Skill | 說明 |
|---|---|
| [lark-bot-development](skills/automation/lark-bot-development/SKILL.md) | 飛書 / Lark 機器人開發：事件訂閱、卡片互動、多維表格（Bitable）雙向串接 |
| [line-messaging-api](skills/automation/line-messaging-api/SKILL.md) | LINE 官方帳號推播：表單/訂單即時通知、客服群組告警閉環 |
| [cloudflare-email-service](skills/automation/cloudflare-email-service/SKILL.md) | Cloudflare Email Routing + Worker 交易郵件收發系統 |
| [turnstile-spin](skills/automation/turnstile-spin/SKILL.md) | Cloudflare Turnstile 無感驗證碼端到端整合與保護管線 |
| [gmail-inbox-organizer](skills/automation/gmail-inbox-organizer/SKILL.md) | AI 驅動之 Gmail 信箱自動分類、標籤分流與智慧摘要 |
| [obsidian-cli](skills/automation/obsidian-cli/SKILL.md) | Obsidian 終端控制：筆記讀寫、搜尋、語意連結建立與知識沉澱 |
| [gas-form-backend](skills/automation/gas-form-backend/SKILL.md) | 靜態表單之 Google Apps Script 無伺服器後端與 Google Sheets 串接 |
| [web-monitor](skills/automation/web-monitor/SKILL.md) | 輕量網頁內容異動監控：基於雜湊比對之靜默告警與 Watchdog |
| [scan-automation](skills/automation/scan-automation/SKILL.md) | 自動化系統與依賴掃描：結構化解析並輸出修復建議 |
| [coupang-partners-api](skills/automation/coupang-partners-api/SKILL.md) | 酷澎台灣分潤（Coupang Partners API）HMAC 簽章與自動化推薦系統 |
| [personal-red-team](skills/automation/personal-red-team/SKILL.md) | 個人與團隊紅隊審計：全系統盤點、排程檢查、隱藏風險與資安修復 |

### content — 內容工程與多媒體產出

高質量文字潤色、音訊生成與影音逐字稿解析管線。

| Skill | 說明 |
|---|---|
| [stop-slop](skills/content/stop-slop/SKILL.md) | 去除 AI 寫作機械味：剔除模板化廢話、套路句式，還原自然人聲 |
| [writing-humanizer](skills/content/writing-humanizer/SKILL.md) | 人性化改寫：保留事實與專業深度，提升文字流暢度與親和力 |
| [s2t-taiwan](skills/content/s2t-taiwan/SKILL.md) | 簡轉繁台灣在地化：依據台灣資訊與商業用語習慣精確轉換 |
| [html-article-author](skills/content/html-article-author/SKILL.md) | 單檔高質感 HTML 文章發布：整合排版美學、RWD 與 SEO 元件 |
| [vocus-article-writing-sop](skills/content/vocus-article-writing-sop/SKILL.md) | 方格子深度專題寫作手冊：科技記者視角、摘要提煉與結構化長文 |
| [markdown-to-podcast](skills/content/markdown-to-podcast/SKILL.md) | Markdown 轉 Podcast 音訊：Edge Neural TTS + 多角色語音合成 |
| [youtube-content](skills/content/youtube-content/SKILL.md) | YouTube 影音逐字稿提取、章節拆解與跨平台內容再製 |
| [ig-video-breakdown](skills/content/ig-video-breakdown/SKILL.md) | Instagram Reels / 短影音逐字稿提取與爆款分鏡腳本拆解 |

### design — 介面與視覺設計

深色美學、行動裝置 RWD 規範與無障礙網頁打磨。

| Skill | 說明 |
|---|---|
| [night-sky-design](skills/design/night-sky-design/SKILL.md) | 夜空風格單檔 HTML：深色星空、玻璃擬物（Glassmorphism）與品牌漸層 |
| [rwd-mobile-rules](skills/design/rwd-mobile-rules/SKILL.md) | RWD 行動版強制規範：觸控 44px 靶區、Viewport 防溢出、零佈局偏移 |
| [static-html-polish](skills/design/static-html-polish/SKILL.md) | 靜態 HTML 全方位翻新：補齊 RWD、語意標籤、a11y 與現代 CSS |
| [popular-web-designs](skills/design/popular-web-designs/SKILL.md) | 現代科技品牌風格手冊：Stripe / Linear / Vercel 極簡美學實作 |

### engineering — 軟體工程與品質驗證

開發環境維護、TypeScript 驗證與嚴格程式碼審查。

| Skill | 說明 |
|---|---|
| [typescript-project-verify](skills/engineering/typescript-project-verify/SKILL.md) | 5 道 TypeScript 建置驗證門戶：型別檢查、依賴合規與執行期防錯 |
| [github-code-review](skills/engineering/github-code-review/SKILL.md) | 嚴格代碼審查：安全性掃描、品質門戶、架構反思與可操作改善建議 |
| [linter-configuration](skills/engineering/linter-configuration/SKILL.md) | Linter 設定自動生成：Biome / Prettier / ESLint 配置一鍵落地 |
| [static-html-biome-audit](skills/engineering/static-html-biome-audit/SKILL.md) | 針對單檔 HTML 執行 Biome 語法、CSS 與 a11y 深度靜態檢查 |
| [npm-global-upgrade](skills/engineering/npm-global-upgrade/SKILL.md) | 全域 npm 套件安全升級：處理符號連結、allow-scripts 與依賴衝突 |
| [local-dev-server-startup](skills/engineering/local-dev-server-startup/SKILL.md) | 本機開發伺服器管理：處理 macOS 系統服務與 Port 佔用共存 |
| [hono-workers-testing](skills/engineering/hono-workers-testing/SKILL.md) | Hono on Cloudflare Workers 測試套件：Vitest、D1 Mock 與環境模擬 |
| [mcp-worker-deploy](skills/engineering/mcp-worker-deploy/SKILL.md) | 無狀態 MCP 伺服器部署至 Cloudflare Workers（2026 最新標準） |

### security — 資訊安全

| Skill | 說明 |
|---|---|
| [website-security-owasp-cve](skills/security/website-security-owasp-cve/SKILL.md) | 網站安全掃描：OWASP Top 10 防護檢驗、CVE 依賴漏洞審計與防禦 |

### note-taking — 第二大腦與知識庫

| Skill | 說明 |
|---|---|
| [obsidian-vault-organizer](skills/note-taking/obsidian-vault-organizer/SKILL.md) | Obsidian 知識庫整理：PARA 架構、雙向連結修復與索引建立 |

---

## 授權條款

本專案採用 [MIT License](LICENSE) 授權開源。
