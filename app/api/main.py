from fastapi import FastAPI, HTTPException
from app.database.supabase_client import get_supabase

app = FastAPI(
    title="NSE Institutional Activity Analyzer API",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/signals/latest")
def latest_signals(limit: int = 50):
    supabase = get_supabase()

    latest_date_response = (
        supabase.table("stock_scores")
        .select("trade_date")
        .order("trade_date", desc=True)
        .limit(1)
        .execute()
    )

    if not latest_date_response.data:
        return []

    latest_date = latest_date_response.data[0]["trade_date"]

    response = (
        supabase.table("stock_scores")
        .select("*")
        .eq("trade_date", latest_date)
        .order("accumulation_score", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data

@app.get("/signals/accumulation")
def accumulation_signals(limit: int = 25):
    supabase = get_supabase()

    response = (
        supabase.table("stock_scores")
        .select("*")
        .in_("signal", ["Strong Accumulation", "Moderate Accumulation"])
        .order("trade_date", desc=True)
        .order("accumulation_score", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data

@app.get("/signals/distribution")
def distribution_signals(limit: int = 25):
    supabase = get_supabase()

    response = (
        supabase.table("stock_scores")
        .select("*")
        .in_("signal", ["Strong Distribution", "Moderate Distribution"])
        .order("trade_date", desc=True)
        .order("distribution_score", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data

@app.get("/stocks/{symbol}/history")
def stock_history(symbol: str, limit: int = 100):
    supabase = get_supabase()

    response = (
        supabase.table("stock_daily")
        .select("*")
        .eq("symbol", symbol.upper())
        .order("trade_date", desc=True)
        .limit(limit)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="No data found for symbol")

    return response.data
