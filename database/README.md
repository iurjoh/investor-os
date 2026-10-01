# Database

The canonical V1 relational model is in `schema.sql`.

## Design principles

- Transactions are the source of truth for portfolio activity.
- Price snapshots provide current/historical valuation inputs.
- Dividend records remain separate because dividend events have their own dates and tax fields.
- All monetary values retain their original currency and an explicit FX rate for base-currency reporting.
- Portfolio calculations should remain deterministic and testable.
- User-facing recommendations are outside the database layer.

## Planned Supabase implementation

When the hosted database is created, the schema should be applied through a versioned migration rather than edited manually in production.

Row Level Security and authentication will be added when multi-user web application development begins. The spreadsheet V1 does not require the production database to be live.
