import json
import numpy as np
from enum import Enum

UINT = np.uint32
FLOAT = np.float64


class LaserApplicatorType(Enum):
    HOMOGENEOUS_SCATTERING_APPLICATOR = "Homogeneous Scattering Applicator"
    DORNIER_RING_MODE_APPLICATOR = "Dornier Ring Mode Applicator"
    BARE_FIBER = "Bare Fiber"
    CUSTOM = "Custom"


class LaserModel(object):
    def __init__(self, position_x: FLOAT,
                 position_y: FLOAT,
                 position_z: FLOAT,
                 applicator_type: LaserApplicatorType):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.applicator_type = applicator_type

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self) -> json:
        return {"position_x": self.position_x,
                "position_y": self.position_y,
                "position_z": self.position_z,
                "applicator_type": self.applicator_type}
