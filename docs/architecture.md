# Target architecture: personal-first, zero-cost

## Principles
- Local-first and single-user until real use proves a need for a hosted app.
- PostgreSQL remains the canonical model; deterministic calculations have no AI dependency.
- Every imported or fetched value stores source, observation time, effective time and currency.
- No service requiring a card, free trial, or automatic overage.

## Components
1. Python calculation/import core with only standard-library runtime dependencies.
2. PostgreSQL for normalized transactions, assets, prices, FX, dividends and audit history.
3. Local web UI in a later phase; start with portfolio, income, allocation, data quality and news views.
4. Scheduled local jobs (cron/systemd/Task Scheduler), not paid n8n Cloud.
5. CSV/JSON export and encrypted local backup; user controls the files.

## Delivery order
- Foundation: weighted-average cost, CAD, MIC/exchange identity, fixtures and regression tests.
- Personal MVP: CSV import, manual price/FX override, holdings/dividends/allocation dashboard, checks and export.
- Useful automation: conservative daily price/FX refresh, deduplicated news, material-event alerts.
- Product options later: auth, multi-tenancy, billing and support only after personal use and demand validation.

## Zero-cost CI rule
Run `./run_tests.sh` locally before each commit. Do not enable GitHub-hosted Actions until billing settings are verified: private repositories have included monthly minutes, but usage beyond the allowance can be billable. A self-hosted runner is free from Actions-minute charges but adds maintenance and security work, so it is not justified yet.
