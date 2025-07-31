from dash import Dash, html, dcc, page_container, get_asset_url
import dash_bootstrap_components as dbc

app = Dash(__name__,
           use_pages=True,
           suppress_callback_exceptions=True,
           external_stylesheets = [dbc.themes.JOURNAL])

app.title = "Differential Gene Expression App"
image_path = 'app_icon.png'

app.layout = html.Div([
    html.Div([
        html.Img(src=get_asset_url(image_path), style={"height": "100px"}),
        html.H1(
            "Differential Gene Expression App",
            className="text-secondary fw-bold my-0",
            style={"flex": "1", "textAlign": "center", "margin": "0"}
        ),
    ], style={
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "gap": "10px",
        "padding": "10px"
    }),

    dcc.Location(id="url"),

    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("About tool", href="/"),
            dbc.Nav(
                [
                    # dbc.NavItem(dbc.NavLink("Home", href="/")),
                    dbc.NavItem(dbc.NavLink("Upload Files", href="/upload")),
                    dbc.NavItem(dbc.NavLink("EDA", href="/eda")),
                    dbc.NavItem(dbc.NavLink("DGE", href="/dge")),
                ],
                navbar=True,
                className="me-auto",  # navigation bar on the left side
            ),
        ]),
        color="primary",
        dark=True,
        expand="md",
    ),

    html.Hr(),

    page_container # pages rendering

], style={
    "padding": "20px"
})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True) # when creating docker
    # app.run( port=8050, debug=True)