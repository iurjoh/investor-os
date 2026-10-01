# Investor OS V1 — User Guide / Private Beta

## 1. What Investor OS does

Investor OS is a spreadsheet-based portfolio organization tool. It helps you record investments and dividends, monitor allocation and income, and track financial goals.

It is an educational and portfolio-organization tool. It is not a broker, automated trading system, personalized investment adviser or tax filing system.

## 2. Before you start

You need:

- Excel, LibreOffice Calc or a compatible spreadsheet application.
- Your current holdings and transaction information.
- Current prices for your assets.
- FX rates when an asset or transaction is not in your portfolio base currency.
- Optional dividend information and portfolio goals.

For best results, collect information from your broker statements or another source you trust.

## 3. Quick setup — target: under 10 minutes

### Step 1 — START HERE

Read the conventions and warnings. Identify which cells are inputs and which are calculated.

### Step 2 — SETUP

Enter:

- Portfolio name
- Base currency: SEK, USD, EUR, GBP or BRL
- Starting cash, if applicable
- Annual dividend target, if you use one
- Portfolio value target, if you use one
- Monthly contribution target, if you use one

### Step 3 — ASSETS

Create one row for each asset.

Complete:

- Ticker
- Asset name
- Asset type
- Sector
- Country/region
- Currency
- ISIN, when available
- Active status

Use one consistent ticker per asset throughout the workbook.

### Step 4 — TRANSACTIONS

Enter deposits, purchases, sales, dividends, fees and withdrawals.

For investment transactions, enter the original transaction currency and the FX rate to the portfolio base currency.

Keep transaction dates in chronological order for each ticker. This is required for the V1 weighted-average cost-basis calculation.

### Step 5 — DIVIDENDS

Record dividend payment information separately when you want dividend reporting.

Enter gross amount, withholding tax, net amount and FX. The workbook checks that the net amount reconciles with gross minus withholding.

### Step 6 — PRICES

Enter the latest price and FX rate for each holding. Record the source and verification date.

V1 uses manual prices and FX rates.

### Step 7 — HOLDINGS

Review the calculated positions. Check:

- Shares/units
- Average cost
- Cost basis
- Market value
- Portfolio weight
- Unrealized P/L
- Dividend income

Do not overwrite calculated cells.

### Step 8 — CHECKS

Resolve all errors before relying on the dashboard.

An `OK` result means the corresponding validation passed. An `ERROR` result means the workbook needs attention.

### Step 9 — DASHBOARD

Use the dashboard for the high-level view of portfolio value, contributions, P/L, dividends, yield and concentration.

### Step 10 — GOALS

Review progress against the targets configured in SETUP.

## 4. How to update the workbook

A practical monthly routine is:

1. Add new deposits/withdrawals.
2. Add buys and sells.
3. Add dividend payments.
4. Update current prices and FX rates.
5. Review HOLDINGS.
6. Review ALLOCATION.
7. Resolve CHECKS errors.
8. Review DASHBOARD and GOALS.

## 5. Important rules

### Do not mix transaction and reporting concepts

A dividend is recorded as dividend income. It is not a new capital contribution.

### Use the correct FX rate

The workbook distinguishes the original currency from the portfolio base currency. Do not enter a converted amount as though it were the original transaction amount.

### Do not sell more than you own

A negative position is an error in V1 and should be corrected before using portfolio totals.

### Keep prices current

A stale or missing price can make market value and portfolio weight misleading. V1 therefore surfaces missing prices instead of silently estimating them.

### Preserve the formulas

Do not type over calculated cells. If a calculated result looks wrong, inspect the relevant input rows and the CHECKS sheet first.

## 6. Understanding the main numbers

### Cost basis

The remaining acquisition cost of the position after accounting for sales using weighted-average cost.

### Market value

Current quantity multiplied by current price and the applicable FX rate.

### Unrealized P/L

Market value minus remaining cost basis.

### Portfolio yield

Estimated annual dividend income divided by current portfolio market value.

### Yield on cost

Estimated annual dividend income divided by the remaining cost basis of the holding.

These are portfolio-organization metrics and should not be interpreted as forecasts or guarantees.

## 7. Private beta checklist

Beta testers should perform the following tasks with a copy of the workbook:

- Configure a new portfolio.
- Add at least 10 assets.
- Enter several buys.
- Enter at least one sale.
- Enter dividends with withholding tax.
- Include at least one USD asset in a SEK portfolio, or another non-base currency.
- Update prices and FX.
- Check HOLDINGS against the user's own calculations or broker records.
- Check that allocation reconciles.
- Check dividend reconciliation.
- Set at least one goal.
- Remove the sample data and confirm the workbook still works.
- Intentionally leave one price or FX field blank and confirm CHECKS identifies the problem.

## 8. Beta feedback

Report issues using this structure:

**Area:** START HERE / SETUP / ASSETS / TRANSACTIONS / DIVIDENDS / PRICES / HOLDINGS / ALLOCATION / GOALS / DASHBOARD / CHECKS

**What I tried:**

**What I expected:**

**What happened:**

**Severity:** Blocking / Major / Minor / Cosmetic

**Spreadsheet application:** Excel / LibreOffice / Other

Screenshots are useful when the problem is visual.

## 9. V1 boundaries

The beta intentionally does not include live prices, broker imports, automated dividend calendars, personalized security recommendations, tax filing, automated trading, CAGR/XIRR, TWR, correlation, beta or Monte Carlo projections.

Those features may be evaluated after the core V1 workflow has been validated by real users.

## 10. Beta success criteria

V1 is considered ready for a broader paid release when independent testers can complete the core workflow without live assistance, calculations reconcile with their source data, errors are understandable, and the workbook remains functional after sample data is removed.
