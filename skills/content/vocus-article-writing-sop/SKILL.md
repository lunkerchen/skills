---
name: vocus-article-writing-sop
description: 方格子深度文章寫作風格固化。從 AI 工具簡報或科技新聞來源，改寫為頂尖科技記者視角的高品質長文。Covers headline crafting, lead paragraph structure, technical accuracy, narrative flow, and the signature analytical depth of top-tier tech journalism. Use when writing 方格子 articles, tech deep-dives, or AI tool reviews.
version: 1.5.0
---

# 方格子深度文章寫作 SOP

## 何時使用

- 生成或改寫方格子草稿時
- 從 AI 工具簡報 Obsidian 筆記條目 → 文章
- 任何需要將新聞筆記轉為深度分析文章的場景

## 角色設定

**頂尖科技記者與知識策展人**

- 視角：行業觀察者 + 技術解讀者，非內部人士也非外行
- 語態：專業、客觀、有洞察但不譁眾取寵
- 讀者假設：對科技有興趣的普通讀者，非該領域專家

## 任務

將來源材料（Obsidian 筆記條目 / 新聞摘要）改寫為高品質的繁體中文長文。

## 寫作準則

### 1. 邏輯重構

- 從來源材料提取 **3-5 個核心主題**
- 以主題塊（H2）組織文章，而非按原文時間線或段落複述
- 每個主題塊下可拆 H3 子主題深入

### 2. 保留精髓

- 保留所有具體 **數據、案例、故事、引述**
- 數字不模糊化（不說「大幅增長」，說「增長 85%」）
- 案例要具體到產品名、人名、時間點

### 3. 補全上下文

- 對來源假設讀者已知但普通讀者陌生的背景提供解釋
- 為什麼這件事重要？它打破了什麼既有認知？
- 這個技術/事件的前因後果是什麼？

### 4. 語調轉換

- 口語 → 專業書面
  - 不使用「殺瘋了」、「太神了」等網路用語
  - 不使用「你不可不知」、「你一定要看」等 clickbait
  - 不使用 emoji、LaTeX
- 簡潔有力：
  - 一句話一個概念
  - 段落不超過 3-4 句
  - 信任讀者理解力，不過度解釋

### 5. 格式結構

```
# 標題（H1，引人入勝但不下標）

**分類：[分類名稱]**

**摘要：** 3-5 條 bullet point 總結全文核心觀點

## 引言

（鉤子開頭：為什麼這則新聞值得關注？
  背景鋪墊：讀者需要知道的前置脈絡
  核心命題：這篇文章要探討什麼）

## [核心主題 1 — H2]

（主題展開，融入數據與案例，搭配 inline 來源）
### [子主題 — H3 可選]
（深入細節）

## [核心主題 2 — H2]

...

## [核心主題 3-5 — H2]

...

## 影響展望

（這件事的更大意義、對行業/讀者的影響
  不加入個人預測，但可分析可預見的趨勢）

## 常見問答

2-3 則 FAQ，圍繞讀者最可能的疑問

來源：[原始連結]
```

### 6. GEO 證據完整性

為確保文章被 AI 搜索引擎（Perplexity、Google AI Overviews）視為可引用來源：

- **每個數據附口徑** — 數字後加（時間範圍、來源、計算方式）
  - 對：`營收增長 85%（2024 Q1-Q2，Crunchbase）`
  - 錯：`營收增長 85%`
- **inline 來源標註** — 關鍵論述/資料旁附簡短出處
  - 對：`根據 WSJ 報導（2025.03），OpenAI 年化營收已突破...`
  - 錯：文末才放來源連結
- **首次實體展開** — 每家公司/產品/人名首次出現時附簡短 context
  - 對：`Anthropic（AI 安全新創、Claude 開發商）發表了...`
  - 錯：直接 `Anthropic 發表了...`
- **嚴禁編造** — 禁止虛構任何研究名稱、百分比、樣本量、報告日期、引用或機構。原文無此資訊時以 `[...]` 或「未揭露」標註

## 文章長度

- **一般文章**：800-1200 字（H2 × 3-4）
- **深度分析**：1200-2000 字（H2 × 4-5 含 H3）

## 語言規範

- 繁體中文（台灣用語）
- 不使用簡體中文
- 不使用 emoji
- 不使用 LaTeX
- 不加入個人評論或未來預測
- 文末附上原始連結
- 嚴禁編造：禁止虛構研究名稱、百分比、樣本量、報告日期、引用或機構。來源不明時誠實標註「未揭露」

## Pipeline Integration

This skill produces **source markdown** (the article draft). In the user's daily cron pipeline, the output is processed further before reaching readers:

```text
vocus-article-writing-sop   ← you are here
        ↓
stop-slop                   → remove AI writing clichés (preserve GEO annotations)
        ↓
clean-vocus.py              → strip YAML+markdown, preserve ##/### H2/H3 markers
        ↓
Telegram                    → paste into vocus editor → format H2/H3 via toolbar
```

**Formatting standard (see published example at vocus.cc/article/6a49cfadfd89780001fef42c):**
- `## H2` and `### H3` markers preserved in clean output — they show which text should be formatted as headings in vocus's Lexical editor
- Paragraphs separated by blank lines (2+ newlines)
- Summary as bullet list under **摘要：**
- Sources inline with (出處, 日期) — e.g., `（PetaPixel，2026.07.02）`
- 800-1200 chars for daily articles, deeper analysis up to 2000

**Implications for writing:**

**To publish the latest draft:**
```bash
bash $HERMES_HOME/scripts/vocus-publish.sh
```

The script handles everything: title extraction, markdown pre-processing, content filling via `fill()` (not pbcopy), and full auto-publish flow (category → public → confirm). See the Publishing section for detailed Playwright selectors.

**Implications for writing:**
- Structure H2/H3 clearly — the cron pipeline no longer runs a separate GEO optimizer, so write with inline sources and entity context from the start (see GEO guidance in section 6)
- Keep data specific (numbers, dates, sources) — attribution in the original text is permanent
- Don't add decorative markdown (em dash, HTML tables, special formatting) — they'll be stripped by the Lexical pre-processor
- Don't write meta commentary ("在本文中我們將探討") — stop-slop will remove it
- The article lands in Telegram same-day but may publish later. Write for a reader seeing it fresh, not as an evergreen piece.

## Publishing (On-Demand)

Vocus has no public API for article creation. Publishing uses Playwright CLI to drive the WYSIWYG editor via clipboard paste.

### Quick Publish (Latest Draft)

```bash
bash $HERMES_HOME/scripts/vocus-publish.sh
```

The script:
1. Finds the latest `.md` in the Obsidian drafts folder
2. Extracts the title from the first `# H1` line
3. Pre-processes the `.md` via Python — strips frontmatter, markdown symbols, collapsed newlines (writes to `/tmp/vocus-*.txt`)
4. Checks for an existing persistent Playwright session — if none, opens `--headed` for manual login
5. Creates a new article via `getByText("文章完整的編輯功能")`
6. Fills title via `fill(getByRole("textbox", { name: "請輸入文章名稱" }), TITLE)`
7. Fills content via `fill()` in headless (NOT pbcopy+Meta+V — system clipboard is inaccessible in background sessions) — uses a Python subprocess wrapper to pass the long content string (shell CLI truncates at ~4K chars)
8. Auto-publishes: 準備發佈 → select category "科技" → 權限和狀態 tab → 公開發佈 radio → 確認發佈
9. Verifies via success dialog "發佈成功" or URL containing `/article/`

### Auto-Publish Flow Details

Full Playwright selectors (stable, not DOM ref-dependent):

```js
// Start new article
page.getByText("文章完整的編輯功能").click();

// Fill title
page.getByRole("textbox", { name: "請輸入文章名稱" }).fill(title);

// Fill content (Lexical editor — contenteditable textbox)
page.getByRole("textbox").filter({ hasText: /^$/ }).fill(content);

// Click 準備發佈
page.getByRole("button", { name: "準備發佈" }).click();

// Select category "科技"
page.getByText("請選擇分類").click();
page.getByRole("option", { name: "科技" }).click();

// Switch to 權限和狀態 tab
page.getByRole("button", { name: "權限和狀態" }).click();

// Set to 公開發佈
page.getByRole("radio", { name: "公開發佈" }).click();

// Confirm — text changes from "確認" to "確認發佈" after radio selection
page.getByRole("button", { name: "確認發佈" }).click();
```

**Key learnings from real publish session (2026-07-05):**
- `fill` works on Lexical contenteditable textboxes — both title and body
- `pbcopy + Meta+V` does NOT work in headless mode (no system clipboard access — required a major debugging session to confirm)
- Long content strings (>4K chars) need Python subprocess wrapper — shell CLI truncates arguments
- DOM refs (`@e###`) go stale after radio click → always use `getByRole`/`getByText` text selectors
- The button text changes from "確認" to "確認發佈" once `公開發佈` radio is selected
- Success is confirmed by dialog "發佈成功" even if page URL still shows `/new-editor/`
- **Spinner compilation wait**: After filling long content, vocus compiles markdown asynchronously (a spinner icon appears). The publish button is disabled during compilation. Wait for the spinner to disappear before clicking 準備發佈 — e.g., poll `page.locator('[class*="spinner"]')` or wait ~3s after `fill()` for contenteditable.
- **直接發佈 shortcut**: When re-publishing an ALREADY-PUBLISHED article (opened from an existing `/article/` URL), the editor shows "直接發佈" instead of "準備發佈". Click "直接發佈" — the category/permissions are already set from the first publish. No dialog flow needed; the article updates instantly.

### Options

```bash
# Show browser window (for debugging / first login)
bash $HERMES_HOME/scripts/vocus-publish.sh --headed

# Publish a specific file
bash $HERMES_HOME/scripts/vocus-publish.sh --file /path/to/article.txt
```

### Pitfalls

- **Playwright in cron fails**: The `--persistent` session Chrome profile exists on disk, but there is no running Chrome process in the cron environment to reconnect to. Headless `--persistent` without a prior headed login run also fails silently. Publishing is always on-demand.
- **BSD sed vs GNU sed**: macOS ships BSD `sed` which doesn't support the `q` command for title extraction. The script uses `perl -ne` instead for portable title extraction.
- **Shell truncates long content**: Passing a multi-KB string as a CLI argument to `playwright-cli fill` truncates at ~4K chars. Use a Python subprocess wrapper for content strings (the `vocus-publish.sh` script handles this).
- **DOM refs go stale after radio click**: Playwright's `@e###` ref IDs from `snapshot` change after DOM mutations (e.g., clicking a radio button in the publish dialog). Always use `getByRole`/`getByText` selectors for multi-step flows, not numeric refs.
- **pbcopy + Meta+V doesn't work headless**: System clipboard is inaccessible from background Playwright sessions. Use `fill()` on the contenteditable textbox instead.
- **No .txt = raw markdown paste**: If the cron's pre-process step didn't run (first run, manual draft), the `.txt` file won't exist and the `.md` is used directly. Lexical will render backticks, bold markers, and `---` literally.
- **Spinner compilation**: After filling content via `fill()`, vocus's Lexical editor compiles markdown asynchronously (loading spinner). The 準備發佈/directly publish button is disabled during compilation. On very long articles, wait ~3s after `fill()` before interacting with buttons — or poll for the spinner to disappear.
- **直接發佈 timeout**: When re-publishing, clicking "直接發佈" is instant (no dialog), but the success confirmation comes from a dialog "發佈成功" appearing. If the page stays on `/new-editor/` without a dialog, the publish may have silently failed — check the article URL via `page.goto()` to confirm.
- **Bracket-style headings (【】)**: vocus Lexical editor renders `## H2` literally if pasted as-is. The `clean-vocus.py` script converts H2/H3 to `【Heading】` format, which renders correctly. Do NOT paste raw markdown headings into vocus — always run through clean-vocus.py first.

## 分類對照

來源筆記中每個條目有 `section` 欄位（如 Agent / Coding），對應到文章的分類標籤：

| 來源 Section | 分類標籤 |
|---|---|
| Agent / Coding | Agent / Coding |
| Video / Image | Video / Image |
| Audio / Music | Audio / Music |
| Photography | Photography |
| Infra / Platform | Infra / Platform |
| Funding / Business | Funding / Business |
