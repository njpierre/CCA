from dash import dcc, html
from sqlalchemy import create_engine
import pandas as pd

# Connexion à la base de données PostgreSQL
DATABASE_URL = "postgresql://user:password@db:5432/analytics_db"
engine = create_engine(DATABASE_URL)

# Lire les données de la table PostgreSQL
df = pd.read_sql("SELECT * FROM data", engine)

# Layout de l'application
layout = html.Div([
    html.H1("Dashboard des Ventes"),
    dcc.Dropdown(
        id="categorie-dropdown",
        options=[{"label": cat, "value": cat} for cat in df["Catégorie"].unique()],
        value=df["Catégorie"].unique()[0]
    ),
    dcc.Graph(id="graph-ventes"),
])
