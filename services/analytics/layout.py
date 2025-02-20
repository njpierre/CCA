from dash import dcc, html
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
import pandas as pd

#Connexion à la base de données PostgreSQL
DATABASE_URL = "postgresql://user:password@db:5432/analytics_db"
engine = create_engine(DATABASE_URL)

#Lire les données de la table PostgreSQL
df = pd.read_sql("SELECT * FROM data", engine)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard des Ventes", className="text-center text-primary mb-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="categorie-dropdown",
                options=[{"label": cat, "value": cat} for cat in df["Catégorie"].unique()],
                value=df["Catégorie"].unique(),
                className="mb-3"
            ),
            dcc.Graph(id="graph-ventes")
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Statistiques", className="card-title"),
                    html.P(id="stats_output", className="card-text"),
                ])
            ], className="mb-4")
        ], width=4)
    ]),
    
    dbc.Row([    
        dbc.Col([
            html.H4("Distribution des ventes"),
            dcc.Graph(id="boxplot")
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("Comparaison des ventes"),
            dcc.Dropdown(
                id="compare-dropdown",
                options=[{"label": cat, "value": cat} for cat in df["Catégorie"].unique()],
                multi=True,
                placeholder="Sélectionnez plusieurs catégories",
                className="mb-3"
            ),
            dcc.Graph(id="graph-comparaison")
        ], width=12)
    ]),

    
    dbc.Row([
        dbc.Col([
            html.H4("Tendance des ventes"),
            dcc.Graph(id="trend-graph")
        ], width=12)
    ]),


    dbc.Row([
        dbc.Col([
            html.H4("Répartition des ventes"),
            dcc.Graph(id="sales-ratio")
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="product-treemap")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Répartition des ventes"),
            dcc.Graph(id="bayesian-forecast")
        ], width=12)
    ])
], fluid=True)
