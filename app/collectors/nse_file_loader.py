from pathlib import Path

import pandas as pd


STOCK_DAILY_COLUMNS = [
    "symbol",
    "trade_date",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "prev_close",
    "volume",
    "traded_value",
    "no_of_trades",
    "delivery_qty",
    "delivery_pct",
]

COLUMN_ALIASES = {
    # Legacy NSE bhavcopy columns
    "date1": "trade_date",
    "ttl_trd_qnty": "volume",
    "turnover_lacs": "traded_value",
    # Current NSE equity bhavcopy columns
    "tckrsymb": "symbol",
    "traddt": "trade_date",
    "opnpric": "open_price",
    "hghpric": "high_price",
    "lwpric": "low_price",
    "clspric": "close_price",
    "prvsclsgpric": "prev_close",
    "ttltradgvol": "volume",
    "ttltrfval": "traded_value",
    "ttlnboftxsexctd": "no_of_trades",
}

REQUIRED_COLUMNS = [
    "symbol",
    "trade_date",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "volume",
]

NUMERIC_COLUMNS = [
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "prev_close",
    "volume",
    "traded_value",
    "no_of_trades",
    "delivery_qty",
    "delivery_pct",
]


def load_bhavcopy_csv(path: str | Path) -> pd.DataFrame:
    """Load legacy or current NSE bhavcopy-style CSV data into the app schema."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns=COLUMN_ALIASES)

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    for column in STOCK_DAILY_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[STOCK_DAILY_COLUMNS].copy()
    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    df["trade_date"] = pd.to_datetime(df["trade_date"], errors="raise").dt.date

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df
