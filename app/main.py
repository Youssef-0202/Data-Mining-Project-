import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import fetch_stock_data, fetch_macro_data
from utils.processor import calculate_indicators

# Page Configuration
st.set_page_config(
    page_title="Finance | AI Stock Predictor",
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
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #3e4259;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Tab Styling Redesign */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: #1e2130;
        border-radius: 8px 8px 0 0;
        padding: 10px 30px;
        color: #888;
        font-weight: 600;
        border: 1px solid #3e4259;
        border-bottom: none;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2980b9 !important;
        color: white !important;
        border-color: #2980b9 !important;
        box-shadow: 0 -4px 10px rgba(41, 128, 185, 0.2);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2c3148;
        color: #fff;
    }
    /* Section Header Styling */
    .section-header {
        padding: 20px;
        border-left: 5px solid #2980b9;
        background-color: rgba(41, 128, 185, 0.05);
        margin-bottom: 25px;
        border-radius: 0 12px 12px 0;
    }
    .section-header h3 {
        color: #2980b9;
        margin-bottom: 10px;
        font-size: 1.5rem;
    }
    .interest-box {
        color: #e0e0e0;
        font-size: 1rem;
        line-height: 1.6;
    }
    .benefit-tag {
        display: inline-block;
        background-color: #2c3148;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 8px;
        margin-top: 8px;
        border: 1px solid #3e4259;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Finance | AI Stock Predictor")
st.sidebar.markdown("---")
ticker = st.sidebar.selectbox("Select Asset", ["AAPL", "MSFT", "TSLA"])
time_period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=4)

st.sidebar.markdown("---")
st.sidebar.info("This app uses a hybrid XGBoost + LSTM model to predict market direction.")

# Main Header
st.title(f"Market Explorer: {ticker}")

# Load Data
with st.spinner("Fetching market data..."):
    data = fetch_stock_data(ticker, period=time_period)
    macro_data = fetch_macro_data(period=time_period)

if data is not None and not data.empty:
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
        st.markdown("""
            <div class="section-header">
                <h3>Technical Analysis (Descriptive)</h3>
                <div class="interest-box">
                    <b>Interest:</b> Understanding market structure and historical behavior. 
                    This module translates raw price data into visual patterns that reveal the "psychology" of the market.
                    <br>
                    <div class="benefit-tag">Trend Identification</div>
                    <div class="benefit-tag">Volatility Mapping</div>
                    <div class="benefit-tag">Support/Resistance</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
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
        
        st.plotly_chart(fig)

    with tab2:
        st.markdown("""
            <div class="section-header">
                <h3>AI Prediction Dashboard (Predictive)</h3>
                <div class="interest-box">
                    <b>Interest:</b> Gaining a statistical edge through machine learning. 
                    While human analysis is limited to a few indicators, our XGBoost model processes dozens of features simultaneously to detect non-linear signals.
                    <br>
                    <div class="benefit-tag">Signal Generation</div>
                    <div class="benefit-tag">Probability Assessment</div>
                    <div class="benefit-tag">Macro-Sentiment Integration</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
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
                latest_features = full_df.tail(1).drop(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Log_Return', 'BB_Upper', 'BB_Lower'], errors='ignore')
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
                        st.progress(float(confidence))
                else:
                    st.error(f"Missing features for prediction: {missing_features}")
            else:
                st.warning("Not enough data to generate a prediction. Try a longer time period.")
        else:
            st.error("AI Model not found. Please ensure the model is trained and saved.")

    with tab3:
        st.markdown("""
            <div class="section-header">
                <h3>Strategy Backtesting (Prescriptive)</h3>
                <div class="interest-box">
                    <b>Interest:</b> Risk management and strategy validation. 
                    A prediction is only useful if it translates into profit. This module simulates real-world trading to ensure the model outperforms a passive investment.
                    <br>
                    <div class="benefit-tag">Performance Audit</div>
                    <div class="benefit-tag">Risk/Reward Analysis</div>
                    <div class="benefit-tag">Strategy Optimization</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
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
                st.plotly_chart(fig_backtest)
            else:
                st.warning("Not enough data for backtesting.")
        else:
            st.error("Model not found.")

else:
    st.error(f"Failed to load market data for {ticker}.")
    st.info(f"The asset '{ticker}' might not be available in the local fallback data or there is a connectivity issue with Yahoo Finance.")
    if st.button("Retry"):
        st.rerun()
