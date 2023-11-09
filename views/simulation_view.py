from dash import html, dcc, callback, Input, Output, State
import json


def create_simulation_view():
    return dcc.Tab(id="simulation", label="Simulation", children=[])
