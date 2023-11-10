import json
from enum import Enum

from config import FLOAT

class LaserApplicatorType(Enum):
    HOMOGENEOUS_SCATTERING_APPLICATOR = 1,
    DORNIER_RING_MODE_APPLICATOR = 2,
    BARE_FIBER = 3,
    CUSTOM = 4


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
