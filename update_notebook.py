import json
import os

notebook_path = 'notebooks/2_feature_engineering.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update cell 2 (index 2) - Data Loading
nb['cells'][2]['source'] = [
    "# Ajout du dossier src au chemin pour importer nos fonctions (si besoin)\n",
    "sys.path.append(os.path.abspath(os.path.join('..')))\n",
    "# On importe les fonctions depuis src/features.py\n",
    "from src.features import (calculate_rsi, calculate_macd, calculate_bollinger_bands, \n",
    "                          add_lags, calculate_log_returns, calculate_atr, \n",
    "                          calculate_adx, calculate_cci)\n",
    "\n",
    "# Chemin du fichier brut (contenant High, Low, Close, Volume)\n",
    "input_path = '../data/raw/stock_prices.csv'\n",
    "\n",
    "if not os.path.exists(input_path):\n",
    "    print(f\"ERREUR : Le fichier {input_path} est introuvable. Avez-vous exécuté le notebook 1 ?\")\n",
    "else:\n",
    "    # Chargement avec multi-index pour gérer Ticker et Price\n",
    "    df_raw = pd.read_csv(input_path, index_col=0, parse_dates=True, header=[0, 1])\n",
    "    print(\"Données brutes chargées avec succès !\")\n",
    "    print(df_raw.head())\n"
]

# Update cell 4 (index 4) - Feature Engineering Loop
nb['cells'][4]['source'] = [
    "# Liste des actions à traiter\n",
    "target_tickers = ['AAPL', 'MSFT', 'TSLA']\n",
    "\n",
    "# Liste pour stocker les résultats\n",
    "processed_data = []\n",
    "\n",
    "print(\"Début du Feature Engineering...\")\n",
    "\n",
    "for ticker in target_tickers:\n",
    "    print(f\"Traitement de l'action : {ticker}\")\n",
    "    \n",
    "    # On récupère les données pour cette action\n",
    "    if ticker not in df_raw.columns.get_level_values(0):\n",
    "        print(f\"  -> Attention : {ticker} non trouvé dans les colonnes.\")\n",
    "        continue\n",
    "        \n",
    "    # Extraction des colonnes OHLCV pour le ticker\n",
    "    ticker_data = df_raw[ticker].copy()\n",
    "    \n",
    "    # Création d'un DataFrame temporaire pour cette action\n",
    "    temp_df = pd.DataFrame(index=ticker_data.index)\n",
    "    temp_df['Close'] = ticker_data['Close']\n",
    "    temp_df['High'] = ticker_data['High']\n",
    "    temp_df['Low'] = ticker_data['Low']\n",
    "    temp_df['Ticker'] = ticker\n",
    "    \n",
    "    # --- 1. Cible (Target) : Log Returns ---\n",
    "    temp_df['Log_Return'] = calculate_log_returns(temp_df['Close'])\n",
    "    \n",
    "    # --- 2. Indicateurs Techniques Classiques ---\n",
    "    temp_df['RSI'] = calculate_rsi(temp_df['Close'])\n",
    "    temp_df['MACD'], temp_df['MACD_Signal'] = calculate_macd(temp_df['Close'])\n",
    "    temp_df['BB_Upper'], temp_df['BB_Lower'] = calculate_bollinger_bands(temp_df['Close'])\n",
    "    \n",
    "    # --- 3. Nouveaux Indicateurs Techniques (ATR, ADX, CCI) ---\n",
    "    temp_df['ATR'] = calculate_atr(ticker_data)\n",
    "    temp_df['ADX'] = calculate_adx(ticker_data)\n",
    "    temp_df['CCI'] = calculate_cci(ticker_data)\n",
    "    \n",
    "    # --- 4. Mémoire (Lags) ---\n",
    "    temp_df = add_lags(temp_df, 'Log_Return', lags=5)\n",
    "    \n",
    "    # --- 5. Contexte Macro (VIX, TNX, S&P500) ---\n",
    "    if '^VIX' in df_raw.columns.get_level_values(0):\n",
    "        temp_df['VIX'] = df_raw['^VIX']['Close']\n",
    "    if '^TNX' in df_raw.columns.get_level_values(0):\n",
    "        temp_df['TNX'] = df_raw['^TNX']['Close']\n",
    "    if '^GSPC' in df_raw.columns.get_level_values(0):\n",
    "        temp_df['SP500_Return'] = calculate_log_returns(df_raw['^GSPC']['Close'])\n",
    "        \n",
    "    # On ajoute ce bloc à la liste\n",
    "    processed_data.append(temp_df)\n",
    "\n",
    "# Fusion de tout en un seul grand tableau\n",
    "full_df = pd.concat(processed_data)\n",
    "\n",
    "# Suppression des colonnes intermédiaires non nécessaires pour le modèle (High, Low)\n",
    "full_df.drop(columns=['High', 'Low'], inplace=True)\n",
    "\n",
    "# Suppression des lignes vides (NaN) créées par les calculs\n",
    "full_df.dropna(inplace=True)\n",
    "\n",
    "print(\"\\nTerminé ! Aperçu des données finales :\")\n",
    "print(full_df.head())\n",
    "print(f\"Dimensions : {full_df.shape}\")\n"
]

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
