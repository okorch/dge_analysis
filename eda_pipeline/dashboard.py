from dash import Dash, html
PLOT_STYLE = {'maxWidth': '800px', 'margin': '0 auto', 'paddingBottom': '30px'}

def run_dashboard(count_matrix, design_matrix, info_messages):

    # Compute logCPM


    # Library sizes calculation

    # PCA and UMAP

    # Density plot of logCPM values

    # Correlation heatmap

    #================ Dash App =====================
    app = Dash(__name__)

    # Information how script called
    info_div = html.Div([
        html.H4("Info and Status Messages:"),
        *[html.P(msg) for msg in info_messages]
    ], style={'padding': '10px', 'backgroundColor': '#f9f9f9', 'border': '1px solid #ddd', 'marginBottom': '20px'})


    app.layout = html.Div([
        info_div,
        # Page name
        html.H1("RNA-Seq Dashboard", style={'textAlign': 'center'}),
        # Add plots here
    ], style=PLOT_STYLE)

    app.run(debug=True)