# Investor OS V1 — Spreadsheet Specification

## Product goal

A sellable Google Sheets investment dashboard for long-term individual investors. The workbook must be understandable without live support, use deterministic formulas, expose inputs clearly, and avoid personalized buy/sell recommendations.

## Workbook tabs

1. `START HERE` — setup instructions and workflow.
2. `SETUP` — portfolio configuration and goals.
3. `ASSETS` — asset master data.
4. `TRANSACTIONS` — source ledger for buys, sells, dividends, fees, deposits and withdrawals.
5. `DIVIDENDS` — dividend event/receipt register.
6. `PRICES` — current price and FX inputs.
7. `HOLDINGS` — calculated positions and performance.
8. `ALLOCATION` — calculated allocation by dimension and optional targets.
9. `GOALS` — progress toward portfolio, dividend and contribution goals.
10. `DASHBOARD` — summary metrics and charts.
11. `CHECKS` — reconciliation and error checks.
12. `SAMPLE DATA` — removable example portfolio.

## 1. START HERE

Purpose: explain the workbook in under five minutes.

Sections:
- What this tool does.
- What it does not do.
- 5-step setup: configure → add assets → enter transactions → update prices/FX → review dashboard.
- Legend: blue/input, gray/calculated, warning/error.
- Important convention: amounts remain in transaction currency and are converted to portfolio base currency using the explicit FX input.
- Data quality warning: prices, dividend data, FX and tax values must be verified by the user.

## 2. SETUP

Inputs:
- Portfolio name
- Base currency: SEK, USD, EUR, GBP, BRL
- Starting cash
- Annual dividend target
- Portfolio value target
- Monthly contribution target

Calculated/displayed:
- Current portfolio value
- Current annualized dividend income
- Current monthly contribution average
- Goal progress percentages

## 3. ASSETS

Columns:
- Asset ID
- Ticker
- Asset name
- Asset type
- Sector
- Country/Region
- Currency
- ISIN
- Active?

Allowed asset types:
- Stock
- REIT
- ETF
- Fund
- Bond
- Crypto
- Cash
- Other

## 4. TRANSACTIONS

One row per transaction.

Columns:
- Transaction ID
- Date
- Ticker
- Transaction type
- Quantity
- Price
- Gross amount
- Fees
- Tax
- Currency
- FX rate to base
- Base-currency amount
- Notes

Transaction types:
- Buy
- Sell
- Dividend
- Fee
- Deposit
- Withdrawal

Formula principle:
- Buy cash impact = -(gross + fees + tax)
- Sell cash impact = +(gross - fees - tax)
- Dividend cash impact = +(gross - tax)
- Fee cash impact = -fees
- Deposit = +gross
- Withdrawal = -gross

The ledger remains the source of truth for capital flows.

## 5. DIVIDENDS

Columns:
- Date
- Ticker
- Ex-date
- Payment date
- Shares
- Dividend/share
- Gross dividend
- Withholding tax
- Net dividend
- Currency
- FX rate to base
- Gross base currency
- Tax base currency
- Net base currency
- Notes

Dashboard aggregations:
- Dividend YTD
- Dividend by month
- Dividend by asset
- Gross vs withholding vs net
- Estimated annual dividend income
- Progress toward annual dividend target

## 6. PRICES

Columns:
- Date
- Ticker
- Current price
- Price currency
- FX rate to base
- Base-currency price
- Source
- Last verified

V1 uses manually entered prices and FX. Automation is a later phase.

## 7. HOLDINGS

Calculated from transactions and current prices.

Columns:
- Ticker
- Asset name
- Asset type
- Sector
- Country/Region
- Currency
- Shares/Units
- Average cost
- Total cost basis
- Current price
- Current value
- Portfolio weight
- Unrealized gain/loss
- Unrealized gain/loss %
- Dividend yield (manual input)
- Dividend yield on cost
- Estimated annual dividend income

Core formulas:
- Shares = buys − sells
- Cost basis = cumulative acquisition cost adjusted for sold quantity using the chosen V1 cost-basis convention
- Current value = shares × current price × FX rate
- Portfolio weight = current value / total portfolio market value
- Unrealized gain/loss = current value − remaining cost basis
- Unrealized gain/loss % = unrealized gain/loss / remaining cost basis
- Estimated annual dividend income = current shares × dividend/share, when supplied
- Dividend yield on cost = estimated annual dividend income / remaining cost basis

V1 cost-basis convention: weighted-average cost. The workbook must state this explicitly and not imply FIFO/tax-lot accounting.

## 8. ALLOCATION

Allow dimension selector:
- Asset
- Sector
- Asset type
- Country/Region
- Currency

For each category:
- Current value
- Current weight
- Target weight (optional)
- Difference
- Status

Status logic:
- No target → `INFO`
- Difference within configurable tolerance → `OK`
- Difference outside tolerance → `REVIEW`

No automatic buy/sell recommendation.

## 9. GOALS

Rows:
- Portfolio value
- Annual dividend income
- Monthly contribution

Columns:
- Current
- Target
- Progress %
- Remaining
- Target date

Progress is capped visually at 100% but raw values remain available for audit.

## 10. DASHBOARD

Top KPI cards:
- Portfolio value
- Total contributed capital
- Estimated gain/loss
- Dividend YTD
- Estimated annual dividend income
- Portfolio yield
- Number of holdings
- Largest holding weight

Charts:
- Portfolio value over time
- Dividend income by month
- Sector allocation
- Asset-type allocation
- Contributions over time

The dashboard must remain usable with an empty portfolio and with at least 10 holdings.

## 11. CHECKS

Required checks:
- Allocation total approximately 100%
- No negative holdings
- No missing ticker metadata
- No missing FX when transaction currency differs from base currency
- No missing current price for active holdings
- Dividend net = gross − withholding tax
- Transaction type is valid
- Currency is valid
- Goal targets are non-negative
- Duplicate transaction IDs
- Dividend records reconciled with dividend transactions where both are used

Severity levels:
- `ERROR` — calculation may be unreliable.
- `WARNING` — data incomplete but dashboard may still work.
- `OK` — no detected issue.

## 12. SAMPLE DATA

Use a deliberately diversified fictional portfolio containing:
- US stock
- US REIT
- Canadian stock
- Swedish asset
- ETF
- Crypto

Include buys, a partial sell, dividends, fees, deposits and withdrawals. Sample data must be clearly marked and removable without breaking formulas.

## Calculation and audit rules

1. Never hide a critical assumption.
2. AI is not used for financial arithmetic.
3. Spreadsheet formulas are deterministic and inspectable.
4. FX conversion is explicit.
5. Tax treatment is informational, not tax advice.
6. Market prices and dividend data are user-verified in V1.
7. No performance guarantee or personalized investment recommendation.

## V1 acceptance test

A new user should be able to:
1. Configure a portfolio in under 10 minutes.
2. Add at least 10 assets.
3. Enter buys, sells, dividends and cash movements.
4. Update prices and FX.
5. Reconcile holdings and dividends.
6. See allocation, goals and dashboard metrics.
7. Resolve every `ERROR` shown in `CHECKS`.
8. Remove sample data without breaking the workbook.
