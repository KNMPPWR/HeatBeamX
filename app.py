from dash import Dash, html, dcc, Input, Output, ctx, callback
from dash.exceptions import PreventUpdate
import json

with open("assets/tissues.json") as tissues_json:
    tissues = json.load(tissues_json)

app = Dash(__name__)

memory = html.Div([
    dcc.Store(id="sources_coordinates_list", data=[], storage_type="memory"),
    dcc.Store(id="sources_display_list", data=[{"display":"none"},{"display":"none"},{"display":"none"}], storage_type="memory")
])

app.layout = html.Div([
    memory,
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
@callback(
    [Output("sources_coordinates_list","data"),Output("sources_display_list","data"),[Output("primary_source_position_parameters", "style"),Output("secondary_source_position_parameters", "style"),Output("third_source_position_parameters", "style")],Output("position_error_message", "displayed")],
    Input("sources_coordinates_list","data"),
    Input("sources_display_list","data"),
    Input("add_source", "n_clicks"),
    Input("remove_source", "n_clicks"),
    Input("add_source_x_coordinate", "value"), Input("add_source_y_coordinate", "value"), Input("add_source_z_coordinate", "value")
)
def update_number_of_sources(sources_coordinates_list,sources_display_list,add_source, remove_source, add_source_x_coordinate,add_source_y_coordinate,add_source_z_coordinate):
    """
    Adding and removing sources
    """
    add_source_coordinates = [add_source_x_coordinate, add_source_y_coordinate, add_source_z_coordinate]

    if ctx.triggered_id == "add_source": #When add source button triggered
        if not add_source_coordinates in sources_coordinates_list: #Check if there isn't other source with the same position
            sources_coordinates_list.append(add_source_coordinates)
        else:
            return sources_coordinates_list,sources_display_list,sources_display_list, True #Display error message and prevent form adding overlaping sources  
    if ctx.triggered_id == "remove_source": #Remove last source
        sources_coordinates_list.pop()
        for i in range(3):
            sources_display_list[i]={"display":"none"}

    number_of_sources = len(sources_coordinates_list)

    for i in range(number_of_sources):#Update display list based on current no. of sources
        sources_display_list[i]={"display":"block"}
    return sources_coordinates_list,sources_display_list,sources_display_list, False #Display current sources inputs

@callback(
    Output("add_source", "disabled"),
    Output("remove_source", "disabled"),
    Input("sources_coordinates_list", "data"),
    Input("add_source", "n_clicks"),
    Input("remove_source", "n_clicks")
)
def disable_source_buttons(sources_coordinates_list,add_source, remove_source):
    """
    Disabling adding and removing buttons
    """
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
    Input("sources_coordinates_list","data"),
    Input("add_source", "n_clicks"),
    [Input("add_source_x_coordinate", "value"), Input("add_source_y_coordinate", "value"), Input("add_source_z_coordinate", "value")],        
)
def update_primary_source_coordinates(sources_coordinates_list,add_source, *add_source_coordinates):
    if (ctx.triggered_id == "add_source" and
        len(sources_coordinates_list) == 1):
        return add_source_coordinates
    
    raise PreventUpdate

@callback(
    [Output("secondary_source_x_coordinate", "value"), Output("secondary_source_y_coordinate", "value"), Output("secondary_source_z_coordinate", "value")],
    Input("sources_coordinates_list","data"),
    Input("add_source", "n_clicks"),
    [Input("add_source_x_coordinate", "value"), Input("add_source_y_coordinate", "value"), Input("add_source_z_coordinate", "value")],        
)
def update_secondary_source_coordinates(sources_coordinates_list,add_source, *add_source_coordinates):
    if (ctx.triggered_id == "add_source" and
        len(sources_coordinates_list) == 2):
        return add_source_coordinates
    
    raise PreventUpdate

@callback(
    [Output("third_source_x_coordinate", "value"), Output("third_source_y_coordinate", "value"), Output("third_source_z_coordinate", "value")],
    Input("sources_coordinates_list","data"),
    Input("add_source", "n_clicks"),
    [Input("add_source_x_coordinate", "value"), Input("add_source_y_coordinate", "value"), Input("add_source_z_coordinate", "value")],        
)
def update_third_source_coordinates(sources_coordinates_list,add_source, *add_source_coordinates):
    if (ctx.triggered_id == "add_source" and
        len(sources_coordinates_list) == 3):
        return add_source_coordinates
    
    raise PreventUpdate
@callback(
    [Output("sources_coordinates_list","data",allow_duplicate=True),Output("primary_source_coordinates_overlap", "displayed"),[Output("primary_source_x_coordinate", "value",allow_duplicate=True), Output("primary_source_y_coordinate", "value",allow_duplicate=True), Output("primary_source_z_coordinate", "value",allow_duplicate=True)]],
    Input("sources_coordinates_list","data"),    
    [Input("primary_source_x_coordinate", "value"), Input("primary_source_y_coordinate", "value"), Input("primary_source_z_coordinate", "value")],
    prevent_initial_call='initial_duplicate'
)
def display_primary_source_coordinates_overlaping_warning(sources_coordinates_list,x,y,z):
    if len(sources_coordinates_list)==3:    
        if [x,y,z] in sources_coordinates_list[1:2]:
            return sources_coordinates_list,True, sources_coordinates_list[0]
        else:
            sources_coordinates_list[0] = [x,y,z]
            return sources_coordinates_list,False, [x,y,z]
    elif len(sources_coordinates_list)==2:
        if [x,y,z] in sources_coordinates_list[1]:
            return sources_coordinates_list,True, sources_coordinates_list[0]
        else:
            sources_coordinates_list[0] = [x,y,z]
            return sources_coordinates_list,False, [x,y,z]
    elif len(sources_coordinates_list)==1:
        sources_coordinates_list[0] = [x,y,z]
        return sources_coordinates_list,False, [x,y,z]
    else:
        raise PreventUpdate

@callback(
    [Output("sources_coordinates_list","data",allow_duplicate=True),Output("secondary_source_coordinates_overlap", "displayed"),[Output("secondary_source_x_coordinate", "value",allow_duplicate=True), Output("secondary_source_y_coordinate", "value",allow_duplicate=True), Output("secondary_source_z_coordinate", "value",allow_duplicate=True)]],
    Input("sources_coordinates_list","data"), 
    [Input("secondary_source_x_coordinate", "value"), Input("secondary_source_y_coordinate", "value"), Input("secondary_source_z_coordinate", "value")],
    prevent_initial_call='initial_duplicate'
)
def display_secondary_source_coordinates_overlaping_warning(sources_coordinates_list,x,y,z):
    if len(sources_coordinates_list)==3:
        if [x,y,z] in [sources_coordinates_list[0],sources_coordinates_list[2]]:
            return sources_coordinates_list,True, sources_coordinates_list[1]
        else:
            sources_coordinates_list[1] = [x,y,z]
            return sources_coordinates_list,False, [x,y,z]
    elif len(sources_coordinates_list)==2:
        if [x,y,z] == sources_coordinates_list[0]:
            return sources_coordinates_list,True, sources_coordinates_list[1]
        else:
            sources_coordinates_list[1] = [x,y,z]
            return sources_coordinates_list,False, [x,y,z]
    else:
        raise PreventUpdate
@callback(
    [Output("sources_coordinates_list","data",allow_duplicate=True),Output("third_source_coordinates_overlap", "displayed"),[Output("third_source_x_coordinate", "value",allow_duplicate=True), Output("third_source_y_coordinate", "value",allow_duplicate=True), Output("third_source_z_coordinate", "value",allow_duplicate=True)]],
    Input("sources_coordinates_list","data"), 
    [Input("third_source_x_coordinate", "value"), Input("third_source_y_coordinate", "value"), Input("third_source_z_coordinate", "value")],
    prevent_initial_call='initial_duplicate'
)
def display_third_source_coordinates_overlaping_warning(sources_coordinates_list,x,y,z):
    if len(sources_coordinates_list)==3:
        if [x,y,z] in [sources_coordinates_list[0],sources_coordinates_list[1]]:
            return sources_coordinates_list,True, sources_coordinates_list[2]
        else:
            sources_coordinates_list[2] = [x,y,z]
            return sources_coordinates_list,False, [x,y,z]
    else:
        raise PreventUpdate
if __name__ == '__main__':
    app.run(debug=True)
    