from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from database import get_data
from charts import generate_sales_chart
import numpy as np


def register_callbacks(app):
    df = get_data()
    df = df.copy() 
    df["Catégorie"] = df["Catégorie"].astype(str)

    @app.callback(
        Output("graph-ventes", "figure"),
        Input("categorie-dropdown", "value")
    )
    def update_graph(selected_category):
        if selected_category:
            selected_category = str(selected_category)
            if selected_category in df["Catégorie"].unique():
                return generate_sales_chart(selected_category)
        return px.scatter(title="Aucune donnée disponible")
    
    @app.callback(
        Output("stats_output", "children"),
        Input("categorie-dropdown", "value")
    )
    def update_stats(selected_category):
        if selected_category and selected_category in df["Catégorie"].unique():
            filtered_df = df[df["Catégorie"] == selected_category]
            if "Total" in filtered_df.columns and not filtered_df.empty:
                return (f"Moyenne : {filtered_df['Total'].mean():.2f} | Min : {filtered_df['Total'].min()} | Max : {filtered_df['Total'].max()} | "
                        f"Médiane : {filtered_df['Total'].median()} | Q1 : {filtered_df['Total'].quantile(0.25)} | Q3 : {filtered_df['Total'].quantile(0.75)}")
        return "Données non disponibles pour cette catégorie."
    
    @app.callback(
        Output("graph-comparaison", "figure"),
        Input("compare-dropdown", "value")
    )
    #Affiche la matrice de corrélation des ventes entre plusieurs catégories
    def update_comparison(selected_categories):
        if not selected_categories:
            return px.imshow(df.select_dtypes(include=["number"]).corr(), title="Corrélation (toutes catégories)")
        
        selected_categories = [str(cat) for cat in selected_categories]  # Assurer les strings
        filtered_df = df[df["Catégorie"].isin(selected_categories)]
        if filtered_df.empty:
            return px.imshow([], title="Aucune donnée pour les catégories sélectionnées")
        
        return px.imshow(filtered_df.select_dtypes(include=["number"]).corr(), title=f"Corrélation ({', '.join(selected_categories)})")

    @app.callback(
        Output("trend-graph", "figure"),
        Input("categorie-dropdown", "value")
    )
    def update_trend(selected_category):
        """Affiche la tendance des ventes sur le temps"""
        filtered_df = df[df["Catégorie"] == selected_category] if selected_category else df
        if "Date" in filtered_df.columns and "Total" in filtered_df.columns:
            filtered_df = filtered_df.sort_values(by="Date")
            return px.line(filtered_df, x="Date", y="Total", title="Tendance des ventes de début janvier")
        return px.line(title="Données insuffisantes pour afficher la tendance")


    @app.callback(
        Output("sales-ratio", "figure"),
        Input("categorie-dropdown", "value")
    )
    def update_sales_ratio(selected_category):
        filtered_df = df[df["Catégorie"] == selected_category] if selected_category else df
        if "Catégorie" in filtered_df.columns and "Total" in filtered_df.columns:
            sales_by_category = filtered_df.groupby("Catégorie")["Total"].sum().reset_index()
            return px.pie(sales_by_category, names="Catégorie", values="Total", title="Répartition des ventes par catégorie")
        return px.pie(title="Données insuffisantes pour afficher le ratio des ventes")
    

    @app.callback(
        Output("boxplot", "figure"),
        Input("categorie-dropdown", "value")
    )
    #Affiche un boxplot des ventes par catégorie
    def update_boxplot(selected_category):
        filtered_df = df[df["Catégorie"] == selected_category] if selected_category else df
        if "Total" in filtered_df.columns and not filtered_df.empty:
            return px.box(filtered_df, x="Catégorie", y="Total", title="Boxplot des ventes par catégorie")
        return px.box(title="Données insuffisantes")
    
    @app.callback(
        Output("bayesian-forecast", "figure"),
        Input("categorie-dropdown", "value")
    )
    #Analyse Bayésienne pour ajuster les prévisions des ventes
    def bayesian_forecast(selected_category):
        filtered_df = df[df["Catégorie"].isin([selected_category])] if selected_category else df
        if "Total" in filtered_df.columns and "Date" in filtered_df.columns:
            filtered_df = filtered_df.dropna(subset=["Total", "Date"]).sort_values(by="Date")
            if filtered_df.empty:
                return px.line(title="Données insuffisantes pour l'analyse Bayésienne.")
            
            mean_sales = filtered_df["Total"].mean()
            std_sales = filtered_df["Total"].std()
            future_dates = pd.date_range(start=filtered_df["Date"].max(), periods=30, freq='D')
            prior_mean = mean_sales
            prior_std = std_sales
            posterior_mean = (prior_mean + mean_sales) / 2
            posterior_std = np.sqrt((prior_std ** 2 + std_sales ** 2) / 2)
            
            forecast_values = np.random.normal(posterior_mean, posterior_std, len(future_dates))
            forecast_df = pd.DataFrame({"Date": future_dates, "Prévision": forecast_values})
            
            return px.line(forecast_df, x="Date", y="Prévision", title="Prévision Bayésienne des ventes")
        return px.line(title="Données insuffisantes pour l'analyse Bayésienne.")

    @app.callback(
        Output("product-treemap", "figure"),
        Input("categorie-dropdown", "value")
    )
    #Affiche un Treemap des ventes par produit pour une représentation hiérarchique plus compacte
    def update_product_treemap(selected_category):
        filtered_df = df[df["Catégorie"].isin([selected_category])] if selected_category else df
        if "Catégorie" in filtered_df.columns and "Produit" in filtered_df.columns and "Total" in filtered_df.columns:
            return px.treemap(filtered_df, path=["Catégorie", "Produit"], values="Total",
                              title="Répartition des ventes par produit")
        return px.treemap(title="Données insuffisantes pour afficher le Treemap des Produits.")
