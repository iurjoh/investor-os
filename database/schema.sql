-- Investor OS V1 logical data model
-- Supabase/PostgreSQL compatible.
-- V1 spreadsheet data should map cleanly to these entities when the web app is built.

create extension if not exists pgcrypto;

create table if not exists portfolios (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  base_currency char(3) not null default 'SEK',
  starting_cash numeric(20,6) not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint portfolios_base_currency_chk check (base_currency in ('SEK','USD','EUR','GBP','BRL','CAD'))
);

create table if not exists assets (
  id uuid primary key default gen_random_uuid(),
  ticker text not null,
  mic char(4) not null,
  exchange_name text,
  name text not null,
  asset_type text not null default 'stock',
  sector text,
  country_region text,
  currency char(3) not null,
  isin text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint assets_type_chk check (asset_type in ('stock','reit','etf','fund','bond','crypto','cash','other')),
  constraint assets_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD')),
  constraint assets_mic_chk check (mic ~ '^[A-Z0-9]{4}$'),
  unique (ticker, mic)
);

create table if not exists transactions (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolios(id) on delete cascade,
  asset_id uuid references assets(id) on delete restrict,
  transaction_date date not null,
  transaction_type text not null,
  quantity numeric(24,8) not null default 0,
  price numeric(20,8) not null default 0,
  gross_amount numeric(20,6) not null default 0,
  fees numeric(20,6) not null default 0,
  tax numeric(20,6) not null default 0,
  currency char(3) not null,
  fx_rate numeric(20,10) not null default 1,
  notes text,
  created_at timestamptz not null default now(),
  constraint transactions_type_chk check (transaction_type in ('buy','sell','dividend','fee','deposit','withdrawal')),
  constraint transactions_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD')),
  constraint transactions_numeric_chk check (quantity >= 0 and price >= 0 and gross_amount >= 0 and fees >= 0 and tax >= 0 and fx_rate > 0),
  constraint asset_required_for_asset_transactions check (
    transaction_type in ('deposit','withdrawal') or asset_id is not null
  )
);

create table if not exists price_snapshots (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolios(id) on delete cascade,
  asset_id uuid not null references assets(id) on delete cascade,
  price_date date not null,
  price numeric(20,8) not null,
  currency char(3) not null,
  source text,
  created_at timestamptz not null default now(),
  constraint price_snapshots_price_chk check (price >= 0),
  constraint price_snapshots_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD')),
  unique (portfolio_id, asset_id, price_date)
);

create table if not exists dividend_records (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolios(id) on delete cascade,
  asset_id uuid not null references assets(id) on delete restrict,
  ex_date date,
  payment_date date,
  record_date date,
  shares numeric(24,8) not null default 0,
  dividend_per_share numeric(20,8) not null default 0,
  gross_amount numeric(20,6) not null default 0,
  withholding_tax numeric(20,6) not null default 0,
  net_amount numeric(20,6) not null default 0,
  currency char(3) not null,
  fx_rate numeric(20,10) not null default 1,
  notes text,
  created_at timestamptz not null default now(),
  constraint dividend_values_chk check (shares >= 0 and dividend_per_share >= 0 and gross_amount >= 0 and withholding_tax >= 0 and net_amount >= 0 and fx_rate > 0),
  constraint dividend_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD'))
);

create table if not exists portfolio_goals (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolios(id) on delete cascade,
  goal_type text not null,
  target_value numeric(20,6) not null,
  currency char(3) not null,
  target_date date,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint goals_type_chk check (goal_type in ('portfolio_value','annual_dividend','monthly_contribution')),
  constraint goals_value_chk check (target_value >= 0),
  constraint goals_currency_chk check (currency in ('SEK','USD','EUR','GBP','BRL','CAD'))
);

create table if not exists target_allocations (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolios(id) on delete cascade,
  allocation_dimension text not null,
  allocation_key text not null,
  target_weight numeric(8,5) not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint target_dimension_chk check (allocation_dimension in ('asset','sector','asset_type','country_region','currency')),
  constraint target_weight_chk check (target_weight >= 0 and target_weight <= 1),
  unique (portfolio_id, allocation_dimension, allocation_key)
);

create index if not exists transactions_portfolio_date_idx on transactions(portfolio_id, transaction_date);
create index if not exists transactions_asset_idx on transactions(asset_id);
create index if not exists price_snapshots_portfolio_date_idx on price_snapshots(portfolio_id, price_date);
create index if not exists dividend_records_portfolio_payment_idx on dividend_records(portfolio_id, payment_date);
create index if not exists dividend_records_asset_idx on dividend_records(asset_id);

-- Deterministic weighted-average holdings derived in transaction order.
-- transaction id is the stable tie-breaker for trades on the same date.
create or replace view v_holdings as
with recursive ordered as (
  select t.*, row_number() over (
    partition by portfolio_id, asset_id
    order by transaction_date, created_at, id
  ) as rn
  from transactions t
  where transaction_type in ('buy', 'sell')
), running as (
  select
    o.portfolio_id, o.asset_id, o.rn, o.transaction_type,
    case when o.transaction_type = 'buy' then o.quantity else -o.quantity end as quantity,
    case when o.transaction_type = 'buy'
      then (o.gross_amount + o.fees + o.tax) * o.fx_rate
      else 0::numeric
    end as cost_basis_base
  from ordered o
  where o.rn = 1

  union all

  select
    o.portfolio_id, o.asset_id, o.rn, o.transaction_type,
    r.quantity + case when o.transaction_type = 'buy' then o.quantity else -o.quantity end,
    case
      when o.transaction_type = 'buy' then
        r.cost_basis_base + (o.gross_amount + o.fees + o.tax) * o.fx_rate
      when o.quantity = r.quantity then 0::numeric
      else r.cost_basis_base - o.quantity * (r.cost_basis_base / nullif(r.quantity, 0))
    end
  from running r
  join ordered o
    on o.portfolio_id = r.portfolio_id
   and o.asset_id = r.asset_id
   and o.rn = r.rn + 1
), latest as (
  select *, row_number() over (
    partition by portfolio_id, asset_id order by rn desc
  ) as latest_rn
  from running
)
select
  portfolio_id, asset_id, quantity, cost_basis_base,
  cost_basis_base / nullif(quantity, 0) as average_cost_base,
  case when quantity < 0 then 'ERROR_OVERSELL' else 'OK' end as data_quality_status
from latest
where latest_rn = 1;

-- Dividend summary in portfolio base currency.
create or replace view v_dividend_summary as
select
  d.portfolio_id,
  d.asset_id,
  coalesce(sum(d.gross_amount * d.fx_rate), 0) as gross_dividends_base,
  coalesce(sum(d.withholding_tax * d.fx_rate), 0) as withholding_tax_base,
  coalesce(sum(d.net_amount * d.fx_rate), 0) as net_dividends_base
from dividend_records d
group by d.portfolio_id, d.asset_id;
