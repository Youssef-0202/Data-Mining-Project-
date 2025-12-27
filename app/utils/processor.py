import pandas as pd
import numpy as np

def calculate_indicators(df):
    """
    Calculate technical indicators for the given dataframe.
    Expects a dataframe with 'Open', 'High', 'Low', 'Close', 'Volume' columns.
    """
    df = df.copy()
    
    # RSI
    if 'RSI' not in df.columns:
        window = 14
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    if 'MACD' not in df.columns:
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    if 'BB_Upper' not in df.columns:
        rolling_mean = df['Close'].rolling(window=20).mean()
        rolling_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = rolling_mean + (rolling_std * 2)
        df['BB_Lower'] = rolling_mean - (rolling_std * 2)
    
    # ATR (Average True Range)
    if 'ATR' not in df.columns and all(col in df.columns for col in ['High', 'Low', 'Close']):
        high = df['High']
        low = df['Low']
        close_prev = df['Close'].shift(1)
        tr1 = high - low
        tr2 = abs(high - close_prev)
        tr3 = abs(low - close_prev)
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=14).mean()
    
    # Log Returns and Lags (Force recalculation for accuracy)
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    
    for lag in range(1, 6):
        col = f'Log_Return_lag_{lag}'
        if col not in df.columns:
            df[col] = df['Log_Return'].shift(lag)
        
    return df

def prepare_features_for_prediction(df, macro_df):
    """
    Merge stock data with macro data and clean up for prediction.
    """
    # Ensure both dataframes are timezone-naive to avoid join errors
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    if macro_df.index.tz is not None:
        macro_df.index = macro_df.index.tz_localize(None)

    # Avoid overlapping columns (e.g., if df already has VIX/TNX from local fallback)
    cols_to_drop = [col for col in macro_df.columns if col in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        
    # Merge on index (Date)
    combined_df = df.join(macro_df, how='inner')
    
    # Drop rows with NaN values (due to indicators/lags)
    combined_df = combined_df.dropna()
    
    return combined_df

def run_backtest(df, model, feature_names):
    """
    Simulate a trading strategy based on model predictions.
    """
    # Prepare data
    X = df[feature_names]
    
    # Generate predictions for the entire dataset
    df['Signal'] = model.predict(X)
    
    # Calculate Strategy Returns
    # If Signal is 1 (Buy), we get the next day's return
    # We add a 0.1% transaction cost whenever the signal changes (trade executed)
    df['Trade'] = df['Signal'].diff().fillna(0).abs()
    transaction_cost = 0.001 # 0.1%
    
    df['Strategy_Return'] = (df['Signal'] * df['Log_Return'].shift(-1)) - (df['Trade'] * transaction_cost)
    
    # Cumulative Returns (Corrected for Log Returns)
    # Formula: exp(cumsum(log_returns))
    df['Cumulative_Market'] = np.exp(df['Log_Return'].cumsum())
    df['Cumulative_Strategy'] = np.exp(df['Strategy_Return'].cumsum())
    
    return df
