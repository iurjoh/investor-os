# Synthetic portfolio test

Status: calculation-core CLI, not a web dashboard. All companies, quantities,
amounts, dates and FX rates in this fixture are invented from scratch. The
fixture is not an anonymized broker export. It has no account identifiers.

## Run

From the repository root with Python 3 and no external dependencies:

```sh
sh run_tests.sh
PYTHONPATH=src python3 -m investor_os.sample_portfolio
# Optional: write the fixture to a new local file. Existing files are rejected.
PYTHONPATH=src python3 -m investor_os.sample_portfolio --write-sample /tmp/investor-os-demo.csv
```

Each CLI run loads the same embedded CSV into memory and calls the existing
Decimal weighted-average calculation core. Nothing is stored or uploaded.
Reset means rerunning the command; delete an optional exported CSV locally.
No network request, dependency installation or hosted CI is needed.

## Format and expected result

Columns: `transaction_id,date,ticker,mic,name,kind,quantity,gross_amount,fees,tax,fx_rate`.
Dates use ISO format and decimals use a period. `kind` is `buy` or `sell`.
All money fields in a row share a currency; `fx_rate` converts that currency
to SEK. Asset identity is ticker + MIC. IDs must be unique. Chronological
ordering uses date then transaction ID, so IDs must preserve same-day order.
`load_trades(text)` and `summarize(text)` accept this normalized format only;
they are not broker CSV importers and perform no deduplication or repair.

Seven invented transactions demonstrate a partial sale, full liquidation,
repurchase, fees and FX across three invented companies:

| Synthetic asset | Final units | Remaining cost, SEK |
| --- | ---: | ---: |
| Fictional Aurora Workshop | 15 | 2265 |
| Fictional Blue Orchard | 8 | 1620 |
| Fictional Cedar Observatory | 3 | 742 |
| Total cost basis | | 4627 |

Cost basis is not market value or portfolio performance. The output contains
an explicit synthetic-data label. There are no prices, dividend forecasts,
cash balances or investment recommendations in this CLI.

## Verification

2026-10-07: 14 local unittest tests passed, comprising four existing core tests
and ten sample-loader tests. Coverage includes exact expected totals, empty
portfolio, repeatability, reversed input ordering, ticker/MIC identity,
duplicate IDs, invalid columns/values, extra fields, conflicting names and
overselling. CLI output reconciled to the table above. Export created a fresh
CSV and refused to overwrite it. This is not UI or end-to-end web verification.

## Privacy boundary and next steps

The source repository is public. Only wholly fictional data belongs in source,
fixtures, issues, screenshots or public demos. Real exports must never be
committed, uploaded to this landing, or disguised as public sample data.

A future private app requires a separately designed private runtime with
login and authorization, data outside Git, private storage and backups,
validated import/reconciliation, retention/deletion controls and security
checks before any real data is loaded. A private repository or a login screen
alone does not establish data safety. No such app is delivered by this change.

The older snapshot fixture and product workbook CSV are separate historical
examples; neither is consumed by this test. No repository visibility,
landing deployment, remote database or workflow configuration was changed.
