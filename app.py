from dash import Dash, html, dcc, page_container
from config.config import MAIN_FONT

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.title = "Differential Gene Expression App"

app.layout = html.Div([
    html.H1("DGE App", style={"textAlign": "center"}),
    dcc.Location(id="url"),
    dcc.Link("Home", href="/"),
    html.Br(),
    dcc.Link("Upload Files", href="/upload"),
    html.Br(),
    dcc.Link("EDA", href="/eda"),
    html.Br(),
    dcc.Link("DGE", href="/dge"),
    html.Hr(),
    page_container
],
style={
    "fontFamily": MAIN_FONT,
    "padding": "20px"
})

if __name__ == "__main__":
    app.run(debug=True, port=8085)