---
name: llms-txt-generation
description: Use when 建/修 llms.txt 或查 GEO 可見性。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [seo, geo, llms-txt, nextjs, ssg, content-site]
---

# llms.txt 生成與維護

## 核心原則：靜態 llms.txt 註定過時

手寫的 `public/llms.txt` 只更新一次就爛 — 部落格持續增長後，AI 引擎（ChatGPT/Perplexity/GEO 評估）看到的內容會落後實際發布內容，落差可達一半（實測 yotron-ai.com：llms.txt 列 33 篇、實際 published 65 篇）。**任何有內容管線的站，llms.txt 都應該從內容集合動態生成。**

## 動態生成（Next.js App Router 模式）

### 1. `app/llms.txt/route.ts`（輕量級導航與模組大綱）
`app/llms.txt/route.ts` + 刪掉 `public/llms.txt`（避免 route 衝突）：

```ts
import { getAllPosts } from "@/lib/mdx";
// ... 其他內容 API：cases/glossary/insights/topics/pricing

export const dynamic = "force-static"; // build 時快取，不每請求重跑

export async function GET() {
  const lines: string[] = [];
  const push = (s = "") => lines.push(s);
  push("# 公司名（品牌）");
  push("");
  push("> 一句話定位"); // 第一段就要說清楚品牌 Entity
  push("");
  // ── 服務頁面 ──
  push("## 服務頁面");
  // 逐頁帶描述，例如：- [SEO](https://...)：一行說明
  push("");
  // ── 主題 Hub ──
  // ── 部落格（依 category 分組）──
  const categories = [...new Set(posts.map((p) => p.category).filter(Boolean))];
  for (const cat of categories) {
    push(`### ${CATEGORY_NAMES[cat] ?? cat}（${posts.filter(p => p.category === cat).length} 篇）`);
    for (const post of posts.filter((p) => p.category === cat)) {
      push(`- [${post.title}](https://.../blog/${post.slug})`);
      if (post.description) push(`  ${post.description}`);
    }
    push("");
  }
  // ── 案例 / 術語表 / Insights / Newsroom ──
  // ── 聯絡：電話、Email、地址、服務時間 ──
  return new Response(lines.join("\n").trimEnd() + "\n", {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
```

### 2. `app/llms-full.txt/route.ts`（全站完整知識語料庫）
提供單檔全站上下文，將核心服務深度說明、技術架構、案例成效數據與常見問答 (FAQ) 整合為單一 Markdown 文件，供 AI Agent 在單次 Context 注入時直接全面理解品牌體系。

完整實作範例見 `references/yotron-llms-route.md`（含分類名對應、區塊結構、驗證數字）。

## 檢查清單（audit 或驗收時）

- **link 數 vs published 數**：`curl -s https://site/llms.txt | grep -c '/blog/'` 對比 `ls content/blog/*.mdx | wc -l`（要扣掉 published:false）
- **unpublished 零洩漏**：grep llms.txt 是否包含任何 `published: false` 文章的 slug — 不該出現
- **各類型都有**：blog/cases/glossary/insights/topics/catalog 逐類 count，缺類別 = 內容管線有洞
- **聯絡資訊完整**：電話、Email、地址、服務時間（LocalBusiness 訊號）
- **Content-Type**：`text/plain; charset=utf-8`

## 陷阱

1. **route 路徑 import 陷阱**：`app/llms.txt/route.ts` 是子目錄，import 站內模組要用 `../`（如 `../insights/[slug]/_data`），`./` 會 TS 報找不到模組。
2. **別保留 public/llms.txt**：與 app route 同路徑衝突，刪掉靜態檔。
3. **published:false 洩漏**：llms.txt 生成要用 `getAllPosts()`（已過濾 published），不要用不過濾的 getBySlug 路徑手動拼。
4. **分類名要對齊 topics hub**：blog category 值（如 `seo-geo`）與 hub 頁 slug 一致時，llms.txt 的分節名稱可直接重用 hub 名稱。
5. **GEO 審計三件套一起驗**：llms.txt、robots.txt（AI crawler Allow）、sitemap。

## 驗證（build 後）

```bash
ls .next/server/app/llms.txt.body  # Next.js build 產物，直接讀內容檢查
node -e "const f=require('fs').readFileSync('.next/server/app/llms.txt.body','utf8');console.log((f.match(/\/blog\//g)||[]).length)"
```
