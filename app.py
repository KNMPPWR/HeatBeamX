from dash import Dash, html, dcc, Input, Output, ctx, callback
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
                                                                        dcc.Input(id="native_refr_index",type="number",min=0.01,max=2,step=0.01),
                                                                        dcc.Input(id="native_absorption",type="number",min=0.001,max=1,step=0.001),
                                                                        dcc.Input(id="native_scattering",type="number",min=1,max=40,step=0.1),
                                                                        dcc.Input(id="native_g_factor",type="number",min=0.001,max=2,step=0.001)
                                                                    ]),
                                                        html.Div(id="coagulated",
                                                                    children=[
                                                                        dcc.Input(id="coag_refr_index",type="number", min=0.01,max=2,step=0.01),
                                                                        dcc.Input(id="coag_absorption",type="number", min=0.001,max=1,step=0.001),
                                                                        dcc.Input(id="coag_scattering",type="number", min=1,max=40,step=0.1),
                                                                        dcc.Input(id="coag_g_factor",type="number", min=0.001,max=2,step=0.001)
                                                                    ])
                                                    ]
                                            ),
                                            html.Br(),
                                            html.Div(id="thermal_parameters",
                                                    children=[
                                                        dcc.Input(id="init_temp",type="number",min=30,max=40,step=0.1),
                                                        dcc.Input(id="blood_perf",type="number",min=0.01,max=1,step=0.01),
                                                        dcc.Input(id="water_cont", type="number",min=50,max=100,step=0.1),
                                                        dcc.Input(id="heat_conduct",type="number",min=0.0001,max=0.01,step=0.0001),
                                                        dcc.Input(id="heat_cap",type="number",min=3,max=4,step=0.0001),
                                                        dcc.Input(id="density",type="number",min=0.9,max=1.5,step=0.001)
                                                    ]
                                            ),
                                            html.Br(),
                                            html.Div(id="damage_parameters",
                                                    children=[
                                                        dcc.Input(id="dmg_threshold",type="number",min=0.1,max=1,step=0.01),
                                                        dcc.Input(id="activation_energy",type="number",min=600000,max=750000,step=10000),
                                                        dcc.Input(id="rate_param",type="number",min=8E+104,max=10E+104,step=0.01E+104, style={"width":100})
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
                                        label="Laser",
                                        children=[      
                                            html.Label("Number of sources: ", htmlFor="number_of_sources"),
                                            dcc.Slider(min=1, step=1, max=3, value=1, id="number_of_sources"),                                 
                                            html.Label("Source number: ", htmlFor="courent_source_number"),
                                            dcc.Dropdown(value=1, id="courent_source_number"),
                                            html.Div(id="source_position_parameters",
                                                    children=[                                            
                                                        html.Label("Position of aplicator center (without peak): ", htmlFor="source_position_parameters"),
                                                        html.Br(),
                                                        html.Label("X (mm): ", htmlFor="source_x_coordinate"),
                                                        dcc.Input(id="source_x_coordinate", type="number", min=0, step=0.001, value=0),
                                                        html.Label("Y (mm): ", htmlFor="source_y_coordinate"),
                                                        dcc.Input(id="source_y_coordinate", type="number", min=0, step=0.001, value=0),
                                                        html.Label("Z (mm): ", htmlFor="source_z_coordinate"),
                                                        dcc.Input(id="source_z_coordinate", type="number", min=0, step=0.001, value=0)
                                                    ]),
                                            html.Button("Save", id="save_source"),
                                            dcc.ConfirmDialog(id="sources_with_same_coordinates", message="Two or more sources have the same coordinates as this one")
                                        ]
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


sources_coordinates_list = [[0,0,0]]

@callback(
    Output("courent_source_number", "options"),
    Input("number_of_sources", "value")
)
def update_number_of_sources(number_of_sources):
    if ctx.triggered_id == "number_of_sources":
        if len(sources_coordinates_list) < number_of_sources:
            sources_coordinates_list.append([0,0,0])

        else:
            sources_coordinates_list.pop()

    return [i+1 for i in range(len(sources_coordinates_list))]

@callback(
    [Output("source_x_coordinate", "max"), Output("source_y_coordinate", "max"), Output("source_z_coordinate", "max")],
    Input("dim_x", "value"),
    Input("dim_y", "value"),
    Input("dim_z", "value")
)
def update_source_coordinate_max(dim_x, dim_y, dim_z):
    return dim_x, dim_y, dim_z

@callback(
    [Output("source_x_coordinate", "value"), Output("source_y_coordinate", "value"), Output("source_z_coordinate", "value")],
    Input("courent_source_number", "value"),
    Input("source_x_coordinate", "value"),
    Input("source_y_coordinate", "value"),
    Input("source_z_coordinate", "value"),
    Input("save_source", "n_clicks")
)
def update_source_coordinate_values(courent_source_number, source_x_coordinate, source_y_coordinate, source_z_coordinate, save_button):
    if ctx.triggered_id == "save_source":
        sources_coordinates_list[courent_source_number - 1] = [source_x_coordinate, source_y_coordinate, source_z_coordinate]

    if ctx.triggered_id == "courent_source_number":
        return sources_coordinates_list[courent_source_number - 1]
        
    return [source_x_coordinate, source_y_coordinate, source_z_coordinate]

@callback(
    Output("sources_with_same_coordinates", "displayed"),
    Input("courent_source_number", "value"),
    Input("save_source", "n_clicks")
)
def display_sources_with_same_coordinates_warning(courent_source_number, save_button):
    if ctx.triggered_id == "save_source":
        if 1 < sources_coordinates_list.count(sources_coordinates_list[courent_source_number - 1]):
            return True

    return False

if __name__ == '__main__':
    app.run(debug=True)