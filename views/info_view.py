from dash import html, dcc, callback, Input, Output, State
import json


def create_info_view():
    return dcc.Tab(id="info", label="Info", children=[])
