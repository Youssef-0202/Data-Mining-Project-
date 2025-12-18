# Plan Semaine 1 : Data & Machine Learning (Le Socle)

Cette semaine est cruciale. Nous allons construire les fondations du projet : les données et le premier modèle de référence. Si cette étape est ratée, les modèles complexes (LSTM) ne fonctionneront pas.

## 📂 Architecture de la Semaine 1

```
DM Project/
├── data/
│   ├── raw/                # Données brutes téléchargées (stock_prices.csv)
│   └── processed/          # Données avec indicateurs (features.csv)
├── notebooks/
│   ├── 1_data_collection.ipynb    # Tâche 1 : Téléchargement & Nettoyage
│   ├── 2_feature_engineering.ipynb # Tâche 2 : Création des indicateurs (RSI, MACD)
│   └── 3_baseline_vs_xgboost.ipynb # Tâche 3 : Modèles (Naïf vs XGBoost)
├── src/
│   ├── data_loader.py      # Fonctions pour charger les données
│   └── features.py         # Fonctions pour calculer RSI, MACD (réutilisable)
└── requirements.txt        # Bibliothèques nécessaires
```

## ✅ Liste des Tâches (To-Do List)

### Jour 1 : Données & Exploration
- [ ] **Installation** : Installer les librairies (`pip install -r requirements.txt`).
- [ ] **Collecte** : Télécharger les données via `yfinance` (AAPL, MSFT, TSLA, SP500, VIX, TNX).
- [ ] **Nettoyage** : Gérer les jours fériés et les valeurs manquantes (interpolation).
- [ ] **Visualisation** : Tracer les courbes de prix et de volume. Vérifier la corrélation avec le VIX.

### Jour 2 : Feature Engineering (La "Recette Secrète")
- [ ] **Indicateurs Techniques** : Calculer RSI, MACD, Bollinger Bands, ATR.
- [ ] **Stationnarité** : Créer la variable cible `Log_Return` (Rendement Logarithmique) au lieu du Prix.
- [ ] **Lags** : Créer les variables retardées (t-1, t-2, t-3) pour donner de la "mémoire" au modèle ML.
- [ ] **Split** : Diviser en Train (2020-2023) / Val (2024) / Test (2025).

### Jour 3 : Modélisation Initiale
- [ ] **Baseline Naïve** : Implémenter la prédiction "Demain = Aujourd'hui". Calculer le RMSE et la Précision Directionnelle.
- [ ] **XGBoost** : Entraîner un modèle XGBoost sur les features créées.
- [ ] **Comparaison** : Le XGBoost bat-il la Baseline ? Si oui, de combien ?
- [ ] **Analyse** : Regarder la "Feature Importance" (Quels indicateurs comptent le plus ?).

---

## 🚀 Objectif de fin de semaine
Avoir un tableau comparatif simple :
| Modèle | RMSE | Directional Accuracy |
| :--- | :--- | :--- |
| Naive | 1.5% | 50% |
| XGBoost | 1.2% | 54% |
