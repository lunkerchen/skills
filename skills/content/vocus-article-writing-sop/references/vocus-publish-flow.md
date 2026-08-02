# vocus Publish Flow — Debugging History

## Problem

The cron job (AI工具簡報→方格子) writes articles to Obsidian drafts folder. Publishing them to vocus.cc requires a Playwright-driven browser automation flow. Two major issues were discovered:

1. **System clipboard inaccessibility**: `pbcopy + Meta+V` fails silently in headless mode
2. **Markdown heading rendering**: vocus Lexical editor renders `## H2` as literal text, not as headings
3. **Spinner compilation wait**: After `fill()`, vocus compiles markdown async — buttons disabled during compile

## Root Cause: System Clipboard Inaccessibility

`pbcopy + Cmd+V` works in **headed** (visible) Playwright sessions because the app has focus and the system clipboard is accessible. In **headless** (background) sessions — including most Playwright CLI runs — the system clipboard is inaccessible. `pbcopy` writes to the system pasteboard but the Playwright browser process can't read it without accessibility permissions / focus.

**Solution:** Use `fill()` on the contenteditable textbox instead. This works in both headed and headless modes on Lexical-based editors (vocus uses Lexical).

## Content Size Limit

Shell CLI truncates arguments at ~4K chars on macOS. Passing a 3,000+ word article as a `playwright-cli fill` argument causes silent truncation (only first ~4K chars get filled).

**Solution:** Use a Python subprocess wrapper to pass the content string:

```python
import subprocess
with open("/tmp/vocus-content.txt") as f:
    content = f.read()
subprocess.run(
    ['playwright-cli', 'fill',
     'getByRole("textbox").filter({ hasText: /^$/ })',
     content],
    timeout=30
)
```

## DOM Ref Staleness

Playwright CLI's `snapshot` command returns DOM refs like `@e1019`. These refs are tied to the DOM snapshot at the moment of capture. After a radio button click (or any DOM mutation), old refs become stale — clicking `@e1019` from the snapshot might fail or target the wrong element.

**Solution:** Use `getByRole`/`getByText` selectors instead of numeric refs for multi-step flows. The selectors are stable across DOM mutations.

## Re-publishing Flow (Edit Existing Article)

When opening an ALREADY-PUBLISHED article for editing, the button text changes:

| Flow | First Publish | Re-publish |
|------|--------------|------------|
| Button | "準備發佈" | "直接發佈" |
| Category | Must select | Pre-set from first publish |
| Permissions | Must set to 公開發佈 | Pre-set from first publish |
| Dialog | Full 3-tab flow | Instant — no dialog, button click publishes directly |

**Re-publish steps:**
1. Open existing article: `page.goto("https://vocus.cc/article/<hex-id>")`
2. Click "編輯文章" button on the published page
3. Or navigate directly to `https://vocus.cc/new-editor/<hex-id>` (the edit URL)
4. Modify content via `fill()` on the contenteditable textbox
5. Click "直接發佈" — no dialog, instantly updates
6. Verify via "發佈成功" dialog or navigate back to the article URL

**Caveat:** "直接發佈" is instant — there's no confirmation dialog. The only signal of success is a "發佈成功" toast. If the page shows no toast, the publish may have failed silently.

## Bracket-Style Headings (【】)

vocus Lexical editor does NOT render markdown headings (`## H2`, `### H3`). They appear as literal text `## H2`. 

**Solution:** Convert H2/H3 to bracket-style 【Heading】 before pasting:

```python
import re
text = re.sub(r'^##\s+(.+)$', r'【\1】', text, flags=re.MULTILINE)
text = re.sub(r'^###\s+(.+)$', r'【\1】', text, flags=re.MULTILINE)
```

This is handled by the dedicated script at `$HERMES_HOME/scripts/clean-vocus.py`:

```bash
python3 $HERMES_HOME/scripts/clean-vocus.py < article.md > clean.txt
```

The script performs:
1. Strip YAML frontmatter
2. Convert H2/H3 → 【bracket-style】 headings
3. Strip remaining markdown symbols (bold `**`, italic `*`, inline code `` ` ``, links `[text](url)`, images, blockquotes, horizontal rules)
4. Strip list markers (`- `, `* `, `1. `) before headings (but NOT heading prefixes — those are converted, not removed)
5. Preserve paragraph spacing (collapse 3+ blank lines to 1, but keep paragraph breaks)

## Spinner Compilation Wait

After `fill()` writes long content to the Lexical editor, vocus performs an async markdown compilation (spinner icon appears). During this time the publish button is disabled.

**Solution approach (from vocus-publish.sh):**
- Wait ~3 seconds after `fill()` before interacting with buttons
- Alternative: poll for the spinner to disappear with `page.locator('[class*="spinner"]').waitFor({ state: 'hidden', timeout: 10000 })`
- For Playwright CLI, a simple `sleep 3` after the fill command is the most reliable approach

Without this wait, clicking "準備發佈" or "直接發佈" immediately after `fill()` has no effect — the button is still disabled from the compilation state.

```
Step                    | Selector                                      | Note
------------------------|-----------------------------------------------|-----
Create article          | getByText("文章完整的編輯功能")                | On creatordesk
Fill title              | getByRole("textbox", {name:"請輸入文章名稱"})  | Works headless
Fill content            | getByRole("textbox").filter({hasText:/^$/})   | Uses fill(), not pbcopy
Open publish dialog     | getByRole("button", {name:"準備發佈"})         |
Open category dropdown  | getByText("請選擇分類")                        |
Select "科技"           | getByRole("option", {name:"科技"})            |
Switch to permissions   | getByRole("button", {name:"權限和狀態"})       |
Set to public           | getByRole("radio", {name:"公開發佈"})          |
Confirm publish         | getByRole("button", {name:"確認發佈"})          | Text was "確認" before
```

After clicking "確認發佈", the page returns to the editor with URL still at `/new-editor/<hex-id>`. Do NOT trust the URL alone — check for the success dialog "發佈成功" instead.

## Verification

```bash
# Check for success dialog
playwright-cli snapshot | grep "發佈成功"

# Or check article is accessible
playwright-cli goto "https://vocus.cc/article/<hex-id>" 2>/dev/null
playwright-cli eval "document.title"  # Should show article title
```

## Published Article (2026-07-05)

- Title: AI 撞牆、機器人自學、Nikon Z9 寫論文
- URL: https://vocus.cc/article/6a49cfadfd89780001fef42c
- Category: 科技
- Status: 公開發佈
