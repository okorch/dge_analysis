from dash import html, dcc
import dash
import markdown
from config.config import MAIN_FONT

dash.register_page(__name__, path="/")

# Read and convert the README.md to HTML
with open("README.md", "r") as f:
    readme_content = f.read()

readme_html = markdown.markdown(readme_content)

layout = html.Div([
    html.H2("Welcome to the Differential Gene Expression App"),
    html.Div([
        dcc.Markdown(readme_content, dangerously_allow_html=True)
    ], style={
        'width': '80%',
        'textAlign': 'left',
        'fontFamily': MAIN_FONT,
        'lineHeight': '1.8'
    }),
    html.Br(),
    dcc.Link("→ Go to File Upload", href="/upload", style={"fontSize": "18px"}),
], style={
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'center',
    'padding': '40px',
    'fontFamily': MAIN_FONT
})
