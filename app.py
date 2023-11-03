from dash import Dash, html, dcc, Input, Output, callback
import json

with open("assets/tissues.json") as tissues_json:
    tissues = json.load(tissues_json)

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
                                        label="Tissue",
                                        children =[
                                            dcc.Dropdown(list(tissues.keys()),value="Liver",id="tissue_select"),
                                            html.Div(id="selected"),
                                            html.Div(id="optical_parameters",
                                                    children=[
                                                        dcc.Input(id="wave_length", type="number", value=850),
                                                        html.Div(id="native",
                                                                    children=[
                                                                        dcc.Input(id="native_refr_index",type="number", value=1.36),
                                                                        dcc.Input(id="native_absorption",type="number", value=0.098),
                                                                        dcc.Input(id="native_scattering",type="number", value=20.2),
                                                                        dcc.Input(id="native_g_factor",type="number", value=0.949)
                                                                    ]),
                                                        html.Div(id="coagulated",
                                                                    children=[
                                                                        dcc.Input(id="coag_refr_index",type="number", value = 1.36),
                                                                        dcc.Input(id="coag_absorption",type="number", value = 0.071),
                                                                        dcc.Input(id="coag_scattering",type="number", value=23.9),
                                                                        dcc.Input(id="coag_g_factor",type="number", value=0.882)
                                                                    ])
                                                    ]
                                            ),
                                            html.Br(),
                                            html.Div(id="thermal_parameters",
                                                    children=[
                                                        dcc.Input(id="init_temp",type="number", value=35),
                                                        dcc.Input(id="blood_perf",type="number", value=0.5),
                                                        dcc.Input(id="water_cont", type="number", value=69),
                                                        dcc.Input(id="heat_conduct",type="number",value=0.0045),
                                                        dcc.Input(id="heat_cap",type="number",value=3.3197),
                                                        dcc.Input(id="density",type="number",value=1.093)
                                                    ]
                                            ),
                                            html.Br(),
                                            html.Div(id="damage_parameters",
                                                    children=[
                                                        dcc.Input(id="dmg_threshold",type="number",value=0.6),
                                                        dcc.Input(id="activation_energy",type="number",value=670000),
                                                        dcc.Input(id="rate_param",type="number",value=9.4E+104, step=0.01E+104)
                                                    ]
                                            )
                                        ]
                                    ),
                                    dcc.Tab(
                                        label="ROI",
                                        children =[
                                            html.Label("Voxel dimension (mm): ",htmlFor="voxel_dim_input"),
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
                                                    ]),
                                            html.Label("Dimensions of ROI", htmlFor="dim_of_roi"),
                                            html.Div(id="dim_of_roi",
                                                    children=[
                                                        html.Label("X: ",htmlFor="dim_x"),
                                                        dcc.Input(id="dim_x",value=60,disabled=True),
                                                        html.Label("Y: ",htmlFor="dim_y"),
                                                        dcc.Input(id="dim_y",value=60,disabled=True),
                                                        html.Label("Z:",htmlFor="dim_z"),
                                                        dcc.Input(id="dim_z",value=60,disabled=True)
                                                    ]
                                            )
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

@callback(
    [Output("dim_x","value"),Output("dim_y","value"),Output("dim_z","value")],
    Input("voxel_dim_input","value"),
    Input("no_of_voxel_x","value"),
    Input("no_of_voxel_y","value"),
    Input("no_of_voxel_z","value"),
)
def calculate_dim(voxel_dim, no_of_voxel_x, no_of_voxel_y, no_of_voxel_z):
    return round(voxel_dim*no_of_voxel_x,3), round(voxel_dim*no_of_voxel_y,3), round(voxel_dim*no_of_voxel_z,3)

@callback(
    [Output("wave_length","value"),
    [Output("native_refr_index","value"),Output("native_absorption","value"),Output("native_scattering","value"),Output("native_g_factor","value")],
    [Output("coag_refr_index","value"),Output("coag_absorption","value"),Output("coag_scattering","value"),Output("coag_g_factor","value")],
    [Output("init_temp","value"),Output("blood_perf","value"),Output("water_cont","value"),Output("heat_conduct","value"),Output("heat_cap","value"),Output("density","value")],
    [Output("dmg_threshold","value"),Output("activation_energy","value"),Output("rate_param","value")]],
    Input("tissue_select","value")
)
def update_tissue(tissue):
    wave_param = tissues[tissue]["Optical parameters"]["Wave length"]
    native = list(tissues[tissue]["Optical parameters"]["Native"].values())
    coagulated = list(tissues[tissue]["Optical parameters"]["Coagulated"].values())
    thermal = list(tissues[tissue]["Thermal parameters"].values())
    damage = list(tissues[tissue]["Damage parameters"].values())
    return wave_param,native,coagulated,thermal,damage

if __name__ == '__main__':
    app.run(debug=True)