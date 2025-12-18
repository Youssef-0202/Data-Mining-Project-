# Plan de Projet Révisé : Plateforme d'Analyse et de Prévision Boursière
**Module :** Data Mining  
**Date :** Décembre 2025  
**Réalisé par :** Chaimaa EL AFFAS & Youssef AIT BAHSSIN  
**Encadré par :** Pr. KHADIJA BOUZAACHANE  

---

## 1. Contexte et Vision
Le marché boursier est un système complexe et bruité. Les approches classiques échouent souvent à capturer les non-linéarités et la volatilité. Ce projet vise à dépasser la simple analyse statistique en appliquant des techniques avancées de **Deep Learning** et de **Machine Learning** pour prédire non seulement les prix, mais aussi la tendance future des actifs.

L'objectif final n'est pas seulement un rapport académique, mais une **Application Web Interactive** permettant à un utilisateur de visualiser les prédictions en temps réel et de comparer les performances des modèles.

## 2. Objectifs du Projet
1.  **Pipeline de Données Robuste :** Collecte automatisée de données financières et macroéconomiques (VIX, Taux d'intérêt).
2.  **Comparaison Scientifique :** Mise en compétition de 6 architectures (ML vs DL) contre une "Baseline" naïve.
3.  **Application de Démonstration :** Développement d'un Dashboard interactif pour visualiser les résultats.
4.  **Stratégie de Trading :** Évaluation de la rentabilité (Backtesting) des modèles.

## 3. Données et Feature Engineering
**Sources :** Yahoo Finance API (`yfinance`).
*   **Actifs Cibles :** S&P 500, Apple (AAPL), Microsoft (MSFT), Tesla (TSLA).
*   **Indicateurs Macro (Nouveau) :** 
    *   `^VIX` (Indice de la peur/volatilité).
    *   `^TNX` (Taux obligataires 10 ans US - contexte économique).

**Traitements :**
*   **Stationnarité :** Utilisation des *Log-Returns* au lieu des prix bruts pour l'entraînement.
*   **Indicateurs Techniques :** RSI, MACD, Bollinger Bands, ATR (Volatilité).
*   **Lags :** Création de variables retardées (t-1, t-2...) pour capturer la mémoire du marché.

## 4. Approches de Modélisation
Nous adopterons une approche incrémentale, du plus simple au plus complexe :

### Niveau 0 : La Référence (Baseline)
*   **Naive Forecast :** Prédiction $P_{t+1} = P_t$. Tout modèle complexe doit battre cette référence pour être considéré comme utile.

### Niveau 1 : Machine Learning (Interprétabilité)
*   **XGBoost & Random Forest :** Pour identifier les variables les plus importantes (Feature Importance) et établir une performance solide sur données tabulaires.

### Niveau 2 : Deep Learning (Séquentiel)
*   **LSTM (Long Short-Term Memory) :** Pour capturer les dépendances à long terme.
*   **GRU-Attention :** Pour focaliser le modèle sur les jours passés les plus pertinents (mécanisme d'attention).
*   **CNN-LSTM :** Hybride (CNN pour extraire les patterns locaux + LSTM pour la séquence).

### Niveau 3 : Modèle Hybride (Stacking)
*   **LSTM + XGBoost Stacking :** Une approche puissante où les prédictions du LSTM et du XGBoost sont utilisées comme *entrées* pour un méta-modèle (Régression Linéaire ou Random Forest).
    *   *Pourquoi ?* Le LSTM capture les tendances temporelles, le XGBoost capture les seuils de décision. Le mélange des deux réduit souvent la variance de l'erreur.

## 5. L'Application de Démonstration (Web App)
Une interface utilisateur simple développée avec **Streamlit (Python)**.
*   **Fonctionnalités :**
    *   Sélecteur d'action (Apple, Tesla, etc.).
    *   Sélecteur de modèle (Voir la prédiction du LSTM vs XGBoost).
    *   Graphiques interactifs (Prix historique + Prédiction future).
    *   Panneau de métriques (RMSE, Précision Directionnelle).

## 6. Métriques d'Évaluation Améliorées
Au-delà du simple RMSE, nous utiliserons :
1.  **Directional Accuracy (DA) :** Le modèle a-t-il correctement prédit la hausse ou la baisse ? (Crucial pour le trading).
2.  **Profitability (Backtest) :** Si on avait suivi le modèle, quel serait le ROI (Retour sur Investissement) ?

## 7. Planning Accéléré (3 Semaines)
Compte tenu des contraintes de temps, le projet se concentre sur l'essentiel : la rigueur de l'analyse Data Mining et la comparaison des modèles. L'application sera minimaliste.

| Semaine | Phase | Tâches Prioritaires |
| :--- | :--- | :--- |
| **S1** | **Data & ML (Le Socle)** | 1. Collecte & Nettoyage (yfinance) - [x].<br>2. Feature Engineering Avancé (+ATR, ADX, CCI) - [x].<br>3. **XGBoost Optimisé (GA)** : Accuracy 63.36% - [x]. |
| **S2** | **Deep Learning & Hybride** | 1. Implémentation **LSTM**.<br>2. Création du **Modèle Hybride (Stacking)**.<br>3. Comparaison : Est-ce que le Hybride bat le LSTM seul ? |
| **S3** | **Démo & Présentation** | 1. **Mini-App Streamlit**.<br>2. **Création de la Présentation (Canva)** : Slides sur l'architecture Hybride et les résultats.<br>3. Rapport final. |

## 8. Livrables
1.  **Notebook Jupyter Principal** : Contient tout le pipeline (Data -> Models -> Eval). C'est le cœur du projet.
2.  **Mini-App de Démo** : Interface simple pour visualiser les courbes.
3.  **Rapport Synthétique** : Focus sur la méthodologie et l'interprétation des résultats.
