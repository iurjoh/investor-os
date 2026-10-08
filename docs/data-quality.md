# Synthetic demo data contract (phase 1)

The fixture is entirely invented. Its ISO date is the fixture's effective date,
not a current market quote or the owner's real portfolio snapshot.

The browser checks schema version, synthetic label, finite non-negative decimal
strings, dates, IDs, asset identity, money/currency fields, and reconciles the
holding cost total before rendering. Invalid or missing input fails the view
without estimating values. Empty portfolios are valid; zero total cost has no
allocation percentage. Display rounding does not change Python Decimal values.

Acquisition cost = (gross amount + fees + tax) * transaction FX to SEK.
A partial sale removes units at the previous weighted average cost. This is a
portfolio cost convention, not tax reporting. The ledger shows original currency,
fees, tax and the SEK-per-currency FX convention. Costs are not market values.

Run `sh run_tests.sh`, `python3 build_demo.py`, and
`node tests/test_data_contract.js`. Node is a development-only test runner; the
static demo has no package dependencies, login, storage, importer or paid API.

Python validates amounts even when callers bypass CSV loading. It rejects
non-finite values, negative amounts, zero quantity/FX and duplicate IDs.
The browser's numerical checks are validation/display checks, not a replacement
for the deterministic Python calculation engine.

Privacy: do not add real broker rows, sheet identifiers, holdings, account data
or personal targets to public fixtures, screenshots or issue/PR descriptions.
