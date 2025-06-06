from dash import html, dcc, callback, Output, Input, State
import dash
import base64, io
import pandas as pd
from config.config import MAIN_FONT

dash.register_page(__name__, path="/upload")

layout = html.Div([
    html.H3("Upload Files", style={"textAlign": "center"}),

    dcc.Upload(id="upload-counts", children=html.Button("Upload Count Matrix")),
    html.Div(id="counts-filename"),
    html.Br(),

    html.Label("Gene names column (in count matrix):"),
    dcc.Input(id="gene-column", type="text", placeholder="Column name"),
    html.Div(id="gene-column-output"),
    html.Br(),

    dcc.Upload(id="upload-design", children=html.Button("Upload Design Matrix")),
    html.Div(id="design-filename"),
    html.Br(),

    dcc.Link("Continue to EDA", href="/eda"),

    dcc.Store(id="stored-counts"),
    dcc.Store(id="stored-design"),
    dcc.Store(id="stored-gene-column")
], style={
    "fontFamily": MAIN_FONT,
    "maxWidth": "600px",
    "margin": "auto",
    "textAlign": "center",
    "padding": "2rem"
})

# Show uploaded file names
@callback(
    Output("counts-filename", "children"),
    Output("design-filename", "children"),
    Input("upload-counts", "filename"),
    Input("upload-design", "filename"),
)
def display_filenames(counts_filename, design_filename):
    counts_text = f"Uploaded: {counts_filename}" if counts_filename else ""
    design_text = f"Uploaded: {design_filename}" if design_filename else ""
    return counts_text, design_text

# Read count matrix with gene column validation
def read_count_matrix(contents, gene_column=None):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    text = decoded.decode('utf-8')

    delimiter = '\t' if '\t' in text.splitlines()[0] else ','
    df = pd.read_csv(io.StringIO(text), delimiter=delimiter)

    if gene_column:
        gene_column = gene_column.strip()
        try:
            df.set_index(gene_column, inplace=True)
            df.index.name = None
        except Exception as e:
            print(f"Gene column parsing failed: {e}")
            return None, str(e)

    return df, None

# Read design matrix
def read_design_matrix(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    text = decoded.decode('utf-8')
    delimiter = '\t' if '\t' in text.splitlines()[0] else ','
    design_matrix = pd.read_csv(io.StringIO(text), delimiter=delimiter, header=None, names=['condition'])
    return design_matrix

# Process uploaded data
@callback(
    Output("stored-counts", "data"),
    Output("stored-design", "data"),
    Output("stored-gene-column", "data"),
    Output("gene-column-output", "children"),

    Input("upload-counts", "contents"),
    Input("upload-design", "contents"),
    Input("gene-column", "value"),
    prevent_initial_call=True
)
def store_files(counts_content, design_content, gene_column):
    if counts_content:
        counts_df, error = read_count_matrix(counts_content, gene_column)
        if counts_df is None:
            return None, None, None, html.Div(['Gene column not found in count matrix.'])
    else:
        counts_df = None

    design_df = read_design_matrix(design_content) if design_content else None

    return (
        counts_df.to_json(date_format='iso', orient='split') if counts_df is not None else None,
        design_df.to_json(date_format='iso', orient='split') if design_df is not None else None,
        gene_column,
        html.Div()  # no error message
    )
