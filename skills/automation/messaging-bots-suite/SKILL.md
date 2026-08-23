---
name: messaging-bots-suite
description: 企業通訊與自動化通知旗艦：飛書/Lark 機器人開發與多維表格整合（lark-bot-development）、LINE 官方帳號推播（line-messaging-api）、Cloudflare 交易郵件服務（cloudflare-email-service）、Google Apps Script 表單無伺服器後端（gas-form-backend）與酷澎分潤自動化（coupang-partners-api）。
version: 1.0.0
author: Community
license: MIT
read_when:
  - User wants to develop or integrate Lark/Feishu bots, event subscriptions, interactive cards, or Bitable APIs
  - User wants to push notifications, forms, or order alerts to LINE Official Account or customer support groups
  - User wants to build transactional email services using Cloudflare Email Routing and Workers
  - User wants a serverless backend for static forms connecting to Google Sheets via Google Apps Script
  - User wants to integrate Coupang Partners Taiwan affiliate API
metadata:
  hermes:
    tags: [automation, messaging, bots, lark, line, email, gas, sheets, coupang, suite]
---

# 企業通訊與自動化通知旗艦（Messaging Bots Suite）

整合即時通訊機器人、表單進件處理、交易郵件與分潤管線的一體化企業通訊與通知旗艦。

---

## 旗艦模組一覽

### 模組 1：飛書 / Lark 機器人與多維表格（Lark Bot & Bitable）
- **事件訂閱與 Webhook**：接收訊息、按鈕點擊事件並即時回應用戶。
- **互動卡片（Card JSON）**：建構包含按鈕、表單輸入、富文字的精美企業訊息卡。
- **多維表格（Bitable API）**：資料雙向同步、自動記錄工單、客戶 CRM 盤點。

### 模組 2：LINE 官方帳號通知管線（LINE Messaging API）
- **Push / Multicast 訊息推播**：訂單成立、報名成功即時通知使用者。
- **客服群組即時告警**：系統異常、新客詢價第一時間推播至管理員群組。

### 模組 3：Cloudflare 交易郵件系統（Cloudflare Email Service）
- **Email Routing + Worker**：自訂網域收信與事件解析。
- **Transactional Email 發送**：免付費第三方服務，以極簡 Worker 實現郵件通知。

### 模組 4：Google Apps Script 無伺服器表單後端（GAS Form Backend）
- **靜態網頁表單直接存入 Google Sheets**：免自建後端資料庫，自帶 CORS 與防重複提交。

### 模組 5：酷澎台灣分潤自動化（Coupang Partners API）
- **HMAC SHA-256 簽章產生**、商品搜尋、每日佣金與點擊率報表排程。
