import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY=os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"


def get_data_daily(symbol: str) -> pd.DataFrame:
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": API_KEY
    }


    response = requests.get(BASE_URL, params=params)
    data = response.json().get("Time Series (Daily)", {})

    print("Len of data:", len(data))
    print("First keys:", list(data.keys())[:3])

    df = pd.DataFrame.from_dict(data, orient="index")
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    })

    df.index = pd.to_datetime(df.index)
    print(response.json())
    return df.astype(float)

def main():
    symbols = ["AAPL", "GOOGL", "MSFT"]
    dfs = []
    for sym in symbols:
        df = get_data_daily(sym)
        df["symbol"] = sym
        dfs.append(df)
    result = pd.concat(dfs)
    result.to_csv("data/new/stock_data.csv")
    print("Saved data/new/stock_data.csv")

if __name__== "__main__":
    main()
