from dash import Dash, html, dcc

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='HeatBeamX. To będzie super projekt!!!', style={'textAlign':'center'}),
    html.Div([
        dcc.Tabs(id ="setting_tabs",
                children=[
                    dcc.Tab(
                        label="Tissue"
                    ),
                    dcc.Tab(
                        label="ROI"
                    ),
                    dcc.Tab(
                        label="Laser"
                    )
                ]
        )
    ])
])

if __name__ == '__main__':
    app.run(debug=True)