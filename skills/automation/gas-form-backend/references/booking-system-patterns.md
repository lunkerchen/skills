# GAS Booking 系統完整模式（2026-08 實作：美甲預約系統）

靜態站預約系統的 GAS 後端 + 雙前端（公開預約頁 + 密碼後台）完整可複製結構。
實作專案：`$DEV_PROJECTS/your-booking-app/`（Code.gs + public/booking.html + admin/index.html + README.md）。

## 檔案結構

```
your-booking-app/
├── Code.gs              # GAS 後端（doPost API + Sheets + LINE）
├── public/booking.html  # 公開預約頁（三步驟：服務→時段→資料）
├── admin/index.html     # 管理後台（密碼保護 + 月曆 + CRUD）
└── README.md            # 部署說明（GAS 發布 + CF Pages）
```

## Sheets 表結構

- `services`: `id | name | price | durationMin | color | enabled`
- `bookings`: `id | date | serviceName | price | durationMin | startTime | endTime | customerName | customerPhone | customerLine | status | notes | createdAt`
- `settings`: `key | value`（備用）

`status` 值：`pending`（公開送出預設）/ `confirmed` / `cancelled`。

## API 路由（doPost switch on body.action）

公開：
- `listServices` → `{data: [...]}`（前端載入服務卡）
- `getSlots {date, serviceId}` → `{data: [{startTime, endTime}]}`（可約起始時間）
- `createBooking {booking}` → 建 `pending` 預約 + LINE 通知

管理（`requireAdmin(body.adminKey)` 擋在前面）：
- `adminListBookings {month:'YYYY-MM'}` → 月預約（日曆 dots）
- `adminUpsertBooking {booking}`（id 存在=更新，缺 id=新增）
- `adminDeleteBooking {id}`
- `adminUpsertService` / `adminDeleteService`
- `adminSendLine {text}`（後台測試 LINE）

## 時段生成演算法（getSlots）

```
for m in OPEN_HOUR*60 .. (CLOSE_HOUR*60 - dur), step SLOT_STEP_MIN:
    startMin = m; endMin = m + dur
    if 今天是同一天 && slotStart <= now: skip          # 過去時段
    for b in 當天 confirmed/pending bookings:
        if startMin < bEndMin && endMin > bStartMin: conflict → skip
    else push {startTime, endTime}
```

`timeToMin('HH:MM')` / `minToTime(min)` 是核心工具函式。`checkConflict(date, startTime, dur, excludeId)` 供 upsert 用（excludeId 排除自己，編輯預約時不會誤判）。

## 後台認證流程（SHA-256，密碼不落地明文）

1. 使用者產生密碼 → `printf '%s' "$PASS" | shasum -a 256` → 得 hash
2. 同一個 hash 填兩處：`Code.gs` 的 `ADMIN_KEY_HASH`、`admin/index.html` 的 `PASSWORD_HASH`
3. 前端登入：SubtleCrypto `crypto.subtle.digest('SHA-256', ...)`（**async**，`.then` 拿 hash）→ 與 `PASSWORD_HASH` 預檢
4. 通過後 `adminKey = 原始密碼`（**不是 hash**）存入變數 + sessionStorage — GAS 端收到後自己 `Utilities.computeDigest` 再比對

⚠️ 前端 hash 只做快速拒絕（少打一次 GAS）；真正的安全邊界在 GAS 的 requireAdmin。sessionStorage 存原始密碼是給單人後台用的便利，非安全邊界（此模式同 course-landing 後台）。

## no-cors 使用規則（重要）

| 呼叫 | mode | 理由 |
|------|------|------|
| createBooking 送出 | `no-cors` | fire-and-forget，成功頁直接顯示，讀不到回應沒關係 |
| listServices / getSlots / 所有 admin 呼叫 | 一般 fetch | 需要 `r.json()` 讀取回應，no-cors 是 opaque 讀不到 |

## LINE 通知

與表單版相同：`notifyLine(text)` 用 `muteHttpExceptions:true`，token/groupId 為佔位符時 skip，失敗只 console.log 不 throw（不擋預約主流程）。新預約通知訊息模板：
`🆕 新預約待確認\n📅 日期 時間～結束\n💅 服務（NT$價格）\n👤 姓名 / 手機 / LINE`

## 前端流程（booking.html）

- Step 1 服務卡（grid，點選高亮 `data-id`）→ Step 2 日期選取（整月月曆網格，見下方「日期選取 UX」）+ 時段按鈕（顯示結束時間 `～HH:MM`）→ Step 3 資料（姓名/手機/LINE/備註）→ 成功頁個資卡片 + 複製按鈕 + LINE CTA（同 gas-form-backend 成功頁模式）
- 手機驗證 regex：`/^0\d{1,2}-?\d{3,4}-?\d{3,4}$/` — ⚠️ **本版 regex 會擋 `0912-345-678`**（`0\d{1,2}` 吃掉 2 碼後，剩餘位數對不上 `\d{3,4}` 分組）。實作修法：**先剝掉分隔符再驗證** `const p = phone.replace(/[- ]/g,''); /^0\d{8,9}$/.test(p)` — 一次就過，不用跟 hyphen 位置纏鬥。
- 後台月曆：`YYYY-MM` 狀態變數 + 7 欄 grid + 其他月補格；每天紅點 = 非 cancelled 預約數；點日期 → 當日預約列表 + 新增/編輯表單

## 日期選取 UX（公開頁 Step 2 — 使用者修正版）

**使用者明確拒絕「橫向捲動的日期條」兩次**（先做 14 天捲動條 → 改兩個月分組捲動 → 最終定案「整月網格不捲動」）。預約系統日期選取的最終形態：

- **整月月曆網格**：當月 + 下月兩組，上下排列，各自 `日一二三四五六` 表頭 + 7 欄 grid，完全不捲動。每組 `firstDow` 前補空 cell（`<div class="cal-empty">`）。
- **過去日期淡出不可點**：`isPast` → `.cal-day.past { opacity:.3; pointer-events:none }`（保留在 DOM 維持 7 欄對齊）。
- **今天高亮 + 預設選中**：`.cal-day.today` 粉紅邊框 glow；`state.date = fmtDate(today)` 開局即選今天。
- **選取邏輯集中**：`markSelDate()` 掃 `.cal-day` 依 `data-date === state.date` toggle `.sel`；`pickDay(date)` 清 `state.startTime` 後 `loadSlots()`。
- 相關 CSS：`.cal-day { aspect-ratio:1 }` 正方形格子、`.cal-head` 表頭字 11px muted。

## Mock-first 開發（先模擬資料，之後再建 API）

使用者要求「先用模擬資料，之後再建 API」時：前端加 `USE_MOCK` 開關，mock 分支回傳與 API 同型（Promise + 相同欄位）的資料，翻一個 flag 就切換真後端，不重寫 UI。

- **共用 localStorage key**：公開頁與後台用**同一個 key**（如 `nb_mock_bookings`），公開頁送的預約後台馬上看到 — mock 跨頁面互通。**多租戶 SaaS 版：key 帶 tenant**（`nb_mock_bookings_<tenant>`）— 公開頁/後台都從 `?tenant=` query param 解析 tenant 再組 key，天然隔離租戶資料（實測 amy 的預約 lisa 後台看不到）。
- **三處資料來源函式都要有 mock 分支**：`loadServices` / `getSlots` / `submitBooking`（後台是 `callApi`）各加 `if (USE_MOCK) { ... return Promise.resolve(...) }`，API 型別一致，切換時只改 flag。
- **後台 mock 登入**：mock 模式任何密碼都過（`if (!USE_MOCK && hash !== PASSWORD_HASH) fail`），方便先測流程。
- **🔴 mock 資料必須 schema 完整**（本 session 實測）：mock save 沒寫 `status` → admin 把 `undefined` 當成 `cancelled`，顯示「已取消」。mock 記錄要帶與 API 相同的完整欄位（`status:'pending'`、`createdAt`、`customerName` 等），否則下游 UI 誤判。
- **🔴 共用 helper 函式要在每個頁面都存在**（本 session 實測）：公開頁 mock 用了 `fmtDateTime`（只有 admin 有）→ `fmtDateTime is not defined`。任何 mock/共用程式碼引用的 helper，每個使用它的頁面都要定義（或把 helper 放兩邊）。
- **驗證**：deploy 後用瀏覽器 console 直接呼叫 `pickService`/`goStep`/`submitBooking` 模擬完整流程（inline onclick 在自動化 click 下不一定觸發，console 直呼函式更可靠），再查 `localStorage.nb_mock_bookings` 確認欄位；後台驗證同 key 資料可見 + `confirmBk` 後 `status === 'confirmed'`。

## SaaS 化（多租戶）決策與路線圖（2026-08 使用者方向）

**核心決策：GAS + Google Sheets 撐不起多租戶 SaaS** — 沒有真資料庫、沒有多用戶認證、Sheets 無法做租戶隔離。資料層換 Supabase（Postgres + RLS + Auth + Edge Functions）。同一套核心，差別只在「多租戶隔離」與「金流」深度。

- **多租戶路由**：CF Pages 用 **query param** `?tenant=<slug>`（不用 path `/b/:slug/` — clean URL 308 會吃掉 slug，見 cloudflare-deploy skill）。前端 `URLSearchParams` 解析 tenant → 品牌化（店名/配色）→ mock key 帶 tenant（見上方 Mock-first 節）。
- **前端接 Supabase**：公開端走 Edge Functions（service role key 在函式內，前端不暴露）；admin 走 Supabase Auth（email+密碼）→ session token → REST + RLS 強制租戶隔離（`tenant_id` 由 token 解析，不需前端手動帶）。
- **競品基準（Folio.tw 2026-08 分析）** — 美業預約 SaaS 的功能矩陣與建議路線圖：
  - **P0（現在做，各半天）**：① 放鳥防線 — bookings 加 `no_show` 標記，後台一鍵標未到店，同客戶（phone）累積 2 次 → 公開頁自動擋預約；② 行前提醒 — 預約前一天自動 LINE 推客戶。
  - **P1（SaaS 商業化時，各 1-2 天）**：③ 客戶視圖（從 bookings 反推客戶列表：姓名/電話/LINE/到訪次數/總消費）；④ 回訪追單（服務完成後 N 天 LINE + 優惠券）；⑤ 儀表板（營收/熱門服務/離峰時段/VIP — 全 SQL）；⑥ 預約日曆週檢視 + 拖放。
  - **P2（收費後）**：訂金（LINE Pay/藍新）、計次券/儲值、AI 品牌文案。
  - **不學 Folio**：iPad POS、多產業支援 — 偏離核心，個人工作室用不到。
- **日期選取 UX 見上方章節**（SaaS 版沿用整月月曆網格）。

## 驗證

- GAS 端：`testInit()`（建表+範例）→ `testPost()`（寫一列）→ `testSlots()`（時段）
- 端到端：公開頁真實送出 → Sheets 多一列 pending → 後台看到 + 可確認
- 部署後：CF Pages `npx wrangler pages deploy . --project-name=<name> --branch main`
