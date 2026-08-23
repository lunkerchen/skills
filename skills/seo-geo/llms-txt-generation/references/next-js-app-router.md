# 動態生成（Next.js App Router 模式）

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
