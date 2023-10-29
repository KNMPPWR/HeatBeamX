from dash import Dash, html, dcc, Input, Output, callback

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='HeatBeamX. To będzie super projekt!!!', style={'textAlign':'center'}),
    html.Div([
        dcc.Tabs(id="main_tabs",
            children=[
                dcc.Tab(id="settings", label="Settings",
                    children = [    
                        dcc.Tabs(id ="setting_tabs",
                                children=[
                                    dcc.Tab(
                                        label="Tissue"
                                    ),
                                    dcc.Tab(
                                        label="ROI",
                                        children =[
                                            html.Label("Voxel dimension: ",htmlFor="voxel_dim_input"),
                                            dcc.Input(id="voxel_dim_input",type="number", min=0.001, step=0.001, value=1.000),
                                            html.Br(),
                                            html.Div(id="no_of_voxels",
                                                    children=[                                            
                                                        html.Label("No. of voxels in X-direction: ",htmlFor="no_of_voxel_x"),
                                                        dcc.Input(id="no_of_voxel_x", type = "number", min=1, step=1,value=60),
                                                        html.Label("No. of voxels in Y-direction: ",htmlFor="no_of_voxel_y"),
                                                        dcc.Input(id="no_of_voxel_y", type="number", min=1, step=1, value=60),
                                                        html.Label("No. of voxels in Z-direction: ",htmlFor="no_of_voxel_y"),
                                                        dcc.Input(id="no_of_voxel_z", type="number", min=1, step=1, value=60)
                                                    ])
                                        ]
                                    ),
                                    dcc.Tab(
                                        label="Laser"
                                    )])
                ]),
                dcc.Tab(id="simulation",label="Simulation"),
                dcc.Tab(id="info_tab",label="Info")
            ])
    ])
])

if __name__ == '__main__':
    app.run(debug=True)