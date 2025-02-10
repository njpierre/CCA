
from flask import Flask, jsonify  # type: ignore
import psycopg2  # type: ignore
import os

app = Flask(__name__)

# Récupération de l'URL de la base de données depuis les variables d'environnement
db_url = os.getenv("DATABASE_URL")

def get_db_connection():
    """Établit une connexion à la base de données."""
    try:
        return psycopg2.connect(db_url)
    except Exception as e:
        print("Erreur de connexion à la base de données :", e)
        return None



@app.route("/data", methods=["GET"])
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



@app.route("/stats", methods=["GET"])
def stats():
    """Retourne la moyenne, le minimum et le maximum d'une colonne numérique."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"erreur": "Impossible de se connecter à la base de données"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT AVG("Number"), MIN("Number"), MAX("Number") FROM data')
        moyenne, minimum, maximum = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify({"moyenne": moyenne, "min": minimum, "max": maximum})
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500



@app.route("/stats/<colonne>", methods=["GET"])
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



@app.route("/columns", methods=["GET"])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
