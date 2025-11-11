# get_data.py
import os
import time
import json
import logging
from typing import List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"
SYMBOLS = os.getenv("SYMBOLS", "AAPL,GOOGL,MSFT").split(",")

DATA_DIR = os.getenv("DATA_DIR", "../data/new")
os.makedirs(DATA_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

RATE_LIMIT_SLEEP = int(os.getenv("RATE_LIMIT_SLEEP", "15"))  # Alpha Vantage free: ~5 req/min


def _fetch_daily_raw(symbol: str) -> dict:
    """Download raw JSON for a single symbol. Handle network errors and rate limits."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": API_KEY,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        logging.error(f"[{symbol}] Network/JSON error: {e}")
        return {}

    # Alpha Vantage specific throttling / errors
    if "Note" in payload:
        logging.warning(f"[{symbol}] Rate limited by Alpha Vantage: {payload['Note']}")
        return {}
    if "Error Message" in payload:
        logging.error(f"[{symbol}] API error: {payload['Error Message']}")
        return {}

    return payload.get("Time Series (Daily)", {})


def _to_dataframe(ts_daily: dict, symbol: str) -> pd.DataFrame:
    """Transform raw 'Time Series (Daily)' dict -> clean DataFrame."""
    if not ts_daily:
        return pd.DataFrame()

    df = pd.DataFrame.from_dict(ts_daily, orient="index")
    df.index.name = "date"
    df.reset_index(inplace=True)

    # Rename columns to clean names
    rename_map = {
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume",
    }
    df.rename(columns=rename_map, inplace=True)

    # Types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Add symbol
    df["symbol"] = symbol

    # Basic data-quality checks / cleaning
    # 1) Drop rows with missing mandatory fields
    df = df.dropna(subset=["date", "open", "high", "low", "close"])
    # 2) Remove duplicates by (symbol, date)
    df = df.drop_duplicates(subset=["symbol", "date"])
    # 3) Enforce ascending date
    df = df.sort_values("date").reset_index(drop=True)

    # Optional lightweight validation
    # - prices must be non-negative
    for col in ["open", "high", "low", "close"]:
        df = df[df[col] >= 0]

    return df


def extract_transform(symbols: List[str]) -> pd.DataFrame:
    """ET step – download & transform for all symbols, respecting rate limits."""
    frames = []
    for i, sym in enumerate(symbols, start=1):
        sym = sym.strip().upper()
        logging.info(f"Fetching: {sym} ({i}/{len(symbols)})")
        ts_daily = _fetch_daily_raw(sym)
        df = _to_dataframe(ts_daily, sym)
        if df.empty:
            logging.warning(f"[{sym}] No data fetched.")
        else:
            logging.info(f"[{sym}] Rows: {len(df)} | Date range: {df['date'].min()} → {df['date'].max()}")
            frames.append(df)

        # Respect API limits between calls
        if i < len(symbols):
            time.sleep(RATE_LIMIT_SLEEP)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def load(df: pd.DataFrame) -> str:
    """L step – save as CSV & Parquet with date-stamped filenames."""
    if df.empty:
        logging.error("No data to save. Skipping LOAD.")
        return ""

    # Ensure output directory
    os.makedirs(DATA_DIR, exist_ok=True)

    # Snapshot filenames
    snapshot = pd.Timestamp.utcnow().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(DATA_DIR, f"stock_data_{snapshot}.csv")
    pq_path = os.path.join(DATA_DIR, f"stock_data_{snapshot}.parquet")

    # Save
    df.to_csv(csv_path, index=False)
    try:
        df.to_parquet(pq_path, index=False)
    except Exception as e:
        logging.warning(f"Parquet save failed (optional dep?): {e}")

    logging.info(f"Saved CSV: {csv_path}")
    logging.info(f"Saved Parquet: {pq_path} (if available)")

    # Also keep/update a latest pointer for quick reads
    latest_csv = os.path.join(DATA_DIR, "stock_data_latest.csv")
    df.to_csv(latest_csv, index=False)
    logging.info(f"Updated latest CSV: {latest_csv}")

    return csv_path


def main():
    if not API_KEY:
        logging.error("Missing ALPHA_VANTAGE_API_KEY in environment.")
        return

    df_all = extract_transform(SYMBOLS)
    load(df_all)


if __name__ == "__main__":
    main()