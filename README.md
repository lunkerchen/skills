[![English](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)
[![繁體中文](https://img.shields.io/badge/lang-zh--tw-blue.svg)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-9%20Flagships-blue)](https://github.com/lunkerchen/skills/tree/main/skills)
[![AI Agent](https://img.shields.io/badge/AI-Agent%20Ready-brightgreen)](https://github.com/lunkerchen/skills)

# AI 導入實戰旗艦技能庫（Production AI Agent Suites）

> 一個 Forward-Deployed Engineer（FDE）每天在用的 Agent 旗艦技能集合 — 全部從真實企業專案、生產環境與高併發工作流淬煉而來，拒絕概念玩具與零碎的 Prompt 堆砌。

## 這是什麼

我以 FDE 身分協助企業與自營品牌完成 AI 落地。這個 Repository 將過去 39+ 個細碎技能深度濃縮為 **9 大旗艦級全能工作台（Flagship Mega-Suites）**。每個工作台皆為**自洽獨立、零外部相依、包含完整規格與實戰手冊**的標準技能。

這些 Skills 相容於主流模型與 CLI Agent（Hermes、Claude Code、Codex、Cursor 等），採用開放規格設計，開箱即用且極易依據具體業務擴充。

## 為什麼需要旗艦化整合

過去零散的小技能容易造成 Agent 路由器（Router）判斷猶豫、選錯工具或重複載入消耗 Token。濃縮為旗艦工作台後帶來三大優勢：

| 核心價值 | 機制與特色 |
|---|---|
| **單一入口閉環** | 每個業務領域只需調用 1 個旗艦技能，內部自動串接多模組流水線（Pipeline） |
| **Context 深度優化** | 避免同時載入多個相似工具，大幅節省上下文視窗（Context Window）與 Token 消耗 |
| **企業級驗證防錯** | 全面內建 2026 最新標準（Is-Agentic 100 分規範、Cloudflare L0–L5、RFC 9110 / RFC 9457 / RFC 9727、TypeScript 5 道品質門戶） |

---

## 安裝與使用

| 環境 / 工具 | 安裝指令 / 操作方式 |
|---|---|
| **npx skills CLI**（推薦） | `npx skills add lunkerchen/skills` |
| **Hermes Agent** | 複製或 Symlink 目錄至 `~/.hermes/skills/` |
| **Claude Code** | 複製至 `~/.claude/skills/` |
| **OpenAI Codex** | 複製至 `~/.codex/skills/` |
| **通用 / 手動安裝** | 直接將特定 Suite 目錄複製到您 Agent 的工作空間中 |

```bash
# 範例：下載全套 9 大旗艦技能
git clone --depth 1 https://github.com/lunkerchen/skills.git
cp -r skills/* ~/.hermes/skills/
```

---

## 9 大旗艦工作台一覽

### 1. 搜尋與代理就緒（SEO & Agent Readiness）

| Flagship Suite | 涵蓋模組與能力 |
|---|---|
| [seo-geo-suite](skills/seo-geo/seo-geo-suite/SKILL.md) | **SEO × GEO × AEO × Agent-Readiness 全能旗艦工作台**：整合四軌搜尋體系、Is-Agentic 100分規範、Cloudflare L0–L5、全站 Reconnaissance 審計、AEO 40-60字答案抽取、Markdown Twin 內容協商與 6 道建置驗證門戶 |

### 2. 企業 AI 導入與組織賦能（Enterprise AI Adoption）

| Flagship Suite | 涵蓋模組與能力 |
|---|---|
| [fde-adoption-suite](skills/ai-adoption/fde-adoption-suite/SKILL.md) | **FDE 企業 AI 落地全能旗艦**：結構化深度訪談（deep-interview 1Q-at-a-time）、QA 品質證據設計、子代理調度決策矩陣（subagent-efficiency）、PSF/MVD 交付框架與組織無阻力變革管理 |

### 3. 內容工程與多媒體轉製（Content & Multimedia）

| Flagship Suite | 涵蓋模組與能力 |
|---|---|
| [content-writing-suite](skills/content/content-writing-suite/SKILL.md) | **文字內容工程與長文發布旗艦**：去除 AI 寫作機械味（stop-slop）、人性化潤色（writing-humanizer）、簡轉繁台灣在地化（s2t-taiwan）、方格子科技長文 SOP 與單檔高質感 HTML 文章排版 |
| [multimedia-repurpose-suite](skills/content/multimedia-repurpose-suite/SKILL.md) | **影音與多媒體內容轉製旗艦**：YouTube 逐字稿提取與章節拆解（youtube-content）、IG Reels 短影音爆款分鏡腳本拆解（ig-video-breakdown）、Markdown 轉 Podcast 多角色音訊合成（Edge Neural TTS） |

### 4. 前端介面與視覺設計（Frontend & Visual Design）

| Flagship Suite | 涵蓋模組與能力 |
|---|---|
| [frontend-design-suite](skills/design/frontend-design-suite/SKILL.md) | **前端設計與 RWD 打磨旗艦**：夜空深色星空美學（night-sky-design）、科技品牌極簡風格（Stripe/Linear/Vercel 美學）、行動端 RWD 強制防錯規範（44px 靶區、零橫向溢出、防 CLS）與靜態 HTML 現代化翻新 |
| [blueprint-concrete-design](skills/design/blueprint-concrete-design/SKILL.md) | **建築藍圖與清水模設計系統**：源自向登群建築師事務所官方重構。深邃玄黑與清水模色階、40px 建築藍圖網格背景、雙字型幾何張力（Plus Jakarta Sans × Space Mono）、科技青藍（Sky-400）重點色與 GSAP 3 視差進場動畫。含完整 Google DESIGN.md 規範檔與 W3C DTCG / Tailwind 匯出樣板 |

### 5. 軟體工程與無伺服器部署（Software Engineering & Cloud）

| Flagship Suite | 涵蓋模組與能力 |
|---|---|
| [code-quality-suite](skills/engineering/code-quality-suite/SKILL.md) | **代碼品質、審查與驗證門戶旗艦**：嚴格 GitHub Code Review、5 道 TypeScript 建置驗證（typescript-project-verify）、自動化 Linter 配置（Biome/Prettier）、單檔 HTML Biome 審計與全域 npm 安全維護 |
| [cloud-workers-suite](skills/engineering/cloud-workers-suite/SKILL.md) | **Cloudflare Workers 與 MCP 服務旗艦**：Hono on Workers 完整測試套件（Vitest、D1 Mock、executionContext）與 2026 最新無狀態 MCP（Model Context Protocol）伺服器建置部署 |

### 6. 系統自動化、通訊與後勤（Automation & Operations）

| Flagship Suite | 涵蓋模組與能力 |
|---|---|
| [messaging-bots-suite](skills/automation/messaging-bots-suite/SKILL.md) | **企業通訊與自動化通知旗艦**：飛書 / Lark 機器人開發與多維表格（Bitable）雙向串接、LINE 官方帳號推播、Cloudflare 交易郵件服務、Google Apps Script 表單無伺服器後端與酷澎分潤自動化 |
| [system-watchdog-suite](skills/automation/system-watchdog-suite/SKILL.md) | **系統監控、資安紅隊與知識庫運維旗艦**：個人與團隊紅隊審計（personal-red-team）、全系統依賴掃描（scan-automation）、輕量網頁內容監控（web-monitor）、OWASP & CVE 漏洞防禦、Cloudflare Turnstile 無感驗證、Gmail 智慧分流與 Obsidian 知識庫維護 |

---

## 授權條款

本專案採用 [MIT License](LICENSE) 授權開源。
