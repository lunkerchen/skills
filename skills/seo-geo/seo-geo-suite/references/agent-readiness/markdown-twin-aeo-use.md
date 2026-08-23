# Use

觸發時機：`npx -y @vercel/agent-readability audit <url>` 的「Can agents read you?」區塊 ✗ 任何 markdown 項目（Agent UA → markdown、.md URL、Accept header、Link alternate、Vary、Frontmatter、Missing page → markdown）；或使用者要求「讓 AI agent 讀得懂網站 / markdown mirror / content negotiation」。

**類別**：AEO（Answer Engine Optimization）的技術實作層。同 URL 依請求端回 HTML 或 markdown，讓 coding agents（Claude Code/Cursor/OpenCode）與 AI crawler 省 token、直接取內容。
