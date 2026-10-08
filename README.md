# Investor OS - An auditable personal investing toolkit

**English** | [Português (Brasil)](README.pt-BR.md)

![Stage: pre-external-beta](https://img.shields.io/badge/stage-pre--external--beta-yellow)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)

Track holdings, dividends, allocation and goals with transparent, deterministic calculations.

**[Synthetic dashboard demo](https://investor-os-dashboard.pages.dev/)** · [Separate product landing](https://investor-os-app.pages.dev/) · Public source repository · Documentation checked on **2026-10-01**.


> A read-only synthetic dashboard is now present in `main` (`web/`) and reachable at the demo URL, checked on 2026-10-08. It shows three invented companies and seven transactions, with 4,627 SEK remaining cost basis, not market value. It accepts no real data and has no login, broker import, backend or private storage. The workbook external-beta gates remain separate and open.

## Contents

- [Idea and planning](#idea-and-planning)
- [Features and scope](#features-and-scope)
- [Architecture](#architecture)
- [Design and snapshots](#design-and-snapshots)
- [Development process](#development-process)
- [Performance](#performance)
- [Security and privacy](#security-and-privacy)
- [Testing and local run](#testing-and-local-run)
- [Release and roadmap](#release-and-roadmap)
- [Credits and license](#credits-and-license)

## Idea and planning

Portfolio information often lives in broker screens and custom spreadsheets. Investor OS aims to bring cost basis, dividends, allocation and goals together while keeping every formula inspectable. It starts with a spreadsheet and a personal-first foundation, not with an opaque financial AI.

| User need | Planned response |
| --- | --- |
| Understand remaining cost after a partial sale. | Weighted-average cost, with fees, tax and currency conversion. |
| See where my portfolio is concentrated. | Allocation by asset, sector, type, country/region and currency. |
| Trust an imported number. | Source, observation time, effective time and currency records. |
| Keep personal control and avoid recurring service costs. | Local-first delivery before hosted accounts or billing. |

Goals: transparent calculations, useful summaries, manual overrides and auditable data. Non-goals: brokerage execution, personalized securities recommendations, automated trading, tax filing, high-frequency prices and social features.

## Features and scope

**V1 workbook, as documented:** holdings and transaction ledger, weighted-average cost, dividends/reconciliation, FX conversion, allocation, goals, dashboard charts and integrity checks with fictional sample data. Manual prices and FX are intentional, not a live market feed.

**Python foundation in this repository:** `Decimal` arithmetic, chronological trade ordering, purchase cost including fees/tax/FX, partial-sale cost reduction, full-sale reset and rejection of overselling.

**Delivered synthetic web demo:** overview, holdings search/empty state, fictional transaction ledger, synthetic JSON export and reset.

**Not delivered for private use:** authentication, multi-user sync, broker connection, automated price feeds, subscription billing or real-data import/storage.

## Architecture

```mermaid
graph TD
    A[Workbook inputs: assets and transactions] --> B[Deterministic ledger calculations]
    B --> C[Holdings, allocation, dividends and goals]
    C --> D[Dashboard and integrity checks]
    E[Python Decimal foundation] --> F[Local regression tests]
    G[Target PostgreSQL model] -. future .-> H[Local UI and scheduled jobs]
```

| Stage | Technology | Status / reason |
| --- | --- | --- |
| V1 product | Excel / LibreOffice-compatible workbook | Implementation is described in product docs; simple inspection of inputs and formulas. |
| Calculation foundation | Python standard library, Decimal | Present in `src/investor_os/portfolio.py`; deterministic arithmetic. |
| Data model | PostgreSQL schema | Model in `database/`; not proof of a running hosted database. |
| Personal-first target | Local UI, local scheduled jobs, CSV/JSON export and encrypted backups | Future delivery in [architecture](docs/architecture.md). |
| Public dashboard | Static HTML/JS and generated JSON in `web/` | Read-only invented portfolio; no accounts or real data. |
| Separate landing | Product landing page | Product introduction, not private portfolio functionality. |

[Architecture](docs/architecture.md) is the current personal-first, zero-cost direction. Older product proposals mention Next.js, Supabase, n8n Cloud, Vercel, OpenAI workflows and Gumroad. Those are historical/planned options, not installed services or subscriptions. Current architecture rejects services requiring cards, trials or automatic overage. AI is not used for deterministic financial arithmetic.

## Design and snapshots

Dated, repository-owned screenshots remain to be supplied. Private Drive evidence is intentionally not linked.

The current public preview uses a dark background, green accents, numbered feature descriptions and an explicit development status. Workbook design separates inputs, calculated areas, checks and onboarding.


These are landing-page images, not dashboard screenshots. Earlier wireframes and a workbook dashboard capture have not been collected here. Add them only from verified artifacts with synthetic data; never substitute a mockup for a working screen without labelling it.

## Development process

1. Define V1 goals, non-goals and a transparent calculation principle.
2. Specify workbook sheets, formulas and checks in [XLSX implementation](product/xlsx-implementation.md).
3. Build the workbook stage and record validation gates in [release checklist](product/release-checklist.md).
4. Establish the personal-first architecture, Python calculation core and local regression tests.
5. Restore a clean repository with synthetic fixtures on 2026-09-30. This describes the current repository, not deletion from every possible cache or copy.
6. Add bilingual documentation, dated public snapshots and MIT on 2026-10-01.

Exact changes remain in Git history. Future changes should record the requirement, decision, implementation, test result and snapshot together. Unverified early dates and approvals are not reconstructed.

## Performance

No measured dashboard response time, throughput or Core Web Vitals baseline is available in the inspected repository documentation. The landing page is not a benchmark of portfolio calculations.

Before claiming speed, measure dataset size, import/calculation time, memory, hardware, Python/browser version and commit. Before a web dashboard release, add dated LCP/INP/CLS measurements and realistic synthetic portfolio scenarios.

## Security and privacy

- Use fictional portfolios in fixtures, docs and screenshots. Do not commit broker exports, balances, credentials or private identifiers.
- The current restored tree uses synthetic sample data. No claim is made that all previous copies or third-party caches were erased.
- Financial formulas are deterministic, not AI guesses. This is portfolio organization, not investment advice or a tax calculation certificate.
- [Beta tracker](product/beta-tracker.md) is intended to be anonymized. Verify the outgoing artifact before sharing it with testers.
- Secrets belong outside Git. Local-first and encrypted backup are target requirements, not proof that every current artifact is encrypted.
- No paid service or hosted CI was enabled by this documentation update. Keep GitHub-hosted Actions off until billing limits are verified, as required by the architecture notes.

## Testing and local run

### Synthetic trade test

An invented three-company portfolio can now be loaded into the Python core:

```sh
PYTHONPATH=src python3 -m investor_os.sample_portfolio
```

[Setup, format, expected results and privacy boundary](docs/synthetic-portfolio.md).
14 local tests passed on 2026-10-07. The CLI generates the fixture used by the separate static dashboard; neither is a broker importer.


The V1 [release checklist](product/release-checklist.md) records 20 workbook cases used for validation, but external testers and public-release gates remain unchecked. This update did not obtain or rerun the workbook, so it does not independently certify those 20 results.

The current Python `tests/test_portfolio.py` contains four tests: partial sale, FX/fees/tax, full-sale reset and oversell rejection. **All four passed locally on 2026-10-01 using the source fetched from this repository.** This is a narrow calculation-core result, not an end-to-end product test.

```sh
# From repository root, with Python 3 available:
PYTHONPATH=src python3 -m unittest discover -s tests -v
# Equivalent repository helper:
sh run_tests.sh
```

No third-party runtime dependency is needed for the inspected calculation module. Read [workbook implementation](product/xlsx-implementation.md) for spreadsheet conventions and setup; the static dashboard runs with `python3 build_demo.py` then `python3 -m http.server 8000 --directory web`. No Node runtime or backend is required. See [web demo scope and QA](docs/web-demo.md).

## Release and roadmap

- [ ] Complete a controlled external beta with 5-10 testers.
- [ ] Review feedback and fix usability issues.
- [ ] Complete distribution, delivery and export/backup instructions.
- [ ] Validate personal MVP import, manual price/FX updates, dashboard and checks.
- [ ] Expand regression coverage and record performance evidence.
- [ ] Consider hosted accounts, multi-tenancy and billing only after personal use and demand validation.

Do not mark the workbook production-ready until the external beta gate is complete and calculation tests pass. Publishing a README is not publishing the product.

### Repository guide

- [Current architecture](docs/architecture.md)
- [XLSX implementation](product/xlsx-implementation.md)
- [Release checklist](product/release-checklist.md)
- [Private beta scope](product/private-beta.md)
- [Tester guide](product/beta-tester-guide.md)
- [Feedback](product/beta-feedback.md)
- [Beta launch procedure](product/beta-launch-sop.md)
- [Invitation draft](product/beta-invitation.md)
- [Anonymized tracker](product/beta-tracker.md)
- [Public launch gates](product/public-launch-readiness.md)

## Credits and license

Created by Iuri Johansson. Python calculation core uses the standard library; the workbook targets Excel / LibreOffice. Planned products and third-party services retain their own terms.

[MIT license](LICENSE), copyright 2026 Iuri Johansson. The source repository is public; keep all personal financial data outside Git.

## Documentation review - 2026-10-07

This is a documentation draft, not a release or a fresh runtime audit. Current repository visibility, README files, package scripts and root license paths were checked. Historical runtime and benchmark results above have not been rerun. Screenshots require a separate capture, privacy check, upload and rendered-image check before completion. Missing images are not replaced with broken embeds.

`docs/synthetic-portfolio.md` now documents the invented three-company, seven-transaction CLI and 14 historical passing tests dated 2026-10-07. No real account records are used. The dashboard source is now in `main`; the separate dashboard URL was opened and visually checked on 2026-10-08. This review does not certify deployment commit parity or private investment use. Old four-test documentation is historical, not the current test count.
