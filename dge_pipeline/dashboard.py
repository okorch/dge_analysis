from dash import html, dcc
import numpy as np
import pandas as pd
from dash import Input, Output, callback
import plotly.express as px


def dge_dashboard_layout():

    return html.Div([
    # Volcano Plot Section: Controls left, plot right
    html.H4("Volcano Plot Controls", style={"textAlign": "center"}),
    html.Div([
        # Left side: controls (sliders + dropdowns)
        html.Div([

            html.Label("P-Value Type:"),
            dcc.Dropdown(
                id="volcano-pval-type",
                options=[
                    {"label": "Raw P-Value", "value": "pvalue"},
                    {"label": "Adjusted P-Value (padj)", "value": "padj"}
                ],
                value="padj",
                style={"width": "220px", "marginBottom": "10px"}
            ),
            html.Label("log2FC Threshold:"),
            dcc.Slider(
                id="volcano-fc",
                min=0, max=3, step=0.1, value=1,
                marks={i: str(i) for i in range(4)},
                tooltip={"placement": "bottom"},
                updatemode='mouseup',
                included=True,
            ),
            html.Br(),
            html.Label("P-Value Threshold:"),
            dcc.Slider(
                id="volcano-p",
                min=0.001, max=0.1, step=0.001, value=0.05,
                marks={0.01: "0.01", 0.05: "0.05", 0.1: "0.1"},
                tooltip={"placement": "bottom"},
                updatemode='mouseup',
                included=True,
            )
        ], style={
            "flex": "0 0 350px",
            "paddingRight": "30px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "height": "400px"  # fix height to align nicely
        }),

        # Right side: plot
        html.Div([
            dcc.Graph(id="volcano-plot", style={"height": "400px", "width": "100%"})
        ], style={"flex": "1"}),
    ], style={"display": "flex", "alignItems": "center", "margin": "20px 0", "width": "100%"}),


    # MA Plot Section: Controls left, plot right
    html.H4("MA Plot Controls", style={"textAlign": "center"}),
    html.Div([
        html.Div([
            html.Label("P-Value Type:"),
            dcc.Dropdown(
                id="ma-pval-type",
                options=[
                    {"label": "Raw P-Value", "value": "pvalue"},
                    {"label": "Adjusted P-Value (padj)", "value": "padj"}
                ],
                value="padj",
                style={"width": "220px", "marginBottom": "10px"}
            ),
            html.Label("log2FC Threshold:"),
            dcc.Slider(
                id="ma-fc",
                min=0, max=3, step=0.1, value=1,
                marks={i: str(i) for i in range(4)},
                tooltip={"placement": "bottom"},
                updatemode='mouseup',
                included=True,
            ),
            html.Br(),
            html.Label("P-Value Threshold:"),
            dcc.Slider(
                id="ma-p",
                min=0.001, max=0.1, step=0.001, value=0.05,
                marks={0.01: "0.01", 0.05: "0.05", 0.1: "0.1"},
                tooltip={"placement": "bottom"},
                updatemode='mouseup',
                included=True,
            )
        ], style={
            "flex": "0 0 350px",
            "paddingRight": "30px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "height": "400px"
        }),

        html.Div([
            dcc.Graph(id="ma-plot", style={"height": "400px", "width": "100%"})
        ], style={"flex": "1"}),
    ], style={"display": "flex", "alignItems": "center", "margin": "20px 0", "width": "100%"}),


    # P-Value Distribution Section: Controls left, plot right
    html.H4("P-Value Distribution Controls", style={"textAlign": "center"}),
    html.Div([
        html.Div([
            html.Label("P-Value Type:"),
            dcc.Dropdown(
                id="dist-pval-type",
                options=[
                    {"label": "Raw P-Value", "value": "pvalue"},
                    {"label": "Adjusted P-Value (padj)", "value": "padj"}
                ],
                value="pvalue",
                style={"width": "220px", "marginBottom": "10px"}
            ),
        ], style={
            "flex": "0 0 350px",
            "paddingRight": "30px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "height": "400px"
        }),

        html.Div([
            dcc.Graph(id="pval-dist", style={"height": "400px", "width": "100%"})
        ], style={"flex": "1"}),
    ], style={"display": "flex", "alignItems": "center", "margin": "20px 0", "width": "100%"}),

])






def register_gde_callbacks(app):

    @app.callback(
        Output("volcano-plot", "figure"),
        Input("dge-result-store", "data"),
        Input("volcano-fc", "value"),
        Input("volcano-p", "value"),
        Input("volcano-pval-type", "value")
    )
    def update_volcano(json_data, fc_thresh, p_thresh, pval_type):
        if not json_data:
            return px.scatter(title="No data")

        dge_data = pd.read_json(json_data, orient="split")
        dge_data = dge_data.dropna(subset=["log2FoldChange", pval_type])

        df = dge_data.copy()
        df["selected_p"] = df[pval_type]
        df["-log10p"] = -np.log10(df["selected_p"])
        df["significant"] = (abs(df["log2FoldChange"]) > fc_thresh) & (df["selected_p"] < p_thresh)
        df["Gene Name"] = df.index

        fig = px.scatter(
            df, x="log2FoldChange", y="-log10p",
            color="significant",
            hover_data=["Gene Name"],
            color_discrete_map={True: "red", False: "gray"},
            title=f"Volcano Plot ({pval_type})"
        )
        fig.add_vline(x=fc_thresh, line_dash="dot", line_color="blue")
        fig.add_vline(x=-fc_thresh, line_dash="dot", line_color="blue")
        fig.add_hline(y=-np.log10(p_thresh), line_dash="dot", line_color="green")
        return fig

    @app.callback(
        Output("ma-plot", "figure"),
        Input("dge-result-store", "data"),
        Input("ma-fc", "value"),
        Input("ma-p", "value"),
        Input("ma-pval-type", "value")
    )
    def update_ma(json_data, fc_thresh, p_thresh, pval_type):
        if not json_data:
            return px.scatter(title="No data")

        dge_data = pd.read_json(json_data, orient="split")
        dge_data = dge_data.dropna(subset=["log2FoldChange", pval_type])

        df = dge_data.copy()
        df["selected_p"] = df[pval_type]
        df["significant"] = (abs(df["log2FoldChange"]) > fc_thresh) & (df["selected_p"] < p_thresh)
        df["Gene name"] = df.index

        fig = px.scatter(
            df, x="baseMean", y="log2FoldChange",
            color="significant", hover_data=["Gene name"],
            log_x=True,
            color_discrete_map={True: "red", False: "gray"},
            title=f"MA Plot ({pval_type})"
        )
        return fig

    @app.callback(
        Output("pval-dist", "figure"),
        Input("dge-result-store", "data"),
        Input("dist-pval-type", "value")
    )
    def update_pval_dist(json_data, pval_type):
        if not json_data:
            return px.scatter(title="No data")

        dge_data = pd.read_json(json_data, orient="split")
        dge_data = dge_data.dropna(subset=["log2FoldChange", pval_type])

        df = dge_data.copy()
        fig = px.histogram(
            df, x=pval_type, nbins=50,
            title=f"P-Value Distribution ({pval_type})",
            labels={pval_type: pval_type}
        )
        return fig