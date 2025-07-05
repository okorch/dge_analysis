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
    {"Sample": "Run", "Condition": "Level_Condition", "Condition2": "Additional_Condition"},
    {"Sample": "Sample 1", "Condition": "control", "Condition2": "condition 1"},
    {"Sample": "Sample 2", "Condition": "control", "Condition2": "condition 2"},
    {"Sample": "Sample 3", "Condition": "treatment", "Condition2": "condition 1"},
    {"Sample": "Sample 4", "Condition": "treatment", "Condition2": "condition 2"},
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
        style_table={"overflowX": "auto", "maxWidth": "800px"},
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
    html.P([
        "The design matrix defines the experimental conditions (e.g., control vs. treatment) for each sample. ",
        "It should include headers representing different factors or groups, enabling multifactorial analysis. ",
        html.Br(),
        "All columns provided in the design matrix will be used in the analysis. ",
        html.Br(),
        "For differential expression analysis, you need to specify the column and the levels to compare, ",
        html.Strong("with the order being tested condition first and control condition second."),
    ]),
    html.P("Example Design Matrix:"),

    dash_table.DataTable(
        columns=[{"name": "", "id": "Sample"}, {"name": "", "id": "Condition"}, {"name": "", "id": "Condition2"}],
        data=design_matrix_data,
        style_table={"overflowX": "auto", "maxWidth": "600px"},
        style_cell={"textAlign": "center", "padding": "5px"},
        style_header={"display": "none"}
    ),

    html.Br(),

    html.P("Note:"),
    html.Ul([
        html.Li("Column names should NOT contain spaces and symbols. Only letters, numbers and underscore are allowed."),
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
        html.Div(id="gene-message"),
        html.Br(),

        dcc.Upload(
            id="upload-design",
            children=dbc.Button("Upload Design Matrix", outline=True, color="primary", className="me-1")
        ),
        html.Div(id="design-filename"),
        html.Br(),

        dbc.Input(type="text", id="contrast-column", placeholder="Enter name of column specifying main contrasts in design matrix"),
        html.Div(id="contrast-message"),
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
    dcc.Store(id="contrast-column-output"),
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
        if gene_column not in df.columns:
            return None, f"Gene column '{gene_column}' not found in uploaded count matrix."
        try:
            df.set_index(gene_column, inplace=True)
            df.index.name = None
        except Exception as e:
            print(f"Gene column parsing failed: {e}")
            return None, str(e)

    return df, None

# Read design matrix
def read_design_matrix(contents, contrast_column):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    text = decoded.decode('utf-8')
    delimiter = '\t' if '\t' in text.splitlines()[0] else ','

    try:
        design_matrix = pd.read_csv(io.StringIO(text), delimiter=delimiter, index_col=0)
    except Exception as e:
        return None, f"Failed to parse design matrix: {e}"

    if contrast_column:
        contrast_column = contrast_column.strip()
        if contrast_column not in design_matrix.columns:
            return None, f"Contrast column '{contrast_column}' not found in design matrix."

    return design_matrix, None

# Process uploaded data
@callback(
    Output("stored-counts", "data"),
    Output("stored-design", "data"),
    Output("contrast-column-output", "data"),
    Output("gene-message", "children"),
    Output("contrast-message", "children"),

    Input("upload-counts", "contents"),
    Input("upload-design", "contents"),
    Input("gene-column", "value"),
    Input("contrast-column", "value"),
    prevent_initial_call=True
)
def store_files(counts_content, design_content, gene_column, contrast_column):
    if counts_content:
        counts_df, error = read_count_matrix(counts_content, gene_column)
        if counts_df is None:
            return None, None, None, html.Div(['Gene column not found in count matrix.']), html.Div()
    else:
        counts_df = None

    if design_content:
        design_df, error = read_design_matrix(design_content, contrast_column)
        if design_df is None:
            return None, None, None, html.Div(), html.Div(['Design matrix column not found in count matrix.'])
    else:
        design_df = None

    return (
        counts_df.to_json(date_format='iso', orient='split') if counts_df is not None else None,
        design_df.to_json(date_format='iso', orient='split') if design_df is not None else None,
        contrast_column,
        html.Div(),
        html.Div()
    )
