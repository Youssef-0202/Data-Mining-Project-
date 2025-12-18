import pandas as pd
import numpy as np

def calculate_rsi(series, window=14):
    """Calcule le Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series, slow=26, fast=12, signal=9):
    """Calcule le MACD et le Signal."""
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_bollinger_bands(series, window=20, num_std=2):
    """Calcule les Bandes de Bollinger (Upper, Lower)."""
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, lower_band

def add_lags(df, col_name, lags=3):
    """Ajoute des colonnes retardées (t-1, t-2, ...)."""
    df_lagged = df.copy()
    for lag in range(1, lags + 1):
        df_lagged[f'{col_name}_lag_{lag}'] = df_lagged[col_name].shift(lag)
    return df_lagged

def calculate_log_returns(series):
    """Calcule les rendements logarithmiques pour la stationnarité."""
    return np.log(series / series.shift(1))
