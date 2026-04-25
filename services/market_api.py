import requests
import time
from services.cache import get_cache, set_cache

API_KEY = "SUA_API_KEY_AQUI"


def get_usd_brl():
    cache_key = "usd_brl"
    cached = get_cache(cache_key)

    if cached is not None:
        return cached

    time.sleep(12)

    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=BRL&apikey={API_KEY}"

    try:
        data = requests.get(url).json()
        rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

        set_cache(cache_key, rate)
        return rate

    except Exception as e:
        print("Erro USD/BRL:", e)
        return None


def get_sp500():
    cache_key = "sp500"
    cached = get_cache(cache_key)

    if cached is not None:
        return cached

    time.sleep(12)

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=SPY&apikey={API_KEY}"

    try:
        data = requests.get(url).json()
        value = float(data["Global Quote"]["10. change percent"].replace('%', ''))

        set_cache(cache_key, value)
        return value

    except Exception as e:
        print("Erro SP500:", e)
        return None


def get_dxy_proxy():
    cache_key = "dxy"
    cached = get_cache(cache_key)

    if cached is not None:
        return cached

    time.sleep(12)

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=UUP&apikey={API_KEY}"

    try:
        data = requests.get(url).json()
        value = float(data["Global Quote"]["10. change percent"].replace('%', ''))

        set_cache(cache_key, value)
        return value

    except Exception as e:
        print("Erro DXY:", e)
        return None
