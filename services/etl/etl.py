import pandas as pd
import time
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

db_url = "postgresql://user:password@db:5432/analytics_db"

#Attend que la base de données Postgres soit prête
def wait_for_db():
    while True:
        try:
            engine = create_engine(db_url)
            with engine.connect() as conn:
                print("PostgreSQL est prêt !")
                return
        except OperationalError:
            print("En attente de PostgreSQL...")
            time.sleep(2)

wait_for_db()

#Connexion à postgre
engine = create_engine(db_url)

#Vérifier que le fichier CSV existe avant de l’importer
csv_file = "/app/data.csv"

if os.path.exists(csv_file):
    print("Fichier CSV trouvé, importation en cours...")
    df_csv = pd.read_csv(csv_file, sep=";", encoding="utf-8")
    df_csv.to_sql("data", engine, if_exists="append", index=False)
    print("Données CSV importées")
else:
    print("ERREUR : Le fichier data.csv est introuvable !")

print("ETL terminé avec succès !")