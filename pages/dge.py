from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
from dge_pipeline.main import main
from dge_pipeline.dashboard import dge_dashboard_layout, register_gde_callbacks
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from io import StringIO


load_figure_template('JOURNAL')

dash.register_page(__name__, path="/dge")

layout = html.Div([
    html.H3("Differential Gene Expression", style={"textAlign": "center"}),

    html.Div([

        html.Label("Contrast Variable:"),
        dcc.Dropdown(id="contrast-variable", placeholder="Choose variable..."),

        html.Label("Levels (exactly 2):"),
        dcc.Dropdown(id="contrast-levels", multi=True, placeholder="Choose 2 levels..."),

        html.Div([
            "You will be asked to choose two levels from the contrast column (e.g., 'treatment' vs 'control'). ",
            "The first selected level will be treated as the test condition, and the second as the reference (control). ",
            "The log2 fold change (LFC) will represent the expression ratio of the form ",
            html.Code("log2(treatment / control)"),
            ". Positive LFC values indicate higher expression in the first (test) condition."
        ], style={"fontSize": "14px", "color": "#555", "maxWidth": "600px", "margin": "10px auto"}),

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

    dcc.Loading(
        id="loading-spinner",
        type="circle",
        children=html.Div(id="dge-layout-container"),
        fullscreen=False,
    ),

    html.Div([
        dbc.Button("Download Results", id="download-button", color="info", className="mt-3"),
        dcc.Download(id="download-dge")
    ], style={"textAlign": "center"}),

    # Stores
    dcc.Store(id="new-stored-counts"),
    dcc.Store(id="new-stored-design"),
    dcc.Store(id="dge-result-store")
], style={
    "padding": "20px"
})

@callback(
    Output("contrast-variable", "options"),
    Input("new-stored-design", "data")
)
def populate_contrast_variable_options(json_data):
    if not json_data:
        return []
    design_df = pd.read_json(json_data, orient="split")
    return [{"label": col, "value": col} for col in design_df.columns]

@callback(
    Output("contrast-levels", "options"),
    Input("contrast-variable", "value"),
    Input("new-stored-design", "data")
)
def populate_contrast_levels(var, json_data):
    if not json_data or not var:
        return []
    df = pd.read_json(json_data, orient="split")
    levels = df[var].dropna().unique().tolist()
    return [{"label": lv, "value": lv} for lv in levels]

@callback(
    Output("download-dge", "data"),
    Input("download-button", "n_clicks"),
    State("dge-result-store", "data"),
    prevent_initial_call=True
)
def download_dge_result(n_clicks, dge_data_json):
    if not dge_data_json:
        return dash.no_update

    dge_df = pd.read_json(StringIO(dge_data_json), orient="split")
    return dcc.send_data_frame(dge_df.to_csv, "dge_results.csv", index=False)


@callback(
    Output("dge-layout-container", "children"),
    Output("dge-result-store", "data"),
    Input("run-dge", "n_clicks"),
    State("contrast-levels", "value"),
    State("contrast-variable", "value"),
    State("new-stored-counts", "data"),
    State("new-stored-design", "data"),
    prevent_initial_call=True
)
def update_dge_layout(n_clicks, contrast_levels, contrast_variable, counts_json, design_json):

    contrasts = [contrast_variable] + contrast_levels
    if not (counts_json and design_json):
        return html.Div("Missing processed data. Please complete EDA first.")

    if not contrast_levels:
        return html.Div("Please select both tested and control conditions.")

    # Load from stored JSON
    count_matrix = pd.read_json(counts_json, orient="split")
    design_matrix = pd.read_json(design_json, orient="split")

    # Run analysis
    dge_df_clear = main(count_matrix, design_matrix, contrast=contrasts)

    return dge_dashboard_layout(), dge_df_clear.to_json(orient="split")

register_gde_callbacks(dash.get_app())
