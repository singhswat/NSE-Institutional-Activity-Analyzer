import pandas as pd
import numpy as np

def calculate_scores(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Calculates accumulation and distribution signals using EOD data.

    Important:
    This does not calculate true buy/sell quantity.
    It estimates likely accumulation/distribution using price, volume, delivery, and close location.
    '''
    data = df.copy()
    data = data.sort_values(["symbol", "trade_date"])

    data["price_change_pct"] = np.where(
        data["prev_close"].fillna(0) > 0,
        ((data["close_price"] - data["prev_close"]) / data["prev_close"]) * 100,
        0,
    )

    data["volume_avg_20"] = (
        data.groupby("symbol")["volume"]
        .transform(lambda x: x.rolling(20, min_periods=3).mean())
        .fillna(0)
        .round()
        .astype("int64")
    )

    data["volume_ratio"] = np.where(
        data["volume_avg_20"] > 0,
        data["volume"] / data["volume_avg_20"],
        1,
    )

    price_range = data["high_price"] - data["low_price"]
    data["close_position"] = np.where(
        price_range > 0,
        (data["close_price"] - data["low_price"]) / price_range,
        0.5,
    )

    delivery_component = np.clip(data["delivery_pct"].fillna(0) / 80 * 35, 0, 35)
    volume_component = np.clip(data["volume_ratio"].fillna(1) / 3 * 30, 0, 30)
    price_component_acc = np.clip(data["price_change_pct"].fillna(0) / 5 * 20, 0, 20)
    close_component_acc = np.clip(data["close_position"].fillna(0.5) * 15, 0, 15)

    data["accumulation_score"] = (
        delivery_component + volume_component + price_component_acc + close_component_acc
    ).round(2)

    price_component_dist = np.clip((-data["price_change_pct"].fillna(0)) / 5 * 20, 0, 20)
    close_component_dist = np.clip((1 - data["close_position"].fillna(0.5)) * 15, 0, 15)

    data["distribution_score"] = (
        delivery_component + volume_component + price_component_dist + close_component_dist
    ).round(2)

    data["signal"] = data.apply(classify_signal, axis=1)
    data["confidence"] = data.apply(classify_confidence, axis=1)
    data["comments"] = data.apply(build_comment, axis=1)

    return data[
        [
            "symbol",
            "trade_date",
            "price_change_pct",
            "volume_avg_20",
            "volume_ratio",
            "close_position",
            "accumulation_score",
            "distribution_score",
            "signal",
            "confidence",
            "comments",
        ]
    ]

def classify_signal(row) -> str:
    if row["accumulation_score"] >= 75 and row["accumulation_score"] > row["distribution_score"] + 15:
        return "Strong Accumulation"
    if row["accumulation_score"] >= 60 and row["accumulation_score"] > row["distribution_score"]:
        return "Moderate Accumulation"
    if row["distribution_score"] >= 75 and row["distribution_score"] > row["accumulation_score"] + 15:
        return "Strong Distribution"
    if row["distribution_score"] >= 60 and row["distribution_score"] > row["accumulation_score"]:
        return "Moderate Distribution"
    if row["volume_ratio"] >= 2:
        return "High Volume Watch"
    return "Neutral"

def classify_confidence(row) -> str:
    max_score = max(row["accumulation_score"], row["distribution_score"])
    if max_score >= 80:
        return "High"
    if max_score >= 60:
        return "Medium"
    return "Low"

def build_comment(row) -> str:
    return (
        f"Price change {row['price_change_pct']:.2f}%, "
        f"volume ratio {row['volume_ratio']:.2f}x, "
        f"close position {row['close_position']:.2f}. "
        "This is an EOD probability signal, not confirmed buy/sell quantity."
    )
