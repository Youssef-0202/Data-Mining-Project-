# 🚀 Guide de Travail : Étapes Restantes du Projet

Ce document résume les tâches à accomplir pour finaliser la partie scientifique du projet. Les Notebooks 1, 2 et 3 étant terminés, voici la suite :

---

## 📂 Notebook 4 : Analyse Économétrique (ARIMA)
**Nom du fichier :** `4_arima_analysis.ipynb`

### 🎯 Objectif
Répondre à la demande de la professeure sur la stationnarisation formelle.
1. **Test ADF :** Prouver la non-stationnarité du prix brut (`Close`).
2. **Stationnarisation :** Appliquer la différenciation ($d=1$).
3. **Modélisation :** Identifier $p$ et $q$ via ACF/PACF et entraîner le modèle ARIMA.
4. **Benchmark :** Comparer l'accuracy d'ARIMA avec celle de XGBoost (Notebook 3).

---

## 📂 Notebook 5 : Modèles de Deep Learning
**Nom du fichier :** `5_deep_learning_models.ipynb`

### 🎯 Objectif
Capturer les dépendances temporelles complexes.
1. **Séquençage :** Préparer les données en 3D `[samples, time_steps, features]`.
2. **Normalisation :** Utiliser `MinMaxScaler` (obligatoire pour les RNN).
3. **Modèles :** Implémenter **LSTM** et **GRU avec Attention**.
4. **Évaluation :** Comparer avec XGBoost et ARIMA.

---

## 📂 Notebook 6 : Évaluation & Backtesting
**Nom du fichier :** `6_evaluation_and_backtesting.ipynb`

### 🎯 Objectif
Transformer les prédictions en résultats financiers.
1. **Simulation :** Calculer les rendements d'une stratégie basée sur les prédictions.
2. **Métriques :** Calculer le **Ratio de Sharpe** et le **Maximum Drawdown**.
3. **Visualisation :** Tracer la courbe de gains (Equity Curve) comparée au "Buy & Hold".

---

## 💡 Conseils pour la réussite
*   **Données :** Utilise toujours `data/processed/features.csv`.
*   **Split :** Garde le split temporel 80/20 pour la cohérence.
*   **Sauvegarde :** Enregistre les modèles dans le dossier `models/` pour l'intégration dans l'application Streamlit.
*   **Interprétation :** Ajoute des explications en Français (HTML/Markdown) pour chaque résultat important.

---

## 🤝 Coordination
Je m'occupe de la partie **Application Streamlit**. Dès que tes modèles sont prêts, nous les intégrerons pour les tests en temps réel.

Bon courage Chaimaa ! 💪
