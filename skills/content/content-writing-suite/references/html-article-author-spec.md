---
name: html-article-author
description: 'Use when user asks "輸出成 HTML 網頁" / "寫成文章頁面" / "做成 HTML". Converts markdown into a standalone dark-themed HTML article with CJK fonts.'
version: 1.0.0
---

# HTML Article Author

Author a standalone `.html` article page — no build step, no external CSS, browser-ready. Designed for technical/informational content where a dark theme and CJK typography are appropriate.

## When to Use

- User says "輸出成 HTML 網頁", "寫成文章頁面", "做成 HTML"
- Converting a markdown article, tool guide, project intro, explainer, or tech deep-dive into a polished standalone HTML page
- Any informational content that needs a dark theme + CJK font support

## Design System

### Tokens

```css
:root {
  --bg-page: #0a0a0f; --bg-card: #181825; --bg-code: #181825;
  --border: #27272a;
  --text-primary: #f0f0ff; --text-body: #d4d4d8; --text-muted: #71717a;
  --accent: #818cf8;
  --accent-gradient: linear-gradient(135deg, #f0f0ff 0%, #818cf8 50%, #f472b6 100%);
  --accent-border: #6366f1;
  --sans: 'Inter', 'Noto Sans TC', system-ui, -apple-system, sans-serif;
  --mono: 'JetBrains Mono', 'SF Mono', ui-monospace, monospace;
}
```

### Visual Characteristics

| Element | Style |
|---------|-------|
| Background | `#0a0a0f` dark page |
| H1 title | Indigo→pink gradient text |
| H2/H3 | White/light gray, 600–700 weight |
| Body text | `#d4d4d8`, line-height 1.75 |
| Tables | Dark borders, card header bg |
| Code | Inline indigo tint, card bg block |
| Callout | Indigo left border, navy gradient |
| Blockquote | Indigo left border, card bg |
| Links | Indigo accent `#818cf8` |
| Container | Max-width 720px centered |

## Layout Components

### Header

```html
<header>
  <div class="container">
    <h1><!-- gradient title --></h1>
    <p class="subtitle"><!-- muted byline --></p>
  </div>
</header>
<article class="container"><!-- body --></article>
```

### KPI Cards

3-column grid, number + label, 2 cols on mobile.

```html
<div class="kpi-row">
  <div class="kpi"><div class="num">290+</div><div class="label">供應商</div></div>
  <div class="kpi"><div class="num">500+</div><div class="label">模型</div></div>
  <div class="kpi"><div class="num">19</div><div class="label">路由策略</div></div>
</div>
```

### Scene Box

Dark card for scenarios, config examples.

```html
<div class="scene-box">
  <h4>場景名稱</h4>
  <p>說明文字</p>
  <pre><code>config</code></pre>
</div>
```

### Callout

Indigo left border, navy gradient bg.

```html
<div class="callout">
  <strong>Key:</strong> value<br>
  <strong>Note:</strong> important info
</div>
```

### Table

Wrap in `.table-wrap` for mobile scroll.

```html
<div class="table-wrap">
<table>
<thead><tr><th>Header</th><th>Header</th></tr></thead>
<tbody>
<tr><td>Cell</td><td>Cell</td></tr>
</tbody>
</table>
</div>
```

## Fonts

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
```

Swap `Noto Sans TC` for `SC` (simplified), `JP` (Japanese), `KR` (Korean).

## Responsive

| Element | Desktop | ≤600px |
|---------|---------|--------|
| H1 | 2rem | 1.5rem |
| KPI grid | 3 cols | 2 cols |
| Table font | 0.85rem | 0.78rem |

## Workflow

1. Read source content
2. Structure: H2 sections, assign KPI/scene-box/callout/table per section
3. Write HTML from scaffold
4. Verify in browser pane
5. Report file path

## Pitfalls

- Google Fonts **preconnect** required before stylesheet
- Gradient H1 needs both `-webkit-background-clip` and `background-clip`
- KPI grid at ≤600px: `repeat(2, 1fr)` not default
- Table: `overflow-x: auto` on wrapper, not table
- Zero JS for static articles unless interactive controls needed
- No external CSS — everything inline `<style>`
- No emoji/LaTeX in article body
- Use `&lt;` / `&gt;` for HTML in code samples
- Not compatible with `html-artifact`'s warm paper tokens
