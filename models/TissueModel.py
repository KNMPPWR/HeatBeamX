import json

from config import FLOAT

class TissueModel(object):
    def __init__(self, name: str,
                 wave_length: FLOAT,
                 native_refractive_index: FLOAT,
                 native_absorption: FLOAT,
                 native_scattering: FLOAT,
                 native_g_factor: FLOAT,
                 coagulated_refractive_index: FLOAT,
                 coagulated_absorption: FLOAT,
                 coagulated_scattering: FLOAT,
                 coagulated_g_factor: FLOAT,
                 initial_temperature: FLOAT,
                 blood_perfusion: FLOAT,
                 water_content: FLOAT,
                 heat_conductivity: FLOAT,
                 heat_capacity: FLOAT,
                 density: FLOAT,
                 damage_threshold: FLOAT,
                 activation_energy: FLOAT,
                 rate_parameter: FLOAT):
        self.name = name
        self.wave_length = wave_length
        self.native_refractive_index = native_refractive_index
        self.native_absorption = native_absorption
        self.native_scattering = native_scattering
        self.native_g_factor = native_g_factor
        self.coagulated_refractive_index = coagulated_refractive_index
        self.coagulated_absorption = coagulated_absorption
        self.coagulated_scattering = coagulated_scattering
        self.coagulated_g_factor = coagulated_g_factor
        self.initial_temperature = initial_temperature
        self.blood_perfusion = blood_perfusion
        self.water_content = water_content
        self.heat_conductivity = heat_conductivity
        self.heat_capacity = heat_capacity
        self.density = density
        self.damage_threshold = damage_threshold
        self.activation_energy = activation_energy
        self.rate_parameter = rate_parameter

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self) -> json:
        return {
            "name": self.name,
            "wave_length": self.wave_length,
            "native_refractive_index": self.native_refractive_index,
            "native_absorption": self.native_absorption,
            "native_scattering": self.native_scattering,
            "native_g_factor": self.native_g_factor,
            "coagulated_refractive_index": self.coagulated_refractive_index,
            "coagulated_absorption": self.coagulated_absorption,
            "coagulated_scattering": self.coagulated_scattering,
            "coagulated_g_factor": self.coagulated_g_factor,
            "initial_temperature": self.initial_temperature,
            "blood_perfusion": self.blood_perfusion,
            "water_content": self.water_content,
            "heat_conductivity": self.heat_conductivity,
            "heat_capacity": self.heat_capacity,
            "density": self.density,
            "damage_threshold": self.damage_threshold,
            "activation_energy": self.activation_energy,
            "rate_parameter": self.rate_parameter
        }
