from dash import html, dcc
import plotly.express as px


PLOT_STYLE = {'maxWidth': '800px', 'margin': '0 auto', 'paddingBottom': '30px'}

def eda_dashboard_layout(lib_df, pca_result, umap_result, corr_matrix, info_messages):


    # Correlation Heatmap
    corr_fig = px.imshow(
        corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        color_continuous_scale="Viridis",
        title="Sample-wise Expression Correlation Heatmap"
    )

    # === Layout Components ===

    info_div = html.Div([
        html.H4("Info and Status Messages:"),
        *[html.P(msg) for msg in info_messages]
    ], style={
        'padding': '10px',
        'backgroundColor': '#f9f9f9',
        'border': '1px solid #ddd',
        'marginBottom': '20px'
    })

    layout = html.Div([
        info_div,

        html.H2("Library Sizes", style={'textAlign': 'center'}),

        dcc.Graph(figure=px.bar(
            lib_df, x="Sample", y="Library Size", color="condition",
            title="Library Sizes per Sample"
        )),

        html.H2("PCA", style={'textAlign': 'center'}),
        dcc.Graph(figure=px.scatter(
            pca_result, x="PC1", y="PC2", color="condition", hover_name=pca_result.index,
            title="PCA of Samples"
        )),

        html.H2("UMAP", style={'textAlign': 'center'}),
        dcc.Graph(figure=px.scatter(
            umap_result, x="UMAP1", y="UMAP2", color="condition", hover_name=umap_result.index,
            title="UMAP of Samples"
        )),

        html.H2("Sample Correlation Heatmap", style={'textAlign': 'center'}),
        dcc.Graph(figure=corr_fig),

    ], style={'padding': '20px'})

    return layout