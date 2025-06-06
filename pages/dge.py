from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
from dge_pipeline.dashboard import dge_dashboard_layout
from config.config import MAIN_FONT

dash.register_page(__name__, path="/dge")

layout = html.Div([
    html.H3("Differential Gene Expression", style={"textAlign": "center"}),

    html.Div([
# Dropdown for tested
        html.Div([
            html.Label("Select Tested Condition:", style={"marginBottom": "5px"}),
            dcc.Dropdown(id="select-tested", options=[], placeholder="Select...",
                         style={"width": "100%"})
        ], style={"width": "100%", "marginBottom": "20px"}),
# Dropdown for control
        html.Div([ # Dropdown for control
            html.Label("Select Control Condition:", style={"marginBottom": "5px"}),
            dcc.Dropdown(id="select-control", options=[], placeholder="Select...",
                         style={"width": "100%"})
        ], style={"width": "100%", "marginBottom": "20px"}),
# Button
        html.Button("Run DGE", id="run-dge", n_clicks=0, style={"marginTop": "10px"})
    ], style={
        "width": "400px",
        "margin": "0 auto",
        "textAlign": "left",
        "fontFamily": MAIN_FONT
    }),

    html.Hr(),

    html.Div(id="dge-layout-container"),

# Stores
    dcc.Store(id="new-stored-counts"),
    dcc.Store(id="new-stored-design"),
    dcc.Store(id="dge-result-store")
], style={
    "fontFamily": MAIN_FONT,
    "padding": "20px"
})

@callback(
    Output("select-tested", "options"),
    Output("select-control", "options"),

    Input("new-stored-design", "data"), # take preprocessed counts as inputs JSON format
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
    State("new-stored-counts", "data"),
    State("new-stored-design", "data"),
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