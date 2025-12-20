import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(page_title="Stock Prediction App", layout="wide")

st.title("📈 Application de Prédiction Boursière")
st.markdown("Cette application utilise le **Data Mining** pour prédire les tendances du marché.")

# --- SIDEBAR ---
st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Sélectionnez un actif", ["AAPL", "MSFT", "TSLA"])
days_to_show = st.sidebar.slider("Nombre de jours à afficher", 30, 365, 180)

# --- DATA LOADING ---
@st.cache_data
def load_data(symbol, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    try:
        # auto_adjust=True removes the warning
        # progress=False cleans up your terminal
        data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True, progress=False)
        return data
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return pd.DataFrame()

st.write(f"### Analyse de {ticker}")
data = load_data(ticker, days_to_show)

# --- VISUALIZATION ---
if not data.empty:
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    
    fig.update_layout(title=f"Prix de {ticker}", yaxis_title="Prix ($)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("#### Aperçu des données")
    st.dataframe(data.tail())
else:
    st.error("Erreur lors du chargement des données.")