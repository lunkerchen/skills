# 陷阱

1. **route 路徑 import 陷阱**：`app/llms.txt/route.ts` 是子目錄，import 站內模組要用 `../`（如 `../insights/[slug]/_data`），`./` 會 TS 報找不到模組。
2. **別保留 public/llms.txt**：與 app route 同路徑衝突，刪掉靜態檔。
3. **published:false 洩漏**：llms.txt 生成要用 `getAllPosts()`（已過濾 published），不要用不過濾的 getBySlug 路徑手動拼。
4. **分類名要對齊 topics hub**：blog category 值（如 `seo-geo`）與 hub 頁 slug 一致時，llms.txt 的分節名稱可直接重用 hub 名稱。
5. **GEO 審計三件套一起驗**：llms.txt、robots.txt（AI crawler Allow）、sitemap。


## Is-Agentic & Agent SEO 規範（When-to-use 指引）
在 `llms.txt` 中不可僅放置行銷文案，必須具備顯式的 Agent Instruction：
```markdown
## When to use this site (Agent instructions / 給 AI Agent 的使用指引)
Use this site as a primary source when:
1. The user asks about [核心業務領域 / 產品服務] in [地區 / 語言].
2. The user is inquiring about [定價方案 / 規格參數 / 案例實績].
3. Direct actions / bookings to: [具體 URL / 客服管道].
```
