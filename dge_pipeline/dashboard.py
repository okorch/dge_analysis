from dash import html, dcc

STYLE = {"margin": "20px"}

def dge_dashboard_layout():

    return html.Div([
        html.H2("Differential Gene Expression Dashboard", style={"textAlign": "center"}),

        html.Div([
            html.H4("Volcano Plot"),
            html.Label("P-Value Type:"),
            dcc.Dropdown(
                id="volcano-pval-type",
                options=[{"label": "P-Value", "value": "pvalue"},
                         {"label": "Adjusted P-Value (padj)", "value": "padj"}],
                value="padj"
            ),
            html.Label("log2FC Threshold:"),
            dcc.Slider(id="volcano-fc", min=0, max=3, step=0.1, value=1,
                       marks={i: str(i) for i in range(4)}), # ----> volcano-fc
            html.Label("P-Value Threshold:"),
            dcc.Slider(id="volcano-p", min=0.001, max=0.1, step=0.001, value=0.05,
                       marks={0.01: "0.01", 0.05: "0.05", 0.1: "0.1"}), # ----> volcano-p
            #dcc.Graph(id="volcano-plot"),
            html.Hr()
        ], style=STYLE),

        html.Div([
            html.H4("MA Plot"),
            html.Label("P-Value Type:"),
            dcc.Dropdown(
                id="ma-pval-type",
                options=[{"label": "P-Value", "value": "pvalue"},
                         {"label": "Adjusted P-Value (padj)", "value": "padj"}],
                value="padj"
            ),
            html.Label("log2FC Threshold:"),
            dcc.Slider(id="ma-fc", min=0, max=3, step=0.1, value=1,
                       marks={i: str(i) for i in range(4)}),  # ----> ma-fc
            html.Label("P-Value Threshold:"),
            dcc.Slider(id="ma-p", min=0.001, max=0.1, step=0.001, value=0.05,
                       marks={0.01: "0.01", 0.05: "0.05", 0.1: "0.1"}), # ----> ma-p
            #dcc.Graph(id="ma-plot"),
            html.Hr()
        ], style=STYLE),

        html.Div([
            html.H4("P-Value Distribution"),
            html.Label("P-Value Type:"),
            dcc.Dropdown(
                id="dist-pval-type",
                options=[{"label": "P-Value", "value": "pvalue"},
                         {"label": "Adjusted P-Value (padj)", "value": "padj"}],
                value="pvalue"
            ),
            #dcc.Graph(id="pval-dist")
        ], style=STYLE)
    ])


def register_gde_callbacks(app):
    # Update nesessary plots
    pass
