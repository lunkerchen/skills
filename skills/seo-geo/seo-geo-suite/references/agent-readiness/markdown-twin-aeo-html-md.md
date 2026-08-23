# HTML→MD 轉換器

```js
export function htmlToMarkdown(html) {
  let text = String(html)
    .replace(/<head[\s\S]*?<\/head>/gi, '')
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
  // ⚠️ 順序：先轉 h1-h6 與 li，再做 block 換行 — 反了開頭 tag 會被吃掉
  text = text.replace(/<h([1-6])[^>]*>([\s\S]*?)<\/h\1>/gi, (_, level, inner) => `${'#'.repeat(Number(level))} ${inlineMd(inner)}\n`)
  text = text.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, (_, inner) => `- ${inlineMd(inner)}\n`)
  text = text
    .replace(/<\/(p|div|section|article|nav|ul|ol|table|tr|blockquote)>/gi, '\n')
    .replace(/<(p|div|section|article|nav|ul|ol|table|tr|blockquote)[^>]*>/gi, '\n')
  text = text
    .replace(/<a[^>]+href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, (_, href, inner) => `[${inlineMd(inner)}](${toAbsolute(href)})`)
    .replace(/<(strong|b)[^>]*>([\s\S]*?)<\/\1>/gi, (_, _t, inner) => `**${inlineMd(inner)}**`)
    .replace(/<(em|i)[^>]*>([\s\S]*?)<\/\1>/gi, (_, _t, inner) => `*${inlineMd(inner)}*`)
    .replace(/<br\s*\/?>/gi, '\n')
  text = text
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/^[ \t]+/gm, '')          // 行首縮排 → 避免標題被當 code block
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
  return text
}
```
