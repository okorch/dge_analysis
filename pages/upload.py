from dash import html, dcc, callback, Output, Input, dash_table
import dash
import base64, io
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

load_figure_template('JOURNAL')

dash.register_page(__name__, path="/upload")

count_matrix_columns = [
    {"name": "Gene ID", "id": "Gene ID"},
    {"name": "Gene Name", "id": "Gene Name"},
    {"name": "Sample 1", "id": "Sample 1"},
    {"name": "Sample 2", "id": "Sample 2"},
    {"name": "Sample 3", "id": "Sample 3"},
    {"name": "Sample 4", "id": "Sample 4"},
]

count_matrix_data = [
    {"Gene ID": "ENSG00000000003", "Gene Name": "TSPAN6", "Sample 1": 232, "Sample 2": 96, "Sample 3": 92, "Sample 4": 167},
    {"Gene ID": "ENSG00000000005", "Gene Name": "TNMD", "Sample 1": 0, "Sample 2": 1, "Sample 3": 0, "Sample 4": 8},
    {"Gene ID": "ENSG00000000419", "Gene Name": "DPM1", "Sample 1": 97, "Sample 2": 59, "Sample 3": 44, "Sample 4": 96},
    {"Gene ID": "ENSG00000000457", "Gene Name": "SCYL3", "Sample 1": 170, "Sample 2": 38, "Sample 3": 42, "Sample 4": 121},
    {"Gene ID": "ENSG00000000460", "Gene Name": "C1orf112", "Sample 1": 25, "Sample 2": 13, "Sample 3": 9, "Sample 4": 28},
    {"Gene ID": "ENSG00000000938", "Gene Name": "FGR", "Sample 1": 42, "Sample 2": 18, "Sample 3": 11, "Sample 4": 54},
    {"Gene ID": "ENSG00000000971", "Gene Name": "CFH", "Sample 1": 160, "Sample 2": 94, "Sample 3": 66, "Sample 4": 507},
    {"Gene ID": "ENSG00000001036", "Gene Name": "FUCA2", "Sample 1": 309, "Sample 2": 71, "Sample 3": 82, "Sample 4": 198},
]

design_matrix_data = [
    {"Sample": "Sample 1", "Condition": "control"},
    {"Sample": "Sample 2", "Condition": "control"},
    {"Sample": "Sample 3", "Condition": "treatment"},
    {"Sample": "Sample 4", "Condition": "treatment"},
]

upload_layout = html.Div([
    html.H3("Upload Instructions"),

    html.P([
        "Please upload your ",
        html.Strong("count matrix"),
        " and ",
        html.Strong("design matrix"),
        " to proceed with differential gene expression (DGE) analysis."
    ]),

    html.Hr(),

    html.H4("Count Matrix"),
    html.P("The count matrix should include gene-level expression values for each sample. "
           "It can contain additional metadata columns (e.g., Gene ID, Gene Name), "
           "but you must specify which column to use as the gene label for downstream analysis."),
    html.P("Example Count Matrix:"),

    dash_table.DataTable(
        columns=count_matrix_columns,
        data=count_matrix_data,
        style_table={"overflowX": "auto", "maxWidth": "600px"},
        style_cell={"textAlign": "center", "padding": "5px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#f9f9f9"}
    ),

    html.Br(),

    html.P([
        "Note: In this example you should specify either ",
        html.Code("Gene Name"),
        " or ",
        html.Code("Gene ID"),
        " as the identifier column. The other column will be removed automatically during preprocessing."
    ]),

    html.Hr(),

    html.H4("Design Matrix"),
    html.P("The design matrix defines experimental conditions (e.g., control vs. treatment) for each sample. "
           "This table should NOT contain headers."),
    html.P("Example Design Matrix:"),

    dash_table.DataTable(
        columns=[{"name": "", "id": "Sample"}, {"name": "", "id": "Condition"}],
        data=design_matrix_data,
        style_table={"overflowX": "auto", "maxWidth": "200px"},
        style_cell={"textAlign": "center", "padding": "5px"},
        style_header={"display": "none"}  # Hide headers for no-header format
    ),

    html.Br(),

    html.P("Note:"),
    html.Ul([
        html.Li("You can include more than two conditions (e.g., multiple treatment groups)."),
        html.Li("You will be asked to choose specific conditions for comparison during the DGE analysis step.")
    ])
],)


layout = html.Div([
    html.Div([
        html.H3("Upload Files", style={"textAlign": "center"}),
        html.Br(),
        dcc.Upload(
            id="upload-counts",
            children=dbc.Button("Upload Count Matrix", outline=True, color="primary", className="me-1")
        ),
        html.Div(id="counts-filename"),
        html.Br(),

        dbc.Input(type="text", id="gene-column", placeholder="Enter name of Gene Names or Genes IDs column"),
        html.Div(id="gene-column-output"),
        html.Br(),

        dcc.Upload(
            id="upload-design",
            children=dbc.Button("Upload Design Matrix", outline=True, color="primary", className="me-1")
        ),
        html.Div(id="design-filename"),
        html.Br(),
    ], style={
        "maxWidth": "600px",
        "margin": "auto",
        "textAlign": "center",
        "padding": "2rem"
    }),

    html.Div([ dbc.Button("Continue to EDA", href="/eda", color="secondary", outline=True, size="lg",
               className="mb-3")], style={"fontSize": "18px", "textAlign": "center"}),

    upload_layout,

    dcc.Store(id="stored-counts"),
    dcc.Store(id="stored-design"),
    dcc.Store(id="stored-gene-column")
])


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
