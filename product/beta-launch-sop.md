# Investor OS V1 — Private Beta Launch SOP

## Purpose

Run a small, controlled beta before public launch. The objective is to validate usability, calculation trust, onboarding clarity, and willingness to use the product repeatedly.

## 1. Before inviting testers

- Confirm the current workbook is the intended beta build.
- Confirm all V1 release checks pass.
- Keep sample data clearly marked and removable.
- Confirm the Jotform feedback form is active.
- Use the language selector: Português (Brasil), English, Svenska.
- Do not promise investment returns or personalized financial advice.
- Keep the beta invitation limited to people who can provide practical feedback.

## 2. Tester flow

1. Receive the workbook and tester guide.
2. Open `START HERE`.
3. Complete `SETUP`.
4. Add several assets.
5. Add buys, sells, deposits and dividends.
6. Enter prices and FX rates.
7. Review `HOLDINGS`, `ALLOCATION`, `GOALS` and `DASHBOARD`.
8. Review `CHECKS` and investigate any errors.
9. Remove sample data and confirm the workbook remains usable.
10. Submit feedback through the Jotform form.

## 3. Feedback classification

Every issue should be classified as one of:

- **Blocker:** prevents normal use or produces materially incorrect results.
- **Calculation:** formula, reconciliation, or accounting problem.
- **UX:** confusing layout, wording, navigation, or instructions.
- **Data:** missing, unclear, or incorrectly represented input.
- **Feature request:** useful capability outside the V1 acceptance scope.
- **Documentation:** product works, but instructions are insufficient.
- **Cosmetic:** visual or formatting issue with no functional impact.

## 4. Triage order

Prioritize:

1. Incorrect financial calculations.
2. Data-loss or transaction-integrity problems.
3. Errors that prevent completion of the main workflow.
4. Ambiguous instructions that can cause incorrect inputs.
5. Repeated UX friction.
6. High-value feature requests.
7. Cosmetic improvements.

## 5. Beta decision gates

### Fix before wider beta

- Any reproducible calculation error.
- Any unresolved reconciliation error.
- Any workflow that can silently produce an incorrect balance.
- Any major misunderstanding caused by the interface or instructions.

### Can remain for V1.1

- Advanced risk analytics.
- Automated market data.
- Correlation and Monte Carlo analysis.
- Advanced performance metrics.
- Automated dividend calendars.
- Multi-portfolio features.

## 6. Release discipline

Do not change formulas, calculation rules, or core workbook structure during an active tester session without recording the change.

For every beta revision:

- increment the version identifier;
- record the change;
- rerun the V1 test cases;
- verify the release checklist;
- distribute only the latest approved build.

## 7. Feedback loop

Jotform responses are the single intake channel for structured beta feedback. Once responses exist, analyze them for recurring problems, feature demand, usability patterns, and purchase intent before deciding what enters the next product revision.

## 8. Scope boundary

Investor OS V1 is an educational portfolio-organization product. It is not a broker, automated trading system, tax-filing service, or personalized investment-advice service. Beta communication must preserve this positioning.
