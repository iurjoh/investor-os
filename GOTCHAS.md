# Regression and gotcha register

Quality trial started 2026-10-20. Review friction around 2026-11-20. Pass counters below record new, independently evidenced runs only, not historical results.

## Regressions

No regression checks recorded yet. Entry format: - [YYYY-MM-DD] <bug> -> check: <deterministic re-run command> | consecutive passes: n/5. Do not record historical results as passes.

Five recorded consecutive passes make a check eligible for automation; adding CI is a separate code change. Record revision, environment and evidence before increasing a count. No automatic edits or release approval follow from a counter.

## Gotchas


- [2026-10-20] Never real financial data: no real broker CSV exports or portfolio values in this public repo - mockup data only | source: owner standing rule 2026-10-01, reaffirmed 2026-10-07 | version: current | validity: permanent | projects: investor-os, investor-os-private (2nd project: propose promotion to a shared rule).
- [2026-10-20] Every number the app shows needs source + date (which file, file date, last update) | source: owner QA rule 2026-10-15 | version: current | validity: permanent | projects: investor-os, ITAI (already adopted as shared rule).
- [2026-10-20] CSV upload parsing was hardened after malformed-input bugs; keep strict validation on every import path | source: merged PR #18 (CSV hardening, 16 tests), 2026-10-11 | version: current | validity: rerun after parser changes | projects: investor-os.

## Check entry points

Inspect the repo's test tooling before claiming coverage; the demo deploys via Cloudflare Pages. Report exactly what ran and where.

If a gotcha is independently observed in a second project, propose a shared rule with both sources.
