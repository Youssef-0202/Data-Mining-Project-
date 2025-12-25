import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib
import os

def train_and_save_model():
    # Load data
    data_path = 'data/processed/features.csv'
    if not os.path.exists(data_path):
        print("Data not found!")
        return

    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    df = df.sort_index()

    # Define features and target
    # Based on the notebook, we use 'pure' features to avoid data leakage
    features = ['RSI', 'MACD', 'MACD_Signal', 'Log_Return_lag_1', 
                'Log_Return_lag_2', 'Log_Return_lag_3', 'Log_Return_lag_4', 
                'Log_Return_lag_5', 'VIX', 'TNX']
    
    X = df[features]
    y = df['Direction']

    # Best parameters from Grid Search
    best_params = {
        'colsample_bytree': 0.8,
        'learning_rate': 0.05,
        'max_depth': 5,
        'n_estimators': 100,
        'subsample': 0.9,
        'use_label_encoder': False,
        'eval_metric': 'logloss',
        'random_state': 42
    }

    # Train model
    model = XGBClassifier(**best_params)
    model.fit(X, y)

    # Save model
    model_dir = 'models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    model_path = os.path.join(model_dir, 'xgboost_model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
