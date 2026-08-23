# New content entry audit (read-only acceptance check)

When asked to audit a newly added portfolio/project entry (read-only — do not
modify), run this exact sequence. It catches scope creep and verifies the
entry actually shipped in the build (not just in source):

1. `git status --short` + `git diff --stat HEAD` FIRST: the only tracked change
   should be the source files for this entry (collection `.md`, `llms.txt`).
   Untracked unrelated dirs (e.g. `your-brand-pricing/`) may pre-exist — note
   them in FINDINGS but ignore/never touch them.
2. Resolve the frontmatter cover path by hand: `cover: "../../assets/…"` inside
   `src/content/<collection>/<slug>.md` → `src/assets/…` (relative to the md
   file). Confirm the file exists and is a valid image (`file` → RIFF/Web-P/VP8),
   and that every body-image reference (`![alt](…)`) points at files that exist.
3. `pnpm build` (note page count) → `node scripts/verify-seo.mjs` (exit 0).
   verify-seo asserts parseability/site-graph, NOT per-entry CreativeWork
   content — the name/date/image assertions below are on YOU.
4. Post-build dist assertions:
   - exactly one new route: `dist/projects/<slug>/` contains only `index.html`;
   - sitemap: the route appears exactly once across `dist/sitemap-*.xml`;
   - `dist/llms.txt` contains the route exactly once;
   - CreativeWork JSON-LD (extract from raw built HTML, see pitfall 6): assert
     `name` == frontmatter title, `dateCreated`/`dateModified` == date ISO,
     `image` == og:image URL, `url` == canonical;
   - every hashed `/_astro/*.webp` src in the page must exist under `dist/` —
     cover appears TWICE (body `<img>` + og:image/JSON-LD, different hashed
     variants) and both must resolve.
5. `git diff --check HEAD` (exit 0) + re-check `git status`: build artifacts
   must not pollute git (`dist/` gitignored). Report as
   `VERDICT: PASS|FAIL` + `FINDINGS` (file evidence) + `COMMANDS` (actual output).

Session-specific expected values for your-brand: see
`references/content-entry-audit-your-brand.md`.
