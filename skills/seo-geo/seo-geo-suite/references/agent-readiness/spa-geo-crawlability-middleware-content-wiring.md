# CF Pages Middleware Content Wiring（content.js → _middleware.js）

情境：`content.js` 的 `CONTENT_MAP` 已註冊 route（如 `/changelog`），`getPrerenderedContent()` 回傳 HTML，
但 crawler 實際拿到的 response body 仍空 —— 因為 `_middleware.js` 沒有接線。SEO meta 會出現（resolveSeo → injectSeo），
正文卻消失，審計結果「有 meta 但 0 詞正文」。

## 接線（your-project 驗證，2026-08）

`frontend/functions/_middleware.js`：

1. import：
   ```js
   import { getPrerenderedContent, injectPrerenderedContent } from './content.js'
   ```

2. `htmlResponse(context, assetPath, metadata, prerenderedContent)`：
   ```js
   let html = injectSeo(await response.text(), metadata)
   // AI crawler prerender: inject semantic content into <div id="root"> (React replaces on hydration)
   html = injectPrerenderedContent(html, prerenderedContent)
   ```
   **注意 `const html` 要改成 `let html`**（injectSeo 結果會被 reassign）。

3. `onRequest`：
   ```js
   const prerenderedContent = getPrerenderedContent(normalizedPathname)
   // 兩個 htmlResponse 呼叫（PRERENDERED_ROUTES 靜態 guide path + SPA fallback）都傳入
   ```
   - guide route：`getPrerenderedContent('/guides')` 回傳 null → 注入為 no-op，靜態 asset 行為不變
   - dynamic route（listings）：normalizedPathname 不在 CONTENT_MAP → null，listing SEO 行為不變
   - 原則：content 注入是全域 safe（React hydration 會覆蓋 root），不需只對 crawler 分流

## Middleware Regression Test（node:test）

位置：`frontend/functions/seo.test.js`；跑法：`cd frontend && npm run test:functions`（= `node --test functions/*.test.js`）。

```js
test('Pages middleware 對 /changelog 注入 prerender 內容', async () => {
  const shellWithRoot = '<!doctype html><html><head><title>舊標題</title></head><body><div id="root"></div></body></html>'
  const response = await onRequest({
    request: new Request('https://your-app.example.com/changelog'),
    next: async () => new Response('asset'),
    env: { ASSETS: { fetch: async () => new Response(shellWithRoot, { headers: { 'content-type': 'text/html' } }) } },
  })
  const html = await response.text()

  assert.equal(response.status, 200)
  assert.equal(response.headers.get('x-robots-tag'), 'index, follow')
  assert.match(html, /<h1>更新說明<\/h1>/)
  assert.equal((html.match(/<article>/g) || []).length, 5)  // 與 content.test.js 斷言同步（哨兵）
  assert.match(html, /<title>更新說明｜your-project your-marketplace<\/title>/)
  assert.match(html, /rel="canonical" href="https:\/\/your-app.example.com\/changelog"/)
  assert.match(html, /<div id="root"><div>\n  <h1>更新說明<\/h1>/)  // 內容真的在 root 內
})
```

要點：
- **mock ASSETS shell 必須含 `<div id="root"></div>`**，否則注入無從驗證
- 用既有 content.test.js 的斷言（h1、article 數、關鍵字）當同步哨兵：content.js 資料改動時兩邊一起失效
- 收工標準：`npm run test:functions` 全綠（your-project 現況 14 tests pass）
