from dash import html, dcc
import dash
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

load_figure_template('JOURNAL')

dash.register_page(__name__, path="/")

with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

layout = html.Div([
    html.Div([
        dcc.Markdown(readme_content)
    ], style={
        'width': '80%',
        'textAlign': 'left',
        'lineHeight': '1.8'
    }),
    html.Br(),
    dbc.Button("→ Go to File Upload", href="/upload", color="secondary", outline=True, size="lg", className="mb-3", style={"fontSize": "18px"})
], style={
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'center',
    'padding': '40px',
})
