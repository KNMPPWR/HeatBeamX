import json

from config import UINT, FLOAT

class ROIModel(object):
    def __init__(self, voxel_dimension: FLOAT,
                 no_of_voxels_in_x_direction: UINT,
                 no_of_voxels_in_y_direction: UINT,
                 no_of_voxels_in_z_direction: UINT):
        self.voxel_dimension = voxel_dimension
        self.no_of_voxels_in_x_direction = no_of_voxels_in_x_direction
        self.no_of_voxels_in_y_direction = no_of_voxels_in_y_direction
        self.no_of_voxels_in_z_direction = no_of_voxels_in_z_direction

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self) -> json:
        return {"voxel_dimension": self.voxel_dimension,
                "no_of_voxels_in_x_direction": self.no_of_voxels_in_x_direction,
                "no_of_voxels_in_y_direction": self.no_of_voxels_in_y_direction,
                "no_of_voxels_in_z_direction": self.no_of_voxels_in_z_direction}

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
