# llms.txt: generate from source, never hand-maintain

Hand-maintained llms.txt rots: a real portfolio file listed two GitHub repos
that 404'd and was missing 4 current entries. Instead:

- `scripts/generate-llms.mjs` (Node built-ins only): glob
  `src/content/<collection>/*.md`, parse frontmatter (title, slug, date,
  category, url) + first non-image body paragraph → rewrite `public/llms.txt`.
- Wire via `"prebuild": "node scripts/generate-llms.mjs"` in package.json —
  npm/pnpm run `pre<name>` automatically before `build`.
- **Bidirectional verification** in the post-build check: every built
  `/projects/<slug>/` page must be listed in llms.txt, AND every project URL
  listed in llms.txt must exist in the build (catches fabricated/rotten
  entries). `curl -sI -L` external links before keeping them.
