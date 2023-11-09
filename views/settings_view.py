from dash import html, dcc, ctx, callback, Input, Output
import json

from models.ROIModel import ROIModel
from models.TissueModel import TissueModel
from views.utils import validate_input, format_bytes_number, get_tissues_names, get_tissue_by_name

with open("assets/default-settings.json") as default_setting_json:
    default_setting = json.load(default_setting_json)

with open("assets/tissues.json") as tissues_json:
    tissues = json.load(tissues_json)

tissue_ranges = default_setting["tissue"]["ranges"]
tissue_model = TissueModel(**default_setting["tissue"]["values"])

roi_ranges = default_setting["roi"]["ranges"]
roi_model = ROIModel(**default_setting["roi"]["values"])


def create_setting_view():
    return dcc.Tab(id="settings", label="Settings",
                   children=[dcc.Tabs(id="settings_tabs", children=[create_tissue_settings(),
                                                                    create_roi_settings(),
                                                                    create_laser_settings()]
                                      )
                             ]
                   )


def create_tissue_settings():
    return dcc.Tab(
        id="tissue_settings",
        label="Tissue",
        children=[
            dcc.Dropdown(get_tissues_names(tissues), id="tissue_select", value=tissue_model.name),
            html.Div(id="selected"),
            html.Label("Optical parameters: ", htmlFor="optical_parameters"),
            html.Div(id="optical_parameters",
                     children=[
                         html.Label("Wave length: ", htmlFor="wave_length"),
                         dcc.Input(id="wave_length", type="number", debounce=True,
                                   min=tissue_ranges["wave_length"]["min"],
                                   max=tissue_ranges["wave_length"]["max"],
                                   step=tissue_ranges["wave_length"]["step"],
                                   value=tissue_model.wave_length),
                         html.Label(" nm", htmlFor="wave_length"),
                         html.Br(),
                         html.Label("Native: ", htmlFor="native"),
                         html.Div(id="native",
                                  children=[
                                      html.Label("Refractive index: ", htmlFor="native_refractive_index"),
                                      dcc.Input(id="native_refractive_index", type="number", debounce=True,
                                                min=tissue_ranges["native_refractive_index"]["min"],
                                                max=tissue_ranges["native_refractive_index"]["max"],
                                                step=tissue_ranges["native_refractive_index"]["step"],
                                                value=tissue_model.native_refractive_index),
                                      html.Label("Absorption: ", htmlFor="native_absorption"),
                                      dcc.Input(id="native_absorption", type="number", debounce=True,
                                                min=tissue_ranges["native_absorption"]["min"],
                                                max=tissue_ranges["native_absorption"]["max"],
                                                step=tissue_ranges["native_absorption"]["step"],
                                                value=tissue_model.native_absorption),
                                      html.Label(" 1/mm", htmlFor="native_absorption"),
                                      html.Label("Scattering: ", htmlFor="native_scattering"),
                                      dcc.Input(id="native_scattering", type="number", debounce=True,
                                                min=tissue_ranges["native_scattering"]["min"],
                                                max=tissue_ranges["native_scattering"]["max"],
                                                step=tissue_ranges["native_scattering"]["step"],
                                                value=tissue_model.native_scattering),
                                      html.Label(" 1/mm", htmlFor="native_scattering"),
                                      html.Label("G-factor: ", htmlFor="native_g_factor"),
                                      dcc.Input(id="native_g_factor", type="number", debounce=True,
                                                min=tissue_ranges["native_g_factor"]["min"],
                                                max=tissue_ranges["native_g_factor"]["max"],
                                                step=tissue_ranges["native_g_factor"]["step"],
                                                value=tissue_model.native_g_factor),
                                  ]),
                         html.Label("Coagulated: ", htmlFor="coagulated"),
                         html.Div(id="coagulated",
                                  children=[
                                      html.Label("Refractive index: ", htmlFor="coagulated_refractive_index"),
                                      dcc.Input(id="coagulated_refractive_index", type="number", debounce=True,
                                                min=tissue_ranges["coagulated_refractive_index"]["min"],
                                                max=tissue_ranges["coagulated_refractive_index"]["max"],
                                                step=tissue_ranges["coagulated_refractive_index"]["step"],
                                                value=tissue_model.coagulated_refractive_index),
                                      html.Label("Absorption: ", htmlFor="coagulated_absorption"),
                                      dcc.Input(id="coagulated_absorption", type="number", debounce=True,
                                                min=tissue_ranges["coagulated_absorption"]["min"],
                                                max=tissue_ranges["coagulated_absorption"]["max"],
                                                step=tissue_ranges["coagulated_absorption"]["step"],
                                                value=tissue_model.coagulated_absorption),
                                      html.Label(" 1/mm", htmlFor="coagulated_absorption"),
                                      html.Label("Scattering: ", htmlFor="coagulated_scattering"),
                                      dcc.Input(id="coagulated_scattering", type="number", debounce=True,
                                                min=tissue_ranges["coagulated_scattering"]["min"],
                                                max=tissue_ranges["coagulated_scattering"]["max"],
                                                step=tissue_ranges["coagulated_scattering"]["step"],
                                                value=tissue_model.coagulated_scattering),
                                      html.Label(" 1/mm", htmlFor="coagulated_scattering"),
                                      html.Label("G-factor: ", htmlFor="coagulated_g_factor"),
                                      dcc.Input(id="coagulated_g_factor", type="number", debounce=True,
                                                min=tissue_ranges["coagulated_g_factor"]["min"],
                                                max=tissue_ranges["coagulated_g_factor"]["max"],
                                                step=tissue_ranges["coagulated_g_factor"]["step"],
                                                value=tissue_model.coagulated_g_factor),
                                  ]),
                     ]),
            html.Br(),
            html.Label("Thermal parameters: ", htmlFor="thermal_parameters"),
            html.Div(id="thermal_parameters",
                     children=[
                         html.Label("Initial temperature: ", htmlFor="initial_temperature"),
                         dcc.Input(id="initial_temperature", type="number", debounce=True,
                                   min=tissue_ranges["initial_temperature"]["min"],
                                   max=tissue_ranges["initial_temperature"]["max"],
                                   step=tissue_ranges["initial_temperature"]["step"],
                                   value=tissue_model.initial_temperature),
                         html.Label(" ^C", htmlFor="initial_temperature"),
                         html.Label("Blood perfusion: ", htmlFor="blood_perfusion"),
                         dcc.Input(id="blood_perfusion", type="number", debounce=True,
                                   min=tissue_ranges["blood_perfusion"]["min"],
                                   max=tissue_ranges["blood_perfusion"]["max"],
                                   step=tissue_ranges["blood_perfusion"]["step"],
                                   value=tissue_model.blood_perfusion),
                         html.Label(" ml/(g min)", htmlFor="blood_perfusion"),
                         html.Label("Water content: ", htmlFor="water_content"),
                         dcc.Input(id="water_content", type="number", debounce=True,
                                   min=tissue_ranges["water_content"]["min"],
                                   max=tissue_ranges["water_content"]["max"],
                                   step=tissue_ranges["water_content"]["step"],
                                   value=tissue_model.water_content),
                         html.Label(" %", htmlFor="water_content"),
                         html.Label("Heat conductivity: ", htmlFor="heat_conductivity"),
                         dcc.Input(id="heat_conductivity", type="number", debounce=True,
                                   min=tissue_ranges["heat_conductivity"]["min"],
                                   max=tissue_ranges["heat_conductivity"]["max"],
                                   step=tissue_ranges["heat_conductivity"]["step"],
                                   value=tissue_model.heat_conductivity),
                         html.Label(" W/(cm K)", htmlFor="heat_conductivity"),
                         html.Label("Heat capacity: ", htmlFor="heat_capacity"),
                         dcc.Input(id="heat_capacity", type="number", debounce=True,
                                   min=tissue_ranges["heat_capacity"]["min"],
                                   max=tissue_ranges["heat_capacity"]["max"],
                                   step=tissue_ranges["heat_capacity"]["step"],
                                   value=tissue_model.heat_capacity),
                         html.Label(" J/(g K)", htmlFor="heat_capacity"),
                         html.Label("Density: ", htmlFor="density"),
                         dcc.Input(id="density", type="number", debounce=True,
                                   min=tissue_ranges["density"]["min"],
                                   max=tissue_ranges["density"]["max"],
                                   step=tissue_ranges["density"]["step"],
                                   value=tissue_model.density),
                         html.Label(" g/cm^3", htmlFor="density"),
                     ]),
            html.Br(),
            html.Label("Damage parameters: ", htmlFor="damage_parameters"),
            html.Div(id="damage_parameters",
                     children=[
                         html.Label("Damage threshold: ", htmlFor="damage_threshold"),
                         dcc.Input(id="damage_threshold", type="number", debounce=True,
                                   min=tissue_ranges["damage_threshold"]["min"],
                                   max=tissue_ranges["damage_threshold"]["max"],
                                   step=tissue_ranges["damage_threshold"]["step"],
                                   value=tissue_model.damage_threshold),
                         html.Label("Activation energy: ", htmlFor="activation_energy"),
                         dcc.Input(id="activation_energy", type="number", debounce=True,
                                   min=tissue_ranges["activation_energy"]["min"],
                                   max=tissue_ranges["activation_energy"]["max"],
                                   step=tissue_ranges["activation_energy"]["step"],
                                   value=tissue_model.activation_energy),
                         html.Label(" J/mol", htmlFor="activation_energy"),
                         html.Label("Rate parameter: ", htmlFor="rate_parameter"),
                         dcc.Input(id="rate_parameter", type="number", debounce=True,
                                   min=tissue_ranges["rate_parameter"]["min"],
                                   max=tissue_ranges["rate_parameter"]["max"],
                                   step=tissue_ranges["rate_parameter"]["step"],
                                   value=tissue_model.rate_parameter),
                         html.Label(" 1/s", htmlFor="rate_parameter"),
                     ])
        ]
    )


@callback(
    Output("wave_length", "value"),
    Output("native_refractive_index", "value"),
    Output("native_absorption", "value"),
    Output("native_scattering", "value"),
    Output("native_g_factor", "value"),
    Output("coagulated_refractive_index", "value"),
    Output("coagulated_absorption", "value"),
    Output("coagulated_scattering", "value"),
    Output("coagulated_g_factor", "value"),
    Output("initial_temperature", "value"),
    Output("blood_perfusion", "value"),
    Output("water_content", "value"),
    Output("heat_conductivity", "value"),
    Output("heat_capacity", "value"),
    Output("density", "value"),
    Output("damage_threshold", "value"),
    Output("activation_energy", "value"),
    Output("rate_parameter", "value"),
    Input("tissue_select", "value"),
    Input("wave_length", "value"),
    Input("native_refractive_index", "value"),
    Input("native_absorption", "value"),
    Input("native_scattering", "value"),
    Input("native_g_factor", "value"),
    Input("coagulated_refractive_index", "value"),
    Input("coagulated_absorption", "value"),
    Input("coagulated_scattering", "value"),
    Input("coagulated_g_factor", "value"),
    Input("initial_temperature", "value"),
    Input("blood_perfusion", "value"),
    Input("water_content", "value"),
    Input("heat_conductivity", "value"),
    Input("heat_capacity", "value"),
    Input("density", "value"),
    Input("damage_threshold", "value"),
    Input("activation_energy", "value"),
    Input("rate_parameter", "value")
)
def tissue_settings_callback(tissue_name, wave_length, native_refractive_index, native_absorption,
                             native_scattering, native_g_factor, coagulated_refractive_index,
                             coagulated_absorption, coagulated_scattering, coagulated_g_factor, initial_temperature,
                             blood_perfusion, water_content, heat_conductivity, heat_capacity, density,
                             damage_threshold, activation_energy, rate_parameter):
    global tissue_model

    if ctx.triggered_id == "tissue_select":
        if tissue_name is not None:
            tissue = get_tissue_by_name(tissues, tissue_name)
            tissue_model = TissueModel(**tissue)
    else:
        if validate_input(wave_length, tissue_ranges["wave_length"]):
            tissue_model.wave_length = wave_length

        if validate_input(native_refractive_index, tissue_ranges["native_refractive_index"]):
            tissue_model.native_refractive_index = native_refractive_index

        if validate_input(native_absorption, tissue_ranges["native_absorption"]):
            tissue_model.native_absorption = native_absorption

        if validate_input(native_scattering, tissue_ranges["native_scattering"]):
            tissue_model.native_scattering = native_scattering

        if validate_input(native_g_factor, tissue_ranges["native_g_factor"]):
            tissue_model.native_g_factor = native_g_factor

        if validate_input(coagulated_refractive_index, tissue_ranges["coagulated_refractive_index"]):
            tissue_model.coagulated_refractive_index = coagulated_refractive_index

        if validate_input(coagulated_absorption, tissue_ranges["coagulated_absorption"]):
            tissue_model.coagulated_absorption = coagulated_absorption

        if validate_input(coagulated_scattering, tissue_ranges["coagulated_scattering"]):
            tissue_model.coagulated_scattering = coagulated_scattering

        if validate_input(coagulated_g_factor, tissue_ranges["coagulated_g_factor"]):
            tissue_model.coagulated_g_factor = coagulated_g_factor

        if validate_input(initial_temperature, tissue_ranges["initial_temperature"]):
            tissue_model.initial_temperature = initial_temperature

        if validate_input(blood_perfusion, tissue_ranges["blood_perfusion"]):
            tissue_model.blood_perfusion = blood_perfusion

        if validate_input(water_content, tissue_ranges["water_content"]):
            tissue_model.water_content = water_content

        if validate_input(heat_conductivity, tissue_ranges["heat_conductivity"]):
            tissue_model.heat_conductivity = heat_conductivity

        if validate_input(heat_capacity, tissue_ranges["heat_capacity"]):
            tissue_model.heat_capacity = heat_capacity

        if validate_input(density, tissue_ranges["density"]):
            tissue_model.density = density

        if validate_input(damage_threshold, tissue_ranges["damage_threshold"]):
            tissue_model.damage_threshold = damage_threshold

        if validate_input(activation_energy, tissue_ranges["activation_energy"]):
            tissue_model.activation_energy = activation_energy

        if validate_input(rate_parameter, tissue_ranges["rate_parameter"]):
            tissue_model.rate_parameter = rate_parameter

    return tissue_model.wave_length, tissue_model.native_refractive_index, tissue_model.native_absorption, \
        tissue_model.native_scattering, tissue_model.native_g_factor, tissue_model.coagulated_refractive_index, \
        tissue_model.coagulated_absorption, tissue_model.coagulated_scattering, tissue_model.coagulated_g_factor, \
        tissue_model.initial_temperature, tissue_model.blood_perfusion, tissue_model.water_content, \
        tissue_model.heat_conductivity, tissue_model.heat_capacity, tissue_model.density, \
        tissue_model.damage_threshold, tissue_model.activation_energy, tissue_model.rate_parameter


def create_roi_settings() -> object:
    return dcc.Tab(
        id="roi_settings",
        label="Region of Interest",
        children=[
            html.Label("Voxel dimension: ", htmlFor="voxel_dimension_input"),
            dcc.Input(id="voxel_dimension_input", type="number", debounce=True,
                      min=roi_ranges["voxel_dimension"]["min"],
                      max=roi_ranges["voxel_dimension"]["max"],
                      step=roi_ranges["voxel_dimension"]["step"],
                      value=roi_model.voxel_dimension),
            html.Label(" mm: ", htmlFor="voxel_dimension_input"),
            html.Br(),
            html.Div(id="no_of_voxels",
                     children=[
                         html.Label("No. of voxels in X-direction: ", htmlFor="no_of_voxels_in_x_direction"),
                         dcc.Input(id="no_of_voxels_in_x_direction", type="number", debounce=True,
                                   min=roi_ranges["no_of_voxels_in_x_direction"]["min"],
                                   max=roi_ranges["no_of_voxels_in_x_direction"]["max"],
                                   step=roi_ranges["no_of_voxels_in_x_direction"]["step"],
                                   value=roi_model.no_of_voxels_in_x_direction),
                         html.Label("No. of voxels in Y-direction: ", htmlFor="no_of_voxels_in_y_direction"),
                         dcc.Input(id="no_of_voxels_in_y_direction", type="number", debounce=True,
                                   min=roi_ranges["no_of_voxels_in_y_direction"]["min"],
                                   max=roi_ranges["no_of_voxels_in_y_direction"]["max"],
                                   step=roi_ranges["no_of_voxels_in_y_direction"]["step"],
                                   value=roi_model.no_of_voxels_in_y_direction),
                         html.Label("No. of voxels in Z-direction: ", htmlFor="no_of_voxels_in_z_direction"),
                         dcc.Input(id="no_of_voxels_in_z_direction", type="number", debounce=True,
                                   min=roi_ranges["no_of_voxels_in_z_direction"]["min"],
                                   max=roi_ranges["no_of_voxels_in_z_direction"]["max"],
                                   step=roi_ranges["no_of_voxels_in_z_direction"]["step"],
                                   value=roi_model.no_of_voxels_in_z_direction)
                     ]),
            html.Label("Calculated dimensions of ROI", htmlFor="dim_of_roi"),
            html.Div(id="dim_of_roi",
                     children=[
                         html.Label("X: ", htmlFor="dimension_x"),
                         dcc.Input(id="dimension_x", value=roi_model.get_dimension()[0], disabled=True),
                         html.Label("Y: ", htmlFor="dimension_y"),
                         dcc.Input(id="dimension_y", value=roi_model.get_dimension()[1], disabled=True),
                         html.Label("Z:", htmlFor="dimension_z"),
                         dcc.Input(id="dimension_z", value=roi_model.get_dimension()[2], disabled=True)
                     ]),
            html.Br(),
            html.Label("Memory requirements", htmlFor="memory_requirements"),
            html.Div(id="memory_requirements",
                     children=[
                         html.Label("Size of voxel: ", htmlFor="voxel_size"),
                         dcc.Input(id="voxel_size", value=96, disabled=True),
                         html.Label(" bytes", htmlFor="voxel_size"),
                         html.Label("Number of voxels: ", htmlFor="voxels_number"),
                         dcc.Input(id="voxels_number", value=roi_model.get_voxels_number(), disabled=True),
                         html.Label("Total memory required: ", htmlFor="required_memory"),
                         dcc.Input(id="required_memory", value=roi_model.get_required_memory(96), disabled=True)
                     ])
        ]
    )


@callback(
    Output("dimension_x", "value"),
    Output("dimension_y", "value"),
    Output("dimension_z", "value"),
    Output("voxel_size", "value"),
    Output("voxels_number", "value"),
    Output("required_memory", "value"),
    Output("voxel_dimension_input", "value"),
    Output("no_of_voxels_in_x_direction", "value"),
    Output("no_of_voxels_in_y_direction", "value"),
    Output("no_of_voxels_in_z_direction", "value"),
    Input("voxel_dimension_input", "value"),
    Input("no_of_voxels_in_x_direction", "value"),
    Input("no_of_voxels_in_y_direction", "value"),
    Input("no_of_voxels_in_z_direction", "value"),
)
def roi_settings_callback(voxel_dim, no_of_voxels_in_x_dir, no_of_voxels_in_y_dir, no_of_voxels_in_z_dir):
    global roi_model

    if validate_input(voxel_dim, roi_ranges["voxel_dimension"]):
        roi_model.voxel_dimension = float(voxel_dim)

    if validate_input(no_of_voxels_in_x_dir, roi_ranges["no_of_voxels_in_x_direction"]):
        roi_model.no_of_voxels_in_x_direction = int(no_of_voxels_in_x_dir)

    if validate_input(no_of_voxels_in_y_dir, roi_ranges["no_of_voxels_in_y_direction"]):
        roi_model.no_of_voxels_in_y_direction = int(no_of_voxels_in_y_dir)

    if validate_input(no_of_voxels_in_z_dir, roi_ranges["no_of_voxels_in_z_direction"]):
        roi_model.no_of_voxels_in_z_direction = int(no_of_voxels_in_z_dir)

    return *roi_model.get_dimension(), 96, roi_model.get_voxels_number(), format_bytes_number(
        roi_model.get_required_memory(96)), roi_model.voxel_dimension, roi_model.no_of_voxels_in_x_direction, \
        roi_model.no_of_voxels_in_y_direction, roi_model.no_of_voxels_in_z_direction


def create_laser_settings():
    return dcc.Tab(
        id="laser_settings",
        label="Laser"
    )
