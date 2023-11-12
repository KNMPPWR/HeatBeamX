from dash import html, dcc, callback, ctx, Input, Output, State, ALL, MATCH
from typing import List, Tuple
import json
import numpy as np

from app import app
from models.AppDataModel import AppDataModel, TissueModel, LaserModel, LaserApplicatorType, UINT, FLOAT


def create_setting_view(app_model: AppDataModel) -> object:
    return dcc.Tab(id="settings", label="Settings",
                   children=[dcc.Tabs(id="settings_tabs", children=[create_tissue_settings(app_model),
                                                                    create_roi_settings(app_model),
                                                                    create_laser_settings(app_model)]
                                      )
                             ]
                   )


def create_tissue_settings(app_model: AppDataModel) -> object:
    return dcc.Tab(
        id="tissue_settings",
        label="Tissue",
        children=[
            dcc.Dropdown(list([app_model.builtin_tissues[tissue]["name"] for tissue in app_model.builtin_tissues]),
                         id="tissue_select", value=app_model.tissue.name),
            html.Div(id="selected"),
            html.Label("Optical parameters: ", htmlFor="optical_parameters"),
            html.Div(id="optical_parameters",
                     children=[
                         html.Label("Wave length: ", htmlFor="wave_length"),
                         dcc.Input(id="wave_length", type="number", debounce=True,
                                   min=app_model.tissue_ranges["wave_length"]["min"],
                                   max=app_model.tissue_ranges["wave_length"]["max"],
                                   step=app_model.tissue_ranges["wave_length"]["step"],
                                   value=app_model.tissue.wave_length),
                         html.Label(" nm", htmlFor="wave_length"),
                         html.Br(),
                         html.Label("Native: ", htmlFor="native"),
                         html.Div(id="native",
                                  children=[
                                      html.Label("Refractive index: ", htmlFor="native_refractive_index"),
                                      dcc.Input(id="native_refractive_index", type="number", debounce=True,
                                                min=app_model.tissue_ranges["native_refractive_index"]["min"],
                                                max=app_model.tissue_ranges["native_refractive_index"]["max"],
                                                step=app_model.tissue_ranges["native_refractive_index"]["step"],
                                                value=app_model.tissue.native_refractive_index),
                                      html.Label("Absorption: ", htmlFor="native_absorption"),
                                      dcc.Input(id="native_absorption", type="number", debounce=True,
                                                min=app_model.tissue_ranges["native_absorption"]["min"],
                                                max=app_model.tissue_ranges["native_absorption"]["max"],
                                                step=app_model.tissue_ranges["native_absorption"]["step"],
                                                value=app_model.tissue.native_absorption),
                                      html.Label(" 1/mm", htmlFor="native_absorption"),
                                      html.Label("Scattering: ", htmlFor="native_scattering"),
                                      dcc.Input(id="native_scattering", type="number", debounce=True,
                                                min=app_model.tissue_ranges["native_scattering"]["min"],
                                                max=app_model.tissue_ranges["native_scattering"]["max"],
                                                step=app_model.tissue_ranges["native_scattering"]["step"],
                                                value=app_model.tissue.native_scattering),
                                      html.Label(" 1/mm", htmlFor="native_scattering"),
                                      html.Label("G-factor: ", htmlFor="native_g_factor"),
                                      dcc.Input(id="native_g_factor", type="number", debounce=True,
                                                min=app_model.tissue_ranges["native_g_factor"]["min"],
                                                max=app_model.tissue_ranges["native_g_factor"]["max"],
                                                step=app_model.tissue_ranges["native_g_factor"]["step"],
                                                value=app_model.tissue.native_g_factor),
                                  ]),
                         html.Label("Coagulated: ", htmlFor="coagulated"),
                         html.Div(id="coagulated",
                                  children=[
                                      html.Label("Refractive index: ", htmlFor="coagulated_refractive_index"),
                                      dcc.Input(id="coagulated_refractive_index", type="number", debounce=True,
                                                min=app_model.tissue_ranges["coagulated_refractive_index"]["min"],
                                                max=app_model.tissue_ranges["coagulated_refractive_index"]["max"],
                                                step=app_model.tissue_ranges["coagulated_refractive_index"]["step"],
                                                value=app_model.tissue.coagulated_refractive_index),
                                      html.Label("Absorption: ", htmlFor="coagulated_absorption"),
                                      dcc.Input(id="coagulated_absorption", type="number", debounce=True,
                                                min=app_model.tissue_ranges["coagulated_absorption"]["min"],
                                                max=app_model.tissue_ranges["coagulated_absorption"]["max"],
                                                step=app_model.tissue_ranges["coagulated_absorption"]["step"],
                                                value=app_model.tissue.coagulated_absorption),
                                      html.Label(" 1/mm", htmlFor="coagulated_absorption"),
                                      html.Label("Scattering: ", htmlFor="coagulated_scattering"),
                                      dcc.Input(id="coagulated_scattering", type="number", debounce=True,
                                                min=app_model.tissue_ranges["coagulated_scattering"]["min"],
                                                max=app_model.tissue_ranges["coagulated_scattering"]["max"],
                                                step=app_model.tissue_ranges["coagulated_scattering"]["step"],
                                                value=app_model.tissue.coagulated_scattering),
                                      html.Label(" 1/mm", htmlFor="coagulated_scattering"),
                                      html.Label("G-factor: ", htmlFor="coagulated_g_factor"),
                                      dcc.Input(id="coagulated_g_factor", type="number", debounce=True,
                                                min=app_model.tissue_ranges["coagulated_g_factor"]["min"],
                                                max=app_model.tissue_ranges["coagulated_g_factor"]["max"],
                                                step=app_model.tissue_ranges["coagulated_g_factor"]["step"],
                                                value=app_model.tissue.coagulated_g_factor),
                                  ]),
                     ]),
            html.Br(),
            html.Label("Thermal parameters: ", htmlFor="thermal_parameters"),
            html.Div(id="thermal_parameters",
                     children=[
                         html.Label("Initial temperature: ", htmlFor="initial_temperature"),
                         dcc.Input(id="initial_temperature", type="number", debounce=True,
                                   min=app_model.tissue_ranges["initial_temperature"]["min"],
                                   max=app_model.tissue_ranges["initial_temperature"]["max"],
                                   step=app_model.tissue_ranges["initial_temperature"]["step"],
                                   value=app_model.tissue.initial_temperature),
                         html.Label(" ^C", htmlFor="initial_temperature"),
                         html.Label("Blood perfusion: ", htmlFor="blood_perfusion"),
                         dcc.Input(id="blood_perfusion", type="number", debounce=True,
                                   min=app_model.tissue_ranges["blood_perfusion"]["min"],
                                   max=app_model.tissue_ranges["blood_perfusion"]["max"],
                                   step=app_model.tissue_ranges["blood_perfusion"]["step"],
                                   value=app_model.tissue.blood_perfusion),
                         html.Label(" ml/(g min)", htmlFor="blood_perfusion"),
                         html.Label("Water content: ", htmlFor="water_content"),
                         dcc.Input(id="water_content", type="number", debounce=True,
                                   min=app_model.tissue_ranges["water_content"]["min"],
                                   max=app_model.tissue_ranges["water_content"]["max"],
                                   step=app_model.tissue_ranges["water_content"]["step"],
                                   value=app_model.tissue.water_content),
                         html.Label(" %", htmlFor="water_content"),
                         html.Label("Heat conductivity: ", htmlFor="heat_conductivity"),
                         dcc.Input(id="heat_conductivity", type="number", debounce=True,
                                   min=app_model.tissue_ranges["heat_conductivity"]["min"],
                                   max=app_model.tissue_ranges["heat_conductivity"]["max"],
                                   step=app_model.tissue_ranges["heat_conductivity"]["step"],
                                   value=app_model.tissue.heat_conductivity),
                         html.Label(" W/(cm K)", htmlFor="heat_conductivity"),
                         html.Label("Heat capacity: ", htmlFor="heat_capacity"),
                         dcc.Input(id="heat_capacity", type="number", debounce=True,
                                   min=app_model.tissue_ranges["heat_capacity"]["min"],
                                   max=app_model.tissue_ranges["heat_capacity"]["max"],
                                   step=app_model.tissue_ranges["heat_capacity"]["step"],
                                   value=app_model.tissue.heat_capacity),
                         html.Label(" J/(g K)", htmlFor="heat_capacity"),
                         html.Label("Density: ", htmlFor="density"),
                         dcc.Input(id="density", type="number", debounce=True,
                                   min=app_model.tissue_ranges["density"]["min"],
                                   max=app_model.tissue_ranges["density"]["max"],
                                   step=app_model.tissue_ranges["density"]["step"],
                                   value=app_model.tissue.density),
                         html.Label(" g/cm^3", htmlFor="density"),
                     ]),
            html.Br(),
            html.Label("Damage parameters: ", htmlFor="damage_parameters"),
            html.Div(id="damage_parameters",
                     children=[
                         html.Label("Damage threshold: ", htmlFor="damage_threshold"),
                         dcc.Input(id="damage_threshold", type="number", debounce=True,
                                   min=app_model.tissue_ranges["damage_threshold"]["min"],
                                   max=app_model.tissue_ranges["damage_threshold"]["max"],
                                   step=app_model.tissue_ranges["damage_threshold"]["step"],
                                   value=app_model.tissue.damage_threshold),
                         html.Label("Activation energy: ", htmlFor="activation_energy"),
                         dcc.Input(id="activation_energy", type="number", debounce=True,
                                   min=app_model.tissue_ranges["activation_energy"]["min"],
                                   max=app_model.tissue_ranges["activation_energy"]["max"],
                                   step=app_model.tissue_ranges["activation_energy"]["step"],
                                   value=app_model.tissue.activation_energy),
                         html.Label(" J/mol", htmlFor="activation_energy"),
                         html.Label("Rate parameter: ", htmlFor="rate_parameter"),
                         dcc.Input(id="rate_parameter", type="number", debounce=True,
                                   min=app_model.tissue_ranges["rate_parameter"]["min"],
                                   max=app_model.tissue_ranges["rate_parameter"]["max"],
                                   step=app_model.tissue_ranges["rate_parameter"]["step"],
                                   value=app_model.tissue.rate_parameter),
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
    if ctx.triggered_id == "tissue_select":
        if tissue_name is not None:
            tissue = get_tissue_by_name(app.model.builtin_tissues, tissue_name)
            app.model.tissue = TissueModel(**tissue)
    else:
        if validate_input(wave_length, app.model.tissue_ranges["wave_length"]):
            app.model.tissue.wave_length = wave_length

        if validate_input(native_refractive_index, app.model.tissue_ranges["native_refractive_index"]):
            app.model.tissue.native_refractive_index = native_refractive_index

        if validate_input(native_absorption, app.model.tissue_ranges["native_absorption"]):
            app.model.tissue.native_absorption = native_absorption

        if validate_input(native_scattering, app.model.tissue_ranges["native_scattering"]):
            app.model.tissue.native_scattering = native_scattering

        if validate_input(native_g_factor, app.model.tissue_ranges["native_g_factor"]):
            app.model.tissue.native_g_factor = native_g_factor

        if validate_input(coagulated_refractive_index, app.model.tissue_ranges["coagulated_refractive_index"]):
            app.model.tissue.coagulated_refractive_index = coagulated_refractive_index

        if validate_input(coagulated_absorption, app.model.tissue_ranges["coagulated_absorption"]):
            app.model.tissue.coagulated_absorption = coagulated_absorption

        if validate_input(coagulated_scattering, app.model.tissue_ranges["coagulated_scattering"]):
            app.model.tissue.coagulated_scattering = coagulated_scattering

        if validate_input(coagulated_g_factor, app.model.tissue_ranges["coagulated_g_factor"]):
            app.model.tissue.coagulated_g_factor = coagulated_g_factor

        if validate_input(initial_temperature, app.model.tissue_ranges["initial_temperature"]):
            app.model.tissue.initial_temperature = initial_temperature

        if validate_input(blood_perfusion, app.model.tissue_ranges["blood_perfusion"]):
            app.model.tissue.blood_perfusion = blood_perfusion

        if validate_input(water_content, app.model.tissue_ranges["water_content"]):
            app.model.tissue.water_content = water_content

        if validate_input(heat_conductivity, app.model.tissue_ranges["heat_conductivity"]):
            app.model.tissue.heat_conductivity = heat_conductivity

        if validate_input(heat_capacity, app.model.tissue_ranges["heat_capacity"]):
            app.model.tissue.heat_capacity = heat_capacity

        if validate_input(density, app.model.tissue_ranges["density"]):
            app.model.tissue.density = density

        if validate_input(damage_threshold, app.model.tissue_ranges["damage_threshold"]):
            app.model.tissue.damage_threshold = damage_threshold

        if validate_input(activation_energy, app.model.tissue_ranges["activation_energy"]):
            app.model.tissue.activation_energy = activation_energy

        if validate_input(rate_parameter, app.model.tissue_ranges["rate_parameter"]):
            app.model.tissue.rate_parameter = rate_parameter

    return app.model.tissue.wave_length, app.model.tissue.native_refractive_index, app.model.tissue.native_absorption, \
        app.model.tissue.native_scattering, app.model.tissue.native_g_factor, app.model.tissue.coagulated_refractive_index, \
        app.model.tissue.coagulated_absorption, app.model.tissue.coagulated_scattering, app.model.tissue.coagulated_g_factor, \
        app.model.tissue.initial_temperature, app.model.tissue.blood_perfusion, app.model.tissue.water_content, \
        app.model.tissue.heat_conductivity, app.model.tissue.heat_capacity, app.model.tissue.density, \
        app.model.tissue.damage_threshold, app.model.tissue.activation_energy, app.model.tissue.rate_parameter


def create_roi_settings(app_model: AppDataModel) -> object:
    return dcc.Tab(
        id="roi_settings",
        label="Region of Interest",
        children=[
            html.Label("Voxel dimension: ", htmlFor="voxel_dimension_input"),
            dcc.Input(id="voxel_dimension_input", type="number", debounce=True,
                      min=app_model.roi_ranges["voxel_dimension"]["min"],
                      max=app_model.roi_ranges["voxel_dimension"]["max"],
                      step=app_model.roi_ranges["voxel_dimension"]["step"],
                      value=app_model.roi.voxel_dimension),
            html.Label(" mm: ", htmlFor="voxel_dimension_input"),
            html.Br(),
            html.Div(id="no_of_voxels",
                     children=[
                         html.Label("No. of voxels in X-direction: ", htmlFor="no_of_voxels_in_x_direction"),
                         dcc.Input(id="no_of_voxels_in_x_direction", type="number", debounce=True,
                                   min=app_model.roi_ranges["no_of_voxels_in_x_direction"]["min"],
                                   max=app_model.roi_ranges["no_of_voxels_in_x_direction"]["max"],
                                   step=app_model.roi_ranges["no_of_voxels_in_x_direction"]["step"],
                                   value=app_model.roi.no_of_voxels_in_x_direction),
                         html.Label("No. of voxels in Y-direction: ", htmlFor="no_of_voxels_in_y_direction"),
                         dcc.Input(id="no_of_voxels_in_y_direction", type="number", debounce=True,
                                   min=app_model.roi_ranges["no_of_voxels_in_y_direction"]["min"],
                                   max=app_model.roi_ranges["no_of_voxels_in_y_direction"]["max"],
                                   step=app_model.roi_ranges["no_of_voxels_in_y_direction"]["step"],
                                   value=app_model.roi.no_of_voxels_in_y_direction),
                         html.Label("No. of voxels in Z-direction: ", htmlFor="no_of_voxels_in_z_direction"),
                         dcc.Input(id="no_of_voxels_in_z_direction", type="number", debounce=True,
                                   min=app_model.roi_ranges["no_of_voxels_in_z_direction"]["min"],
                                   max=app_model.roi_ranges["no_of_voxels_in_z_direction"]["max"],
                                   step=app_model.roi_ranges["no_of_voxels_in_z_direction"]["step"],
                                   value=app_model.roi.no_of_voxels_in_z_direction)
                     ]),
            html.Label("Calculated dimensions of ROI", htmlFor="dim_of_roi"),
            html.Div(id="dim_of_roi",
                     children=[
                         html.Label("X: ", htmlFor="dimension_x"),
                         dcc.Input(id="dimension_x", value=app_model.roi.get_dimension()[0], disabled=True),
                         html.Label("Y: ", htmlFor="dimension_y"),
                         dcc.Input(id="dimension_y", value=app_model.roi.get_dimension()[1], disabled=True),
                         html.Label("Z:", htmlFor="dimension_z"),
                         dcc.Input(id="dimension_z", value=app_model.roi.get_dimension()[2], disabled=True)
                     ]),
            html.Br(),
            html.Label("Memory requirements", htmlFor="memory_requirements"),
            html.Div(id="memory_requirements",
                     children=[
                         html.Label("Size of voxel: ", htmlFor="voxel_size"),
                         dcc.Input(id="voxel_size", value=96, disabled=True),
                         html.Label(" bytes", htmlFor="voxel_size"),
                         html.Label("Number of voxels: ", htmlFor="voxels_number"),
                         dcc.Input(id="voxels_number", value=app_model.roi.get_voxels_number(), disabled=True),
                         html.Label("Total memory required: ", htmlFor="required_memory"),
                         dcc.Input(id="required_memory", value=app_model.roi.get_required_memory(UINT(96)),
                                   disabled=True)
                     ]),
            html.Br(),
            html.Label("ROI boundaries", htmlFor="roi_boundaries"),
            html.Div(id="roi_boundaries",
                     children=[
                         html.Div(id="left_bound", children=[
                             html.Label("Left bound:"),
                             html.Br(),
                             html.Label("Bound type:", htmlFor="left_bound_type_select"),
                             dcc.Dropdown(list(app_model.roi_ranges["bound_type"]), id="left_bound_type_select",
                                          clearable=False, value=app_model.roi.left_bound_type),
                             html.Label("Fixed temperature:", htmlFor="left_bound_fixed_temperature"),
                             dcc.Input(id="left_bound_fixed_temperature", type="number", debounce=True,
                                       min=app_model.roi_ranges["bound_fixed_temperature"]["min"],
                                       max=app_model.roi_ranges["bound_fixed_temperature"]["max"],
                                       step=app_model.roi_ranges["bound_fixed_temperature"]["step"],
                                       value=app_model.roi.left_bound_fixed_temperature)
                         ]),
                         html.Div(id="top_bound", children=[
                             html.Label("Top bound:"),
                             html.Br(),
                             html.Label("Bound type:", htmlFor="top_bound_type_select"),
                             dcc.Dropdown(list(app_model.roi_ranges["bound_type"]), id="top_bound_type_select",
                                          clearable=False, value=app_model.roi.top_bound_type),
                             html.Label("Fixed temperature:", htmlFor="top_bound_fixed_temperature"),
                             dcc.Input(id="top_bound_fixed_temperature", type="number", debounce=True,
                                       min=app_model.roi_ranges["bound_fixed_temperature"]["min"],
                                       max=app_model.roi_ranges["bound_fixed_temperature"]["max"],
                                       step=app_model.roi_ranges["bound_fixed_temperature"]["step"],
                                       value=app_model.roi.top_bound_fixed_temperature)
                         ]),
                         html.Div(id="back_bound", children=[
                             html.Label("Back bound:"),
                             html.Br(),
                             html.Label("Bound type:", htmlFor="back_bound_type_select"),
                             dcc.Dropdown(list(app_model.roi_ranges["bound_type"]), id="back_bound_type_select",
                                          clearable=False, value=app_model.roi.back_bound_type),
                             html.Label("Fixed temperature:", htmlFor="back_bound_fixed_temperature"),
                             dcc.Input(id="back_bound_fixed_temperature", type="number", debounce=True,
                                       min=app_model.roi_ranges["bound_fixed_temperature"]["min"],
                                       max=app_model.roi_ranges["bound_fixed_temperature"]["max"],
                                       step=app_model.roi_ranges["bound_fixed_temperature"]["step"],
                                       value=app_model.roi.back_bound_fixed_temperature)
                         ]),
                         html.Div(id="front_bound", children=[
                             html.Label("Front bound:"),
                             html.Br(),
                             html.Label("Bound type:", htmlFor="front_bound_type_select"),
                             dcc.Dropdown(list(app_model.roi_ranges["bound_type"]), id="front_bound_type_select",
                                          clearable=False, value=app_model.roi.front_bound_type),
                             html.Label("Fixed temperature:", htmlFor="front_bound_fixed_temperature"),
                             dcc.Input(id="front_bound_fixed_temperature", type="number", debounce=True,
                                       min=app_model.roi_ranges["bound_fixed_temperature"]["min"],
                                       max=app_model.roi_ranges["bound_fixed_temperature"]["max"],
                                       step=app_model.roi_ranges["bound_fixed_temperature"]["step"],
                                       value=app_model.roi.front_bound_fixed_temperature)
                         ]),
                         html.Div(id="bottom_bound", children=[
                             html.Label("Bottom bound:"),
                             html.Br(),
                             html.Label("Bound type:", htmlFor="bottom_bound_type_select"),
                             dcc.Dropdown(list(app_model.roi_ranges["bound_type"]), id="bottom_bound_type_select",
                                          clearable=False, value=app_model.roi.bottom_bound_type),
                             html.Label("Fixed temperature:", htmlFor="bottom_bound_fixed_temperature"),
                             dcc.Input(id="bottom_bound_fixed_temperature", type="number", debounce=True,
                                       min=app_model.roi_ranges["bound_fixed_temperature"]["min"],
                                       max=app_model.roi_ranges["bound_fixed_temperature"]["max"],
                                       step=app_model.roi_ranges["bound_fixed_temperature"]["step"],
                                       value=app_model.roi.bottom_bound_fixed_temperature)
                         ]),
                         html.Div(id="right_bound", children=[
                             html.Label("Right bound:"),
                             html.Br(),
                             html.Label("Bound type:", htmlFor="right_bound_type_select"),
                             dcc.Dropdown(list(app_model.roi_ranges["bound_type"]), id="right_bound_type_select",
                                          clearable=False, value=app_model.roi.right_bound_type),
                             html.Label("Fixed temperature:", htmlFor="right_bound_fixed_temperature"),
                             dcc.Input(id="right_bound_fixed_temperature", type="number", debounce=True,
                                       min=app_model.roi_ranges["bound_fixed_temperature"]["min"],
                                       max=app_model.roi_ranges["bound_fixed_temperature"]["max"],
                                       step=app_model.roi_ranges["bound_fixed_temperature"]["step"],
                                       value=app_model.roi.right_bound_fixed_temperature)
                         ])
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
    Output("left_bound_fixed_temperature", "value"),
    Output("top_bound_fixed_temperature", "value"),
    Output("back_bound_fixed_temperature", "value"),
    Output("front_bound_fixed_temperature", "value"),
    Output("bottom_bound_fixed_temperature", "value"),
    Output("right_bound_fixed_temperature", "value"),
    Input("voxel_dimension_input", "value"),
    Input("no_of_voxels_in_x_direction", "value"),
    Input("no_of_voxels_in_y_direction", "value"),
    Input("no_of_voxels_in_z_direction", "value"),
    Input("left_bound_type_select", "value"),
    Input("left_bound_fixed_temperature", "value"),
    Input("top_bound_type_select", "value"),
    Input("top_bound_fixed_temperature", "value"),
    Input("back_bound_type_select", "value"),
    Input("back_bound_fixed_temperature", "value"),
    Input("front_bound_type_select", "value"),
    Input("front_bound_fixed_temperature", "value"),
    Input("bottom_bound_type_select", "value"),
    Input("bottom_bound_fixed_temperature", "value"),
    Input("right_bound_type_select", "value"),
    Input("right_bound_fixed_temperature", "value")
)
def roi_settings_callback(voxel_dim, no_of_voxels_in_x_dir, no_of_voxels_in_y_dir, no_of_voxels_in_z_dir,
                          left_bound_type, left_bound_temp, top_bound_type, top_bound_temp,
                          back_bound_type, back_bound_temp, front_bound_type, front_bound_temp,
                          bottom_bound_type, bottom_bound_temp, right_bound_type, right_bound_temp):
    if validate_input(voxel_dim, app.model.roi_ranges["voxel_dimension"]):
        app.model.roi.voxel_dimension = FLOAT(voxel_dim)

    if validate_input(no_of_voxels_in_x_dir, app.model.roi_ranges["no_of_voxels_in_x_direction"]):
        app.model.roi.no_of_voxels_in_x_direction = UINT(no_of_voxels_in_x_dir)

    if validate_input(no_of_voxels_in_y_dir, app.model.roi_ranges["no_of_voxels_in_y_direction"]):
        app.model.roi.no_of_voxels_in_y_direction = UINT(no_of_voxels_in_y_dir)

    if validate_input(no_of_voxels_in_z_dir, app.model.roi_ranges["no_of_voxels_in_z_direction"]):
        app.model.roi.no_of_voxels_in_z_direction = UINT(no_of_voxels_in_z_dir)

    if validate_input(left_bound_temp, app.model.roi_ranges["bound_fixed_temperature"]):
        app.model.roi.left_bound_fixed_temperature = FLOAT(left_bound_temp)

    app.model.roi.left_bound_type = left_bound_type

    if validate_input(top_bound_temp, app.model.roi_ranges["bound_fixed_temperature"]):
        app.model.roi.top_bound_fixed_temperature = FLOAT(top_bound_temp)

    app.model.roi.top_bound_type = top_bound_type

    if validate_input(back_bound_temp, app.model.roi_ranges["bound_fixed_temperature"]):
        app.model.roi.back_bound_fixed_temperature = FLOAT(back_bound_temp)

    app.model.roi.back_bound_type = back_bound_type

    if validate_input(front_bound_temp, app.model.roi_ranges["bound_fixed_temperature"]):
        app.model.roi.front_bound_fixed_temperature = FLOAT(front_bound_temp)

    app.model.roi.front_bound_type = front_bound_type

    if validate_input(bottom_bound_temp, app.model.roi_ranges["bound_fixed_temperature"]):
        app.model.roi.bottom_bound_fixed_temperature = FLOAT(bottom_bound_temp)

    app.model.roi.bottom_bound_type = bottom_bound_type

    if validate_input(right_bound_temp, app.model.roi_ranges["bound_fixed_temperature"]):
        app.model.roi.right_bound_fixed_temperature = FLOAT(right_bound_temp)

    app.model.roi.right_bound_type = right_bound_type

    return *app.model.roi.get_dimension(), 32, app.model.roi.get_voxels_number(), \
        format_bytes_number(app.model.roi.get_required_memory(UINT(32))), app.model.roi.voxel_dimension, \
        app.model.roi.no_of_voxels_in_x_direction, app.model.roi.no_of_voxels_in_y_direction, app.model.roi.no_of_voxels_in_z_direction, \
        app.model.roi.left_bound_fixed_temperature, app.model.roi.top_bound_fixed_temperature, app.model.roi.back_bound_fixed_temperature, \
        app.model.roi.front_bound_fixed_temperature, app.model.roi.bottom_bound_fixed_temperature, app.model.roi.right_bound_fixed_temperature


def create_laser_settings(app_model: AppDataModel) -> object:
    return dcc.Tab(
        id="laser_settings",
        label="Laser",
        children=[
            html.Label("Add new source"),
            html.Br(),
            html.Label("Position of applicator center (without peak): ", htmlFor="add_source_position_parameters"),
            html.Div(id="add_source_position_parameters",
                     children=[
                         html.Label("X: ", htmlFor="add_source_x_coordinate"),
                         dcc.Input(id="add_source_x_coordinate", type="number", debounce=True,
                                   min=app_model.laser_ranges["position"]["min"],
                                   max=app_model.roi.get_dimension()[0],
                                   step=app_model.laser_ranges["position"]["step"],
                                   value=app_model.default_laser.position_x),
                         html.Label(" mm", htmlFor="add_source_x_coordinate"),
                         html.Label("Y: ", htmlFor="add_source_y_coordinate"),
                         dcc.Input(id="add_source_y_coordinate", type="number", debounce=True,
                                   min=app_model.laser_ranges["position"]["min"],
                                   max=app_model.roi.get_dimension()[1],
                                   step=app_model.laser_ranges["position"]["step"],
                                   value=app_model.default_laser.position_y),
                         html.Label(" mm", htmlFor="add_source_y_coordinate"),
                         html.Label("Z: ", htmlFor="add_source_z_coordinate"),
                         dcc.Input(id="add_source_z_coordinate", type="number", debounce=True,
                                   min=app_model.laser_ranges["position"]["min"],
                                   max=app_model.roi.get_dimension()[2],
                                   step=app_model.laser_ranges["position"]["step"],
                                   value=app_model.default_laser.position_z),
                         html.Label(" mm", htmlFor="add_source_z_coordinate"),
                         html.Br(),
                         html.Button("Add source", id="add_source", n_clicks=0)
                     ]),
            html.Label("Active sources"),
            html.Br(),
            html.Div(id="sources_list", children=[])
        ])


@callback(
    Output("add_source_x_coordinate", "max"),
    Output("add_source_y_coordinate", "max"),
    Output("add_source_z_coordinate", "max"),
    Input("dimension_x", "value"),
    Input("dimension_y", "value"),
    Input("dimension_z", "value"),
)
def new_source_position_ranges_callback(dim_x, dim_y, dim_z):
    return dim_x, dim_y, dim_z


@callback(
    Output("add_source_x_coordinate", "value"),
    Output("add_source_y_coordinate", "value"),
    Output("add_source_z_coordinate", "value"),
    Input("add_source_x_coordinate", "value"),
    Input("add_source_y_coordinate", "value"),
    Input("add_source_z_coordinate", "value"),
    Input("dimension_x", "value"),
    Input("dimension_y", "value"),
    Input("dimension_z", "value"),
)
def new_source_position_callback(pos_x, pos_y, pos_z, dim_x, dim_y, dim_z):
    if validate_input(pos_x, {**app.model.laser_ranges["position"], "max": dim_x}):
        app.model.default_laser.position_x = pos_x
    else:
        app.model.default_laser.position_x = min(app.model.default_laser.position_x, dim_x)

    if validate_input(pos_y, {**app.model.laser_ranges["position"], "max": dim_y}):
        app.model.default_laser.position_y = pos_y
    else:
        app.model.default_laser.position_y = min(app.model.default_laser.position_y, dim_y)

    if validate_input(pos_z, {**app.model.laser_ranges["position"], "max": dim_z}):
        app.model.default_laser.position_z = pos_z
    else:
        app.model.default_laser.position_z = min(app.model.default_laser.position_z, dim_z)

    return app.model.default_laser.position_x, app.model.default_laser.position_y, app.model.default_laser.position_z


@callback(
    Output("sources_list", "children"),
    Input("add_source_x_coordinate", "value"),
    Input("add_source_y_coordinate", "value"),
    Input("add_source_z_coordinate", "value"),
    Input("add_source", "n_clicks"),
    Input({"type": "remove_source", "index": ALL}, "n_clicks"),
    State("sources_list", "children")
)
def add_remove_laser_source_callback(pos_x, pos_y, pos_z, add_clicks, remove_clicks, children):
    if add_clicks is None or remove_clicks is None or ctx.triggered_id is None:
        return children

    if ctx.triggered_id == "add_source":
        if check_if_laser_position_is_available(app.model.lasers, pos_x, pos_y, pos_z):
            app.model.lasers_counter += 1
            app.model.lasers.append(
                [app.model.lasers_counter, LaserModel(pos_x, pos_y, pos_z, LaserApplicatorType.CUSTOM)])

            children.append(html.Div(id=f"source{app.model.lasers_counter}", children=[
                html.Label(f"Source {app.model.lasers_counter}:"),
                html.Br(),
                html.Label("X: ", htmlFor=f"source{app.model.lasers_counter}_x_coordinate"),
                dcc.Input(id={"type": "source_x_coordinate", "index": int(app.model.lasers_counter)},
                          type="number", debounce=True,
                          min=app.model.laser_ranges["position"]["min"],
                          max=app.model.roi.get_dimension()[0],
                          step=app.model.laser_ranges["position"]["step"],
                          value=pos_x),
                html.Label("Y: ", htmlFor=f"source{app.model.lasers_counter}_y_coordinate"),
                dcc.Input(id={"type": "source_y_coordinate", "index": int(app.model.lasers_counter)},
                          type="number", debounce=True,
                          min=app.model.laser_ranges["position"]["min"],
                          max=app.model.roi.get_dimension()[1],
                          step=app.model.laser_ranges["position"]["step"],
                          value=pos_y),
                html.Label("Z: ", htmlFor=f"source{app.model.lasers_counter}_z_coordinate"),
                dcc.Input(id={"type": "source_z_coordinate", "index": int(app.model.lasers_counter)},
                          type="number", debounce=True,
                          min=app.model.laser_ranges["position"]["min"],
                          max=app.model.roi.get_dimension()[2],
                          step=app.model.laser_ranges["position"]["step"],
                          value=pos_z),
                html.Button("Remove source", id={"type": "remove_source", "index": int(app.model.lasers_counter)},
                            n_clicks=0)
            ]))
    elif isinstance(ctx.triggered_id, dict) and "type" in ctx.triggered_id and "index" in ctx.triggered_id and \
            ctx.triggered_id["type"] == "remove_source":
        index = int(ctx.triggered_id["index"])

        new_lasers = []
        for model_index, model in app.model.lasers:
            if model_index != index:
                new_lasers.append([model_index, model])
        app.model.lasers = new_lasers

        new_children = []
        for child in children:
            if child["props"]["id"] != f"source{index}":
                new_children.append(child)
        children = new_children

    return children


@callback(
    Output({"type": "source_x_coordinate", "index": MATCH}, "value"),
    Output({"type": "source_y_coordinate", "index": MATCH}, "value"),
    Output({"type": "source_z_coordinate", "index": MATCH}, "value"),
    Input({"type": "source_x_coordinate", "index": MATCH}, "value"),
    Input({"type": "source_y_coordinate", "index": MATCH}, "value"),
    Input({"type": "source_z_coordinate", "index": MATCH}, "value"),
    Input("dimension_x", "value"),
    Input("dimension_y", "value"),
    Input("dimension_z", "value"),
    State({"type": "source_x_coordinate", "index": MATCH}, "id"),
    State({"type": "source_y_coordinate", "index": MATCH}, "id"),
    State({"type": "source_z_coordinate", "index": MATCH}, "id")
)
def laser_settings_callback(pos_x, pos_y, pos_z, dim_x, dim_y, dim_z,
                            pos_x_id, pos_y_id, pos_z_id):
    index_x = pos_x_id["index"]
    index_y = pos_y_id["index"]
    index_z = pos_z_id["index"]

    if validate_input(pos_x, {**app.model.laser_ranges["position"], "max": dim_x}) and \
            check_if_laser_position_is_available(app.model.lasers, FLOAT(pos_x), FLOAT(pos_y), FLOAT(pos_z)):
        get_laser_model_by_index(app.model.lasers, index_x).position_x = FLOAT(pos_x)
    elif dim_x < get_laser_model_by_index(app.model.lasers, index_x).position_x:
        old_x_value = get_laser_model_by_index(app.model.lasers, index_x).position_x
        new_x_value = dim_x - index_x * app.model.laser_ranges["position"]["step"]
        get_laser_model_by_index(app.model.lasers, index_x).position_x = min(old_x_value, new_x_value)

    if validate_input(pos_y, {**app.model.laser_ranges["position"], "max": dim_y}) and \
            check_if_laser_position_is_available(app.model.lasers, FLOAT(pos_x), FLOAT(pos_y), FLOAT(pos_z)):
        get_laser_model_by_index(app.model.lasers, index_y).position_y = FLOAT(pos_y)
    elif dim_y < get_laser_model_by_index(app.model.lasers, index_y).position_y:
        old_y_value = get_laser_model_by_index(app.model.lasers, index_y).position_y
        new_y_value = dim_y - index_y * app.model.laser_ranges["position"]["step"]
        get_laser_model_by_index(app.model.lasers, index_y).position_y = min(old_y_value, new_y_value)

    if validate_input(pos_z, {**app.model.laser_ranges["position"], "max": dim_z}) and \
            check_if_laser_position_is_available(app.model.lasers, FLOAT(pos_x), FLOAT(pos_y), FLOAT(pos_z)):
        get_laser_model_by_index(app.model.lasers, index_z).position_z = FLOAT(pos_z)
    elif dim_z < get_laser_model_by_index(app.model.lasers, index_z).position_z:
        old_z_value = get_laser_model_by_index(app.model.lasers, index_z).position_z
        new_z_value = dim_z - index_z * app.model.laser_ranges["position"]["step"]
        get_laser_model_by_index(app.model.lasers, index_z).position_z = min(old_z_value, new_z_value)

    return get_laser_model_by_index(app.model.lasers, index_x).position_x, \
        get_laser_model_by_index(app.model.lasers, index_y).position_y, \
        get_laser_model_by_index(app.model.lasers, index_z).position_z


def validate_input(value: any, ranges: json) -> bool:
    try:
        float_value = FLOAT(value)
    except ValueError:
        return False
    except TypeError:
        return False

    if not ranges["min"] <= float_value <= ranges["max"]:
        return False

    return np.alltrue(np.isclose(float_value / ranges["step"], round(float_value / ranges["step"])))


def check_if_laser_position_is_available(laser_models: List[Tuple[UINT, LaserModel]], x: FLOAT, y: FLOAT,
                                         z: FLOAT) -> bool:
    if x is None or y is None or z is None:
        return False

    for model_index, model in laser_models:
        if np.isclose(model.position_x, x) and np.isclose(model.position_y, y) and np.isclose(model.position_z, z):
            return False

    return True


def get_laser_model_by_index(laser_models: List[Tuple[UINT, LaserModel]], laser_index: UINT) -> LaserModel:
    for index, model in laser_models:
        if index == laser_index:
            return model


def format_bytes_number(bytes_number: UINT) -> str:
    if bytes_number >= 10e9:
        return "{:.2f} gigabytes".format(bytes_number / 10e9)

    if bytes_number >= 10e6:
        return "{:.2f} megabytes".format(bytes_number / 10e6)

    if bytes_number >= 10e3:
        return "{:.2f} kilobytes".format(bytes_number / 10e3)

    return "{:.2f} bytes".format(bytes_number)


def get_tissue_by_name(tissues: json, tissue_name: str) -> json:
    for tissue in tissues:
        if tissues[tissue]["name"] == tissue_name:
            return tissues[tissue]

    return None
