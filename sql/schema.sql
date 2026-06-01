create table if not exists stock_master (
    symbol text primary key,
    company_name text,
    sector text,
    industry text,
    is_group_a boolean default true,
    is_fo_stock boolean default false,
    created_at timestamptz default now()
);

create table if not exists stock_daily (
    id bigint generated always as identity primary key,
    symbol text not null references stock_master(symbol),
    trade_date date not null,
    open_price numeric(18,4),
    high_price numeric(18,4),
    low_price numeric(18,4),
    close_price numeric(18,4),
    prev_close numeric(18,4),
    volume bigint,
    traded_value numeric(20,4),
    no_of_trades bigint,
    delivery_qty bigint,
    delivery_pct numeric(10,4),
    created_at timestamptz default now(),
    unique(symbol, trade_date)
);

create table if not exists stock_scores (
    id bigint generated always as identity primary key,
    symbol text not null references stock_master(symbol),
    trade_date date not null,
    price_change_pct numeric(10,4),
    volume_avg_20 bigint,
    volume_ratio numeric(10,4),
    close_position numeric(10,4),
    accumulation_score numeric(10,4),
    distribution_score numeric(10,4),
    signal text,
    confidence text,
    comments text,
    created_at timestamptz default now(),
    unique(symbol, trade_date)
);

create index if not exists idx_stock_daily_symbol_date
on stock_daily(symbol, trade_date desc);

create index if not exists idx_stock_scores_date_signal
on stock_scores(trade_date desc, signal);

create index if not exists idx_stock_scores_accumulation
on stock_scores(trade_date desc, accumulation_score desc);

create index if not exists idx_stock_scores_distribution
on stock_scores(trade_date desc, distribution_score desc);
