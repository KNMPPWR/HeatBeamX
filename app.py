from dash import Dash, html, dcc

from views.settings_view import create_setting_view
from views.simulation_view import create_simulation_view
from views.info_view import create_info_view

app = Dash(__name__)

app.layout = html.Div([
    html.H1(id="navbar", children='HeatBeamX. To będzie super projekt!!!', style={'textAlign': 'center'}),
    html.Div([
        dcc.Tabs(id="main_tabs", children=[create_setting_view(), create_simulation_view(), create_info_view()])
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
