# 檢查清單（audit 或驗收時）

- **link 數 vs published 數**：`curl -s https://site/llms.txt | grep -c '/blog/'` 對比 `ls content/blog/*.mdx | wc -l`（要扣掉 published:false）
- **unpublished 零洩漏**：grep llms.txt 是否包含任何 `published: false` 文章的 slug — 不該出現
- **各類型都有**：blog/cases/glossary/insights/topics/catalog 逐類 count，缺類別 = 內容管線有洞
- **聯絡資訊完整**：電話、Email、地址、服務時間（LocalBusiness 訊號）
- **Content-Type**：`text/plain; charset=utf-8`


### Is-Agentic 必備檢查項
- [ ] 必須包含 `## When to use this site (Agent instructions / 給 AI Agent 的使用指引)` 區塊。
- [ ] 明確陳述 Agent 觸發情境、適合回答的查詢、不適合的查詢、定價與客服閉環導引。
- [ ] 標頭必須支援 `Accept: text/markdown` 與 `Vary: Accept, Accept-Encoding`。
