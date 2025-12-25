import yfinance as yf
import pandas as pd
import numpy as np
import os

def fetch_stock_data(ticker, period="5y", interval="1d"):
    """
    Fetch historical stock data from yfinance with local fallback.
    """
    try:
        # Try online first
        tk = yf.Ticker(ticker)
        data = tk.history(period=period, interval=interval, auto_adjust=True)
        
        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            return data
    except Exception as e:
        print(f"Online fetch failed for {ticker}: {e}")

    # Fallback to local data
    print(f"Attempting local fallback for {ticker}...")
    local_path = "data/processed/features.csv"
    try:
        if os.path.exists(local_path):
            df = pd.read_csv(local_path, index_col=0, parse_dates=True)
            if 'Ticker' in df.columns:
                df = df[df['Ticker'] == ticker]
            
            # Ensure required columns for the UI exist
            # If local data is missing OHLC, we try to map them or fill with Close
            required = ['Open', 'High', 'Low', 'Close']
            for col in required:
                if col not in df.columns:
                    if 'Close' in df.columns:
                        df[col] = df['Close']
                    else:
                        # If even Close is missing, this local file is not suitable
                        return None
            return df
    except Exception as e:
        print(f"Local fallback failed: {e}")
    
    return None

def fetch_macro_data(period="5y"):
    """
    Fetch macro indicators with local fallback.
    """
    try:
        vix_tk = yf.Ticker("^VIX")
        vix_data = vix_tk.history(period=period, auto_adjust=True)
        
        tnx_tk = yf.Ticker("^TNX")
        tnx_data = tnx_tk.history(period=period, auto_adjust=True)
        
        if not vix_data.empty and not tnx_data.empty:
            vix = vix_data['Close']
            tnx = tnx_data['Close']
            macro_df = pd.concat([vix, tnx], axis=1)
            macro_df.columns = ["VIX", "TNX"]
            return macro_df.ffill().bfill()
    except Exception as e:
        print(f"Online macro fetch failed: {e}")

    # Fallback to local data
    local_path = "data/processed/features.csv"
    try:
        if os.path.exists(local_path):
            df = pd.read_csv(local_path, index_col=0, parse_dates=True)
            if "VIX" in df.columns and "TNX" in df.columns:
                return df[["VIX", "TNX"]].ffill().bfill()
    except Exception as e:
        print(f"Local macro fallback failed: {e}")
        
    return pd.DataFrame(columns=["VIX", "TNX"])
