# Public synthetic dashboard base

Read-only static UI, not a private investment app. All displayed trades and
values are generated from the wholly fictional `SAMPLE_CSV` in the Python
fixture. No real exports, accounts or data are accepted.

## Build and run

```sh
sh run_tests.sh
python3 build_demo.py
python3 -m http.server 8000 --directory web
```

Open localhost:8000. No Node build, dependencies, network API, database,
localStorage, login, upload or paid service is required by the app.

## Views

- Overview: remaining synthetic cost, asset count and cost allocation.
- Holdings: ticker/name search, empty state and clear.
- Transactions: invented buy/sell rows with fees and FX.
- Export: downloads synthetic JSON only. Reset restores the initial view.

This is cost basis, not market value, return, cash or projected dividends.
The public landing is separate; deployment must serve the `web` folder.

## QA

2026-10-07: 14 calculation tests pass. Browser checks at 390x844 and 1280x844
verify all three tabs, search, empty state, clear, reset, JSON download, no
horizontal overflow and no JavaScript errors. Full-page screenshots reviewed
for readable mobile and desktop layouts. Keyboard tab navigation supports
left/right arrows. Data generation is deterministic and repeatable.

For Cloudflare Pages, use a static project with output directory `web` and
build command `python3 build_demo.py` if Git-connected, or upload the contents
of `web` directly. Do not enable Workers, paid services or real-data imports.

Follow-up: base review before implementing selected DivSmart features in #3.
Private use requires a separate security-reviewed runtime, authorization,
private storage/backups, import/reconciliation and retention controls. A
public static site is not that environment.

Phase 1 data validation and calculation explanations: [contract](data-quality.md).
