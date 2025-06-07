from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
from eda_pipeline.dashboard import eda_dashboard_layout
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc


load_figure_template('JOURNAL')

dash.register_page(__name__, path="/eda")

layout = html.Div([
    html.H3("Exploratory Data Analysis", style={"textAlign": "center"}),

    dcc.Loading(html.Div(id="eda-output")),
    html.Br(),
    dbc.Button("Continue to DGE", href="/dge", color="secondary", outline=True, size="lg", className="mb-3",
               style={"fontSize": "18px"}),


    # Hidden stores
    dcc.Store(id="stored-counts"),
    dcc.Store(id="stored-design"),
    dcc.Store(id="new-stored-counts"),
    dcc.Store(id="new-stored-design")
], style={
    "maxWidth": "600px",
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
    counts_df = pd.read_json(counts_data, orient='split')
    design_df = pd.read_json(design_data, orient='split')

    # Run preprocessing

    # Convert back to JSON to store

    # Return output div and updated stores
    layout = eda_dashboard_layout(counts_df, design_df, ['info_messages'])
    new_counts_json = None
    new_design_json = None

    return layout, new_counts_json, new_design_json



