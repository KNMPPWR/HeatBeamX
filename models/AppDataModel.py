import json
import numpy as np
from typing import List, Tuple

from models.ROIModel import ROIModel
from models.TissueModel import TissueModel
from models.LaserModel import LaserModel, LaserApplicatorType
from simulation.Simulation import Simulation

UINT = np.uint32
FLOAT = np.float64

with open("assets/default-settings.json") as default_setting_json:
    default_setting = json.load(default_setting_json)

with open("assets/tissues.json") as tissues_json:
    tissues = json.load(tissues_json)


class AppDataModel(object):
    def __init__(self):
        self.tissue_ranges: json = default_setting["tissue"]["ranges"]
        self.tissue: TissueModel = TissueModel(**default_setting["tissue"]["values"])
        self.builtin_tissues: json = tissues

        self.roi_ranges: json = default_setting["roi"]["ranges"]
        self.roi: ROIModel = ROIModel(**default_setting["roi"]["values"])

        self.laser_ranges: json = default_setting["laser"]["ranges"]
        self.default_laser_data = default_setting["laser"]["values"]
        self.default_laser: LaserModel = LaserModel(**self.default_laser_data)
        self.lasers: List[Tuple[UINT, LaserModel]] = []
        self.lasers_counter: UINT = UINT(0)

        self.simulation_ranges = default_setting["simulation"]["ranges"]
        self.simulation_defaults = default_setting["simulation"]["values"]
        self.simulation = Simulation(self.tissue, self.roi, [pair[1] for pair in self.lasers],
                                     self.simulation_defaults["time_interval"], self.simulation_defaults["total_time"])
