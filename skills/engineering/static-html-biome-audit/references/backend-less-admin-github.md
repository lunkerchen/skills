# Backend-Less Admin Panel for Static Vercel Sites (JSON + GitHub API)

Pattern captured 2026-08: user asked for "a management backend that can add videos" to a static single-file landing page with NO backend. Chosen approach: a JSON data file as the source of truth + a standalone `admin.html` that edits it and writes back via the GitHub Contents API. No database, no serverless function, no auth infra.

## When to use
- Static Vercel/GitHub Pages site, content is a small structured list (videos, FAQ items, testimonials, products).
- User wants non-technical editing but does NOT want a database or monthly cost.
- Content changes are low-frequency (a few per week) — the "re-deploy after edit" cost is acceptable.

## Architecture

```
videos.json          ← source of truth (data only, no logic)
  ├── front page     fetches /videos.json → renders
  └── admin.html     fetches, edits, writes back via GitHub Contents API
```

### Data file shape
```json
{ "videos": [ { "id": "N7-0it2zuaw", "title": "...", "subtitle": "...", "enabled": true } ] }
```
Front page always has a **built-in default entry** as fallback — if the fetch fails, the page still renders. Never let missing JSON break the page.

### admin.html essentials (vanilla, zero deps)
- List view with per-item ↑↓ (reorder) / ✎ (edit) / ✕ (delete), first item = featured.
- Edit form with live preview (YouTube ID → thumbnail via `https://i.ytimg.com/vi/{id}/mqdefault.jpg`).
- Deploy card: GitHub token input (stored in `localStorage`, `repo` scope) + "寫回 GitHub" button.
- Export fallback: dump JSON to a textarea for copy/paste when no token is set.

### GitHub Contents API write-back
```js
const REPO = 'owner/repo', BRANCH = 'main', FILE = 'videos.json';
// 1. GET /repos/{REPO}/contents/{FILE}?ref={BRANCH} → { sha }
//    (404 = file doesn't exist yet → sha null)
// 2. PUT /repos/{REPO}/contents/{FILE}
//    body: { message, content: base64(JSON), sha?, branch }
```
UTF-8-safe base64: `btoa(unescape(encodeURIComponent(json)))` — plain `btoa` mangles CJK.
Response `{ commit: {...} }` = success. The commit lands on the branch; Vercel needs a re-deploy (manual `vercel --prod` or Git integration) to serve it.

## Pitfalls
- **Token safety**: token lives in the browser's localStorage — fine for a single-owner internal tool, NOT for multi-user/public admin. No CORS issue (GitHub API allows browser calls).
- **Deploy gap**: writing back to GitHub does NOT auto-deploy unless Vercel has Git integration. Tell the user explicitly, or wire CI. Don't claim "saved = live".
- **First fetch in admin**: `fetch('/videos.json')` only works served over HTTP(S), not via `file://` — catch the error and show "需在網站環境開啟".
- **Ordering semantics**: document that array order = display order (first = featured/hero), so reorder arrows are meaningful.
- **Front-page switching**: when list > 1, render a thumbnail grid (aspect-ratio 16/9); clicking an item swaps the featured video and resets the iframe to idle (`removeAttribute('src')`), so the click-to-load pattern still applies per selection.
