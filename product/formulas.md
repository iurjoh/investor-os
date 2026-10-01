# Investor OS V1 — Calculation Rules

These rules are the calculation contract for the spreadsheet and future web application.

## Notation

- `Q` = quantity
- `P` = price per unit
- `FX` = units of portfolio base currency per unit of transaction/asset currency
- `C` = portfolio base currency

## Transaction conversion

`Base Amount = Original Currency Amount × FX`

The FX rate must be recorded with the transaction or valuation input. Do not infer historical FX from today's rate.

## Position quantity

For each asset:

`Quantity = Σ Buy Quantity − Σ Sell Quantity`

Dividend, fee, deposit and withdrawal rows do not change quantity.

## Weighted-average cost basis

For each buy:

`Acquisition Cost = Gross Amount + Fees + Tax`

Average cost is recalculated after each buy:

`New Average Cost = (Previous Cost Basis + New Acquisition Cost) / (Previous Quantity + New Quantity)`

For a sale:

`Cost Removed = Sold Quantity × Current Average Cost`

`Remaining Cost Basis = Previous Cost Basis − Cost Removed`

This is a portfolio-management convention, not a tax-lot method.

## Market value

`Market Value Base = Quantity × Current Price × Current FX`

## Unrealized gain/loss

`Unrealized P/L = Market Value Base − Remaining Cost Basis Base`

`Unrealized P/L % = Unrealized P/L / Remaining Cost Basis Base`

If remaining cost basis is zero, percentage return displays `N/A` rather than an error.

## Portfolio weight

`Weight = Asset Market Value / Total Portfolio Market Value`

If total portfolio market value is zero, weight displays `N/A`.

## Dividend income

`Gross Dividend = Shares × Dividend Per Share`

`Net Dividend = Gross Dividend − Withholding Tax`

`Net Dividend Base = Net Dividend × FX`

## Dividend yield on cost

`Yield on Cost = Estimated Annual Dividend Income / Current Remaining Cost Basis`

## Current portfolio yield

`Portfolio Yield = Estimated Annual Dividend Income / Current Portfolio Market Value`

## Contributions

`Net Contributions = Deposits − Withdrawals`

Dividends are investment income and are not treated as external contributions.

## Goal progress

`Progress = Current / Target`

For display only:

`Display Progress = MIN(MAX(Progress, 0), 1)`

Keep the raw progress value available for audit.

## Reconciliation tolerances

Because spreadsheets may contain rounding differences:

- Allocation total: acceptable range `99.5%–100.5%`.
- Currency conversions: compare rounded display values separately from raw values.
- Dividend reconciliation: use a small configurable tolerance rather than forcing exact equality after rounding.

## Missing-data behavior

- Missing FX for a non-base-currency value → `ERROR`.
- Missing current price for a held asset → `ERROR` for market-value metrics.
- Zero quantity → omit from active holdings display.
- Negative quantity → `ERROR`.
- Missing dividend/share → annual dividend estimate remains unavailable; do not assume zero.

## Separation of responsibilities

Spreadsheet formulas calculate arithmetic and aggregation.

AI may explain results, summarize trends, identify data-quality issues, or produce educational content, but it must not replace deterministic portfolio calculations.
