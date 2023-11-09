import json
from typing import List


def validate_input(value: any, ranges: json) -> bool:
    try:
        float_value = float(value)
    except ValueError:
        return False
    except TypeError:
        return False

    if not ranges["min"] <= float_value <= ranges["max"]:
        return False

    return int(float_value * (1.0 / ranges["step"])) * ranges["step"] == float_value


def format_bytes_number(bytes_number: int) -> str:
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
