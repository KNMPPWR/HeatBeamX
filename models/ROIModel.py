import json


class ROIModel(object):
    def __init__(self, voxel_dimension: float,
                 no_of_voxels_in_x_direction: int,
                 no_of_voxels_in_y_direction: int,
                 no_of_voxels_in_z_direction: int):
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

    def get_dimension(self) -> [float, float, float]:
        return [
            self.no_of_voxels_in_x_direction * self.voxel_dimension,
            self.no_of_voxels_in_y_direction * self.voxel_dimension,
            self.no_of_voxels_in_z_direction * self.voxel_dimension
        ]

    def get_voxels_number(self) -> int:
        return self.no_of_voxels_in_x_direction * self.no_of_voxels_in_y_direction * self.no_of_voxels_in_z_direction

    def get_required_memory(self, single_voxel_size: int) -> int:
        return self.get_voxels_number() * single_voxel_size
