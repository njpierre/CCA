from dash.dependencies import Input, Output
from charts import generate_sales_chart

def register_callbacks(app):
    @app.callback(
        Output("graph-ventes", "figure"),
        Input("categorie-dropdown", "value")
    )
    def update_graph(selected_category):
        return generate_sales_chart(selected_category)
