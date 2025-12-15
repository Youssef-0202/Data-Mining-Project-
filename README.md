# Projet Data Mining : Prévision Boursière Hybride

## Structure du Projet

```
├── app/                # Application Streamlit
├── data/               # Données
│   ├── raw/            # Données brutes (yfinance)
│   └── processed/      # Données nettoyées et features
├── models/             # Modèles entraînés (.pkl, .h5)
├── notebooks/          # Jupyter Notebooks d'analyse
├── src/                # Code source réutilisable
└── README.md           # Documentation
```

## Installation

1.  Créer un environnement virtuel :
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```
2.  Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

*   **Notebooks :** Lancer `jupyter notebook` et ouvrir `notebooks/`.
*   **App :** Lancer `streamlit run app/main.py`.
