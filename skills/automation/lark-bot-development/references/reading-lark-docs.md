# Reading Lark/Feishu docs — extraction playbook (verified 2026-08)

Companion to the SKILL.md「Accessing Lark docs」section. All patterns verified against open.larksuite.com / bytedance.larkoffice.com.

## URL formats → what works

| URL shape | Example | web_extract | browser |
|---|---|---|---|
| Old-format `/document/ukTMukTMukTM/...` | open.larksuite.com/document/ukTM... | ✅ works | — |
| New-format `/document/server-docs/...` etc. | open.larksuite.com/document/server-docs/getting-started/terminology | ❌ "Failed to fetch url" | ✅ loads, nav-heavy snapshot |
| Wiki `/wiki/<wikiToken>` | bytedance.larkoffice.com/wiki/ILuTww7Xcimb6GkhH0mcK2f4nS7 | ❌ "no content extracted" | ✅ renders SSR content |

## Browser extraction pattern

Navigate, then pull text via `browser_console`:

```js
// /document/ pages (article body lives in <main>):
document.querySelector('main').innerText.slice(0, 50000)

// /wiki/ pages (content is in body; verify length first — tiny length = not hydrated):
({len: document.body.innerText.length, text: document.body.innerText.slice(0, 120000)})

// TOC + every anchor (use to reconstruct structure and find source links):
[...document.querySelectorAll('a')].map(a => ({t: a.innerText, h: a.href}))
```

Wiki doc metadata (objToken, spaceId, objType) lives in the global `window.wiki_info_map[<wikiToken>]`:
```js
window.wiki_info_map  // -> {"ILuTww7Xcimb6GkhH0mcK2f4nS7": {objToken, spaceId, objType, wikiToken}}
```

Notes:
- `document.body.innerText` on a wiki page can legitimately be short (2K chars) if the article is a summary/landing page — cross-check with the anchor list before concluding the doc is empty.
- Old-format URLs: do NOT append `?lang=zh-CN` — breaks web_extract.

## Delegation pitfall

Lark doc pages are huge (17–25K chars clean). A subagent running a small-context model blows up with "Context length exceeded" after ~1 API call. Research Lark docs in the MAIN context, not via `delegate_task`.
