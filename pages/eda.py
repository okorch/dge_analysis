from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
from eda_pipeline.dashboard import eda_dashboard_layout

dash.register_page(__name__, path="/eda")

layout = html.Div([
    html.H3("Exploratory Data Analysis"),
    dcc.Loading(html.Div(id="eda-output")),
    dcc.Link("Continue to DGE", href="/dge"),

    dcc.Store(id="stored-counts"), # counts from upload.py JSON format
    dcc.Store(id="stored-design"), # design matrix from upload.py JSON format

    dcc.Store(id="new-stored-counts"), # will load them later in update eda JSON format
    dcc.Store(id="new-stored-design") # will load them later in update eda JSON format
])

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
    counts_df = pd.read_json(counts_data, orient='split')
    design_df = pd.read_json(design_data, orient='split')

    # Run preprocessing

    # Convert back to JSON to store

    # Return output div and updated stores
    layout = eda_dashboard_layout(counts_df, design_df, ['info_messages'])
    new_counts_json = None
    new_design_json = None

    return layout, new_counts_json, new_design_json



