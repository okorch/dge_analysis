from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
from dge_pipeline.dashboard import dge_dashboard_layout
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

load_figure_template('JOURNAL')

dash.register_page(__name__, path="/dge")

layout = html.Div([
    html.H3("Differential Gene Expression", style={"textAlign": "center"}),

    html.Div([
        # Dropdown for tested condition
        html.Div([
            html.Label("Select Tested Condition:", style={"marginBottom": "5px"}),
            dbc.Select(id="select-tested", options=[], placeholder="Select..."),
        ], style={"width": "100%", "marginBottom": "20px"}),

        # Dropdown for control condition
        html.Div([
            html.Label("Select Control Condition:", style={"marginBottom": "5px"}),
            dbc.Select(id="select-control", options=[], placeholder="Select..."),
        ], style={"width": "100%", "marginBottom": "20px"}),

        # Button
        html.Div([
            dbc.Button("Run DGE", id="run-dge", n_clicks=0, outline=True,
                       color="primary", className="me-1", style={"marginTop": "10px"})
        ], style={"textAlign": "center"}),
    ], style={
        "width": "400px",
        "margin": "0 auto",
        "textAlign": "left",
    }),

    html.Hr(),

    html.Div(id="dge-layout-container"),

    # Stores
    dcc.Store(id="stored-counts"), # Rename to new-stored-counts
    dcc.Store(id="stored-design"), # Rename to new-stored-design
    dcc.Store(id="dge-result-store")
], style={
    "padding": "20px"
})

@callback(
    Output("select-tested", "options"),
    Output("select-control", "options"),

    Input("stored-design", "data"), # take preprocessed data matrix as inputs JSON format
    prevent_initial_call=True
)
def populate_condition_dropdowns(design_json):

    if not design_json:
        return [], []

    design_matrix = pd.read_json(design_json, orient="split")
    condition_levels = sorted(design_matrix["condition"].unique()) # find unique levels

    options = [ {"label": cond, "value": cond} for cond in condition_levels ]
    return options, options

@callback(
    Output("dge-layout-container", "children"), # dash layout
    Output("dge-result-store", "data"), # output dge results JSON format

    Input("run-dge", "n_clicks"),
    # levels for comparison
    State("select-tested", "value"),
    State("select-control", "value"),
    # data
    State("stored-counts", "data"), # Rename to new-stored-counts
    State("stored-design", "data"), # Rename to new-stored-design
    prevent_initial_call=True
)
def update_dge_layout(n_clicks, tested, control, counts_json, design_json):

    if not (counts_json and design_json):
        return html.Div("Missing processed data. Please complete EDA first."), None

    if not tested or not control:
        return html.Div("Please select both tested and control conditions."), None

    # Load from stored JSON
    count_matrix = pd.read_json(counts_json, orient="split")
    design_matrix = pd.read_json(design_json, orient="split")

    # Prepare data

    # Run DGE pipeline
    dge_df_json = None

    return dge_dashboard_layout(), dge_df_json

# register_gde_callbacks(dash.get_app()) later updating