# Investor OS — V1 XLSX Implementation

## Purpose

This document maps the V1 product specification to the implemented Excel/LibreOffice-compatible workbook. The workbook is the first sellable implementation of Investor OS and is designed to preserve the same conceptual data model planned for the future web application.

## Workbook structure

### Visible sheets

1. `START HERE` — product purpose, setup instructions, conventions, warnings and legend.
2. `SETUP` — portfolio name, base currency, starting cash, dividend/value/contribution goals and calculated snapshots.
3. `ASSETS` — master asset register and metadata.
4. `TRANSACTIONS` — transaction ledger and base-currency conversion.
5. `DIVIDENDS` — dividend records, withholding and reconciliation.
6. `PRICES` — manually maintained prices and FX rates.
7. `HOLDINGS` — calculated positions, cost basis, market value, P/L and income.
8. `ALLOCATION` — allocation by asset, sector, asset type, country/region and currency.
9. `GOALS` — progress against portfolio, dividend and contribution goals.
10. `DASHBOARD` — principal KPIs and charts.
11. `CHECKS` — data-quality and reconciliation checks.
12. `SAMPLE DATA` — removable example data for onboarding/testing.

### Hidden calculation sheet

`LEDGER_CALC` contains the running position calculation used to handle buys and sells correctly under the V1 weighted-average cost-basis method.

## Data model

The spreadsheet uses the following conceptual entities:

- Portfolio
- Asset
- Transaction
- Dividend
- Price/FX snapshot
- Goal
- Target allocation

These correspond closely to the tables planned in `database/schema.sql` for the future Supabase implementation.

## Calculation architecture

Financial arithmetic is deterministic and spreadsheet-based. AI is not required for V1 calculations.

### Transaction amounts

`Base Amount = Original Currency Amount × FX Rate`

Cash effects:

- Buy: `-(Gross + Fees + Tax)`
- Sell: `+(Gross - Fees - Tax)`
- Dividend: `+(Gross - Tax)`
- Fee: `-Fees`
- Deposit: `+Gross`
- Withdrawal: `-Gross`

### Position quantity

`Running quantity = Previous quantity + Buy quantity - Sell quantity`

### Weighted-average cost basis

For a purchase:

`New basis = Previous basis + (Buy quantity × Buy price + fees + tax)`

`New average cost = New basis / New quantity`

For a sale:

`Cost removed = Sold quantity × Previous average cost`

`Remaining basis = Previous basis - Cost removed`

The workbook assumes transaction rows are entered chronologically for each ticker. Selling more units than currently held is surfaced by the checks sheet.

### Market value and P/L

`Market value = Quantity × Current Price × Current FX`

`Unrealized P/L = Market Value - Remaining Cost Basis`

`Unrealized P/L % = Unrealized P/L / Remaining Cost Basis`

`Portfolio Weight = Holding Market Value / Total Portfolio Market Value`

### Dividends

`Gross dividend = Shares × Dividend per share`

`Net dividend = Gross dividend - Withholding`

`Net base dividend = Net dividend × FX`

`Yield on Cost = Estimated Annual Dividend / Remaining Cost Basis`

`Portfolio Yield = Estimated Annual Dividend / Portfolio Market Value`

The workbook includes a per-row dividend reconciliation check. The summary check reports an error if any dividend row fails reconciliation.

## Manual-input convention

V1 intentionally uses manual market prices and FX rates. Each price row includes source and last-verified fields so the user can audit the information.

The user enters raw investment information; calculated fields should not be manually overwritten.

## Error handling

`CHECKS` validates, among other items:

- Allocation reconciliation
- Negative holdings
- Missing prices
- Missing FX
- Dividend reconciliation
- Valid transaction types
- Valid currencies
- Missing asset metadata
- Goal configuration
- Duplicate transaction IDs

Missing market price or FX information is treated as an explicit error rather than silently assuming a value.

## Sample portfolio

The workbook contains 10 fictional assets covering equities, REITs and crypto across Sweden, the USA, Canada and global exposure. Sample transactions demonstrate deposits, buys, sells, dividends, fees and withdrawals.

Sample data is designed for functional testing and is not investment advice or a real portfolio recommendation.

## QA status

The V1 workbook was tested against the 20 test cases in `product/test-cases.md`, including weighted-average cost after a sale followed by further transactions, currency conversion, dividend reconciliation, allocation checks, goal progress and removal of sample data.

Release gate: all defined test cases must pass and the workbook must not contain unexplained errors with sample data.

## Known V1 boundaries

V1 does not provide:

- Automated broker connectivity
- Live market prices
- Automated dividend calendars
- Personalized buy/sell recommendations
- Tax filing or tax advice
- Automated trading
- CAGR/XIRR, TWR, correlation, beta or Monte Carlo analysis

These are candidates for V1.1 or later and must not be confused with V1 functionality.

## Migration to the web application

The workbook is deliberately structured so that the same entities and calculations can later move to Supabase/Postgres and a Next.js interface. The spreadsheet is therefore both a sellable product and a functional specification for the eventual SaaS version.
