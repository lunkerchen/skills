# Browser Smoke Gate (Gate 6)

Run when the change touches routes, links, or rendered UI (new page, footer link, nav change).
Gates 1-5 prove it compiles; Gate 6 proves it renders.

## Sequence

```bash
# 1. Start dev server in background
npm run dev -- --host 127.0.0.1 --port 54349

# 2. Direct route request — SPA shells are server-rendered HTML:
curl -fsS -D /tmp/h.txt http://127.0.0.1:54349/<route> -o /tmp/p.html
# expect HTTP 200 + Content-Type text/html + <div id="root"> in body
```

## browser_console batch-assertion pattern

One JS expression returning a dict of every runtime fact, instead of many separate calls:

```js
(() => ({
  path: location.pathname,
  title: document.title,
  h1: document.querySelector('h1')?.textContent?.trim(),
  articleCount: document.querySelectorAll('main article').length,
  footerLinkFound: Boolean(document.querySelector('footer a[href="/changelog"]')),
  horizontalOverflow: document.documentElement.scrollWidth > innerWidth,
}))()
```

Then check the console-error buffer in a *separate* `browser_console` call (clear=true, no expression)
— a page can render fine while still logging JS errors.

## Pitfalls

- `browser_navigate` snapshot on a React SPA returns a near-empty accessibility tree (often 1 generic
  element) — the page renders via JS. Verify content with `browser_console` expressions, not the snapshot.
- A link existing on the target page doesn't prove it's reachable — navigate to the page that *contains*
  the link (e.g. `/`) and assert the anchor target before following it.
- `git diff --check` (whitespace errors) before wrap-up; kill the dev server via `process(action='kill')`
  — don't leave it running.
