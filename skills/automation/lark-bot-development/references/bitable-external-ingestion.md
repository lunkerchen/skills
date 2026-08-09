# Bitable / 多維表格 as data layer — external ingestion research

Research date: 2026-08-06. Question: can Feishu/Lark Base (多維表格) alone handle "Gmail 收到 104 應徵履歷信 → 擷取姓名/職位 → 填入表格"?

**Bottom line: 多維表格是 HR 操作與資料管理層，不是 Gmail 抓信引擎。** Email reading, subject parsing, dedup, retry, and Gmail label write-back belong to an external trigger (Apps Script / n8n / Make / custom service); Base does storage, views, dashboards, status, collaboration, notifications.

## Bitable API capability map (confirmed from official docs)

- **Records**: create `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records`, batch_create (≤1000/req), update `PUT .../records/{record_id}`, batch_update, list, search, batch_get (≤100 records), delete.
- **Search + filter** (`records/search`): `{"filter":{"conjunction":"and","conditions":[{"field_name":"...","operator":"is","value":["..."]}]}}`
  - Operators: `is, isNot, contains, doesNotContain, isEmpty, isNotEmpty, isGreater, isGreaterEqual, isLess, isLessEqual`. `like` / `in` NOT supported.
  - Only ONE level of `children` nesting supported. Formula/lookup fields not usable as filter conditions.
  - Field value formats: text = string; single select = string; date = ms timestamp (`["ExactDate","1702449755000"]` or `["Today"]`); person = open_id; checkbox = `"true"`/`"false"`; hyperlink filter = display name.
- **Auth**: tenant_access_token or user_access_token. App must be owner/collaborator of the Base or calls fail (code 99991 permission denied). With 進階權限 enabled, app must be in a role with read/write (1254302 RolePermNotAllow).
- **Limits**: batch ≤1000 records; recommend ONE write op at a time per Base; no concurrent writes to the same table (1254291 LockNotObtainedError); ≤20,000 records/table (1254103); 300 fields, 200 views, 100 tables per Base.
- **No unique constraint guarantee** on text fields — dedup must be app-side: search by key → create only if absent → serialize writes.

## Feishu 多維表格 automation (native; China-version docs, Lark equivalent assumed)

Triggers: 添加新記錄時 / 修改記錄時 / 新增修改記錄滿足條件時 / 到達記錄中的時間時 / 定時觸發 / 點擊按鈕 / 接收到飛書消息時 / **接收到 webhook 時**.
Actions: 發送飛書消息/郵件 / 新增/查找/更新記錄 / AI 生成文本 / 條件判斷 / **發送 HTTP 請求** / 飛書應用接入.

- **Webhook trigger**: external `POST` → workflow → add/update record. URL per workflow. https://www.feishu.cn/hc/zh-CN/articles/612376356355
- **HTTP request action** (developer feature): public URL only (內網 URL 不支援); 60s response cap; on timeout the external call may have succeeded — confirm with the callee, retry externally; response parse none/text/JSON.
- **Outlook connector CONFIRMED**: trigger 接收到 Outlook 郵件時 + action 發送 Outlook 郵件; third-party account auth per workflow (not preserved on copy/duplicate). https://www.feishu.cn/hc/zh-CN/articles/033488625793
- **Gmail connector — 國際版 Lark 已確認（2026-08-06）**：官方 AnyCross 有 `Archive Email from Gmail to Lark Base` 範本（https://anycross.larksuite.com/documentation/template/all/archive-gmail-to-base）。**Gmail Trigger 每 5 分鐘輪詢，非即時 push**。AnyCross = Lark 官方 Zapier 類整合產品（https://www.larksuite.com/en_us/product/anycross），Gmail/Base 皆在其連接器庫。中國版飛書（feishu.cn）與租戶等級的連接器清單仍須在實際連接器中心實測，別假設相同。仍需在範本中確認：message ID 是否暴露、subject 是否完整、能否查 Base 既有 record 做條件分支、能否加 Gmail label（範本只證明「存進 Base」，不回寫 Gmail 標籤）。
- 連接器 (sync external data INTO a 閃電-flagged table) ≠ 自動化 (event → action). https://www.feishu.cn/hc/zh-CN/articles/725304182725

## Gmail side (official endpoints for the ingestion side)

- Search: `GET users/me/messages?q=<gmail query>` e.g. `subject:"104應徵履歷" -label:104/已匯入` (Gmail search-box syntax; not available under gmail.metadata scope).
- Label modify: `POST users/me/messages/{id}/modify` body `{"addLabelIds":[...]}`; `batchModify` up to 1000 ids.
- Push: `watch` → Cloud Pub/Sub → webhook → `history.list` from startHistoryId. Overkill for MVP — 1–5 min polling is simpler and resume-emails are not second-critical.
- Apps Script alternative (zero server): `GmailApp.search(query)` + `thread.addLabel(label)`; triggers on time interval.

## Data-consistency rules

1. **Write-then-mark ordering**: read Gmail → parse → search Base by message_id → create if absent → verify create (read back) → THEN add Gmail「已匯入」label. Never label first, then write — a failed write silently drops the candidate.
2. **Parse-failure path**: write to「待人工確認」+ a 格式異常 Gmail label; never silently drop; never mark as normal processed.
3. **Dedup key = Gmail message ID**, not 姓名 or 姓名+職位 (same person re-applies, forwarded mail, same-name different people, multi-position all collide on name-based keys).
4. One worker writes; retry re-queries before re-create.

Suggested table fields: 應徵者姓名(text), 應徵職位(text), 處理狀態(single select 已匯入/待人工確認/處理失敗), Gmail Message ID(text, dedup key), Gmail Thread ID(text), Gmail 連結(hyperlink), 原始主旨(multi-line text), 處理時間(datetime), 錯誤原因(multi-line text). 職缺分類 — keep as spare field + full original subject; don't silently discard.

## 104 主旨 parsing (rule-based, no AI)

Format: `104應徵履歷【【職缺分類】應徵職位】應徵者姓名(所在地)`
1. prefix check `104應徵履歷`
2. take 2nd-level `【...】` content; split on first `】` → 職缺分類 / 應徵職位
3. text after last `】` before `(` = 姓名; strip whitespace
4. malformed → 待人工確認

Example: `104應徵履歷【【AI Agent】AI Agent 工程師｜自媒體自動化】張哲鋼(台北)` → 分類=AI Agent, 職位=AI Agent 工程師｜自媒體自動化, 姓名=張哲鋼.

## Label scheme

`104/待處理` (Gmail filter lands new mail here), `104/已匯入`, `104/待人工確認`, `104/處理失敗`. Poll query: `label:104/待處理`.

## Architecture options

| Option | Speed | Control | Cost | Verdict |
|---|---|---|---|---|
| **Lark AnyCross（國際版）** | fast | mid | included | **first choice for 國際版 (2026-08-06)** — official Gmail→Base template confirmed; 5-min poll; verify message ID/subject/label nodes in a small PoC before committing |
| Native Feishu 自動化（中國版） | fastest | low | low–unknown | verify in tenant first; don't bet on it |
| Make / Zapier | fast | mid | per-task/subscription | good MVP; Zapier has Gmail→Lark "Create New Base Table Record" |
| n8n | mid | high | self-host | best fit when engineering resources exist; Gmail node covers trigger/message/label |
| Custom Python service | mid–slow | highest | maintenance | long-term; poll every 1–5 min, no Pub/Sub for MVP |

## Tenant verification checklist (docs cannot confirm these)

- 中國版飛書 (open.feishu.cn) vs 國際版 Lark (open.larksuite.com)
- Connector center: does Gmail appear? new-mail trigger? message ID exposed? label write?
- Base: app_token (from URL or wiki get_node), table_id, actual field names, app added as collaborator, advanced permissions off
- Automation version supports webhook trigger + HTTP action
- Admin allows third-party account authorization
