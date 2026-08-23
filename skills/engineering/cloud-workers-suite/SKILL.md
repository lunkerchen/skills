---
name: cloud-workers-suite
description: Cloudflare Workers 與 MCP 服務旗艦：Hono on Workers 完整測試套件（hono-workers-testing: Vitest, D1 mock, execution context）與無狀態 MCP 伺服器部署（mcp-worker-deploy: 2026 最新標準）。
version: 1.0.0
author: Community
license: MIT
read_when:
  - User asks to test, build, or debug Hono on Cloudflare Workers (Vitest, D1 mock, executionContext)
  - User asks to build, test, or deploy stateless MCP (Model Context Protocol) servers on Cloudflare Workers
metadata:
  hermes:
    tags: [engineering, cloudflare, workers, hono, mcp, testing, deployment, suite]
---

# Cloudflare Workers 與 MCP 服務旗艦（Cloud Workers Suite）

專注於 Serverless 邊緣運算、Hono 微服務測試與 2026 最新無狀態 MCP 伺服器建置部署的工程工作台。

---

## 旗艦模組一覽

### 模組 1：Hono on Workers 測試管線（Hono Workers Testing）
- **Vitest + Cloudflare Workers Pool**：在真實隔離環境下測試 Worker 路由。
- **D1 Database Mocking**：本地模擬 SQLite/D1 資料庫交易與 Migrations。
- **Execution Context 模擬**：測試 `ctx.waitUntil()` 與背景任務執行。

### 模組 2：無狀態 MCP 伺服器部署（Stateless MCP Deploy）
- **2026 最新 MCP Streamable HTTP 規範**：支援 SSE / Streamable HTTP 傳輸協定。
- **Tool 宣告與行為標註**：宣告 `readOnlyHint` 與 `destructiveHint`，確保 Agent 安全調用。
- **一鍵部署至 Cloudflare Workers**：冷啟動 < 10ms，全球邊緣分發。
