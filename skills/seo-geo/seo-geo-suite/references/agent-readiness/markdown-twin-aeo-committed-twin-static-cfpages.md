# Committed-Twin 變體（純靜態站 CF Pages）— 實例：your-course-landing

有別於 SKILL.md 的 runtime HTML→MD 轉換變體（your-project），純靜態站可直接採用
**committed twin**：把 `.md` 鏡像當 build 產物 commit，CF Pages 自行伺服檔案，
`_middleware.js` 只做 header 注入，不需要 AI_UA 判斷與 htmlToMarkdown。

## 適用判斷

- 站是純靜態產生（Hugo / 手工 HTML / build 時直接吐 md），不是 SPA。
- 內容節奏慢（landing / 招生頁），twin 更新頻率可接受。
- 希望少寫 code、全程靠既有檔案伺服，metadata 由 middleware 統一加。

## 檔案布局

```
public/
  index.md            ← 首頁 markdown 鏡像（手工或 build 產出，commit）
  llms.txt            ← 輕量目錄
  llms-full.txt       ← 完整知識語料庫
  sitemap.md          ← sitemap markdown 版
  sitemap.xml
  robots.txt          ← 明確 Allow AI crawlers (GPTBot/ChatGPT-User/OAI-SearchBot/
                        ClaudeBot/Claude-Web/anthropic-ai/Google-Extended/
                        GoogleOther/PerplexityBot/Applebot/Applebot-Extended/cohere-ai)
functions/_middleware.js
```

## `_middleware.js`（只加 header，不轉換內容）

```js
// 對 HTML 回應附加 Link alternate 廣告 twin，並宣告 Vary（防 CDN 快取錯格式）
export async function onRequest(context) {
  const res = await context.next();
  const type = res.headers.get('content-type') || '';
  if (type.includes('text/markdown')) return res;   // twin 本身不再加 Link
  const url = new URL(context.request.url);
  // '/' 對應 /index.md（切勿拼成 "{origin}.md"）
  const twin = (url.pathname === '/' ? '/index' : url.pathname) + '.md';
  res.headers.set('Link',
    `<${url.origin}${twin}>; rel="alternate"; type="text/markdown"`);
  res.headers.set('Vary', 'Accept, User-Agent');
  return res;
}
```

註：純靜態站不設 AI_UA → 回 md 的邏輯——`Accept: text/markdown` 由 CF Pages 對
`.md` 檔自動按 Content-Type 伺服；middleware 只補 Link/Vary。

## 實作陷阱

1. **Link header 只加在 HTML 回應**：若對 `.md` 回應也加，會出現 self-referential
   alternate（`index.md → index.md.md`）。以 `content-type` 判斷避開。
2. **`/` 對應 `/index.md`**：`pathname==='/' ? '/index' : pathname`，否則會拼成
   `https://origin.md`（整串變域名）。
3. **每頁都要有對應 `.md`**：缺檔時 Link 指向 404 → 驗證時逐頁 curl 確認。
4. **內容同步**：HTML 動了 twin 沒動 → AI 與使用者看到不一致。改為 build 時從
   同一內容源生成 html + md，或列為人工同步事項。

## 驗證（production curl 全端點 200 即 pass）

```bash
curl -sI https://site/ | grep -i '^link'          # 有 Link alternate
curl -sI https://site/ | grep -i '^vary'          # Accept, User-Agent
curl -s -A "GPTBot/1.0" https://site/ | head -c 200  # AI UA 正常拿內容
curl -s https://site/index.md | head -c 200       # twin 直讀
curl -s https://site/llms.txt | head -c 200
curl -s https://site/llms-full.txt | head -c 200
curl -s https://site/sitemap.md | head -c 200
curl -s https://site/sitemap.xml
curl -s https://site/robots.txt                    # AI crawler Allow 存在
```
