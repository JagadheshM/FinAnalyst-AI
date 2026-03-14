from typing import Dict, Any, List
from ..orchestration.state import WorkflowState
from ..tools.market_data import get_multiple_stocks, get_crypto_data

def market_data_node(state: WorkflowState) -> WorkflowState:
    """
    Agent 4: Market Data Fetcher
    Takes identified stocks from the state and fetches their real-time data.
    """
    print("--- 📈 Market Data Agent: Fetching Prices ---")
    
    stocks = state.get("stocks_identified", [])
    if not stocks:
        print("No stocks identified to fetch data for.")
        return {"market_data": {}}
        
    print(f"Fetching data for: {stocks}")
    
    # We differentiate crypto vs equities basically. 
    # For MVP, rely on yfinance for everything except known top cryptos.
    cryptos = {"BITCOIN", "ETHEREUM", "SOLANA", "BINANCECOIN", "RIPPLE", "CARDANO"}
    
    crypto_to_fetch = []
    equities_to_fetch = []
    
    for symbol in stocks:
        sym_upper = symbol.upper()
        if sym_upper in cryptos:
            crypto_to_fetch.append(sym_upper.lower())
        else:
            equities_to_fetch.append(symbol)
            
    market_data = {}
    
    # Fetch equities (NSE/BSE)
    if equities_to_fetch:
        stock_data = get_multiple_stocks(equities_to_fetch)
        market_data.update(stock_data)
        
    # Fetch crypto
    if crypto_to_fetch:
        crypto_data = get_crypto_data(crypto_to_fetch)
        # Re-key with the original uppercase symbol name expected by the system
        for key, val in crypto_data.items():
            market_data[key.upper()] = val
            
    print(f"✅ Fetched data for {len(market_data)} assets.")
    
    return {"market_data": market_data}
