# 📈 Antigravity Finance App

Cette application Streamlit permet de visualiser les données boursières, de générer des prédictions via un modèle XGBoost et de tester des stratégies de trading.

## Structure
- `main.py` : Point d'entrée de l'application.
- `utils/` : Modules pour le chargement et le traitement des données.
- `models/` : Contient le modèle XGBoost entraîné.

## Installation
Assurez-vous d'avoir installé les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement
Pour lancer l'application localement :
```bash
streamlit run app/main.py
```

## Fonctionnalités
1. **Market Explorer** : Visualisation interactive des prix et indicateurs techniques (RSI, MACD, Bollinger).
2. **AI Prediction** : Signaux d'achat/vente générés en temps réel par le modèle XGBoost.
3. **Backtesting** : Comparaison de la performance de l'IA par rapport à une stratégie passive.
