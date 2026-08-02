---
name: gas-form-backend
description: Use when a static form or booking system needs a Google Apps Script backend.
---

# GAS Form Backend (Google Apps Script)

靜態站（CF Pages / Vercel / GitHub Pages）最便宜的表單後端：GAS 網頁應用程式接收 POST → 寫 Google Sheets + Email 通知 + LINE 群組推送。免伺服器、免費、5 分鐘上線。

## 架構

```
index.html 表單 → fetch POST → GAS /exec (doPost)
                                   ├─ ① SpreadsheetApp.appendRow → Sheets
                                   ├─ ② MailApp.sendEmail → NOTIFY_EMAIL
                                   └─ ③ LINE Messaging API push → 客服群組 (muteHttpExceptions, 失敗不擋報名)
```

- GAS 部署網址貼回 index.html 的 `SHEET_URL`（no-cors 直接模式：`mode:'no-cors', headers:{'Content-Type':'text/plain'}` — 讀不到回應，永遠顯示成功）。
- 測試函式（`testPost` 等）在 Apps Script 編輯器直接執行，不需部署；模擬 `{postData:{contents: JSON.stringify({...})}}` 餵給 doPost。
- **現成範本**：`templates/Code.gs` — 三通道完整可用的 Code.gs（含 testPost / testLineNotify / doPostWebhook），複製後填五個常數即可。

## 部署設定（最容易卡關的地方）

1. 試算表 → 擴充功能 → Apps Script → 貼 Code.gs → ⌘S
2. 先跑 `testPost` 驗證寫入（執行前會跳授權 → 允許）
3. 部署 → 新增部署 → 網頁應用程式：
   - **執行身份：我（你的帳號）**
   - **誰可以存取：所有人** ← 最關鍵。選「只有我自己」→ 匿名 POST 被擋，curl 拿到錯誤/登入頁
4. ⚠️ **編輯既有部署（改權限等）不會換網址** — 只有「新增部署」才產生新網址。改權限後同網址仍有效（見下方🔴細節）。

### 🔴 部署綁定版本快照 — 改程式碼後必須重新部署（本 session 實測卡關）
GAS 部署指向「部署當下的程式碼版本快照」。**貼新 Code.gs + ⌘S 不會更新已部署的版本**。改了 doPost 之後線上仍跑舊碼：
- 症狀：Apps Script 編輯器跑 `testPost()` 正常（用最新碼），但線上 curl/瀏覽器 POST 卻 404/找不到網頁（部署仍指向舊版，例如貼碼前部署的初始空白版）
- 解法：**部署 → 管理部署 → 編輯 → 版本選「新增版本」（New version）→ 部署**。網址通常**不變**，但內部指向新版本
- 判別：編輯器測試過、部署設定也對，POST 還是 404 → 九成是版本快照沒更新
- 注意：**編輯既有部署的存取權限（執行身份/誰可存取）不會換網址** — 網址變更只發生在「新增部署」時。所以「改權限後舊網址失效」要改成「新增部署才產生新網址」；權限改完用同網址但記得同步新版本

## curl 測試 GAS 端點（容易誤判）

GAS 對每個請求先回 **302**（跳到 googleusercontent 執行端）。curl 測試的鐵律：

```bash
curl -s --post302 -L -X POST "<GAS_URL>/exec" \
  -H "Content-Type: text/plain" \
  -d '{"name":"驗證","phone":"0912","class":"9月班","cf-turnstile-response":""}'
```

- ❌ `curl -L` 單獨用：302 後 POST 降級成 GET → GAS 沒有 doGet → 回「找不到網頁」錯誤頁（看起來像部署壞了，其實是方法降級）。
- ❌ 沒 `-L`：只看到 302 HTML。
- ✅ `--post302 -L`：保留 POST 跟隨重導，拿到 JSON 回應。
- GET `/exec` 回 200 +「錯誤」頁是正常的（無 doGet）— 不代表壞。
- 若 `--post302` 仍拿不到 JSON（實測偶發）：分兩步 — 先 `curl -D -` 抓 302 的 `location`（每次不同的一次性 echo URL），再 `curl -X POST "<location>"`。最終極判法：**瀏覽器頁面 `fetch(url, {method:'POST', mode:'no-cors'})` 回 status=0（opaque）即成功送達** → 檢查 Sheets 是否多一列，這是唯一不誤判的端到端驗證。

## LINE 通知（Messaging API push 到群組）

**需求是「客服看到資料」時的注意點：**
- LINE 官方帳號後台的聊天室（manager.line.biz Chat）**只顯示客戶主動發來的訊息** — 系統自動產生的資料不會出現在那。要「客服看得到」用 **客服 LINE 群組**（push 到群組，所有成員可見），不是官方帳號後台。
- 前置：官方帳號必須**已加入群組**（否則 push 回 400）；客服異動隨時加人即可，不用改程式。

**拿 groupId（webhook echo 法）：**
1. 把 GAS 部署網址填到 LINE Developers → Messaging API → Webhook URL，開啟 webhook
2. 群組發一則訊息 → GAS 執行記錄印出 `GROUP_ID → Cxxxx...`
3. 填回 `LINE_GROUP_ID`，之後可改回正式部署

**推送程式碼要點：**
- `muteHttpExceptions: true` + HTTP >= 400 只 `console.log` **不 throw** — LINE 掛掉不能擋報名（主通道是 Sheets）。
- token/userId 仍為佔位符時直接 skip（`indexOf('YOUR_LINE') !== -1`）— 設定前不會報錯。

## Pitfalls

- **`getActiveSheet()` 在部署環境不可靠** — 用 `SpreadsheetApp.openById(ID).getSheets()[0]`（第一張表），否則可能寫錯表或取不到。
- **🔴 聊天視窗貼程式碼會被截斷（本 session 實測）** — 長 Code.gs 經聊天傳輸後常數值被截成 `'YOUR_T..._KEY'` 這種殘缺字串，使用者貼進 Apps Script 後 `TURNSTILE_SECRET !== 'YOUR_TURNSTILE_SECRET_KEY'` 誤判成立 → doPost 直接回 `{"error":"missing token"}`，資料不寫入。**要引導使用者貼程式碼時，用 MEDIA: 檔案連結交付（`MEDIA:/abs/path/Code.gs`），不要貼在聊天內文**；貼完叫使用者檢查常數行是否完整。
- **Turnstile 佔位符邏輯**：`if (TURNSTILE_SECRET !== 'YOUR_TURNSTILE_SECRET_KEY')` 才做驗證 — 佔位符＝驗證關閉。所以截斷的佔位符會意外「開啟」驗證 → missing token。
- **前端成功頁顯示已填資料 + 複製按鈕**（客戶貼給客服流程）：表單送出後 `showSuccess(payload)` 渲染個資卡片；`navigator.clipboard.writeText` + `execCommand('copy')` fallback；卡片內容先 `escapeHtml` 再塞 innerHTML（XSS）；LINE CTA 用 `https://line.me/R/ti/p/@<官方帳號ID>`。
- **GAS 部署 URL 貼進 index.html 後**：驗證「表單後端尚未完成設定」防護（`SHEET_URL.indexOf('YOUR_DEPLOYMENT_ID') !== -1`）不再觸發。

## Booking 系統（美甲/髮廊/按摩等預約）

同一 GAS 後端可升級成預約系統：多一張 `bookings` 表 + 時段衝突檢查 + 密碼保護的管理後台。完整可複製模式（表結構、API 路由、時段生成演算法、衝突檢查、後台認證）見 `references/booking-system-patterns.md`。重點：

- **時段生成**：`OPEN_HOUR`/`CLOSE_HOUR`/`SLOT_STEP_MIN` 常數 + 服務時長 → 產生候選起始時間；排除與既有預約重疊（`start < bEnd && end > bStart`）與「今天已過去的時段」。
- **🔴 no-cors 讀寫陷阱（本 session 實測）**：`mode:'no-cors'` 回傳 opaque response **讀不到 JSON** — 只有 fire-and-forget 寫入（createBooking 送出後直接顯示成功頁）能用；**讀取回應的呼叫（listServices / getSlots）必須用一般 fetch**（GAS 支援 CORS，`headers:{'Content-Type':'text/plain'}` + `.then(r => r.json())` 即可）。
- **後台認證**：adminKey 送**原始密碼**，GAS 端 `Utilities.computeDigest(SHA_256)` 再比對 `ADMIN_KEY_HASH`；前端用 SubtleCrypto（async，`.then`）做快速預檢。前端 hash 常數 `PASSWORD_HASH` 與後端 `ADMIN_KEY_HASH` 同值。
- **testInit 模式**：一貼 Code.gs 就能跑 — 建三張表（services/bookings/settings）+ 填入範例服務，使用者先驗證再部署。
- **Mock-first 開發（先模擬資料、後建 API）**：使用者說「先用模擬資料，之後再建 API」→ 前端加 `USE_MOCK` 開關，mock 分支回傳與 API 同型的 Promise 資料，翻一個 flag 就切換真後端。完整模式（共用 localStorage key、後台 mock 登入、schema 完整性陷阱、跨頁 helper 一致性、**多租戶 per-tenant key**）見 `references/booking-system-patterns.md`。
- **日期選取 = 整月月曆網格，不要橫向捲動條**（使用者修正過兩次）：當月+下月各 7 欄 grid、過去日期淡出不可點、今天高亮預設選中。實作細節見 `references/booking-system-patterns.md` 的「日期選取 UX」。
- **多租戶 SaaS 化決策**：GAS+Sheets 撐不起多租戶（無真 DB/認證/隔離）→ 換 Supabase；CF Pages 路由用 query param 不用 path（clean URL 308 會吃掉 slug）。競品（Folio.tw）功能路線圖 P0/P1/P2 見 `references/booking-system-patterns.md`。

## 驗證清單

1. Apps Script 編輯器跑 `testPost` → Sheet 多一列
2. curl `--post302 -L` → `{"success":true}`
3. `testLineNotify` → 客服群組收到訊息
4. 網頁真實填單 → Sheet/Email/LINE 三通道 + 成功頁卡片
