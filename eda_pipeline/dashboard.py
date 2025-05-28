# dashboard.py

import pandas as pd
import plotly.express as px
from config import DATA_PATH
from dash import Dash, dcc, html, Input, Output


# Initialize app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("RNA-Seq Dashboard (in procces)", style={'textAlign': 'center'}),
])

# Run server
if __name__ == "__main__":
    app.run(debug=True)
