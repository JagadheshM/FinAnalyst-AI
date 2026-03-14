import yfinance as yf
import pandas as pd
from typing import Dict, List, Any
import requests
from ..config import get_settings

config = get_settings()

def get_stock_data(symbol: str) -> Dict[str, Any]:
    """
    Fetches latest price, trend, and volume data for an Indian stock (NSE) using yfinance.
    Appends '.NS' for NSE stocks if not provided.
    """
    if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
        # Default to NSE
        query_symbol = f"{symbol}.NS"
    else:
        query_symbol = symbol
        
    try:
        ticker = yf.Ticker(query_symbol)
        
        # Get historical data for the last 5 days to calculate short-term trend
        hist = ticker.history(period="5d")
        
        if hist.empty:
            return _empty_market_data(symbol)
            
        latest_data = hist.iloc[-1]
        prev_data = hist.iloc[-2] if len(hist) > 1 else latest_data
        
        # Calculate trend (%)
        price_change_pct = ((latest_data['Close'] - prev_data['Close']) / prev_data['Close']) * 100
        
        trend = "Neutral"
        if price_change_pct > 0.5:
            trend = "Positive"
        elif price_change_pct < -0.5:
            trend = "Negative"
            
        return {
            "symbol": symbol,
            "price": round(latest_data['Close'], 2),
            "trend": trend,
            "trend_pct": round(price_change_pct, 2),
            "volume": int(latest_data['Volume']),
            "error": None
        }
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return _empty_market_data(symbol, str(e))


def get_crypto_data(crypto_ids: List[str] = ["bitcoin", "ethereum"]) -> Dict[str, Dict]:
    """
    Fetches data for specified cryptocurrencies using CoinGecko API.
    crypto_ids should be coingecko IDs (e.g., 'bitcoin').
    """
    # Uses the free tier public API endpoint
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        "ids": ",".join(crypto_ids),
        "vs_currencies": "usd",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    
    headers = {"accept": "application/json"}
    if config.coingecko_api_key:
        headers["x-cg-pro-api-key"] = config.coingecko_api_key
        
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = {}
        for cid in crypto_ids:
            if cid in data:
                c_data = data[cid]
                change_pct = c_data.get('usd_24h_change', 0)
                
                trend = "Neutral"
                if change_pct > 1.0:
                    trend = "Positive"
                elif change_pct < -1.0:
                    trend = "Negative"
                    
                results[cid] = {
                    "symbol": cid.upper(),
                    "price": round(c_data.get('usd', 0), 2),
                    "trend": trend,
                    "trend_pct": round(change_pct, 2),
                    "volume": int(c_data.get('usd_24h_vol', 0)),
                    "error": None
                }
            else:
                results[cid] = _empty_market_data(cid, "Not found on CoinGecko")
                
        return results
        
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        return {cid: _empty_market_data(cid, str(e)) for cid in crypto_ids}

def _empty_market_data(symbol: str, error: str = "Data unavailable") -> Dict[str, Any]:
    return {
        "symbol": symbol,
        "price": 0.0,
        "trend": "Unknown",
        "trend_pct": 0.0,
        "volume": 0,
        "error": error
    }

def get_multiple_stocks(symbols: List[str]) -> Dict[str, Dict]:
    """Batch fetch utility for multiple stocks."""
    results = {}
    for symbol in symbols:
        results[symbol] = get_stock_data(symbol)
    return results

if __name__ == "__main__":
    # Test script
    print("Testing Stock Data Fetch (TCS, RELIANCE):")
    print(get_multiple_stocks(["TCS", "RELIANCE"]))
    
    print("\nTesting Crypto Data Fetch:")
    print(get_crypto_data(["bitcoin", "ethereum"]))
