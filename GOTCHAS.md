# GOTCHAS.md — Investor OS (public demo)

Traps that already bit this project. Read before editing. When one becomes a general rule it moves to AGENTS.md.

- **Never real financial data**: no real broker CSV exports or portfolio values in this public repo — mockup data only. This was the owner's explicit rule from day one.
- **Source + date on numbers**: every figure the app shows must say which file/source it came from and its date.
- **CSV hardening**: upload parsing was hardened after malformed-input bugs — keep strict validation on any import path.
