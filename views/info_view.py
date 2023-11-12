from dash import html, dcc, callback, Input, Output, State
import json

from models.AppDataModel import AppDataModel


def create_info_view(app_model: AppDataModel):
    return dcc.Tab(id="info", label="Info", children=[])
