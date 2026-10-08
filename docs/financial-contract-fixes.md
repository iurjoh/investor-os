# Financial contract corrections (synthetic only)

This draft fixes the four high-priority findings from the independent review.
It does not certify tax treatment or broker imports. No personal data is used.

## Ordering

A transaction ID identifies a record, not execution order. Multiple trades for
one position on the same date now need a unique non-negative safe integer `sequence` (maximum 9007199254740991)
per position/date. The source must establish the execution order. Missing,
duplicate or invalid sequence fails closed; input row order is not inferred.
Single-trade dates keep compatibility. The normalized fictional CSV accepts
an optional `sequence` column. Older ambiguous same-day CSV files are rejected.
The JSON validator enforces the same rule before exact rational ledger replay.
Do not synthesize sequence from IDs or guess it from an unsorted export.

## Reconciliation

The JSON contract replays buys/sells, FX and acquisition fees/tax against every
holding. Rational arithmetic avoids binary-float cost drift; reported costs
use the existing 0.000001 SEK absolute reconciliation tolerance. Quantity must
match exactly. It rejects oversells even when holdings were made to look valid.
Sale proceeds/fees do not change remaining acquisition cost.
Monthly and annual income buckets are recomputed from payment dates and statuses.
Missing, extra and changed buckets fail. Refunds remain separate from dividends;
unknown expected amounts remain missing, not zero-value confirmed receipts.

## FX

Known SEK-to-SEK rates must numerically equal 1. Zero FX in any decimal spelling
is rejected in Python and JavaScript. Missing FX on an unconfirmed foreign event
remains unknown. These checks are not historical FX source verification.

## Test locally before approval

From the checked-out draft branch, with Python 3.10+ and Node:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests
for f in tests/*.js; do node "$f"; done
```

The regressions include same-day A-buy100/C-sell/B-buy300 -> remaining cost300;
missing/duplicate execution sequence; valid oversell rejection; modified trade
amount/fees/quantity/FX; modified/missing monthly and annual buckets; SEK FX2;
and fully recomputed zero-FX0.0 events. Python-generated fixture output is also
fed through the JavaScript validator. All inputs are fictional.

Not included: intermediate valuation rounding, new tax/account models, private
import/storage, workbook repairs, deployment or merge. Approval of this draft
and the user's test are required before merge.
