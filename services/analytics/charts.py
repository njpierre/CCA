import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd

# Connexion à la base de données PostgreSQL
DATABASE_URL = "postgresql://user:password@db:5432/analytics_db"
engine = create_engine(DATABASE_URL)

# Lire les données de la table PostgreSQL
df = pd.read_sql("SELECT * FROM data", engine)
print(df.columns)

def generate_sales_chart(category):
    """ Génère un graphique des ventes par catégorie """
    filtered_df = df[df["Catégorie"] == category]
    fig = px.bar(filtered_df, x="Produit", y="Total", title=f"Ventes de {category}")
    return fig
