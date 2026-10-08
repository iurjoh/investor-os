# Goals and scenarios (phase 4)

Invented editable defaults only; no personal targets copied into this demo.
Separate annual external contributions from monthly estimated net income.

Annual capital = previous capital * (1 + total return) + year-end contribution.
Total return includes reinvestment. Do not add dividend yield to it again.
Monthly net income = end-year capital * assumed gross yield * (1 - withholding) / 12.
Purchasing-power capital = nominal capital / compounded assumed inflation.

Return/yield/withholding/inflation are constant hypothetical rates, not sourced
forecasts, guarantees, tax calculations or advice. Nominal income targets do not
rise with inflation in this simple model; purchasing-power capital is shown
separately. Corporate actions, fees, taxes on gains and variable contributions
are outside the model. Total return is limited to -100 to 100%, other rates to 0-100%, horizon to 1-50 whole years.

Fixed-point BigInt with 8 places, half-up multiplications; division truncates at
8 places. Raw goal progress can exceed 100%; only its display bar is capped.
Inputs are memory-only, resettable and not sent to a service.

Run `node tests/test_scenarios.js` for formula, no double-counting, zero/invalid
inputs, horizon, over-goal and inflation cases. Not retirement-date promises.
