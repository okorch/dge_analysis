from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
from eda_pipeline.dashboard import eda_dashboard_layout
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from io import StringIO
from eda_pipeline.main import main


load_figure_template('JOURNAL')

dash.register_page(__name__, path="/eda")

layout = html.Div([
    html.H3("Exploratory Data Analysis", style={"textAlign": "center"}),

    dcc.Loading(html.Div(id="eda-output")),
    html.Br(),
    dbc.Button("Continue to DGE", href="/dge", color="secondary", outline=True, size="lg", className="mb-3",
               style={"fontSize": "18px"}),



    dcc.Store(id="stored-counts"),
    dcc.Store(id="stored-design"),
    dcc.Store(id="new-stored-counts"),
    dcc.Store(id="new-stored-design")
], style={
    "maxWidth": "900px",
    "margin": "auto",
    "textAlign": "center",
    "padding": "2rem"
})

@callback(
    Output("eda-output", "children"),
    Output("new-stored-counts", "data"),
    Output("new-stored-design", "data"),

    Input("stored-counts", "data"),
    Input("stored-design", "data"),
    prevent_initial_call=True
)
def update_eda(counts_data, design_data):

    if not counts_data or not design_data:
        return dash.no_update, dash.no_update, dash.no_update

    # Convert JSON to DataFrames
    counts_df = pd.read_json(StringIO(counts_data), orient='split')
    design_df = pd.read_json(StringIO(design_data), orient='split')

    # Run preprocessing
    preprocessed_data = main(counts_df, design_df)
    new_counts_matrix, new_design_matrix = preprocessed_data[0], preprocessed_data[1]

    # Convert back to JSON to store
    new_counts_json = new_counts_matrix.to_json(date_format='iso', orient='split')
    new_design_json = new_design_matrix.to_json(date_format='iso', orient='split')

    # Run preprocessing and layout configuration
    layout = eda_dashboard_layout(*preprocessed_data[2:])

    return layout, new_counts_json, new_design_json
