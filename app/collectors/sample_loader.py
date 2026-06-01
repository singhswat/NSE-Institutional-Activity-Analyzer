from pathlib import Path
import pandas as pd

def load_sample_daily_data() -> pd.DataFrame:
    path = Path(__file__).resolve().parents[2] / "sample_data" / "stock_daily_sample.csv"
    df = pd.read_csv(path)
    df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.date
    return df
