# Out of scope

This repo is a curated public collection. Deliberately excluded, with reasons:

| Category | Reason |
|---|---|
| `project-context/*` | Client- and project-specific data (nail-booking, course-landing-yongtai, camera-market, …). Private. |
| `dbs-*` commercial toolbox | A commercial product (dontbesilent). Not open source. |
| `nuwa-skill` perspective collection (~45 personas) | Personal research asset. May become a separate repo. |
| `.archive/` (97 skills) | Retired. |
| Hermes-internal tooling (`hermes-*`, `prepforreset`, …) | Niche to one agent framework; may move in later. |
| Personal productivity one-offs | Too personal to generalize (`iphone-home-screen-organizer`, `organize-phone`, …). |
| `baoyu-*` suite, `gzh-design` | Third-party imports with existing public upstreams (JimLiu/baoyu-skills, isjiamu/gzh-design-skill). Mirroring adds no value; `gzh-design` is also AGPL. |

## Deferred to v2 (publishable after curation)

These passed review with a clean core but need content surgery before release:

| Skill | Work needed |
|---|---|
| `cloudflare-deploy` | Strip per-client project inventory (achang-erp, kamera-ichi, …) + private email from references; triage 12 session-log references |
| `ai-cli-tooling` | Genericize OmniRoute/private-infra naming; drop dated personal debug references |
| `geolook-tw` | SKILL.md is a personal ops runbook for a private fork; rewrite into generic TW-market methodology |
| `multi-agent-debate` | 18 references are personal case studies (camera-market schema, personal finance); keep SKILL.md + generic refs only |
| `loop-engineering` | Fix broken `loop-conditions.md` pointer; genericize paths; drop camera-market cron reference |
| `xiaohu-video-translate` | Wrapper over a private repo's scripts — bundle or genericize |
| `org-ai-adoption`, `organizational-ai-adoption` | ~95% duplicates of `enterprise-ai-adoption` — merge locally, publish one |

If a skill belongs here, this document is the place to record why.
