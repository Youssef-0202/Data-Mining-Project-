import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import fetch_stock_data, fetch_macro_data
from utils.processor import calculate_indicators

# Page Configuration
st.set_page_config(
    page_title="Antigravity Finance | AI Stock Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e4259;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e2130;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2980b9;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Antigravity Finance")
st.sidebar.markdown("---")
ticker = st.sidebar.selectbox("Select Asset", ["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL"])
time_period = st.sidebar.selectbox("Time Period", ["1y", "2y", "5y", "max"], index=2)

st.sidebar.markdown("---")
st.sidebar.info("This app uses a hybrid XGBoost + LSTM model to predict market direction.")

# Main Header
st.title(f"Market Explorer: {ticker}")

# Load Data
with st.spinner("Fetching market data..."):
    data = fetch_stock_data(ticker, period=time_period)
    macro_data = fetch_macro_data(period=time_period)

if data is not None:
    # Process Indicators
    df = calculate_indicators(data)
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    last_close = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    
    col1.metric("Current Price", f"${last_close:,.2f}", f"{change:+.2f} ({pct_change:+.2f}%)")
    col2.metric("RSI (14)", f"{df['RSI'].iloc[-1]:.2f}")
    col3.metric("MACD", f"{df['MACD'].iloc[-1]:.4f}")
    
    atr_val = df['ATR'].iloc[-1] if 'ATR' in df.columns and not pd.isna(df['ATR'].iloc[-1]) else 0.0
    col4.metric("Volatility (ATR)", f"{atr_val:.2f}")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Technical Analysis", "AI Predictions", "Backtesting"])

    with tab1:
        st.subheader("Interactive Price Chart")
        
        # Add a Key/Legend for symbols
        with st.expander("Legend & Indicator Meanings"):
            st.markdown("""
            - **Candlestick/Line**: Represents the price movement (Open, High, Low, Close).
            - **Blue Shaded Area (Bollinger Bands)**: Measures market volatility. Prices touching the edges often signal potential reversals.
            - **Orange Line (RSI)**: Relative Strength Index. Measures momentum.
                - <span style='color:red'>**Red Dash (70)**</span>: Overbought zone (Price might be too high).
                - <span style='color:green'>**Green Dash (30)**</span>: Oversold zone (Price might be too low).
            """, unsafe_allow_html=True)

        # Create Plotly Chart with more spacing
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.15, # Increased spacing
                           subplot_titles=(f'{ticker} Price & Volatility', 'Momentum (RSI)'), 
                           row_width=[0.4, 0.6])

        # Candlestick or Line Chart depending on available data
        if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            fig.add_trace(go.Candlestick(x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'],
                            name="Price"), row=1, col=1)
        elif 'Close' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Price (Close Only)", line=dict(color='white')), row=1, col=1)
            st.warning("⚠️ Local data is missing OHLC values. Displaying Close price only.")

        # Bollinger Bands
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='Upper Band', line=dict(color='rgba(173, 216, 230, 0.4)')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='Lower Band', line=dict(color='rgba(173, 216, 230, 0.4)'), fill='tonexty'), row=1, col=1)

        # RSI
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='orange')), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        fig.update_layout(height=800, template="plotly_dark", showlegend=False,
                          xaxis_rangeslider_visible=False)
        
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("AI Prediction Dashboard")
        
        # Load Model
        import joblib
        import os
        
        model_path = "app/models/xgboost_model.joblib"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            
            # Prepare features for the latest date
            from utils.processor import prepare_features_for_prediction
            
            # We need macro data for prediction
            full_df = prepare_features_for_prediction(df, macro_data)
            
            if not full_df.empty:
                latest_features = full_df.tail(1).drop(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Log_Return', 'BB_Upper', 'BB_Lower'])
                # Ensure feature order matches training
                feature_names = ['RSI', 'MACD', 'MACD_Signal', 'Log_Return_lag_1', 
                                'Log_Return_lag_2', 'Log_Return_lag_3', 'Log_Return_lag_4', 
                                'Log_Return_lag_5', 'VIX', 'TNX']
                
                # Check if all features are present
                missing_features = [f for f in feature_names if f not in latest_features.columns]
                if not missing_features:
                    X_pred = latest_features[feature_names]
                    
                    # Prediction
                    prediction = model.predict(X_pred)[0]
                    prob = model.predict_proba(X_pred)[0]
                    confidence = prob[1] if prediction == 1 else prob[0]
                    
                    # Display Signal
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if prediction == 1:
                            st.success("SIGNAL: BUY / BULLISH")
                        else:
                            st.error("SIGNAL: SELL / BEARISH")
                        st.metric("Confidence Score", f"{confidence:.2%}")
                    
                    with col2:
                        st.write("### Model Interpretation")
                        st.write("The model analyzes technical indicators and macro volatility to determine the most likely direction for the next period.")
                        st.progress(confidence)
                else:
                    st.error(f"Missing features for prediction: {missing_features}")
            else:
                st.warning("Not enough data to generate a prediction. Try a longer time period.")
        else:
            st.error("AI Model not found. Please ensure the model is trained and saved.")

    with tab3:
        st.subheader("Strategy Backtesting")
        
        if os.path.exists(model_path):
            from utils.processor import run_backtest
            
            # We need the full processed data
            full_df = prepare_features_for_prediction(df, macro_data)
            
            if not full_df.empty:
                feature_names = ['RSI', 'MACD', 'MACD_Signal', 'Log_Return_lag_1', 
                                'Log_Return_lag_2', 'Log_Return_lag_3', 'Log_Return_lag_4', 
                                'Log_Return_lag_5', 'VIX', 'TNX']
                
                backtest_results = run_backtest(full_df, model, feature_names)
                
                # Metrics
                final_market = backtest_results['Cumulative_Market'].iloc[-2] # -2 because shift(-1)
                final_strategy = backtest_results['Cumulative_Strategy'].iloc[-2]
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Market Return (Buy & Hold)", f"{(final_market-1):.2%}")
                col2.metric("AI Strategy Return", f"{(final_strategy-1):.2%}")
                col3.metric("Outperformance", f"{(final_strategy - final_market):+.2%}")
                
                # Chart
                fig_backtest = go.Figure()
                fig_backtest.add_trace(go.Scatter(x=backtest_results.index, y=backtest_results['Cumulative_Market'], name="Buy & Hold", line=dict(color='gray', dash='dash')))
                fig_backtest.add_trace(go.Scatter(x=backtest_results.index, y=backtest_results['Cumulative_Strategy'], name="AI Strategy", line=dict(color='cyan', width=3)))
                
                fig_backtest.update_layout(title="Cumulative Returns Comparison", template="plotly_dark", height=500)
                st.plotly_chart(fig_backtest, use_container_width=True)
            else:
                st.warning("Not enough data for backtesting.")
        else:
            st.error("Model not found.")

else:
    st.error("Failed to load market data.")
    st.info("This is often due to a network timeout or DNS issue with the Yahoo Finance API. Please check your internet connection and try again.")
    st.button("Retry")
