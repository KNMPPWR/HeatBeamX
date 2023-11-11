import json
from enum import Enum

from config import UINT, FLOAT


class ROIBoundType(Enum):
    ISOLATED = "Isolated",
    OPEN = "Open"


class ROIModel(object):
    def __init__(self, voxel_dimension: FLOAT,
                 no_of_voxels_in_x_direction: UINT,
                 no_of_voxels_in_y_direction: UINT,
                 no_of_voxels_in_z_direction: UINT,
                 left_bound_type: ROIBoundType,
                 left_bound_fixed_temperature: FLOAT,
                 top_bound_type: ROIBoundType,
                 top_bound_fixed_temperature: FLOAT,
                 back_bound_type: ROIBoundType,
                 back_bound_fixed_temperature: FLOAT,
                 front_bound_type: ROIBoundType,
                 front_bound_fixed_temperature: FLOAT,
                 bottom_bound_type: ROIBoundType,
                 bottom_bound_fixed_temperature: FLOAT,
                 right_bound_type: ROIBoundType,
                 right_bound_fixed_temperature: FLOAT):
        self.voxel_dimension = voxel_dimension
        self.no_of_voxels_in_x_direction = no_of_voxels_in_x_direction
        self.no_of_voxels_in_y_direction = no_of_voxels_in_y_direction
        self.no_of_voxels_in_z_direction = no_of_voxels_in_z_direction
        self.left_bound_type = left_bound_type
        self.left_bound_fixed_temperature = left_bound_fixed_temperature
        self.top_bound_type = top_bound_type
        self.top_bound_fixed_temperature = top_bound_fixed_temperature
        self.back_bound_type = back_bound_type
        self.back_bound_fixed_temperature = back_bound_fixed_temperature
        self.front_bound_type = front_bound_type
        self.front_bound_fixed_temperature = front_bound_fixed_temperature
        self.bottom_bound_type = bottom_bound_type
        self.bottom_bound_fixed_temperature = bottom_bound_fixed_temperature
        self.right_bound_type = right_bound_type
        self.right_bound_fixed_temperature = right_bound_fixed_temperature

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self) -> json:
        return {"voxel_dimension": self.voxel_dimension,
                "no_of_voxels_in_x_direction": self.no_of_voxels_in_x_direction,
                "no_of_voxels_in_y_direction": self.no_of_voxels_in_y_direction,
                "no_of_voxels_in_z_direction": self.no_of_voxels_in_z_direction,
                "left_bound_type": self.left_bound_type,
                "left_bound_fixed_temperature": self.left_bound_fixed_temperature,
                "top_bound_type": self.top_bound_type,
                "top_bound_fixed_temperature": self.top_bound_fixed_temperature,
                "back_bound_type": self.back_bound_type,
                "back_bound_fixed_temperature": self.back_bound_fixed_temperature,
                "front_bound_type": self.front_bound_type,
                "front_bound_fixed_temperature": self.front_bound_fixed_temperature,
                "bottom_bound_type": self.bottom_bound_type,
                "bottom_bound_fixed_temperature": self.bottom_bound_fixed_temperature,
                "right_bound_type": self.right_bound_type,
                "right_bound_fixed_temperature": self.right_bound_fixed_temperature}

    def get_dimension(self) -> [FLOAT, FLOAT, FLOAT]:
        return [
            self.no_of_voxels_in_x_direction * self.voxel_dimension,
            self.no_of_voxels_in_y_direction * self.voxel_dimension,
            self.no_of_voxels_in_z_direction * self.voxel_dimension
        ]

    def get_voxels_number(self) -> UINT:
        return self.no_of_voxels_in_x_direction * self.no_of_voxels_in_y_direction * self.no_of_voxels_in_z_direction

    def get_required_memory(self, single_voxel_size: UINT) -> UINT:
        return self.get_voxels_number() * single_voxel_size
