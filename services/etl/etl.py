import pandas as pd
import requests
import time
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Attendre que PostgreSQL soit prêt
db_url = "postgresql://user:password@db:5432/analytics_db"

def wait_for_db():
    """Attend que la base de données PostgreSQL soit prête."""
    while True:
        try:
            engine = create_engine(db_url)
            with engine.connect() as conn:
                print("✅ PostgreSQL est prêt !")
                return
        except OperationalError:
            print("⏳ En attente de PostgreSQL...")
            time.sleep(2)

wait_for_db()

# Connexion à PostgreSQL
engine = create_engine(db_url)

# Vérifier que le fichier CSV existe avant de l’importer
csv_file = "/app/data.csv"  # Assure-toi que ce chemin est correct

if os.path.exists(csv_file):
    print("Fichier CSV trouvé, importation en cours...")
    df_csv = pd.read_csv(csv_file, sep=";", encoding="utf-8")
    df_csv.to_sql("data", engine, if_exists="append", index=False)
    print("Données CSV importées avec succès !")
else:
    print("ERREUR : Le fichier data.csv est introuvable !")

# Importer des données depuis une API externe
api_url = "https://api.exemple.com/data"
try:
    response = requests.get(api_url)
    response.raise_for_status()  # Vérifie si l'API répond bien
    df_api = pd.DataFrame(response.json())
    df_api.to_sql("data", engine, if_exists="append", index=False)
    print("✅ Données API importées avec succès !")
except requests.exceptions.RequestException as e:
    print(f"Erreur lors de la récupération des données API : {e}")

print("ETL terminé avec succès !")