# dashboard.py
from dash import Dash, html

PLOT_STYLE = {'maxWidth': '800px', 'margin': '0 auto', 'paddingBottom': '30px'}


def run_dashboard(dge_data):

    # ================ Dash App =====================
    app = Dash(__name__)
    app.title = "Differential Gene Expression"

    app.layout = html.Div([
        html.H2("Differential Gene Expression Dashboard", style={"textAlign": "center"}),

    ])

    # =================== P-value distribution ===================

    # ==================== Volcano plot ===================

    # =================== MA plot ===================

    # =================== Interactive Table ===================

    # Add some more visualisations
    app.run(debug=True)