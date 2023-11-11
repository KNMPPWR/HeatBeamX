import json
from typing import List, Tuple

import numpy as np

from models.LaserModel import LaserModel
from config import UINT, FLOAT


def validate_input(value: any, ranges: json) -> bool:
    try:
        float_value = FLOAT(value)
    except ValueError:
        return False
    except TypeError:
        return False

    if not ranges["min"] <= float_value <= ranges["max"]:
        return False

    return np.isclose(float_value / ranges["step"], round(float_value / ranges["step"]))


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


def get_tissues_names(tissues: json) -> List[str]:
    names = []
    for tissue in tissues:
        names.append(tissues[tissue]["name"])

    return list(names)


def get_tissue_by_name(tissues: json, tissue_name: str) -> json:
    for tissue in tissues:
        if tissues[tissue]["name"] == tissue_name:
            return tissues[tissue]

    return None
