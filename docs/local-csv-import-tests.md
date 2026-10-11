# Local normalized CSV guardrails

Scope: the stateless Python synthetic-trade loader, not an Avanza importer, a
private application, database persistence, or backup/restore. All inputs are
invented from `SAMPLE_CSV`. No account files, real holdings or broker exports
were accessed. No network or production data path was added.

## Expected behavior and observations

| Scenario | Before this patch | Required behavior after patch |
| --- | --- | --- |
| Duplicate header | A repeated column could overwrite the original value. Repeated `fees` changed a one-trade cost from 1010 to 1999. | Reject duplicate column names before mapping any rows, including optional `sequence`. |
| Text after closing quote | `"Fictional Aurora"junk` was accepted as `Fictional Aurorajunk`. | Reject parser-detected malformed quoting with `ValueError`, not silent repair. |
| Unterminated quoted field | Rejected as missing row fields in the tested input. | Reject with a CSV syntax error translated to `ValueError`. |
| Missing required header/value or short row | Rejected. | Continue rejecting every required missing column, empty value and short row. Fees and tax cannot silently default to zero. |
| Unknown column/extra cell | Rejected. | Continue rejecting instead of dropping extra input. |
| Invalid date, decimal, nonfinite/negative amount, zero FX/quantity | Rejected. | Continue rejecting. Quoted comma decimals are not converted. |
| Valid rows followed by an invalid row | Exception, no returned partial portfolio. | Continue returning nothing on failure. Previously returned results remain unchanged. This is not a database rollback test. |
| Same batch repeated inside one CSV | Duplicate transaction ID rejection. | Reject the whole input, never silently double-count. |
| Existing ID with changed amount in the same CSV | Rejected. | Reject, never silently update. |
| Same valid CSV loaded in two separate calls | Equal output, seven transactions each time. | Continue producing equal independent results; mutation of one returned object must not affect the next call. |
| Quoted comma/newline/escaped quote, CRLF, reordered columns | Accepted. | Preserve valid values and calculation output. |
| Blank lines/header only | Blank lines ignored; header-only input gives an empty portfolio. | Keep these explicit existing conventions. Empty/no-header file is invalid. |

Duplicate headers were previously hidden by a set comparison and Python's row
dictionary overwriting repeated keys. The patch checks header uniqueness first,
uses the standard-library CSV parser's strict mode, and translates `csv.Error`
into the loader's existing `ValueError` interface. Strict mode is not a claim
of exhaustive RFC conformance or broker-format compatibility.

## Reproduce locally

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -p test_csv_import.py -v
sh run_tests.sh
node tests/test_data_contract.js
node tests/test_multicurrency.js
node tests/test_scenarios.js
node tests/test_valuation.js
```

Local evidence, 2026-10-11, base `c9b1753`:

- Baseline: 34 Python tests passed.
- New suite on the unmodified loader: 16 test methods, 10 failed assertions
  across two methods (duplicate-header subcases and quote-junk regression).
- After correction: 50 Python tests passed, including 16 new methods.
- Separate non-browser JavaScript suites: 107 checks passed (49 + 24 + 19 + 15).
- `git diff --check` passed.
- Browser journey/language suites were not run successfully: this environment
  lacked `@playwright/test`. No UI/deployment assertion is made by this work.

## Still required before persistent private imports

This loader has no existing ledger, batch store, transaction commit or import
UI. Separate calls do not append anything, so equal output is determinism,
not proved persistent idempotency. A future private importer must separately
prove repeat-batch deduplication, same-ID collision review, all-or-nothing
storage, source hashes, reconciliation, offline/privacy boundaries, and backup
restore using invented data. These tests do not authorize any real-data trial.
