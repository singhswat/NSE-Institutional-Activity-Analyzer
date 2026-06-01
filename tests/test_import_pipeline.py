from datetime import date

import pandas as pd

from app.collectors.nse_file_loader import STOCK_DAILY_COLUMNS, load_bhavcopy_csv
from app.jobs.daily_import import serialize_records
from app.processors.scoring import calculate_scores


def test_loader_normalizes_current_bhavcopy_and_drops_extra_columns(tmp_path):
    path = tmp_path / "bhavcopy.csv"
    pd.DataFrame(
        [
            {
                "TckrSymb": " reliance ",
                "TradDt": "2026-05-19",
                "OpnPric": "100",
                "HghPric": "110",
                "LwPric": "90",
                "ClsPric": "105",
                "PrvsClsgPric": "99",
                "TtlTradgVol": "1000",
                "unexpected": "ignored",
            }
        ]
    ).to_csv(path, index=False)

    result = load_bhavcopy_csv(path)

    assert result.columns.tolist() == STOCK_DAILY_COLUMNS
    assert result.loc[0, "symbol"] == "RELIANCE"
    assert result.loc[0, "trade_date"] == date(2026, 5, 19)
    assert pd.isna(result.loc[0, "delivery_pct"])


def test_scoring_accepts_missing_delivery_data_and_clamps_close_position(tmp_path):
    path = tmp_path / "bhavcopy.csv"
    pd.DataFrame(
        [
            {
                "symbol": "TEST",
                "date1": "2026-05-19",
                "open_price": 100,
                "high_price": 110,
                "low_price": 90,
                "close_price": 120,
                "prev_close": 100,
                "ttl_trd_qnty": 1000,
            }
        ]
    ).to_csv(path, index=False)

    scores = calculate_scores(load_bhavcopy_csv(path))

    assert scores.loc[0, "close_position"] == 1


def test_serialize_records_converts_dates_and_missing_values():
    result = serialize_records(
        pd.DataFrame([{"trade_date": date(2026, 5, 19), "delivery_pct": float("nan")}])
    )

    assert result == [{"trade_date": "2026-05-19", "delivery_pct": None}]
