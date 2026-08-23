---
name: system-watchdog-suite
description: 系統監控、資安紅隊與知識庫運維旗艦：個人與團隊紅隊審計（personal-red-team）、全系統依賴掃描（scan-automation）、輕量網頁內容監控（web-monitor）、OWASP & CVE 漏洞防禦（website-security-owasp-cve）、Cloudflare Turnstile 整合（turnstile-spin）、Gmail 自動化分流與 Obsidian 第二大腦知識庫維護。
version: 1.0.0
author: Community
license: MIT
read_when:
  - User asks for a personal/team red team audit, system inventory, cron checks, or hidden risk discovery
  - User wants to scan dependencies, vulnerabilities (OWASP, CVE), or automate health checks
  - User wants to monitor web page content changes with hash-based watchdogs
  - User wants to set up Cloudflare Turnstile anti-bot protection
  - User wants to organize Gmail inbox with AI triage or organize Obsidian vault
metadata:
  hermes:
    tags: [automation, system, security, watchdog, red-team, scan, obsidian, gmail, suite]
---

# 系統監控、資安紅隊與知識庫運維旗艦（System Watchdog Suite）

全方位涵蓋本機與雲端系統健康檢查、安全漏洞防禦、網頁變動監控、郵件智慧分流與 Obsidian 知識庫維護的後勤旗艦。

---

## 旗艦模組一覽

### 模組 1：個人與團隊紅隊審計（Personal Red Team Audit）
- **全系統盤點**：清查所有本機專案、Launchd 服務、排程 Cron 與過期金鑰。
- **風險等級劃分**：P0 安全修復立即執行，P1/P2 決策產出結構化簡報。

### 模組 2：依賴與資安漏洞掃描（Security & CVE Scanners）
- **OWASP Top 10 防禦檢驗**：XSS、CSRF、CORS 錯誤配置與敏感端點暴露檢查。
- **CVE 依賴掃描**：npm / pip 套件漏洞比對與自動升級修復建議。

### 模組 3：網頁變動監控看門狗（Web Monitor Watchdog）
- **基於雜湊的比對機制**：定時抓取目標網頁，內容無變動保持靜默，偵測到實質差異即刻警報。

### 模組 4：Cloudflare Turnstile 無感驗證碼防護（Turnstile Integration）
- 前端 Widget 嵌入 + 後端 Worker 密鑰校驗，徹底阻擋惡意爬蟲與表單濫填。

### 模組 5：郵件智慧分流與摘要（Gmail AI Triage）
- 自動讀取收件匣、依商務重要性套用標籤，每日產出待辦事項精華摘要。

### 模組 6：Obsidian 第二大腦知識庫維護（Obsidian Organizer）
- PARA 階層整理、雙向 Wiki 連結修復、Daily Notes 與專案日誌結構化沉澱。
