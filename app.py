from dash import Dash, html, dcc, Input, Output, ctx, callback
from dash.exceptions import PreventUpdate
import json

#Reading data from json file
with open("assets/tissues.json") as tissues_json:
    tissues = json.load(tissues_json)

app = Dash(__name__)

#Variables 
memory = html.Div([
    dcc.Store(id="sources_coordinates_list", data=[], storage_type="session"),
    dcc.Store(id="sources_display_list", data=[{"display":"none"},{"display":"none"},{"display":"none"}], storage_type="session")
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
                                                        dcc.Input(id="add_source_x_coordinate", type="number", min=0, step=0.001, value=0, debounce=True),
                                                        html.Label("Y (mm): ", htmlFor="add_source_y_coordinate"),
                                                        dcc.Input(id="add_source_y_coordinate", type="number", min=0, step=0.001, value=0, debounce=True),
                                                        html.Label("Z (mm): ", htmlFor="add_source_z_coordinate"),
                                                        dcc.Input(id="add_source_z_coordinate", type="number", min=0, step=0.001, value=0, debounce=True),
                                                        html.Button("Add source", id="add_source", n_clicks=0, disabled=False),
                                                        dcc.ConfirmDialog(id="sources_with_overlapping_coordinates", message="Can't add source because of overlapping coordinates")
                                                    ]),
                                            html.Div(id="primary_source_position_parameters", style={"display":"none"},
                                                    children=[                                            
                                                        html.Label("Primary source: ", htmlFor="primary_source"), 
                                                        html.Br(),
                                                        html.Label("X (mm): ", htmlFor="primary_source_x_coordinate"),
                                                        dcc.Input(id="primary_source_x_coordinate", type="number", min=0, step=0.001, debounce=True),
                                                        html.Label("Y (mm): ", htmlFor="primary_source_y_coordinate"),
                                                        dcc.Input(id="primary_source_y_coordinate", type="number", min=0, step=0.001, debounce=True),
                                                        html.Label("Z (mm): ", htmlFor="primary_source_z_coordinate"),
                                                        dcc.Input(id="primary_source_z_coordinate", type="number", min=0, step=0.001, debounce=True),
                                                        dcc.ConfirmDialog(id="primary_source_coordinates_overlap", message="Primary source can't overlap with another source")
                                                    ]),
                                            html.Div(id="secondary_source_position_parameters", style={"display":"none"},
                                                    children=[                                            
                                                        html.Label("Secondary source: ", htmlFor="secondary_source"),
                                                        html.Br(),
                                                        html.Label("X (mm): ", htmlFor="secondary_source_x_coordinate"),
                                                        dcc.Input(id="secondary_source_x_coordinate", type="number", min=0, step=0.001, debounce=True),
                                                        html.Label("Y (mm): ", htmlFor="secondary_source_y_coordinate"),
                                                        dcc.Input(id="secondary_source_y_coordinate", type="number", min=0, step=0.001, debounce=True),
                                                        html.Label("Z (mm): ", htmlFor="secondary_source_z_coordinate"),
                                                        dcc.Input(id="secondary_source_z_coordinate", type="number", min=0, step=0.001, debounce=True),
                                                        dcc.ConfirmDialog(id="secondary_source_coordinates_overlap", message="Secondary source can't overlap with another source")
                                                    ]),
                                            html.Div(id="third_source_position_parameters", style={"display":"none"},
                                                    children=[                                            
                                                        html.Label("Third source: ", htmlFor="third_source"),
                                                        html.Br(),
                                                        html.Label("X (mm): ", htmlFor="third_source_x_coordinate"),
                                                        dcc.Input(id="third_source_x_coordinate", type="number", min=0, step=0.001, debounce=True),
                                                        html.Label("Y (mm): ", htmlFor="third_source_y_coordinate"),
                                                        dcc.Input(id="third_source_y_coordinate", type="number", min=0, step=0.001, debounce=True),
                                                        html.Label("Z (mm): ", htmlFor="third_source_z_coordinate"),
                                                        dcc.Input(id="third_source_z_coordinate", type="number", min=0, step=0.001, debounce=True),
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
    """
    Calculating size of ROI
    """
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
    """
    Reading tissue parameters form tissues.json
    """
    wave_param = tissues[tissue]["Optical parameters"]["Wave length"]
    native = list(tissues[tissue]["Optical parameters"]["Native"].values())
    coagulated = list(tissues[tissue]["Optical parameters"]["Coagulated"].values())
    thermal = list(tissues[tissue]["Thermal parameters"].values())
    damage = list(tissues[tissue]["Damage parameters"].values())
    return wave_param,native,coagulated,thermal,damage

#Source Callbacks
@callback(
    output = dict(sources_coordinates_output=Output("sources_coordinates_list","data"),sources_display_output=Output("sources_display_list","data"),
                    x1_out=Output("primary_source_x_coordinate", "value"), y1_out=Output("primary_source_y_coordinate", "value"), z1_out=Output("primary_source_z_coordinate", "value"),
                    x2_out=Output("secondary_source_x_coordinate", "value"), y2_out=Output("secondary_source_y_coordinate", "value"), z2_out=Output("secondary_source_z_coordinate", "value"),
                    x3_out=Output("third_source_x_coordinate", "value"), y3_out=Output("third_source_y_coordinate", "value"), z3_out=Output("third_source_z_coordinate", "value"),
                    warning1=Output("primary_source_coordinates_overlap", "displayed"),warning2=Output("secondary_source_coordinates_overlap", "displayed"),warning3=Output("third_source_coordinates_overlap", "displayed"),
                    new_warning=Output("position_error_message", "displayed")),
    inputs = dict(sources_coordinates_input=Input("sources_coordinates_list","data"),sources_display_input=Input("sources_display_list","data"),
                    x1_in=Input("primary_source_x_coordinate", "value"), y1_in=Input("primary_source_y_coordinate", "value"), z1_in=Input("primary_source_z_coordinate", "value"),
                    x2_in=Input("secondary_source_x_coordinate", "value"), y2_in=Input("secondary_source_y_coordinate", "value"), z2_in=Input("secondary_source_z_coordinate", "value"),
                    x3_in=Input("third_source_x_coordinate", "value"), y3_in=Input("third_source_y_coordinate", "value"), z3_in=Input("third_source_z_coordinate", "value"),
                    new_x = Input("add_source_x_coordinate", "value"), new_y = Input("add_source_y_coordinate", "value"), new_z = Input("add_source_z_coordinate", "value"),
                    add_source = Input("add_source","n_clicks"), remove_source = Input("remove_source", "n_clicks"))
)
def update_source_postions(sources_coordinates_input,sources_display_input,x1_in,y1_in,z1_in,x2_in,y2_in,z2_in,x3_in,y3_in,z3_in,new_x,new_y,new_z,add_source,remove_source):
    """
    Function to adding, removing and changing postions of sources
    """
    add_source_coordinates = [new_x,new_y,new_z]
    sources_coordinates = sources_coordinates_input
    sources_display = sources_display_input
    
    if ctx.triggered_id == "add_source": #Checking if add source button is clicked
        if not add_source_coordinates in sources_coordinates: #Check if new source positiond isn't overlapping with already existing sources
            sources_coordinates.append(add_source_coordinates)
        else:
            #Return warning if postions are overlapping
            return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display, 
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=True)
    if ctx.triggered_id == "remove_source":#Check if remove last source button is clicked. If yes remove last value form source coordinates
        sources_coordinates.pop()
        #Start of changing display values
        for i in range(3):
            sources_display[i]={"display":"none"}
    for i in range(len(sources_coordinates)): #This probably can be improved !!!
        sources_display[i] = {"display":"block"}
    #End of changing display values
    if ctx.triggered_id == "add_source" and len(sources_coordinates)==1: #If we are adding first source
        x1, y1, z1 = new_x, new_y, new_z
        #Update first source's position
        return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1, y1_out=y1, z1_out=z1,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
    elif ctx.triggered_id == "add_source" and len(sources_coordinates)==2: #If we are adding second source
        x2, y2, z2 = new_x, new_y, new_z
        #Update second source's position
        return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=x2, y2_out=y2, z2_out=z2,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
    elif ctx.triggered_id == "add_source" and len(sources_coordinates)==3: #If we are adding third source
        x3, y3, z3 = new_x, new_y, new_z
        #Update third source's postion
        return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3, y3_out=y3, z3_out=z3,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
    #Changing first source's postion
    if ctx.triggered_id=="primary_source_x_coordinate" or ctx.triggered_id=="primary_source_y_coordinate"  or ctx.triggered_id=="primary_source_z_coordinate" :#If we change first source's position
        x,y,z = x1_in, y1_in, z1_in
        if len(sources_coordinates)==3:
            #Checking if changed position isn't overlapping with already existing ones    
            if [x,y,z] in sources_coordinates[1:2]:
                #Prevent change and raise warning about overlapping positions
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=sources_coordinates[0][0], y1_out=sources_coordinates[0][1], z1_out=sources_coordinates[0][2],
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=True,warning2=False,warning3=False,
                    new_warning=False)
            else:
                #If positions aren't overlapping, change the position of first source
                sources_coordinates[0] = [x,y,z]
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x, y1_out=y, z1_out=z,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
        elif len(sources_coordinates)==2:
            print("len2")
            print([x,y,z], sources_coordinates[1])
            #Checking if changed position isn't overlapping with already existing ones    
            if [x,y,z] == sources_coordinates[1]:
                print("1 as 2")
                #Prevent change and raise warning about overlapping positions
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=sources_coordinates[0][0], y1_out=sources_coordinates[0][1], z1_out=sources_coordinates[0][2],
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=True,warning2=False,warning3=False,
                    new_warning=False)
            else:
                #If positions aren't overlapping, change the position of first source
                sources_coordinates[0] = [x,y,z]
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x, y1_out=y, z1_out=z,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
        elif len(sources_coordinates)==1:
            #There's only one source so we can change the postion
            sources_coordinates[0] = [x,y,z]
            return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x, y1_out=y, z1_out=z,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
        else:
            #Prevent auto update when we don't have any sources
            raise PreventUpdate
    #Changing second source's postion
    if ctx.triggered_id=="secondary_source_x_coordinate" or ctx.triggered_id=="secondary_source_y_coordinate"  or ctx.triggered_id=="secondary_source_z_coordinate":
        x,y,z = x2_in, y2_in, z2_in
        if len(sources_coordinates)==3:
            #Checking if changed position isn't overlapping with already existing ones    
            if [x,y,z] in [sources_coordinates[0],sources_coordinates[2]]:
                #Prevent change and raise warning about overlapping positions
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=sources_coordinates[1][0], y2_out=sources_coordinates[1][1], z2_out=sources_coordinates[1][2],
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=True,warning3=False,
                    new_warning=False)
            else:
                #If positions aren't overlapping, change the position of second source
                sources_coordinates[1] = [x,y,z]
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=x, y2_out=y, z2_out=z,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
        elif len(sources_coordinates)==2:
            #Checking if changed position isn't overlapping with already existing ones
            if [x,y,z] == sources_coordinates[0]:
                #Prevent change and raise warning about overlapping positions
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=sources_coordinates[1][0], y2_out=sources_coordinates[1][1], z2_out=sources_coordinates[1][2],
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=True,warning3=False,
                    new_warning=False)
            else:
                #If positions aren't overlapping, change the position of second source
                sources_coordinates[1] = [x,y,z]
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=x, y2_out=y, z2_out=z,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
        else:
            #Prevent auto update when we don't have any sources
            raise PreventUpdate
    #Changing third source's postion
    if ctx.triggered_id=="third_source_x_coordinate" or ctx.triggered_id=="third_source_y_coordinate"  or ctx.triggered_id=="third_source_z_coordinate":
        x,y,z = x3_in, y3_in, z3_in
        if len(sources_coordinates)==3:   
            #Checking if changed position isn't overlapping with already existing ones 
            if [x,y,z] in [sources_coordinates[0],sources_coordinates[1]]:
                #Prevent change and raise warning about overlapping positions
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=sources_coordinates[2][0], y3_out=sources_coordinates[2][1], z3_out=sources_coordinates[2][2],
                    warning1=False,warning2=False,warning3=True,
                    new_warning=False)
            else:
                #If positions aren't overlapping, change the position of third source
                sources_coordinates[2] = [x,y,z]
                return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x, y3_out=y, z3_out=z,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
        else:
            #Prevent auto update when we don't have any sources
            raise PreventUpdate
    #Preserving postions when we refresh app
    if len(sources_coordinates) == 0:
        return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1_in, y1_out=y1_in, z1_out=z1_in,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
    if len(sources_coordinates)==1:
        x1 ,y1, z1 = sources_coordinates[0]
        return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1, y1_out=y1, z1_out=z1,
                    x2_out=x2_in, y2_out=y2_in, z2_out=z2_in,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
    if len(sources_coordinates)==2:
        x1 ,y1, z1 = sources_coordinates[0]
        x2 ,y2, z2 = sources_coordinates[1]
        return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1, y1_out=y1, z1_out=z1,
                    x2_out=x2, y2_out=y2, z2_out=z2,
                    x3_out=x3_in, y3_out=y3_in, z3_out=z3_in,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
    if len(sources_coordinates)==3:
        x1 ,y1, z1 = sources_coordinates[0]
        x2 ,y2, z2 = sources_coordinates[1]
        x3 ,y3, z3 = sources_coordinates[2]
        return dict(sources_coordinates_output=sources_coordinates,sources_display_output=sources_display,
                    x1_out=x1, y1_out=y1, z1_out=z1,
                    x2_out=x2, y2_out=y2, z2_out=z2,
                    x3_out=x3, y3_out=y3, z3_out=z3,
                    warning1=False,warning2=False,warning3=False,
                    new_warning=False)
    
    raise PreventUpdate #Just in case if we get here, to prevent rasing errror

@callback(
    [Output("primary_source_position_parameters", "style"),Output("secondary_source_position_parameters", "style"),Output("third_source_position_parameters", "style")],
    Input("sources_display_list","data"),
)
def update_sources_display(sources_display_list):
    """
    Updating sources display 
    """
    return sources_display_list

@callback(
    Output("add_source", "disabled"),
    Output("remove_source", "disabled"),
    Input("sources_coordinates_list", "data"),
    Input("add_source", "n_clicks"),
    Input("remove_source", "n_clicks")
)
def disable_source_buttons(sources_coordinates_list,add_source, remove_source):

    if len(sources_coordinates_list) == 0:#Disable remove button, because we don't have any sources
        return False, True
    
    if len(sources_coordinates_list) < 3 and len(sources_coordinates_list)>0:#You can add and remove sources. At least one source, but below limit
        return False, False
    
    if len(sources_coordinates_list) >= 3:#Disable adding button, because we have reached the limit
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
    """
    Updating maximum value of source postion, so it's in the ROI
    """
    return 4*[dim_x, dim_y, dim_z]

if __name__ == '__main__':
    app.run(debug=True)
    