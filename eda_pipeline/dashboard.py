from dash import html
PLOT_STYLE = {'maxWidth': '800px', 'margin': '0 auto', 'paddingBottom': '30px'}

def eda_dashboard_layout(count_matrix, design_matrix, info_messages):
    # === Preprocessing ===

    # === Figures ===

    # Density Plot

    # Correlation Heatmap

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
        html.H1("RNA-Seq Dashboard", style={'textAlign': 'center'}),

        html.H2("Library Sizes", style={'textAlign': 'center'}),
        # Add bar chart Library sizes

        html.H2("PCA", style={'textAlign': 'center'}),
        # Add scatter plot PCA

        html.H2("UMAP", style={'textAlign': 'center'}),
        # Add scatter plot UMAP

        html.H2("Sample Correlation Heatmap", style={'textAlign': 'center'}),
        # Add correlation heatmap
    ], style={'padding': '20px'})

    return layout