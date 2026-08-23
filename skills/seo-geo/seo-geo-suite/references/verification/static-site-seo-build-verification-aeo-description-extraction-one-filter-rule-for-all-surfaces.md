# AEO description extraction: one filter rule for ALL surfaces

Meta description, JSON-LD `description`, and llms.txt all pull the "first
meaningful paragraph" from the same markdown body — they MUST share one filter
rule. Real bug (caught by a blind audit, NOT by the verifier): the project-page
extractor skipped only image lines, so `<p class="project-cta"><a href="…">`
leaked into 9/30 meta descriptions and `CreativeWork.description`, while the
llms generator filtered that exact pattern. Search snippets and AI citations
then contained escaped anchor markup.

Filter list (apply identically on every extraction surface): skip image lines
(`^![`), lines starting with `<`, lines containing `<a `, and lines whose
stripped form is ≤10 chars. If nothing qualifies, emit a category fallback
(e.g. `` `${title} — ${category} 攝影作品。` ``). Then have the verifier assert
the result contains no HTML — raw (`/<\/?[a-z][^>]*>/i`) or escaped
(`&lt;`/`&gt;`).
