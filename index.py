from dash import html, dcc

from app import app
from models.AppDataModel import AppDataModel
from views.settings_view import create_setting_view
from views.simulation_view import create_simulation_view
from views.info_view import create_info_view


def create_main_layout() -> object:
    app_model: AppDataModel = AppDataModel()
    app.model = app_model

    return html.Div([
        html.H1(id="navbar", children="HeatBeamX. To będzie super projekt!!!", style={"textAlign": "center"}),
        html.Div([
            dcc.Tabs(id="main_tabs", children=[create_setting_view(app_model),
                                               create_simulation_view(app_model),
                                               create_info_view(app_model)]
                     )
        ])
    ])


app.layout = create_main_layout

if __name__ == "__main__":
    app.run(debug=True)
