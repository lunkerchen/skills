# Edge SEO Pipeline — Deploy 與 Production 驗證（2026-08-04 / your-project /changelog 實例）

情境：edge SEO pipeline（`_middleware.js` + `seo.js` + `content.js`）已實作並通過單元測試後，要 deploy 到 Cloudflare Pages 並驗證 production 真的吃到 prerender。內容與 `adding-public-route-checklist.md` 的「不 deploy 的端到端驗證」互補：那份驗證 local，這份驗證 production。

## Deploy（含 Functions 的專案）

**從 `frontend/` 用 project-aware Pages deploy；不要從 repo root 用 positional `dist/`。**

```bash
cd frontend && npm run build && wrangler pages deploy --project-name=<name> --branch main
```

- positional `dist/`（`wrangler pages deploy dist/`）不會把 `functions/` 一起上傳 → prerender/SEO 靜默失效：頁面還是 200，但 raw HTML 沒有注入正文。這是**最難抓的失敗模式**：功能上完全看不出錯，只有 curl raw HTML 才發現
- 舊 repo root deploy script 若寫死 positional 路徑，要改用 frontend 目錄的 project-aware 呼叫

## Production 雙層驗證（crawler + user）

```bash
# 1) crawler 層：raw HTML 要有注入正文（h1/摘要/articles），不是空殼
curl -s https://<domain>/changelog | grep -c '<h1'       # 1
curl -s https://<domain>/changelog | grep -c '<article>' # = 更新筆數
curl -s https://<domain>/changelog | grep -o '<title>[^<]*</title>'
# 2) sitemap 收錄
curl -s https://<domain>/sitemap.xml | grep -c '/changelog'  # 1
# 3) API health（若有獨立 Worker）
curl -s https://<worker>/api/health
# 4) user 層：browser_navigate + browser_snapshot 確認 hydration 後 h1、每筆 article、
#    footer 連結、無水平溢位；browser_console 檢查無 JS error
```

## 踩坑

- **Preview hash URL 短暫 404（deployment propagation）**：剛 deploy 完 `https://<hash>.<project>.pages.dev/<route>` 第一次 smoke 可能 404，稍後重試即 200；custom domain 通常先恢復。production 驗證以 custom domain 為準，preview 404 不要立刻宣告失敗，retry 一次再判斷
- **未追蹤檔不要納入 commit**：deploy 後 `git log -1 --oneline` + `git diff HEAD^ HEAD --check` + `git status --short --untracked-files=all`，確認無漏 stage、無多包（scratchpad/工具目錄的 untracked 檔放著即可）
