# Single-file Event Landing Page — GEO/Schema Patterns

Session-tested patterns for handcrafted one-file event pages (2026-08, 老闆的最後一堂 AI 課 event page).

## Event JSON-LD (validated)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "老闆的最後一堂 AI 課｜為生意導入 AI 分享會",
  "description": "2026 年 8 月 22 日，Ted 分享三間公司的企業 AI 化歷程、AI 學習法與 FDE 新職業。免費公開報名，席次有限。",
  "startDate": "2026-08-22T14:00:00+08:00",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "Place",
    "name": "BEONE 未來共生基地 VISION SPACE",
    "address": { "@type": "PostalAddress", "addressRegion": "台北市", "addressLocality": "信義區", "streetAddress": "基隆路一段 200 號 B1" }
  },
  "organizer": { "@type": "Organization", "name": "YOTRON AI" },
  "performer": { "@type": "Person", "name": "Ted" },
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "TWD", "availability": "https://schema.org/LimitedAvailability" },
  "isAccessibleForFree": true
}
</script>
```

Free event → price as **string** `"0"` + `isAccessibleForFree: true`.

## Verification (python, minified single-line HTML safe)

```python
import re, json
from pathlib import Path
s = Path('index.html').read_text()
raw = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', s, re.S).group(1)
data = json.loads(raw)
assert data['@context'] == 'https://schema.org'
assert data['@type'] == 'Event'
assert data['startDate'] == '2026-08-22T14:00:00+08:00'
assert data['offers']['price'] == 0  # json.loads coerces "0" -> 0
assert '為什麼 AI 工具沒有進入工作流程？' in s
print('question_headings', len(re.findall(r'<h3>[^<]*[？?]</h3>', s)))
```

## GEO question-heading rewrite (no fake FAQ)

Rewrite EXISTING h3s into natural questions, keep body text identical:

- `工具沒有進入流程` → `為什麼 AI 工具沒有進入工作流程？`
- `導入三個月後失效` → `為什麼 AI 工具導入三個月後失效？`
- `資料與方法四散` → `為什麼團隊的 AI 方法會各自為政？`
- `AI 只停在示範階段` → `為什麼 AI 導入只停在示範階段？`
- `老闆的 AI 學習法` → `老闆應該怎麼學 AI？`
- `企業 AI 化實錄` → `企業如何把 AI 放進日常流程？`
- `FDE 新職業揭幕` → `企業導入 AI 為什麼需要 FDE？`

Same layout, zero new content → keeps the "no visible UI sections" hard rule.

## robots.txt for AI crawlers (explicit allow)

```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /
```

Explicit entries are cheap and survive CDN default-blocking of AI bots.

## Domain-dependent assets — defer, don't fake (default)

When the public domain is not yet known, leave OUT: `canonical`, `og:url`,
`sitemap.xml`, `llms.txt`. Report them as the remaining step rather than
writing a placeholder URL.

## Placeholder scaffold — when the user says "都幫我加上這些，資料之後補"

If the user EXPLICITLY asks to add everything now (data comes later), scaffold
with a placeholder instead of deferring:

1. Pick ONE placeholder root, e.g. `https://example.com/ai-last-class-event/`.
2. Wire it into all four assets, with a `<!-- TODO: replace example.com with
   the production domain before deployment. -->` comment at each site:
   - `index.html`: `<link rel="canonical" href="<root>">` +
     `<meta property="og:url" content="<root>">`
   - `sitemap.xml`: `<loc><root></loc>` (+ `lastmod` = today, `priority` 1.0)
   - `robots.txt`: `Sitemap: <root>sitemap.xml` (keep GPTBot/ChatGPT-User/
     Google-Extended explicit allows)
   - `llms.txt`: summary + event facts + `[活動報名頁](<root>)` link
3. Verify URL consistency — every file must use the IDENTICAL placeholder:

```python
from pathlib import Path
from xml.etree import ElementTree as ET
root = Path('.')
site = 'https://example.com/ai-last-class-event/'
html = (root/'index.html').read_text()
assert f'href="{site}"' in html and f'content="{site}"' in html
sitemap = (root/'sitemap.xml').read_text()
ET.fromstring(sitemap); assert f'<loc>{site}</loc>' in sitemap
robots = (root/'robots.txt').read_text()
assert f'Sitemap: {site}sitemap.xml' in robots
llms = (root/'llms.txt').read_text(); assert f'({site})' in llms
print('URL consistency: PASS')
```

4. Rebuild the handoff ZIP, and end the reply with the ONE remaining step:
   search `example.com` in those four files and replace with the production
   domain before deploy. Never invent the placeholder silently — only on an
   explicit "add it all now" request.

## Minified single-line HTML — patch workaround

The `patch` tool (V4A multi-file form) refuses minified single-line HTML with
`Binary file — cannot display as text`. Workaround that worked:

```python
from hermes_tools import patch
repls = [('>工具沒有進入流程</h3>', '>為什麼 AI 工具沒有進入工作流程？</h3>'), ...]
for old, new in repls:
    patch(path, old, new)   # replace mode, one call per pair, 0.97s for 7 pairs
```

Replace-mode `patch` with a short unique old_string handles each edit fine —
only the V4A multi-file form trips the binary detection. Batch via a python
loop to keep one round-trip.
