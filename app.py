from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__,
           use_pages=True,
           suppress_callback_exceptions=True,
           external_stylesheets = [dbc.themes.JOURNAL])

app.title = "Differential Gene Expression App"


app.layout = html.Div([
    html.H1(
        "Differential Gene Expression App",
        className="text-secondary fw-bold my-4",
        style={"textAlign": "center"}
    ),

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
    app.run(host="0.0.0.0", port=8050, debug=True)
