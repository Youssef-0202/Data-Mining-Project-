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

## 5. Ingénierie des Caractéristiques (Feature Engineering)

Cette phase transforme les prix bruts en indicateurs exploitables par les modèles d'apprentissage automatique.

### A. Indicateurs Techniques
*   **Log Returns (Rendements Logarithmiques) :** Utilisés à la place des prix bruts pour assurer la stationnarité de la série temporelle.
*   **RSI (Relative Strength Index) :** Mesure la vitesse et le changement des mouvements de prix (surachat > 70, survente < 30).
*   **MACD (Moving Average Convergence Divergence) :** Indicateur de tendance qui montre la relation entre deux moyennes mobiles des prix.
*   **Bandes de Bollinger :** Mesurent la volatilité du marché (l'écart entre les bandes supérieures et inférieures).

### B. Caractéristiques Temporelles (Lags)
*   **Lag_1 à Lag_5 :** Nous avons inclus les rendements des 5 jours précédents. Cela permet au modèle de capturer la mémoire à court terme du marché (autocorrélation).

### C. Indicateurs Macro-économiques
*   **VIX (Indice de Volatilité) :** Surnommé "l'indice de la peur", il mesure la volatilité attendue du S&P 500.
*   **TNX (Treasury Yield 10 Years) :** Représente le taux d'intérêt des obligations d'État américaines à 10 ans, influençant le coût du capital pour les entreprises technologiques.

### D. Variable Cible (Target)
*   **Direction :** Variable binaire (0 ou 1). 
    *   `1` : Le rendement logarithmique est positif (Hausse).
    *   `0` : Le rendement logarithmique est négatif ou nul (Baisse).
