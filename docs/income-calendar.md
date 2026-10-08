# Synthetic income and calendar (phase 2)

This builds on phase 1's data contract. All events, currencies, amounts, dates,
sources and refund examples are invented. No private workbook data is copied.

- Paid = dated receipt, reconciled explicitly, with complete gross/withholding/FX.
- Net receipt = (gross - withholding) * receipt FX; withholding is a positive amount.
- Expected net = same arithmetic with explicitly estimated inputs. Missing inputs
  remain unavailable, not zero. Known expected totals exclude incomplete events.
- KF reimbursement is a separate reconciled SEK cash flow, not a dividend or an
  automatic forecast of future recovery. Paid dividend totals exclude KF.
- A past expected payment date changes its display to pending reconciliation,
  never to received. Passing a date is not proof of a broker credit.
- Monthly/annual rows separate net received, KF received and expected known net.
- Calendar filters by asset, state, payment/ex-date and month. Unknown dates stay
  unknown; a month filter cannot place them into a made-up month.
- Source strings are clearly fictional evidence labels, not external source links.

Run `sh run_tests.sh`, `python3 build_demo.py`, `node tests/test_data_contract.js`.
Tests cover cash separation, missing data, dates/reconciliation, invalid amounts,
duplicates, FX, periods and empty data. No real import, persistence, live quote,
portfolio-return calculation, paid dependency or investment recommendation.
