import pandas as pd
from get_data import _to_dataframe

def test_transform_basic():
    sample = {
        "2025-01-02": {
            "1. open": "1.0", "2. high": "2.0", "3. low": "0.5",
            "4. close": "1.8", "5. volume": "100"
        },
        "2025-01-01": {
            "1. open": "0.8", "2. high": "1.5", "3. low": "0.7",
            "4. close": "1.2", "5. volume": "90"
        },
    }
    df = _to_dataframe(sample, "AAPL")
    assert list(df.columns) == ["date","open","high","low","close","volume","symbol"]
    assert df["symbol"].unique().tolist() == ["AAPL"]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df["open"].min() >= 0
    # sorted ascending:
    assert df.iloc[0]["date"] < df.iloc[-1]["date"]