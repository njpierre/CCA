
from flask import Flask, jsonify
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd
import os
import plotly.express as px
from dash import html
from layout import layout # Import du layout
from callbacks import register_callbacks # type: ignore # Import des callbacks

server = Flask(__name__)

# Récupération de l'URL de la base de données depuis les variables d'environnement
db_url = os.getenv("DATABASE_URL")

def get_db_connection():
    """Établit une connexion à la base de données."""
    try:
        return psycopg2.connect(db_url)
    except Exception as e:
        print("Erreur de connexion à la base de données :", e)
        return None



@server.route("/data", methods=["GET"])
def get_data():
    """Récupère toutes les données de la table `data`."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"erreur": "Impossible de se connecter à la base de données"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(records)
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500



@server.route("/stats", methods=["GET"])
def stats():
    """Retourne la moyenne, le minimum et le maximum pour toutes les colonnes numériques."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"erreur": "Impossible de se connecter à la base de données"}), 500

    try:
        cursor = conn.cursor()
        
        # Récupérer toutes les colonnes numériques de la table `data`
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'data' 
            AND data_type IN ('integer', 'numeric', 'double precision', 'real')
        """)
        
        numeric_columns = [row[0] for row in cursor.fetchall()]
        
        if not numeric_columns:
            return jsonify({"erreur": "Aucune colonne numérique trouvée dans la table `data`"}), 400

        # Construire dynamiquement la requête SQL
        stats_query = ", ".join([f"AVG(\"{col}\"), MIN(\"{col}\"), MAX(\"{col}\")" for col in numeric_columns])
        cursor.execute(f"SELECT {stats_query} FROM data")

        # Récupérer les résultats et organiser sous forme de dictionnaire
        stats_values = cursor.fetchone()
        stats_dict = {}

        for i, col in enumerate(numeric_columns):
            stats_dict[col] = {
                "moyenne": stats_values[i * 3],  # AVG
                "min": stats_values[i * 3 + 1],  # MIN
                "max": stats_values[i * 3 + 2]   # MAX
            }

        cursor.close()
        conn.close()

        return jsonify(stats_dict)

    except Exception as e:
        return jsonify({"erreur": str(e)}), 500




@server.route("/stats/<colonne>", methods=["GET"])
def stats_colonne(colonne):
    """Retourne les statistiques (moyenne, min, max) d'une colonne spécifique."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"erreur": "Impossible de se connecter à la base de données"}), 500

    try:
        cursor = conn.cursor()
        query = f"SELECT AVG({colonne}), MIN({colonne}), MAX({colonne}) FROM data"
        cursor.execute(query)
        moyenne, minimum, maximum = cursor.fetchone()
        cursor.close()
        conn.close()

        if moyenne is None:
            return jsonify({"erreur": f"La colonne '{colonne}' est invalide ou vide"}), 400

        return jsonify({"colonne": colonne, "moyenne": moyenne, "min": minimum, "max": maximum})
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500



@server.route("/columns", methods=["GET"])
def get_columns():
    """Retourne la liste des colonnes de la table `data`."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"erreur": "Impossible de se connecter à la base de données"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'data'")
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(columns)
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500
    
# Création de l'application Dash intégrée à Flask
app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/")

# Définition du layout
app.layout = layout

# Enregistrement des callbacks
register_callbacks(app)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)