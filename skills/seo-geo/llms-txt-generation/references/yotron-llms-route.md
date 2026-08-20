# yotron-ai.com llms.txt 動態 route 實作（2026-08-15）

優創官網（yotron-website, Next 16.2.3 App Router）實作紀錄 — 把過時的靜態 `public/llms.txt`（33 篇 blog）改成動態 route handler，build 後 65 篇全進、unpublished 零洩漏。

## 檔案位置

- `app/llms.txt/route.ts` — 動態生成
- `public/llms.txt` — **已刪除**（避免與 app route 同路徑衝突）
- 驗證產物：`.next/server/app/llms.txt.body`

## 資料 API（依內容集合自動更新）

| 內容 | API | 數量（2026-08） |
|------|-----|------|
| Blog（已過濾 published） | `getAllPosts()` from `@/lib/mdx` | 65 |
| 服務型錄 | `PRICING_SERVICES` from `@/lib/pricing` | 7 |
| 主題 Hub | `TOPICS` from `@/lib/topics` | 6 |
| 成功案例 | `getAllCases()` | 6 |
| Insights 月報 | `getAllIssues()` from `../insights/[slug]/_data` | 17 |
| 術語表 | `getAllGlossaryTerms()` from `@/lib/glossary` | 25 |
| Newsroom | `getAllNewsroom()` | 5 |

## 分類名對應（blog category → 中文分節名）

```
seo-geo: SEO / GEO 搜尋能見度
ai-implementation: AI 導入實戰
ai-video: AI 影片製作
automation: 流程自動化
line-ai: LINE AI 客服
industry-guide: 產業 AI 指南
ai-business: AI 商業應用（無 hub 頁，仍列為分節）
```

分類顯示順序用 `CATEGORY_ORDER` 控制，未列出的依字母序。

## 關鍵實作細節

1. `export const dynamic = "force-static"` — build 時 prerender，內容新增後重 build 自動更新，不每請求重跑。
2. 每篇文章帶 `description` 當第二行（AI 引用時可拿來摘要）。
3. 每節標題帶篇數（如「AI 導入實戰（19 篇）」）— 數量是 GEO 權威訊號。
4. 聯絡區保留電話/Email/地址/服務時間（LocalBusiness 訊號）。

## 驗收數字（live）

```
curl -s https://yotron-ai.com/llms.txt
blog: 65 | catalog: 7 | topics: 6 | cases: 6 | insights: 17 | glossary: 25 | newsroom: 5
unpublished leak (sop-standardization-guide): false
lines: 309
```

## 注意

- `getAllPosts()` 已過濾 `published: false`（11 篇隱藏文不會進 llms.txt），但 `getPostBySlug()` **不過濾** — hidden 文章直連仍 200 且無 noindex，是獨立 P1 待修（generateMetadata 加 `robots: { index: false }`）。
- 部署走 Zeabur auto-deploy on push，驗證 live 要等約 10 分鐘，可用 `gh api repos/yotron-ai/yotron-website/deployments` 查 deployment 建立時間再決定等多久。
