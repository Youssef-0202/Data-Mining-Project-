# Documentation de l'Application Streamlit

Ce document décrit la conception, les fonctionnalités et la pile technologique de l'application de démonstration pour le projet de Data Mining.

## 1. Objectif de l'App
L'objectif est de fournir une interface interactive permettant de visualiser les données financières, de générer des prédictions en temps réel à l'aide de nos modèles (XGBoost & LSTM) et de simuler des stratégies de trading basées sur ces prédictions.

## 2. Pile Technologique (Tech Stack)
*   **Framework UI :** [Streamlit](https://streamlit.io/) (Python-based web framework).
*   **Visualisation :** [Plotly](https://plotly.com/python/) pour des graphiques financiers interactifs.
*   **Backend :** Python (reutilisation des scripts de `src/`).
*   **Modèles :** 
    *   XGBoost (via `joblib`)
    *   LSTM (via `TensorFlow/Keras`)
*   **Données :** API `yfinance` pour les données de marché en direct.

## 3. Fonctionnalités Clés

### A. Explorateur de Marché (Analyse Descriptive)
*   **Sélecteur d'Actifs :** Choisir entre AAPL, MSFT, TSLA.
*   **Graphiques Techniques :** Visualisation interactive des prix avec indicateurs (RSI, MACD, Bandes de Bollinger).
*   **Analyse de Corrélation :** Heatmap dynamique montrant les relations entre les actifs et les indicateurs macro (VIX, TNX).

### B. Dashboard de Prédiction (Analyse Prédictive)
*   **Signal de Trading :** Affichage clair du signal (ACHAT / VENTE / NEUTRE).
*   **Score de Confiance :** Probabilité associée à la prédiction (ex: "65% de probabilité de hausse").
*   **Interprétabilité (SHAP/Feature Importance) :** Graphique montrant quels indicateurs influencent la décision actuelle du modèle.

### C. Simulateur de Backtesting (Analyse Prescriptive)
*   **Performance Historique :** Comparaison entre une stratégie "Buy & Hold" et la stratégie basée sur le modèle.
*   **Métriques de Trading :** Calcul du rendement cumulé, du drawdown maximum et du ratio de Sharpe.
*   **Comparaison de Modèles :** Duel entre XGBoost et LSTM sur une période donnée.

## 4. Structure du Code de l'App
L'application sera organisée dans un dossier `app/` :
```text
app/
├── main.py              # Point d'entrée Streamlit
├── pages/               # (Optionnel) Pour une app multi-pages
├── utils/
│   ├── data_loader.py   # Récupération des données via yfinance
│   └── processor.py     # Calcul des indicateurs (reprend src/features.py)
└── models/              # Stockage des modèles entraînés (.json, .h5)
```

## 5. Guide d'Installation (Futur)
Pour lancer l'application, il suffira d'exécuter :
```bash
pip install streamlit plotly
streamlit run app/main.py
```
