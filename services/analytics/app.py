import dash
import dash_bootstrap_components as dbc
from server import server
from layout import layout
from callbacks import register_callbacks

#Création de l'application Dash
app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/", external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = layout

register_callbacks(app)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)
