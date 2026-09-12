#Import module 
from requests import Response
import os
import sys
import requests

Base_url = "https://www.alphavantage.co/query"

def get_daily_series(ma, api_key):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ma,
        "apikey": api_key
    }

    Response = requests.get(Base_url, params = params, timeout=15)
    Response.raise_for_status()
    return Response.json()

def main():
    
    