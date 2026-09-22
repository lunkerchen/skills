---
name: skills
description: 技能庫兩階段路由器——任務涉及 SEO/GEO/AEO、企業 AI 導入、內容寫作、多媒體轉製、前端/建築設計、代碼品質、Cloudflare Workers、通訊機器人、系統監控、Lark Wiki 同步或 Labangram 查詢時，先讀本檔「路由表」定位 skills/<category>/<name>/SKILL.md，載入該旗艦 Suite 後再依其索引按需取 references/ 明細。
---

# Production AI Agent Suites — 技能庫路由器

本 repo 鏡像 10 大旗艦 Suite 與 2 個獨立技能（另見 [README.md](README.md)）。單一 SKILL.md 不含全部細節；兩階段載入：**1)** 依下表選技能、讀其路徑；**2)** 該技能的 SKILL.md 內有 `references/` 索引，再按需取明細。不要憑記憶改寫技能內容，一律以讀檔為準。

## 路由表

| 技能路徑 | 領域 | 一句話 |
|---|---|---|
| `skills/seo-geo/seo-geo-suite/SKILL.md` | SEO/GEO/AEO | 四軌搜尋全能工作台：全站審計、內容改造、llms.txt、Is-Agentic、6 道驗證門戶 |
| `skills/ai-adoption/fde-adoption-suite/SKILL.md` | 企業 AI 導入 | 深度訪談、QA 證據設計、子代理調度決策、PSF/MVD 交付與變革管理 |
| `skills/content/content-writing-suite/SKILL.md` | 文字內容 | stop-slop 去 AI 味、人性化潤色、簡轉繁、方格子 SOP、單檔 HTML 長文 |
| `skills/content/multimedia-repurpose-suite/SKILL.md` | 多媒體轉製 | YouTube 逐字稿章節拆解、IG Reels 爆款分鏡、Markdown 轉 Podcast |
| `skills/design/frontend-design-suite/SKILL.md` | 前端設計 | 夜空深色美學、科技品牌極簡、44px 靶區、零橫向溢出、防 CLS |
| `skills/design/blueprint-concrete-design/SKILL.md` | 建築設計 | 藍圖網格與清水模色階、雙字型幾何張力、GSAP 視差；含 DESIGN.md 規範 |
| `skills/engineering/code-quality-suite/SKILL.md` | 代碼品質 | GitHub Code Review、5 道 TypeScript 建置驗證、Biome/Prettier 配置 |
| `skills/engineering/cloud-workers-suite/SKILL.md` | Workers/MCP | Hono on Workers 測試套件（Vitest、D1 Mock）與無狀態 MCP 伺服器建置 |
| `skills/automation/messaging-bots-suite/SKILL.md` | 企業通訊 | Lark/Bitable 串接、LINE 推播、CF 交易郵件、GAS 表單後端、酷澎分潤 |
| `skills/automation/system-watchdog-suite/SKILL.md` | 監控/紅隊 | 紅隊審計、依賴掃描、網頁變更監控、OWASP/CVE 防禦、Gmail 分流 |
| `skills/automation/sync-lark-wiki/SKILL.md` | 獨立技能 | 本機 Markdown 安全同步到既有 Lark Wiki：分階段 OAuth、preview、read-back |
| `skills/plugin/labangram-agent/SKILL.md` | 獨立技能 | 經公開 MCP/REST 查詢作品集、服務與定價；詢價草稿需人工確認才對外 |

## 使用規則

- 一次只載入最對口的單一技能；跨領域任務先讀最核心的一個，再依其內部索引橫向擴展。
- 明細、範本與實戰手冊都在各技能的 `references/` 目錄；本路由層不複製其內容。
- 本檔是 repo 原生路由器（非鏡像技能）；鏡像與同步規則見 [AGENTS.md](AGENTS.md)，技能 canonical 來源是 `~/.hermes/skills/`。
- 新增或移除技能時，同步更新本路由表與 `scripts/allowlist.tsv`。
