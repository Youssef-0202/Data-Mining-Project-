# Explication des Données du Projet

Ce document détaille les données financières et macroéconomiques collectées pour le projet de prédiction boursière.

## 1. Les Actifs Cibles (Stocks)
Ce sont les entreprises dont nous voulons prédire le prix ou la tendance.

| Symbole | Entreprise | Secteur | Pourquoi ce choix ? |
| :--- | :--- | :--- | :--- |
| **AAPL** | Apple Inc. | Technologie (Hardware) | La plus grande capitalisation boursière. Très liquide et représentative du marché tech. |
| **MSFT** | Microsoft Corp. | Technologie (Software/Cloud) | Un géant stable, souvent corrélé à Apple mais avec des dynamiques différentes (Cloud/AI). |
| **TSLA** | Tesla Inc. | Automobile / Tech | **Très volatile**. C'est un excellent test pour voir si nos modèles peuvent gérer des mouvements de prix rapides et imprévisibles. |

## 2. Les Indicateurs Macro-Économiques (Context)
Ces indicateurs ne sont pas prédits, mais utilisés comme **features (entrées)** pour aider le modèle à comprendre l'environnement global.

### `^GSPC` (S&P 500 Index)
*   **Définition :** L'indice des 500 plus grandes entreprises américaines cotées.
*   **Rôle :** Représente la "santé générale" du marché US.
*   **Utilité :** Si le S&P 500 chute, il est probable que AAPL et MSFT chutent aussi (Corrélation de marché).

### `^VIX` (CBOE Volatility Index)
*   **Surnom :** "L'indice de la peur" (Fear Index).
*   **Définition :** Mesure l'anticipation de la volatilité par le marché pour les 30 prochains jours.
*   **Interprétation :**
    *   **< 20 :** Marché calme, confiance (Bull Market).
    *   **> 30 :** Peur, incertitude, risque de crash (Bear Market).
*   **Utilité :** Prédire les retournements de tendance majeurs.

### `^TNX` (CBOE 10-Year Treasury Note Yield)
*   **Définition :** Le taux d'intérêt des obligations d'État américaines à 10 ans.
*   **Rôle :** Représente le "coût de l'argent" sans risque.
*   **Utilité :**
    *   Quand les taux **montent**, les actions technologiques (Growth Stocks comme Tesla) ont tendance à **baisser** car leurs profits futurs valent moins aujourd'hui (actualisation).
    *   C'est une relation inverse clé à capturer par le modèle.

## 3. Structure des Données
Les données sont des séries temporelles journalières (Daily Time Series).

*   **Période :** 01/01/2020 au 31/12/2025 (ou date actuelle).
*   **Fréquence :** Jours de bourse (lundi au vendredi, hors jours fériés).
*   **Variable Clé :** `Close` (Prix de clôture ajusté).

## 4. Prochaines Étapes (Feature Engineering)
Nous allons transformer ces prix bruts en indicateurs mathématiques :
1.  **Log-Returns :** $\ln(P_t / P_{t-1})$ pour rendre la série stationnaire.
2.  **RSI (Relative Strength Index) :** Pour savoir si l'action est surachetée ou survendue.
3.  **MACD :** Pour identifier la direction du momentum.
4.  **Lags :** Utiliser les rendements des jours J-1, J-2, J-3 pour prédire J.
