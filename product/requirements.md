# Investor OS — V1 Product Requirements

## 1. Product purpose

Investor OS V1 is a spreadsheet-first investment dashboard for individual investors. It helps users record investments and dividends, understand portfolio allocation, monitor performance, and track progress toward financial goals.

The product must be simple enough for a beginner to configure and useful enough for an experienced buy-and-hold investor to keep using.

## 2. Target user

Primary user:
- Individual long-term investor
- Holds stocks, REITs, ETFs, or similar listed assets
- Wants portfolio and dividend visibility without building a spreadsheet from scratch
- May invest in more than one currency
- Values transparency and control over calculations

V1 should work especially well for dividend-focused investors, but must not depend on dividends as the only investment strategy.

## 3. Core user outcomes

After setup, a user should be able to:
1. Enter holdings and transactions.
2. See current portfolio value and cost basis.
3. See allocation by holding and sector.
4. Record and summarize dividend income.
5. Track contributions over time.
6. Define portfolio and income goals.
7. Understand whether the portfolio is becoming more or less concentrated.
8. Audit the underlying transactions and formulas.

## 4. V1 modules

### 4.1 Setup

Inputs:
- Base currency
- Portfolio name
- Starting cash balance
- Optional target allocation
- Optional annual dividend target
- Optional portfolio value target

Supported currencies should initially include SEK, USD, EUR, GBP and BRL.

### 4.2 Holdings

Fields:
- Ticker/symbol
- Asset name
- Asset type
- Sector
- Country/region
- Currency
- Shares/units
- Average cost per unit
- Total cost
- Current price
- Current value
- Portfolio weight
- Unrealized gain/loss
- Unrealized gain/loss %
- Dividend yield when manually supplied
- Estimated annual dividend income

V1 must allow manual price updates. Automated market-price APIs are not required for the first sellable version.

### 4.3 Transactions

Transaction types:
- Buy
- Sell
- Dividend
- Fee
- Deposit
- Withdrawal

Fields:
- Date
- Ticker/asset
- Transaction type
- Quantity
- Price
- Gross amount
- Fees
- Tax/withholding
- Currency
- FX rate to base currency
- Notes

Calculations should derive portfolio quantities and cash-flow summaries from transaction data wherever practical.

### 4.4 Dividends

Display:
- Dividend income by month
- Dividend income by year
- Dividend income by asset
- Gross dividends
- Withholding tax
- Net dividends
- Annualized dividend income
- Progress toward dividend goal

### 4.5 Allocation

Views:
- By asset
- By sector
- By asset type
- By country/region
- By currency

Allow optional target weights and show:
- Current weight
- Target weight
- Difference

V1 should flag large deviations but should not issue personalized buy/sell recommendations.

### 4.6 Dashboard

Primary KPIs:
- Portfolio value
- Total contributed capital
- Estimated gain/loss
- Dividend income YTD
- Estimated annual dividend income
- Portfolio yield
- Number of holdings
- Largest holding weight

Charts:
- Portfolio value over time
- Dividend income by month
- Allocation by sector
- Allocation by asset
- Contributions over time

### 4.7 Goals

Supported goals:
- Portfolio value target
- Annual dividend target
- Monthly contribution target

Display current value, target, progress %, and required remaining amount.

## 5. Calculation rules

All financial calculations must be deterministic and inspectable. AI must not calculate portfolio balances or return figures.

Minimum calculations:
- Total cost basis
- Current market value
- Unrealized P/L
- Unrealized P/L %
- Portfolio weight
- Dividend income
- Dividend yield on cost
- Current portfolio yield based on estimated annual dividends
- Contribution totals
- Goal progress

Currency conversion must clearly distinguish the transaction currency, asset currency, and portfolio base currency.

V1 should avoid claiming tax accuracy. Tax fields are for user-recorded information and reporting convenience only.

## 6. User experience requirements

- Clear separation between inputs and calculated fields.
- No hidden formulas where avoidable.
- Include an Instructions/Guide sheet.
- Include sample data that demonstrates the product.
- Include a clean empty-template state.
- Minimize required manual fields.
- Protect formula cells from accidental editing where the platform allows it.

## 7. Product format

V1 delivery format: Google Sheets template plus PDF/online user guide.

The product should be designed so that its logic can later be migrated to a web application without changing the conceptual data model.

## 8. Compliance and positioning

Investor OS is an educational and portfolio-organization tool. It is not:
- A broker
- An automated trading system
- A personalized investment advisory service
- A tax filing system
- A guarantee of investment performance

Marketing must avoid promises of returns or individualized securities recommendations.

## 9. V1 acceptance criteria

The V1 is ready for private beta when:
- A new user can configure the template in under 10 minutes.
- A user can add at least 10 holdings.
- A user can record buys, sells and dividends.
- Dashboard totals reconcile with transaction/holding inputs.
- Allocation percentages reconcile to approximately 100% when applicable.
- Dividend summaries reconcile with recorded dividend transactions.
- Currency conversion is visible and understandable.
- Sample data can be deleted without breaking formulas.
- Formula/input errors are clearly surfaced.
- A second person can use the template from the guide without live assistance.

## 10. V1.1 candidates

After beta validation:
- CAGR/XIRR
- Time-weighted return
- Correlation matrix
- Volatility and beta
- Monte Carlo projections
- Rebalancing helper
- Automated market-price import
- Automated dividend-calendar import
- Multi-portfolio support
- More advanced risk dashboard

These features must not delay the first sellable V1.
