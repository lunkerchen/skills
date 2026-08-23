# Pitfalls

1. **block 換行先於標題轉換 → 標題的 `#` 消失**：先跑 `.replace(/<(h[1-6]|p|li|...)[^>]*>/gi, '\n')` 會把 `<h1>` 開頭 tag 換成換行，後續 heading regex 匹配不到。順序：heading/li 轉換 → block 換行 → inline 轉換。
2. **漏 import 輔助函數 → CF Pages error 1101（500）**：middleware import 只帶了 `markdownResponse` 漏 `markdown404`，未知路由 + AI UA 時 TypeError → 500。production 驗證必測：`curl -A "GPTBot/1.0" <url>/random-missing-xyz` 應 404 非 500。
3. **首頁 Link header 域名錯誤**：`pathname === '/' ? '' : pathname` 接上 `.md` 會生出 `https://your-app.example.com.md`（整串變域名）。`/` 要對應 `/index` → `https://your-app.example.com/index.md`。HTML response 與 markdown response 都要處理。
4. **sitemap.md 被 twin 分支攔截**：`/sitemap.md` 經 stripMarkdownExt → `/sitemap`（非 known public）→ 誤回 404。在 markdown 分支前對 `/sitemap.md` `return next()` 放行給獨立 function。
5. **測試斷言用 `includes()` 不用 regex**：markdown 字串含 `[text](url)`，寫 `assert.match(md, /\[...\]\(...\)/)` 在 patch 工具下會踩 `\/` 雙重轉義陷阱。`assert.ok(md.includes('[text](url)'))` 更穩。
6. **Vary 要含 User-Agent**：只設 `Vary: Accept` 時，AI UA 與瀏覽器共用快取會互相污染；`Vary: Accept, User-Agent`。
