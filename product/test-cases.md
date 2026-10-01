# Investor OS V1 — Test Cases

## Purpose

Validate that the spreadsheet calculations remain deterministic and that common user errors are visible.

| ID | Scenario | Expected result |
|---|---|---|
| TC01 | Deposit 10,000 SEK | Net contributions = 10,000 SEK; no asset position created |
| TC02 | Buy 10 shares at 100 SEK with 10 SEK fee | Quantity = 10; cost basis = 1,010 SEK |
| TC03 | Buy another 10 shares at 120 SEK with 10 SEK fee | Quantity = 20; weighted average cost = 106 SEK/share |
| TC04 | Sell 5 shares at 130 SEK with 5 SEK fee | Quantity = 15; cost removed = 530 SEK; remaining cost basis = 1,590 SEK |
| TC05 | Current price 140 SEK | Market value = 2,100 SEK; unrealized P/L = 510 SEK |
| TC06 | USD asset, base SEK, FX = 10 | USD 100 market value becomes SEK 1,000 |
| TC07 | USD asset with missing FX | `ERROR` for base-currency valuation |
| TC08 | Dividend gross 100, tax 15 | Net dividend = 85 |
| TC09 | Annual dividend estimate 600 and cost basis 10,000 | Yield on cost = 6% |
| TC10 | Annual dividend estimate 600 and market value 12,000 | Portfolio yield contribution = 5% |
| TC11 | Deposit 10,000, withdrawal 2,000 | Net contributions = 8,000 |
| TC12 | Portfolio has 4 assets totaling 100% | Allocation check = `OK` |
| TC13 | Portfolio allocation totals 98% | Allocation check = `ERROR` or warning according to configured tolerance |
| TC14 | Negative calculated shares after excessive sale | `ERROR` |
| TC15 | Missing current price for held asset | `ERROR` for market-value metrics |
| TC16 | Dividend gross 100, withholding 15, net entered as 90 | `ERROR` / reconciliation warning |
| TC17 | Goal current 50,000, target 100,000 | Progress = 50% |
| TC18 | Goal current 120,000, target 100,000 | Raw progress = 120%; display progress capped at 100% |
| TC19 | Empty portfolio | Dashboard loads without formula errors |
| TC20 | Sample data removed | Workbook remains functional and checks identify missing user inputs only |

## Edge cases

- Fractional shares are supported in the data model even if a user's broker does not support them.
- Zero-cost positions must not cause division-by-zero errors.
- Zero portfolio value must not create invalid allocation percentages.
- Base-currency transactions use FX = 1.
- Historical transactions use their recorded FX rather than current FX.
- Same ticker in different currencies must not silently merge into one asset.
- Selling more shares than held must be surfaced as an error.

## Release gate

V1 is not ready for sale until every test case passes in the production spreadsheet and the `CHECKS` tab reports no unexplained errors with the supplied sample data.
