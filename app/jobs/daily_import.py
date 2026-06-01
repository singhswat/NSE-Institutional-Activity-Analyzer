import argparse
import pandas as pd

from app.collectors.sample_loader import load_sample_daily_data
from app.collectors.nse_file_loader import load_bhavcopy_csv
from app.processors.scoring import calculate_scores
from app.database.supabase_client import get_supabase

def upsert_stock_master(df: pd.DataFrame):
    supabase = get_supabase()
    records = []

    for symbol in sorted(df["symbol"].unique()):
        records.append({
            "symbol": symbol,
            "company_name": symbol,
            "is_group_a": True
        })

    supabase.table("stock_master").upsert(records, on_conflict="symbol").execute()

def upsert_daily(df: pd.DataFrame):
    supabase = get_supabase()
    records = df.where(pd.notnull(df), None).to_dict(orient="records")
    supabase.table("stock_daily").upsert(records, on_conflict="symbol,trade_date").execute()

def upsert_scores(scores: pd.DataFrame):
    supabase = get_supabase()
    records = scores.where(pd.notnull(scores), None).to_dict(orient="records")
    supabase.table("stock_scores").upsert(records, on_conflict="symbol,trade_date").execute()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true", help="Load demo sample data")
    parser.add_argument("--file", type=str, help="Load NSE bhavcopy-style CSV")
    args = parser.parse_args()

    if args.sample:
        df = load_sample_daily_data()
    elif args.file:
        df = load_bhavcopy_csv(args.file)
    else:
        raise ValueError("Use --sample or --file path/to/file.csv")

    upsert_stock_master(df)
    upsert_daily(df)

    scores = calculate_scores(df)
    upsert_scores(scores)

    print(f"Imported {len(df)} stock daily rows")
    print(f"Generated {len(scores)} score rows")
    print(scores.sort_values('accumulation_score', ascending=False).head(10).to_string(index=False))

if __name__ == "__main__":
    main()
