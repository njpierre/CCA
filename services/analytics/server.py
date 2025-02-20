from flask import Flask
import os
import psycopg2

server = Flask(__name__)

#Récupération de l'URL de la base de données depuis les variables d'environnement
db_url = os.getenv("DATABASE_URL")

#Établit une connexion à la base de données
def get_db_connection():
    try:
        return psycopg2.connect(db_url)
    except Exception as e:
        print("Erreur de connexion à la base de données :", e)
        return None
