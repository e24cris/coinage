import requests
from config.settings import Config

def get_stock_price(symbol):
    """
    Retrieve current stock price using Finnhub API
    """
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={Config.FINNHUB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data.get('c'):
        return data['c']  # Current price
    else:
        raise ValueError(f"Unable to retrieve stock price for {symbol}")

def get_forex_rate(symbol_pair):
    """
    Retrieve current forex exchange rate using Alpha Vantage
    symbol_pair should be in format 'EURUSD'
    """
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol_pair[:3]}&to_currency={symbol_pair[3:]}&apikey={Config.ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'Realtime Currency Exchange Rate' in data:
        return float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    else:
        raise ValueError(f"Unable to retrieve forex rate for {symbol_pair}")

def get_crypto_price(symbol):
    """
    Retrieve current cryptocurrency price using CoinGecko API
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and symbol in data:
        return data[symbol]['usd']
    else:
        raise ValueError(f"Unable to retrieve crypto price for {symbol}")

def get_market_news():
    """
    Retrieve market news from Finnhub
    """
    url = f"https://finnhub.io/api/v1/news?category=general&token={Config.FINNHUB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Unable to retrieve market news")
