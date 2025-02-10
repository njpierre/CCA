import pandas as pd
import requests
from sqlalchemy import create_engine

# Connexion à PostgreSQL
db_url = "postgresql://user:password@cca-db-1:5432/analytics_db"
engine = create_engine(db_url)

# Importer un fichier CSV
csv_file = "data.csv"
df_csv = pd.read_csv(csv_file, sep=";", encoding="utf-8")
df_csv.to_sql("data", engine, if_exists="replace", index=False)

# Importer des données depuis une API externe
api_url = "https://api.exemple.com/data"
response = requests.get(api_url)
if response.status_code == 200:
    df_api = pd.DataFrame(response.json())
    df_api.to_sql("data", engine, if_exists="append", index=False)
else:
    print("Erreur lors de la récupération des données API")

print("Données importées avec succès !")
