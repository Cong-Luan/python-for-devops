#Import module 
from requests import Response
import os
import sys
import requests

#URL
Base_url = "https://www.alphavantage.co/query"

#Hàm lấy dữ liệu
def get_daily_series(ma, api_key):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ma,
        "apikey": api_key
    }
    try:
        response = requests.get(Base_url, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as l:
        print(f"Requests failed: {l}")
        sys.exit(1)
    return response.json()


def main():
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    if not api_key:
        print(f"Set ALPHAVANTAGE_API_KEY first: export ALPHAVANTAGE_API_KEY=...")
        sys.exit(1)
    ma = input("Enter a stock ma (e.g. IBM, AMZN, GOOGL): ").strip().upper()
    data = get_daily_series(ma, api_key)
    
    Daily = data.get("Time Series (Daily)")
    if not Daily:
        print("No time series returned: ", data)
        return
    for day in list(Daily)[:5]:
        close = Daily[day]["4. close"]
        print(f"{day:5} Close={close}")

if __name__ == "__main__":
    main()

