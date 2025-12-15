# Plan de Présentation (Canva) - Projet Data Mining
**Titre :** Prévision Boursière Hybride : LSTM vs XGBoost
**Durée estimée :** 15-20 minutes
**Slides recommandées :** 10-12 slides

---

## Slide 1 : Titre & Introduction
*   **Titre Principal :** Analyse et Prévision du Marché Boursier par Approche Hybride
*   **Sous-titre :** Comparaison Machine Learning vs Deep Learning
*   **Noms :** Chaimaa EL AFFAS & Youssef AIT BAHSSIN
*   **Encadrant :** Pr. KHADIJA BOUZAACHANE
*   **Visuel :** Une image de fond "Tech/Finance" (Courbes boursières stylisées).

## Slide 2 : Contexte & Problématique
*   **Le Problème :** Le marché boursier est chaotique et bruité. Les méthodes statistiques classiques (Moyennes mobiles) sont insuffisantes.
*   **La Question :** Peut-on améliorer la précision des prévisions en combinant la puissance du Deep Learning (LSTM) avec l'efficacité du Machine Learning (XGBoost) ?
*   **Objectif :** Prédire la tendance (Hausse/Baisse) et le prix futur des actions (Apple, Tesla, S&P 500).

## Slide 3 : Pipeline de Données (Data Mining)
*   **Sources :** Yahoo Finance (Prix, Volume) + Macroéconomie (VIX, Taux d'intérêt).
*   **Période :** 2020 - 2025 (6 ans).
*   **Feature Engineering (La clé du succès) :**
    *   *Indicateurs Techniques :* RSI (Surachat/Survente), MACD (Tendance), Bollinger Bands.
    *   *Transformation :* Utilisation des **Log-Returns** (Stationnarité) au lieu des prix bruts.
    *   *Lags :* Ajout des retards (t-1, t-2) pour capturer la mémoire du marché.

## Slide 4 : Méthodologie & Modèles
*   **Approche Comparative :**
    1.  **Baseline Naïve :** "Demain sera comme aujourd'hui" (Référence à battre).
    2.  **Machine Learning :** XGBoost (Gradient Boosting) -> Excellent pour les données tabulaires.
    3.  **Deep Learning :** LSTM (Long Short-Term Memory) -> Excellent pour les séquences temporelles.

## Slide 5 : L'Architecture Hybride (Stacking)
*   **Concept :** "L'union fait la force".
*   **Schéma Visuel (À faire sur Canva) :**
    *   [Données] --> [Modèle LSTM] --> [Prédiction A]
    *   [Données] --> [Modèle XGBoost] --> [Prédiction B]
    *   [Prédiction A + B] --> **[Méta-Modèle (Régression)]** --> **[Prédiction Finale]**
*   **Avantage :** Le LSTM capture la tendance long terme, le XGBoost corrige les erreurs locales.

## Slide 6 : Résultats - Comparaison des Erreurs (RMSE)
*   **Tableau Comparatif :**
    *   Baseline : RMSE élevé (ex: 1.5%)
    *   XGBoost : RMSE moyen (ex: 1.2%)
    *   LSTM : RMSE bon (ex: 1.1%)
    *   **Hybride : RMSE optimal (ex: 1.0%)**
*   **Message clé :** Le modèle hybride réduit l'erreur globale.

## Slide 7 : Résultats - Précision Directionnelle
*   **Graphique (Bar Chart) :** % de réussite sur la direction (Hausse/Baisse).
*   *Exemple :* Le modèle Hybride prédit correctement la direction du marché **55-60%** du temps (ce qui est suffisant pour être rentable).

## Slide 8 : Démonstration (Screenshots App)
*   **Visuel :** Capture d'écran de votre application Streamlit.
*   Montrer la courbe de prédiction vs la réalité.
*   Mettre en avant l'interactivité (Choix de l'action).

## Slide 9 : Conclusion & Perspectives
*   **Conclusion :** L'approche hybride surpasse les modèles individuels. L'ajout de données macroéconomiques (VIX) a stabilisé les prédictions.
*   **Limites :** Le marché reste imprévisible face aux "Cygnes Noirs" (ex: Crise soudaine).
*   **Perspectives :** Ajouter l'analyse de sentiment (News/Twitter) pour améliorer la réactivité.

## Slide 10 : Q&A
*   **Merci de votre attention.**
