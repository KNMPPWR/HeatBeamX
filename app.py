from dash import Dash, html, dcc

from views.settings_view import init_settings_variables, create_setting_view
from views.simulation_view import create_simulation_view
from views.info_view import create_info_view

app = Dash(__name__)


def create_main_layout() -> object:
    init_settings_variables()

    return html.Div([
        html.H1(id="navbar", children='HeatBeamX. To będzie super projekt!!!', style={'textAlign': 'center'}),
        html.Div([
            dcc.Tabs(id="main_tabs", children=[create_setting_view(), create_simulation_view(), create_info_view()])
        ])
    ])


app.layout = create_main_layout

if __name__ == '__main__':
    app.run(debug=True)
