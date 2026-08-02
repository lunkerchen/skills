---
name: hono-workers-testing
description: Test Hono/Workers backends - vitest, D1 mock, execCtx.
---

# Hono / Cloudflare Workers Testing Patterns

適用於 Hono + Cloudflare Workers 的 backend（如 your-project 的 `backend-api/`，Cloudflare Pages + D1 + R2）。
Dev/test 指令：`cd backend-api && npm run dev`、`npx vitest run`、`npx tsc --noEmit`。

## 測試基建

- `test/mockDb.ts` — 輕量 D1 mock（async prepared statement API：`prepare().bind().run()/first()/all()`）。
  支援 `INSERT INTO t (cols) VALUES (?)`、`UPDATE t SET ... WHERE col = ?`、`SELECT ... WHERE col = ?`、
  `DELETE FROM t WHERE col = ?`。**不支援**聚合（COUNT 回 `{changes:0}`）、JOIN、複雜 WHERE。
  `resetMockDb({ users, listings, listing_images, ... })` 每測試重設。
- `test/helpers.ts` — `makeToken(user)`（async，JWT）、`makeEnv(db)`（AppEnv，含 JWT_SECRET 等）、`ORIGIN_HEADER`。
- 測 router 前先 mount：`app.route('/api/listings', listingsRouter)`；`app.onError((err, c) => c.json({detail, stack}, 500))` 讓 500 有 body 可查。

## Pitfall: Hono 測試沒有 ExecutionContext（必踩）

`app.request(path, init, env)` 在測試環境沒有 ExecutionContext。Handler 只要呼叫
`c.executionCtx.waitUntil()`（如 `queueTelegramNotification`）就會炸：

```
Error: This context has no ExecutionContext
```

**Fix:** 改用 `app.fetch` 並注入 fake executionCtx：

```ts
const fakeExecutionCtx = {
  waitUntil: () => {},
  passThroughOnException: () => {},
} as any

function send(method: string, path: string, token: string | null, body?: any) {
  const headers: Record<string, string> = { ...ORIGIN_HEADER }
  if (token) headers['Authorization'] = `Bearer ${token}`
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  return app.fetch(new Request(`https://your-app.example.com${path}`, {
    method, headers, body: body !== undefined ? JSON.stringify(body) : undefined,
  }), makeEnv(mockDb), fakeExecutionCtx)
}
```

真實 Workers 一定有 executionCtx — 這是測試基建缺口，不是生產 bug。

## Pitfall: mockDb 對未 seed 的表會 throw

`mockDb.getTable()` 遇到未 seed 的表（`featured_listings`、`conversations`…）會 throw `unknown table`，
導致 GET detail 這類查詢多張表的端點測試炸掉。**Fix:** 把 `getTable` 改成未知表 auto-create 空表：

```ts
private getTable(name: string): MockTable {
  let t = tables.get(name)
  if (!t) { t = { name, rows: [], columns: new Set<string>() }; tables.set(name, t) }
  return t
}
```

## Pitfall: mockDb seed 淺拷貝 → 測試順序污染（最難抓的一類）

`resetMockDb` 的 `mk()` 用 `rows: [...rows]` **淺拷貝** — seed 物件是共享引用。
前面的測試若跑 `UPDATE`（例如 PATCH 把 listing 改成 inactive），會直接突變 module-level
的 seed 常數；後面的測試即使重新 `resetMockDb({ listings: [sellListing] })`，拿到的還是
已被改過的物件（`status: 'inactive'`），guard 條件失靈。

**症狀特徵**：`npx vitest run <file> -t "<test名>"` 單獨跑 PASS；整檔跑 FAIL。
**診斷**：用 `-t` 逐 describe 隔離，找出哪個先前測試造成污染；在懷疑的測試裡直接
`mockDb.prepare('SELECT * FROM listings WHERE id = ?').bind(id).first()` 印出 seed 狀態
比對預期值（實例：status 從 active 被前一測試改成 inactive）。
**Fix（根因，一行）**：mock 的 `mk()` 改深拷貝：
`const copies = rows.map((r) => structuredClone(r))` — 一勞永逸，後續測試不需防禦性寫法。
完整復現流程見 `references/mockdb-seed-mutation.md`。

## FormData / 圖片上傳測試

```ts
function uploadFormData(listingId: string, token: string) {
  const fd = new FormData()
  const jpg = new File([new Uint8Array([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10])], 'a.jpg', { type: 'image/jpeg' })
  fd.append('files', jpg)
  fd.append('thumbs', jpg)
  return app.fetch(new Request(`https://your-app.example.com/api/upload/${listingId}`, {
    method: 'POST', headers: { Authorization: `Bearer ${token}`, ...ORIGIN_HEADER }, body: fd,
  }), makeEnvWithUploads(mockDb), fakeExecutionCtx)
}
```

- JPEG magic bytes `[0xFF, 0xD8, 0xFF]` 才能過後端 magic-byte 驗證。
- **`makeEnv` 的 `UPLOADS` 是 `{}`** — 測上傳要覆蓋成 `{ put: async () => {} }`（`env.UPLOADS = { put: async () => {} }`）。
- **upload 回應不含 image id**（只回 `{url, thumbnail, sort_order}`）— 要刪圖/改序時，先 `GET /api/listings/:id` 從 `images[].id` 拿。
- 測試檔放 `test/<feature>.test.ts`，`makeToken` 是 async — 用 top-level await 或 beforeAll 造 token。

## 狀態機強制模式（兩階段發布）

C2C 上架「至少一張圖」類的業務規則，若 create 即公開、圖片後補，前端擋會被 API 繞過。
用既有 CHECK constraint 的狀態（如 `draft`）做兩階段，**先看 schema 約束再決定要不要 migration**：

1. `POST /listings`（sell）→ `status='draft'`；`GET /:id` 對 draft 非 owner → 404（防洩漏）
2. `POST /upload/:id` 首圖成功 → `draft → active`，**通知（Telegram/wishlist）移到這裡才發**
3. `DELETE /upload/:id/images/:img` 刪到 0 圖 → 退回 `draft`
4. `PATCH /:id` 想轉 active 但無圖 → 400
5. 前端 submit 同步擋（sell 零圖 → error），編輯頁要計入既有圖（`item.images.length + 新圖數`）
6. 搜尋/列表 SQL 通常只查 `status='active'` — draft 自動不可見，檢查確認即可

測試案例清單（見 brick-loop `backend-api/test/listings-image-required.test.ts`）：draft 建立 / 豁免類型（seek 無圖需求）/
owner-only 可見 / 上圖轉 active / PATCH 阻擋 / 刪圖退回。

**輕量守衛替代方案**（不想動 create/通知流程時）：不引入 draft 兩階段，直接
① 前端 submit 擋（sell 零圖 → error）② `PATCH` 轉 `active` 時查 `listing_images` 無圖 → 400
③ `DELETE` 最後一張圖時，active sell 拒絕 → 400。誠實的代價：create 端點本身無法檢查
（圖在 create 之後才上傳，upload endpoint 需要 listing_id），直接打 API 仍可建立無圖 active
商品 — 守衛是事後不變式，不是發布門檻。要真正伺服器端封死，還是得走上面的 draft 兩階段。
實作參考：brick-loop `src/routes/listings.ts`（PATCH guard）+ `src/routes/upload.ts`（DELETE guard）。

## 驗證流程

改完跑：`npx vitest run`（全量，確認無 regression）+ `npx tsc --noEmit`（backend + frontend）。
`vitest run` 失敗時看 `~/Library/Application Support/rtk/tee/*_vitest_run.log`（JSON reporter）。
- 若 `tsc --noEmit` 報錯但看似與本次變更無關：先 `git stash && npx tsc --noEmit && git stash pop`
  證明是 HEAD 既有錯誤再決定是否順手修（RULES 綠燈允許修 bug；修完重跑驗證）。
