# Astro inline-script pitfalls (empirically verified on Astro 6)

1. **`import.meta.env.X` is NOT replaced inside `<script>` / `<script is:inline>` bodies.**
   The literal text lands in `dist/*.html`. In a classic (non-module) script
   the browser throws a SyntaxError, silently killing the whole script —
   e.g. `gtag('config', import.meta.env.PUBLIC_GA_MEASUREMENT_ID ?? 'G-…')`
   means NO analytics at all, with no build error.
2. **`{}` template expressions are NOT evaluated inside `is:inline` bodies.**
   `gtag('config', {gaId})` stays literal in dist. Attribute expressions
   (`src={...}`) ARE interpolated — only script bodies are verbatim.
3. **Fix for both:** compute the value in frontmatter, inject via
   `<script is:inline define:vars={{ gaId }}>`, reference the bare variable
   in the body (`gtag('config', gaId)`). `define:vars` works with `is:inline`.
4. **Env fallbacks: use `||`, not `??`** — `??` doesn't catch empty-string
   env, so `'' ?? fallback` still yields a broken `gtag.js?id=` URL.
5. **Scoped attributes break class regexes:** Astro injects
   `data-astro-cid-xxxxx` on every element. `<h3 class="faq-question">` matches
   nothing in dist — write `class="faq-question"[^>]*>` or match the substring.
6. **`read_file` round-trips produce FALSE JSON-LD parse errors.** `read_file`
   prepends `LINE_NUM|CONTENT` to every line; those prefixes land inside
   `[\s\S]*?` captures, so `JSON.parse` fails with a misleading
   "Expecting ',' delimiter" — the JSON is fine, the capture is polluted.
   Extract from the RAW file on disk in one process: `node -e` reading the
   file, or python `open(path, encoding='utf8')`. Never regex-capture script
   blocks from read_file output. (Python quirk: the execute_code sandbox
   rejects `open(path, 'utf8')` positional-mode — use the `encoding=` keyword.
   And for regex-heavy extraction, prefer python/execute_code over inline
   shell one-liners with nested quote/glob soup — those trip the hardline
   command blocklist.)
