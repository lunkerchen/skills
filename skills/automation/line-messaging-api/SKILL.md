---
name: line-messaging-api
description: 表單/報名/訂單資料自動送 LINE 官方帳號或客服群組（Messaging API push）。
---

# LINE Messaging API 整合

## 觸發條件
- 使用者想讓表單/報名/訂單資料自動送到 LINE（官方帳號或客服群組）
- 「LINE 通知」「官方帳號自動發訊息」「客服看到表單資料」
- 任何需要 `api.line.me` 的整合

## 核心架構（GAS 表單 → 三通道）

```
客戶填網頁表單（純網頁，客戶完全不碰 LINE）
   │
   ▼
Google Apps Script doPost → ① Google Sheets 寫入
                          → ② MailApp.sendEmail → 通知信箱
                          → ③ LINE push → 客服群組（所有客服即時看到）
```

關鍵事實：**客戶不需要加官方帳號好友**。LINE push 是「官方帳號 → 客服群組」方向，客戶從頭到尾不涉及 LINE。唯一前置條件是官方帳號要已在目標群組內。

## 🔴 最重要的陷阱：官方帳號後台 Chat 看不到系統訊息

使用者常以為「資料送到官方帳號，後台客服介面就看得到」。**錯** — LINE 官方帳號後台的聊天室（manager.line.biz Chat）**只顯示客戶主動發來的訊息**。系統自動產生的報名資料不會出現在那裡，除非客戶自己加好友並傳訊息。

所以「表單 → 官方帳號後台 Chat」這條路走不通。正確做法：

| 方案 | 客服怎麼看到 | 適合 |
|---|---|---|
| **客服 LINE 群組（推薦）** | 建 LINE 群組加客服人員 + 官方帳號也加入 → push 到群組 `groupId`，所有人即時看到 | 客服 2 人以上 |
| 單一客服帳號 | push 到某個專責客服的個人 LINE `userId` | 客服只有 1 人 |

先問清楚「客服要怎麼看到」，再決定 push 目標是 groupId 還是 userId。群組好處：客服異動不用改程式碼，加人退人即可。

## GAS 部署引導流程（使用者一步一步走）

當使用者說「先引導我建立 Google Sheet」或需要從零部署 GAS 後端時，依序引導（每步等使用者確認再繼續）：

1. **建試算表**：`https://sheets.new` → 改名 → 第一列手打欄位標題（時間戳記 | 姓名 | 手機 | Email | LINE ID | 報名班別 | 護理人員 | 備註）→ 不要預設資料列（程式自動 append）
2. **拿 SPREADSHEET_ID**：URL `docs.google.com/spreadsheets/d/<ID>/edit` 中間段（約 44 字元大小寫英數）。**拿到的 ID 立刻填入 Code.gs**，把完整 Code.gs 內容給使用者整段貼進 Apps Script（使用者通常不自己改檔案 — 給整段可貼的 code block，SPREADSHEET_ID 已填好）
3. **貼入 Apps Script**：試算表 → 擴充功能 → Apps Script → 刪掉預設 `myFunction` → 整段貼上 → ⌘S
4. **先測不部署**：函式下拉選 `testPost` → 執行 → 第一次跳 Google 授權（選帳號 → 允許）→ 回試算表確認多一列測試資料
5. **部署拿 URL**：部署 → 新增部署 → 網頁應用程式 → 執行身份設「自己」→ 允許任何人存取 → 複製 `/exec` 網址
6. **貼回前端**：把部署網址貼回 index.html 的 `SHEET_URL`（佔位符 `YOUR_DEPLOYMENT_ID`）→ commit → 部署

引導時每次只給 1-2 步、明確告訴使用者「做完跟我說」— 這類 Google 帳號操作只能使用者本人做，agent 無法代勞。

## 設定步驟

### 1. 拿 Channel access token
LINE Developers（https://developers.line.biz）→ 登入 → 選官方帳號 Channel（沒有就先建：Providers → Create Channel → Messaging API）→ **Messaging API 分頁** → Channel access token → Issue（long-lived）→ 複製。

### 2. 建客服群組 + 拿 groupId
1. LINE 上建群組，加客服人員
2. **官方帳號加進群組**（群組設定 → 邀請 → 搜尋官方帳號名）
3. 拿 groupId 兩種方法：
   - **webhook echo（推薦，可寫死在 GAS）**：GAS 部署為網頁應用程式 → 網址填到 LINE Developers → Messaging API → Webhook URL → 開啟 Webhook → 群組發一則訊息 → 回 Apps Script 看執行記錄，Log 印出 `GROUP_ID → Cxxxx...`
   - 官方後台 Webhook 測試功能直接看 raw JSON 的 `source.groupId`

### 3. GAS push 程式碼（核心片段）

```javascript
const LINE_CHANNEL_TOKEN = 'YOUR_LINE_CHANNEL_ACCESS_TOKEN';
const LINE_GROUP_ID      = 'YOUR_LINE_GROUP_ID';

function sendLineNotify(subject, body) {
  if (LINE_CHANNEL_TOKEN.indexOf('YOUR_LINE') !== -1 || LINE_GROUP_ID.indexOf('YOUR_LINE') !== -1) {
    console.log('LINE notify skipped: token/groupId 未設定');
    return; // 佔位符防護：未設定就跳過，不影響主流程
  }
  var params = {
    method: 'post',
    headers: { 'Authorization': 'Bearer ' + LINE_CHANNEL_TOKEN, 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      to: LINE_GROUP_ID,
      messages: [{ type: 'text', text: '🔔 ' + subject + '\n' + body }]
    }),
    muteHttpExceptions: true
  };
  var res = UrlFetchApp.fetch('https://api.line.me/v2/bot/message/push', params);
  if (res.getResponseCode() >= 400) {
    console.log('LINE push failed: HTTP ' + res.getResponseCode() + ' ' + res.getContentText());
  }
}
```

### 4. webhook echo 函式（拿 groupId 用，也可驗證 webhook 活著）

```javascript
function doPostWebhook(e) {
  const body = JSON.parse(e.postData.contents);
  console.log('WEBHOOK_RAW →', e.postData.contents);
  const event = body.events && body.events[0];
  if (event && event.source && event.source.groupId) {
    console.log('GROUP_ID →', event.source.groupId);
    return ContentService.createTextOutput(JSON.stringify({ groupId: event.source.groupId }))
      .setMimeType(ContentService.MimeType.JSON);
  }
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

## 前端成功頁 + 複製引導（客戶主動貼給客服）

後端自動 push 之外的另一種需求：「客戶填完表單 → 跳出成功頁 → 自己複製個資 → 加官方帳號 → 貼給客服」。兩者不衝突，可並存（後端自動推 + 前端引導客戶）。

- 成功頁（表單送出後）顯示已填資料卡片 + **複製按鈕** + 綠色「加入 LINE 官方帳號」CTA（`https://line.me/R/ti/p/@<官方ID>`）
- 複製實作：`navigator.clipboard.writeText(text)`，失敗 fallback `execCommand('copy')`（textarea + select + copy）；成功即時回饋（按鈕文字改「已複製 ✓」+ hint，2.5s 還原）
- 個資渲染必須 `escapeHtml`（XSS 防護）；用 template literal 組 HTML 符合 Biome
- 卡片只在有 payload 時顯示（honeypot 假成功路徑不帶 payload → 不顯示卡片，bot 看不到引導）

### Playwright 驗證完整表單流程（無真實後端時）

```bash
# 1. 假 GAS 端點：回 {success:true}（node http server，CORS headers 記得開）
# 2. sed 把 index.html 的 SHEET_URL 換成本地端點
sed "s|https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec|http://localhost:8799/exec|" index.html > /tmp/flow-test.html
# 3. Playwright：填表 → submit → 驗證成功頁 show、卡片顯示、內容正確、CTA href
```

注意：file:// 開頁時 `fetch('/videos.json')` 會報 scheme 錯誤 — 那是測試環境限制，忽略；部署後不存在。

## 設計原則

- **LINE 失敗不擋主流程**：`muteHttpExceptions: true` + 只記 log 不 throw。表單主通道是 Sheets；LINE/Email 是通知，壞了不該讓客戶報不了名。告知使用者這個設計決策。
- **佔位符防護**：token/groupId 未設定時靜默跳過（`indexOf('YOUR_LINE') !== -1`），避免部署未設定就推送到假目標。
- **測試函式**：`testLineNotify()` 發一則測試訊息到群組，設定後第一個驗證步驟。

## 陷阱
- push 到群組回 400 = 官方帳號不在群組內（或 token 無效）。先確認官方帳號已加入群組。
- 錯誤訊息的 HTTP code 一定要看（`getResponseCode()`）— 400 是群組問題，401 是 token 問題。
- 「客戶沒加好友會不會卡住？」→ 不會，客戶端零 LINE 依賴；只有客服接收端需要官方帳號在群組內。
- 若客戶想要「官方帳號主動回覆客戶 LINE」→ 那需要客戶加好友 + webhook 拿 userId，是另一套流程（LIFF/Login），不要混為一談。

## 實作案例
- 批貨課程網站（your-course-landing）：Code.gs 表單三通道（Sheets + Email + LINE 客服群組），完整程式碼在專案 `Code.gs`。
