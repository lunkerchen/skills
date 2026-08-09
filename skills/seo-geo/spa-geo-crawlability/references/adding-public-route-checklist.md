# 新增公開 SPA 路由到 Edge SEO Pipeline — 逐檔清單（2026-08-04 / your-project /changelog 實例）

情境：既有 SPA 已有 edge SEO pipeline（`_middleware.js` + `seo.js` + `content.js` + `sitemap.xml.js`），要把一個新公開頁面（如 `/changelog`，UI 已存在於 `App.tsx`）加入可被抓取的公開路由。

## 逐檔步驟

| 檔案 | 改什麼 | 驗證 |
|---|---|---|
| `functions/sitemap.xml.js` | `PROFILES.<name>.staticPaths` 加 `'/changelog'` | sitemap 測試 assert `/changelog` URL |
| `functions/seo.js` | `PUBLIC_ROUTES['/changelog']` 加 `{ title, description }`（繁中、含站名、不設 noindex） | seo 測試 assert title + canonical + robots `index,follow` |
| `functions/content.js` | 加 `CHANGELOG_ENTRIES` + `changelogHtml()`（語意化 `<h1>`、摘要 `<p>`、每筆 `<article><h2>版本</h2><ul>`）+ 註冊 `CONTENT_MAP['/changelog']` | content 測試 assert h1/摘要/article 數 |
| `functions/content.test.js` | （可新增）最小測試 | `node --test` 全綠 |
| `_middleware.js` | **通常不動**（見下） | 端到端 smoke test |

## PRERENDERED_ROUTES 判定（關鍵決策）

- `PRERENDERED_ROUTES` 只 gate **建置期產生的靜態 HTML assets**（如 `guides/*/index.html`，由 generator 產生）
- 純 SPA 路由（`/changelog`）在 `public/` **沒有**自己的 `index.html` → 走 `resolveSeo` → SPA fallback 路徑，middleware 自動注入 SEO
- 判定問題：「該 route 在 `public/` 是否有建置產生的 `index.html`？」沒有 → 不需要進 `PRERENDERED_ROUTES`，別動 middleware
- 事後確認法：直接跑 middleware smoke test，若 200 + `index,follow` + title 注入成功，即證明不需改

## 不 deploy 的端到端驗證（本 session 實測通過）

```bash
# 1) 單元測試（既有 pattern：node --test functions/*.test.js）
cd frontend && node --test functions/*.test.js

# 2) prerender 內容 smoke test
node -e "import('./functions/content.js').then(m => {
  const h = m.getPrerenderedContent('/changelog');
  console.log('articles:', (h.match(/<article>/g)||[]).length);
})"

# 3) middleware 端到端：mock Request + ASSETS env，不 deploy 就驗到 SEO 注入
node -e "import('./functions/_middleware.js').then(async m => {
  const resp = await m.onRequest({
    request: new Request('https://your-app.example.com/changelog'),
    next: async () => new Response('asset'),
    env: { ASSETS: { fetch: async () => new Response('<html><head><title>x</title></head><body></body></html>', { headers: { 'content-type': 'text/html' } }) } },
  });
  const html = await resp.text();
  console.log(resp.status, resp.headers.get('x-robots-tag'), html.includes('更新說明'));
})"
```

3 的 mock 手法：`next` 回傳 asset response、`env.ASSETS.fetch` 回傳假 index.html —— 因為 middleware 只讀 ASSETS 拿 shell 再注入，不需要真部署。

## 驗收清單

- [ ] 寫檔前對每個檔案跑 `$HERMES_HOME/hooks/run-hook.sh pre-write <path>`（exit != 0 = abort）
- [ ] `node --test functions/*.test.js` 全綠（既有 + 新增）
- [ ] `git diff --check` clean
- [ ] middleware smoke test：200 / index,follow / title 注入
- [ ] 未 commit、未 deploy、未動不相關檔案（除非任務要求）

## 實例：/changelog（your-project 2026-08-04）

- 資料源：`src/data/changelog.ts` 的 `changelogEntries`（5 筆，最新「開發版 2026.07.18」）
- 內聯進 `content.js` 的 `CHANGELOG_ENTRIES`，逐字同步 + 頂端註解標來源
- 改動 6 檔：`sitemap.xml.js`、`seo.js`、`content.js`、`content.test.js`(new)、`seo.test.js`、`sitemap.test.js`
- 結果：13/13 tests pass；middleware smoke 驗到 200 + index,follow + 「更新說明｜your-project your-marketplace」注入
