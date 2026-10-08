# Synthetic multi-currency example (phase 6)

The new currencies tab is a separate invented one-account/one-position example,
not a migration of the existing SEK portfolio or a real importer. Its local
currency and account base are selected from a bundled searchable ISO list.
No personal data, saved account settings, network FX feed or broker is involved.

## Currency metadata

`web/currencies.json` is the current currency/funds list retrieved from SIX on
2026-10-08, published 2026-09-17. SIX maintains ISO 4217:
https://www.six-group.com/en/products-services/financial-information/market-reference-data/data-standards.html
Source XML:
https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml
178 unique codes are bundled. Codes with no numeric minor-unit designation use
the browser's formatting convention; unit-precision arithmetic stays at 8 places.
A list snapshot is not guaranteed to include future currency changes. Refresh it
explicitly from the official source, not from arbitrary unvalidated user codes.
VND has 0 display minor units in this snapshot; SEK/USD have 2. These are display
rules, never intermediate rounding or exchange-rate evidence.

## Calculation and provenance

Local market value = quantity * local price.
Base market value = local market value * base-units-per-local-unit FX.
The pair is explicit (1 VND = X SEK), never an unlabeled interchangeable rate.
Price and market FX dates must match and cannot exceed valuation date. Their
source is entered manually and displayed as an invented example.

Cost retains original currency, local amount and operation date. A different
base needs that operation's own FX for the destination base, not today's rate.
Changing the market price/FX never edits original cost or the historical rate.
Explicitly editing the separate historical FX is a correction to that assumption.
Missing historical FX leaves cost/result unavailable but can leave market value
known. Missing market FX makes the complete portfolio total unavailable, not 0.
Same-currency conversion is identity 1. Inverted/mismatched pairs are rejected.

Default invented example: 10 units * 25,000 VND = 250,000 VND. Fictional market
FX 0.0004 SEK/VND gives 100 SEK (or invented 0.00004 USD/VND gives 10 USD).
Original invented 200,000 VND cost uses operation FX 0.0005 SEK/VND (100 SEK).
No default rate is a real quotation. No cross-rate/triangulation is inferred.

Changing local currency starts a NEW invented example and clears historical and
market FX; it never re-labels a real immutable operation. Changing account base
keeps source cost, with separate stored in-memory historical rates per base.
Only one demonstration account is provided. Multi-account consolidation and
real ledger migration are future work requiring their own checks and approval.

Fixed-point BigInt arithmetic: 8 decimal places, half-up multiplication. Inputs
have at most 15 integer digits and 8 fractional places. Missing is distinct from
zero. No persistence or export of edited inputs; reset restores invented defaults.

## Checks

`node tests/test_multicurrency.js`: 24 cases, including VND/SEK/USD/identity,
missing/current vs historical FX, cost invariance, wrong pair/date, non-finite or
negative data, duplicate positions, unknown codes, zero quantity and VND display
precision. Browser checks include base switching, missing/invalid fail-closed,
new local currency, reset and mobile overflow. No real-data use is certified.
