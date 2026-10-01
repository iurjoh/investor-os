-- Phase 1 migration for an existing Investor OS database.
-- Run in a transaction after backup. Review unknown MICs before enforcing NOT NULL.
begin;

alter table assets add column if not exists mic char(4);
alter table assets add column if not exists exchange_name text;

-- Known rows must be backfilled explicitly, for example:
-- update assets set mic = 'XSTO' where ticker = '...' and ...;
-- Do not infer MIC from currency: the same currency trades on many venues.

alter table assets drop constraint if exists assets_ticker_currency_key;
alter table assets drop constraint if exists assets_currency_chk;
alter table assets add constraint assets_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD')) not valid;
alter table portfolios drop constraint if exists portfolios_base_currency_chk;
alter table portfolios add constraint portfolios_base_currency_chk check (base_currency in ('SEK','USD','EUR','GBP','BRL','CAD')) not valid;
alter table transactions drop constraint if exists transactions_currency_chk;
alter table transactions add constraint transactions_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD')) not valid;
alter table price_snapshots drop constraint if exists price_snapshots_currency_chk;
alter table price_snapshots add constraint price_snapshots_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD')) not valid;
alter table dividend_records drop constraint if exists dividend_currency_chk;
alter table dividend_records add constraint dividend_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD')) not valid;
alter table portfolio_goals drop constraint if exists goals_currency_chk;
alter table portfolio_goals add constraint goals_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD')) not valid;

commit;

-- After every existing asset has the correct ISO 10383 MIC:
-- alter table assets alter column mic set not null;
-- alter table assets add constraint assets_mic_chk check (mic ~ '^[A-Z0-9]{4}$');
-- alter table assets add constraint assets_ticker_mic_key unique (ticker, mic);
