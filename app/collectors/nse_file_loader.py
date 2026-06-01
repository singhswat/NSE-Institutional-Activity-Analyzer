import pandas as pd
from pathlib import Path

def load_bhavcopy_csv(path: str | Path) -> pd.DataFrame:
    '''
    Generic NSE bhavcopy-style loader.

    Expected columns can be mapped from:
    SYMBOL, DATE1, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE,
    PREV_CLOSE, TTL_TRD_QNTY, TURNOVER_LACS, NO_OF_TRADES

    You may need to adjust this mapper depending on the exact NSE report format.
    '''
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    column_map = {
        "symbol": "symbol",
        "date1": "trade_date",
        "open_price": "open_price",
        "high_price": "high_price",
        "low_price": "low_price",
        "close_price": "close_price",
        "prev_close": "prev_close",
        "ttl_trd_qnty": "volume",
        "turnover_lacs": "traded_value",
        "no_of_trades": "no_of_trades",
    }

    df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})

    required = ["symbol", "trade_date", "open_price", "high_price", "low_price", "close_price", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.date
    return df
