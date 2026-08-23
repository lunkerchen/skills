---
name: code-quality-suite
description: 代碼品質、審查與驗證門戶旗艦：嚴格 GitHub Code Review、5 道 TypeScript 建置驗證（typescript-project-verify）、自動化 Linter 配置（linter-configuration）、單檔 HTML Biome 審計、全域 npm 安全升級與開發伺服器管理。
version: 1.0.0
author: Community
license: MIT
read_when:
  - User asks for a code review, pre-landing PR review, or security audit on code changes
  - User needs post-build / post-deploy TypeScript 5-gate verification
  - User wants to configure linters (Biome, Prettier, ESLint) matching project style
  - User wants to audit single-file HTML with Biome or troubleshoot local dev servers
metadata:
  hermes:
    tags: [engineering, code-review, typescript, verification, linter, biome, quality, suite]
---

# 代碼品質與驗證門戶旗艦（Code Quality Suite）

從開發時規範（Linter）、本機執行期環境、到發布前 5 道品質門戶與嚴格代碼審查的全流程工程旗艦。

---

## 旗艦模組一覽

### 模組 1：嚴格代碼審查（GitHub Code Review）
- **審查 4 大維度**：
  1. 正確性（Correctness & Logic）：邊界條件、非同步競爭、型別安全。
  2. 安全性（Security）：SQL Injection、XSS、未授權端點、金鑰洩漏。
  3. 效能與可維護性（Performance & Simplicity）：避免過度工程（Ponytail 原則）。
  4. 測試覆蓋（Test Evidence）：真實測試執行結果而非口頭宣稱。

### 模組 2：TypeScript 5 道驗證門戶（TypeScript 5-Gate Verification）
- **Gate 1**：Type-check 零錯誤（`tsc --noEmit`）。
- **Gate 2**：靜態 Linter 零告警（Biome / ESLint）。
- **Gate 3**：單元與整合測試全數通過（Vitest / Jest）。
- **Gate 4**：生產環境 Build 成功（Next.js / Astro / Vite）。
- **Gate 5**：產出產物驗證（Dist assets & bundle size check）。

### 模組 3：Linter 自動化配置（Linter Configuration）
- 依據專案框架自動輸出標準 `biome.json`、`eslint.config.mjs` 或 `.prettierrc`，統一程式碼排版規範。

### 模組 4：單檔 HTML Biome 審計（Single HTML Audit）
- 針對單一 HTML 檔案進行 CSS 效能、HTML 語意與無障礙（a11y）之深度靜態掃描與自動修復。
