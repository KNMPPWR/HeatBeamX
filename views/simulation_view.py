import numpy as np
import plotly.graph_objects as go
from dash import html, dcc, callback, Input, Output, State

from app import app
from models.AppDataModel import AppDataModel, UINT, FLOAT


def create_simulation_view(app_model: AppDataModel) -> object:
    return dcc.Tab(id="simulation",className='tab',selected_className='tab--selected', label="Simulation",style={'background-color':'#001a33'}, children=[
        html.Label("Plane selection:", htmlFor="plane_select"),
        dcc.Dropdown(("x", "y", "z", "all"), id="plane_select", value="x"),
        html.Label("Layer selection:", htmlFor="layer_select"),
        dcc.Slider(
            id="layer_select", value=0, step=1, min=0, max=min(app_model.roi.no_of_voxels_in_x_direction,
                                                               app_model.roi.no_of_voxels_in_y_direction,
                                                               app_model.roi.no_of_voxels_in_z_direction)
        ),
        html.Label("Simulation step selection:", htmlFor="simulation_step"),
        dcc.Slider(
            id="simulation_step", marks=None, disabled=True,
            min=1, max=app_model.simulation.total_steps, step=1, value=1),
        html.Button("Next step", id="next_simulation_step", n_clicks=0),
        html.Br(),
        dcc.Graph(
            id="3d_current_temperature",
            style={"height": "700px"}
        ),
        dcc.Graph(
            id="2d_current_temperature",
            style={"height": "700px"}
        ),
        dcc.Graph(
            id="1d_max_temperature",
            style={"height": "700px"}
        ),
    ])


@callback(
    Output("3d_current_temperature", "figure"),
    Output("2d_current_temperature", "figure"),
    Output("1d_max_temperature", "figure"),
    Input("plane_select", "value"),
    Input("layer_select", "value"),
    Input("simulation_step", "value")
    # State("3d_current_temperature", "figure"),
    # State("2d_current_temperature", "figure"),
    # State("1d_max_temperature", "figure"),
)
def update_output_callback(plane, layer, sim_step):
    return generate_3d_graph_figure(app.model.simulation.current_temperature, plane, layer), \
        generate_2d_graph_figure(app.model.simulation.current_temperature, plane, layer), \
        generate_1d_graph_figure(np.arange(app.model.simulation.current_step),
                                 app.model.simulation.max_temperature_over_time[:app.model.simulation.current_step])


@callback(
    Output("simulation_step", "value"),
    Input("next_simulation_step", "n_clicks"),
    State("simulation_step", "value")
)
def next_simulation_step_callback(next_step_clicks, current_simulation_step):
    if next_step_clicks == 0:
        return current_simulation_step

    app.model.simulation.next_step()

    return current_simulation_step + 1


def generate_3d_graph_figure(data: np.ndarray, plane: UINT, layer: UINT) -> object:
    shape = data.shape
    if plane == "x":
        layer_data = data[layer, :, :]
        layer_data_flat = layer_data.flatten()
        y, z = np.meshgrid(np.arange(shape[1]), np.arange(shape[2]))
        y_flat = y.flatten()
        z_flat = z.flatten()
        x_flat = np.ones_like(y_flat) * layer
    elif plane == "y":
        layer_data = data[:, layer, :]
        layer_data_flat = layer_data.flatten()
        x, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[2]))
        x_flat = x.flatten()
        z_flat = z.flatten()
        y_flat = np.ones_like(x_flat) * layer
    elif plane == "z":
        layer_data = data[:, :, layer]
        layer_data_flat = layer_data.flatten()
        x, y = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]))
        x_flat = x.flatten()
        y_flat = y.flatten()
        z_flat = np.ones_like(x_flat) * layer
    else:  # show all data
        layer_data = data[:, :, :]
        layer_data_flat = np.array([layer_data[:,x,:].flatten()for x in range(len(data[1,:,1]))]).flatten()
        x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]))
        x_flat = x.flatten()
        y_flat = y.flatten()
        z_flat = z.flatten()
    return {
        "data": [go.Scatter3d(
            x=x_flat,
            y=y_flat,
            z=z_flat,
            mode="markers",
            marker=dict(
                symbol="square",
                color=layer_data_flat,
                colorscale="YlOrRd",
                size = np.minimum(layer_data_flat,12*np.ones(len(layer_data_flat))),
                opacity=1,
            )
        )],
        "layout": go.Layout(
            title="3D Heatmap",
            scene=dict(
                xaxis=dict(title="X-axis", range=[-1, shape[0]+1]),
                yaxis=dict(title="Y-axis", range=[-1, shape[1]+1]),
                zaxis=dict(title="Z-axis", range=[-1, shape[2]+1]),
            )
        )
    }


def generate_2d_graph_figure(data: np.ndarray, plane: UINT, layer: UINT) -> object:
    if plane == "x":
        plot_data = data[layer, :, :]
    elif plane == "y":
        plot_data = data[:, layer, :]
    else:
        plot_data = data[:, :, layer]

    return {
        "data": [go.Heatmap(
            z=plot_data,
            colorscale="YlOrRd",
            opacity=0.8
        )],
        "layout": go.Layout(
            title="Simple Heatmap",
            yaxis = dict(scaleanchor = 'x')
        )
    }


def generate_1d_graph_figure(x: np.ndarray, y: np.ndarray) -> object:
    return {
        "data": [go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(
                symbol="diamond",
                size=10,
                color=y,
                colorscale="YlOrRd",
                opacity=0.8,
            )
        )],
        "layout": go.Layout(
            title="Simple Plot"
        )
    }
