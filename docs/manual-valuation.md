# Manual synthetic valuation (phase 3)

Only invented demonstration positions and inputs are supported. Inputs remain in
page memory; they are not saved, synced or sent to a service. Reset restores the
fictional snapshot. Never use this public demo as private financial storage.

Market value = quantity * local price * SEK-per-local-currency FX.
Unrealized result = market value - remaining portfolio cost basis. This is not
total return, cash-flow-adjusted performance or a tax calculation.

The browser uses fixed-point BigInt arithmetic with 8 decimal places and rounds
half-up at each multiplication. Input decimals use a period and at most 8 places.
This is a bounded UI arithmetic convention, not the arbitrary-precision Python
ledger. Base-currency FX must be 1; missing price/FX makes the portfolio total and
result unavailable. A known subtotal and its sector/currency exposure are
explicitly partial. Zero price is distinct from missing price.

All price/FX inputs have a date and fictional source label. Future/invalid dates
are rejected. Older dated snapshots are labelled, not marketed as current feeds.
Sector and currency assignments belong to the fixed invented fixture.

Run `node tests/test_valuation.js` for expected snapshot, missing data, zero price,
empty positions, invalid numbers, decimal precision, date and FX checks.
No paid quotes, trading instructions or real import are included.
