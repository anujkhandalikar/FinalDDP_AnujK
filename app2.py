from ctypes import alignment
import dash  # pip install dash
import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
from dash import Dash, dcc, html, Input, Output, callback

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP]

)


navbar = dbc.NavbarSimple(
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(page["name"], href=page["path"])
                    for page in dash.page_registry.values()
                    if page["module"] != "pages.not_found_404"
                ],
                nav=True,
                label="Choose Chart Type",
            ),

            brand="EDA for Crash Analytics",
            color="Black",
            id="navbar",
            dark=True,
            style={"align":"center"},
            className="mb-2"
)

app.layout = html.Div(children=[navbar, dl.plugins.page_container])
# dbc.Container(
#     [navbar, dl.plugins.page_container],
#     fluid=True,
# )

if __name__ == "__main__":
    app.run_server(debug=True, port=5005)
