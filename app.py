from dash import Dash, html, dcc, Input, Output, ctx, callback
from dash.exceptions import PreventUpdate
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
                                            html.Label("Position of aplicator center (without peak): ", htmlFor="source_position_parameters"),
                                            html.Div(id="add_source_position_parameters", style={"display":"block"},
                                                    children=[                                            
                                                        html.Label("X (mm): ", htmlFor="add_source_x_coordinate"),
                                                        dcc.Input(id="add_source_x_coordinate", type="number", min=0, step=0.001, value=0),
                                                        html.Label("Y (mm): ", htmlFor="add_source_y_coordinate"),
                                                        dcc.Input(id="add_source_y_coordinate", type="number", min=0, step=0.001, value=0),
                                                        html.Label("Z (mm): ", htmlFor="add_source_z_coordinate"),
                                                        dcc.Input(id="add_source_z_coordinate", type="number", min=0, step=0.001, value=0),
                                                        html.Button("Add source", id="add_source", n_clicks=0, disabled=False),
                                                        dcc.ConfirmDialog(id="sources_with_overlapping_coordinates", message="Can't add source because of overlapping coordinates")
                                                    ]),
                                            html.Div(id="primary_source_position_parameters", style={"display":"none"},
                                                    children=[                                            
                                                        html.Label("Primary source: ", htmlFor="primary_source"), 
                                                        html.Br(),
                                                        html.Label("X (mm): ", htmlFor="primary_source_x_coordinate"),
                                                        dcc.Input(id="primary_source_x_coordinate", type="number", min=0, step=0.001),
                                                        html.Label("Y (mm): ", htmlFor="primary_source_y_coordinate"),
                                                        dcc.Input(id="primary_source_y_coordinate", type="number", min=0, step=0.001),
                                                        html.Label("Z (mm): ", htmlFor="primary_source_z_coordinate"),
                                                        dcc.Input(id="primary_source_z_coordinate", type="number", min=0, step=0.001),
                                                        dcc.ConfirmDialog(id="primary_source_coordinates_overlap", message="Primary source can't overlap with another source")
                                                    ]),
                                            html.Div(id="secondary_source_position_parameters", style={"display":"none"},
                                                    children=[                                            
                                                        html.Label("Secondary source: ", htmlFor="secondary_source"),
                                                        html.Br(),
                                                        html.Label("X (mm): ", htmlFor="secondary_source_x_coordinate"),
                                                        dcc.Input(id="secondary_source_x_coordinate", type="number", min=0, step=0.001),
                                                        html.Label("Y (mm): ", htmlFor="secondary_source_y_coordinate"),
                                                        dcc.Input(id="secondary_source_y_coordinate", type="number", min=0, step=0.001),
                                                        html.Label("Z (mm): ", htmlFor="secondary_source_z_coordinate"),
                                                        dcc.Input(id="secondary_source_z_coordinate", type="number", min=0, step=0.001),
                                                        dcc.ConfirmDialog(id="secondary_source_coordinates_overlap", message="Secondary source can't overlap with another source")
                                                    ]),
                                            html.Div(id="third_source_position_parameters", style={"display":"none"},
                                                    children=[                                            
                                                        html.Label("Third source: ", htmlFor="third_source"),
                                                        html.Br(),
                                                        html.Label("X (mm): ", htmlFor="third_source_x_coordinate"),
                                                        dcc.Input(id="third_source_x_coordinate", type="number", min=0, step=0.001),
                                                        html.Label("Y (mm): ", htmlFor="third_source_y_coordinate"),
                                                        dcc.Input(id="third_source_y_coordinate", type="number", min=0, step=0.001),
                                                        html.Label("Z (mm): ", htmlFor="third_source_z_coordinate"),
                                                        dcc.Input(id="third_source_z_coordinate", type="number", min=0, step=0.001),
                                                        dcc.ConfirmDialog(id="third_source_coordinates_overlap", message="Third source can't overlap with another source")
                                                    ]),
                                            html.Button("Remove last source", id="remove_source", n_clicks=0, disabled=True),
                                            dcc.ConfirmDialog(id="position_error_message", message="Source can't overlap with another source")
                                        ]
                                    )])
                ]),
                dcc.Tab(id="simulation",label="Simulation"),
                dcc.Tab(id="info_tab",label="Info")
            ])
    ])
])

#ROI Callbacks
@callback(
    [Output("dim_x","value"),Output("dim_y","value"),Output("dim_z","value")],
    Input("voxel_dim_input","value"),
    Input("no_of_voxel_x","value"),
    Input("no_of_voxel_y","value"),
    Input("no_of_voxel_z","value"),
)
def calculate_dim(voxel_dim, no_of_voxel_x, no_of_voxel_y, no_of_voxel_z):
    return round(voxel_dim*no_of_voxel_x,3), round(voxel_dim*no_of_voxel_y,3), round(voxel_dim*no_of_voxel_z,3)

#Tissue Callbacks
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

#Source Callbacks
sources_coordinates_list = []
sources_display_list = [{"display":"none"},{"display":"none"},{"display":"none"}]
@callback(
    [[Output("primary_source_position_parameters", "style"),Output("secondary_source_position_parameters", "style"),Output("third_source_position_parameters", "style")],Output("position_error_message", "displayed")],
    Input("add_source", "n_clicks"),
    Input("remove_source", "n_clicks"),
    Input("add_source_x_coordinate", "value"), Input("add_source_y_coordinate", "value"), Input("add_source_z_coordinate", "value")
)
def update_number_of_sources(add_source, remove_source, add_source_x_coordinate,add_source_y_coordinate,add_source_z_coordinate):
    """
    Adding and removing sources
    """
    add_source_coordinates = [add_source_x_coordinate, add_source_y_coordinate, add_source_z_coordinate]

    if ctx.triggered_id == "add_source": #When add source button triggered
        if not add_source_coordinates in sources_coordinates_list: #Check if there isn't other source with the same position
            sources_coordinates_list.append(add_source_coordinates)
        else:
            return sources_display_list, True #Display error message and prevent form adding overlaping sources  
    if ctx.triggered_id == "remove_source": #Remove last source
        sources_coordinates_list.pop()
    
    number_of_sources = len(sources_coordinates_list)

    for i in range(number_of_sources):#Update display list based on current no. of sources
        sources_display_list[i]={"display":"block"}
    return sources_display_list, False #Display current sources inputs

@callback(
    Output("add_source", "disabled"),
    Output("remove_source", "disabled"),
    Input("add_source", "n_clicks"),
    Input("remove_source", "n_clicks")
)
def disable_source_buttons(add_source, remove_source):
    if len(sources_coordinates_list) == 0:
        return False, True
    
    if len(sources_coordinates_list) < 3:
        return False, False
    
    if len(sources_coordinates_list) == 3:
        return True, False

@callback(
    [Output("add_source_x_coordinate", "max"), Output("add_source_y_coordinate", "max"), Output("add_source_z_coordinate", "max")],
    [Output("primary_source_x_coordinate", "max"), Output("primary_source_y_coordinate", "max"), Output("primary_source_z_coordinate", "max")],
    [Output("secondary_source_x_coordinate", "max"), Output("secondary_source_y_coordinate", "max"), Output("secondary_source_z_coordinate", "max")],
    [Output("third_source_x_coordinate", "max"), Output("third_source_y_coordinate", "max"), Output("third_source_z_coordinate", "max")],
    Input("dim_x", "value"),
    Input("dim_y", "value"),
    Input("dim_z", "value")
)
def update_source_coordinate_max(dim_x, dim_y, dim_z):
    return 4*[dim_x, dim_y, dim_z]

@callback(
    [Output("primary_source_x_coordinate", "value"), Output("primary_source_y_coordinate", "value"), Output("primary_source_z_coordinate", "value")],
    Input("add_source", "n_clicks"),
    [Input("add_source_x_coordinate", "value"), Input("add_source_y_coordinate", "value"), Input("add_source_z_coordinate", "value")],        
)
def update_primary_source_coordinates(add_source, *add_source_coordinates):
    if (ctx.triggered_id == "add_source" and
        len(sources_coordinates_list) == 1):
        return add_source_coordinates
    
    raise PreventUpdate

@callback(
    [Output("secondary_source_x_coordinate", "value"), Output("secondary_source_y_coordinate", "value"), Output("secondary_source_z_coordinate", "value")],
    Input("add_source", "n_clicks"),
    [Input("add_source_x_coordinate", "value"), Input("add_source_y_coordinate", "value"), Input("add_source_z_coordinate", "value")],        
)
def update_secondary_source_coordinates(add_source, *add_source_coordinates):
    if (ctx.triggered_id == "add_source" and
        len(sources_coordinates_list) == 2):
        return add_source_coordinates
    
    raise PreventUpdate

@callback(
    [Output("third_source_x_coordinate", "value"), Output("third_source_y_coordinate", "value"), Output("third_source_z_coordinate", "value")],
    Input("add_source", "n_clicks"),
    [Input("add_source_x_coordinate", "value"), Input("add_source_y_coordinate", "value"), Input("add_source_z_coordinate", "value")],        
)
def update_third_source_coordinates(add_source, *add_source_coordinates):
    if (ctx.triggered_id == "add_source" and
        len(sources_coordinates_list) == 3):
        return add_source_coordinates
    
    raise PreventUpdate

@callback(
    Output("sources_with_overlapping_coordinates", "displayed"),
    Input("add_source", "n_clicks"),
)
def display_cant_add_source_warning(add_source):
    if ctx.triggered_id == "add_source":
        duplicate_coordinates = [coordinates for coordinates in sources_coordinates_list if sources_coordinates_list.count(coordinates) > 1]

        if len(duplicate_coordinates):
            return True

    return False

@callback(
    Output("primary_source_coordinates_overlap", "displayed"),
    [Input("primary_source_x_coordinate", "value"), Input("primary_source_y_coordinate", "value"), Input("primary_source_z_coordinate", "value")]
)
def display_primary_source_coordinates_overlaping_warning(*primary_source_coordinates):
    if (ctx.triggered_id.startswith("primary") and
        sources_coordinates_list.count(primary_source_coordinates) > 1):
        return True

    return False

@callback(
    Output("secondary_source_coordinates_overlap", "displayed"),
    [Input("secondary_source_x_coordinate", "value"), Input("secondary_source_y_coordinate", "value"), Input("secondary_source_z_coordinate", "value")]
)
def display_secondary_source_coordinates_overlaping_warning(*secondary_source_coordinates):
    if (ctx.triggered_id.startswith("secondary") and
        sources_coordinates_list.count(secondary_source_coordinates) > 1):
        return True

    return False

@callback(
    Output("third_source_coordinates_overlap", "displayed"),
    [Input("third_source_x_coordinate", "value"), Input("third_source_y_coordinate", "value"), Input("third_source_z_coordinate", "value")]
)
def display_third_source_coordinates_overlaping_warning(*third_source_coordinates):
    if (ctx.triggered_id.startswith("third") and
        sources_coordinates_list.count(third_source_coordinates) > 1):
        return True

    return False


if __name__ == '__main__':
    app.run(debug=True)