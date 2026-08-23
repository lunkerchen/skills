# mockDb seed 淺拷貝 → 測試順序污染（完整復現）

來源：brick-loop `listings-image-required.test.ts` 開發中踩到（2026-08）。

## 症狀

新測試檔 7 個測試：6 PASS、1 FAIL（"拒絕刪除上架中出售商品的最後一張照片"，
expected 400 got 200）。但單獨跑那一個測試（`vitest run -t`）PASS，`-t "刪除照片"`
跑整個 describe 也 PASS — 只有整檔跑才 FAIL。

## 污染鏈

1. 測試檔 module-level 共享 seed 常數：`const sellListing = { ..., status: 'active', ... }`。
2. `beforeEach` / `it` 內都呼叫 `resetMockDb({ listings: [sellListing], ... })`。
3. `resetMockDb` 的 `mk()`：`rows: [...rows]` — **淺拷貝**，陣列是新的、物件是共享的。
4. 前面 describe 的 PATCH 測試跑 `UPDATE listings SET status = 'inactive' WHERE id = ?`，
   mock 直接 `row[col] = val` 突變共享物件 → module-level `sellListing.status` 變成 `'inactive'`。
5. 後面 DELETE 測試重新 seed 同一個（已被污染的）物件 → guard 條件
   `listing.status === 'active'` 為 false → 守衛沒觸發 → delete 成功 → 200。

## 診斷路徑（照做即可）

```bash
# 1. 先確認是順序問題：單獨跑 PASS、整檔跑 FAIL
npx vitest run test/<file>.test.ts -t "<失敗測試名>"   # PASS
npx vitest run test/<file>.test.ts                      # FAIL

# 2. 逐 describe 隔離，收窄污染源
npx vitest run test/<file>.test.ts -t "<describe關鍵字>"

# 3. 在失敗測試的 request 前直接查 mock 狀態，印出實際值
const listing = await mockDb.prepare('SELECT * FROM listings WHERE id = ?').bind(id).first() as any
console.log('PRE listing:', JSON.stringify(listing))
```

實例輸出：`PRE listing: {"id":"listing-sell", ..., "status":"inactive"}` — 明明剛 seed
`status: 'active'`，值卻被前一測試改掉。

## Fix（根因）

mock 的 `mk()` 深拷貝 seed 列，一勞永逸：

```ts
const mk = (name: string, rows: Row[] = []) => {
  const copies = rows.map((r) => structuredClone(r))
  tables.set(name, { name, rows: copies, columns: new Set(copies.flatMap((r) => Object.keys(r))) })
}
```

- `structuredClone` 對純資料 seed（plain objects/arrays）安全；seed 含 function 時不可用。
- 修 mock 而非改測試：改測試只是換一個不共享的寫法，下次新測試還是會踩同一個坑。

## 通用教訓

- 手寫 DB mock 的 `reset()` 用淺拷貝 = 時間炸彈；測試基建的 seed 一律深拷貝。
- vitest 測試「單獨 PASS、整檔 FAIL」第一優先懷疑共享可變狀態，不是測試邏輯本身。
- module-level seed 常數是污染源 — 修基建，不要只修當下測試。
