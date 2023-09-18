import pandas as pd
import numpy as np

from pydantic import BaseModel
from pydantic import PrivateAttr
from datetime import datetime
from datamodel_b07_tc.modified import Experiment
from datamodel_b07_tc.modified import Measurement

import scipy.constants as const

class Calculator(BaseModel):

    experiment : Experiment
    correction_factors_dict: dict
    electrode_surface_area: float
    _volumetric_flow_mean: float = PrivateAttr()
    _volumetric_fractions_df: pd.DataFrame = PrivateAttr()
    _conversion_factor: float = PrivateAttr()
    _real_volumetric_flow: float = PrivateAttr()
    _volumetric_flow_fractions_df: pd.DataFrame = PrivateAttr()
    _material_flow_df: pd.DataFrame = PrivateAttr()
    _theoretical_material_flow_df: pd.DataFrame = PrivateAttr()

    def _calculate_volumetric_flow_mean(self, gc_measurement: Measurement, mean_radius: int = 10) -> float:

        volumetric_flow_datetime_list, volumetric_flow_values_list = self.experiment.volumetric_flow_time_course
        gc_measurement_dict = gc_measurement.__dict__
        gc_measurement=Measurement(**gc_measurement_dict)
        inj_date_datetime = datetime.strptime(
            gc_measurement.injection_date, "%d-%b-%y, %H:%M:%S"
        )
        match_datetime = min(volumetric_flow_datetime_list, key=lambda dt: abs(dt - inj_date_datetime))
        index_match = volumetric_flow_datetime_list.index(match_datetime)
        mean_indices_list = [i for i in range(index_match-mean_radius, index_match + mean_radius + 1)]
        self._volumetric_flow_mean = np.average([volumetric_flow_values_list[i] for i in mean_indices_list])

    def _calculate_volumetric_fractions(self, assigned_peak_areas_dict:dict):
         
        self._volumetric_fractions_df = pd.DataFrame(
            index=[species for species in assigned_peak_areas_dict.keys()], columns=["Volumetric_fraction"]
        )
        for species, peak_areas in assigned_peak_areas_dict.items():
            self._volumetric_fractions_df.loc[species] = (
                peak_areas * self.experiment.analysis.get("calibrations", "species", species)[0][0].slope.values[0]
                + self.experiment.analysis.get("calibrations", "species", species)[0][0].intercept.values[0]
            )


    def _calculate_conversion_factor(self):

        self._conversion_factor = (
            1
            / (
                (self._volumetric_fractions_df.loc["H2"][0] / 100)
                / self.correction_factors_dict["H2"]
                + (
                    1
                    - (self._volumetric_fractions_df.loc["H2"][0] / 100)
                    + (self._volumetric_fractions_df.loc["CO"][0]) / 100
                )
                / self.correction_factors_dict["CO2"]
                + (self._volumetric_fractions_df.loc["CO"][0] / 100)
                / self.correction_factors_dict["CO"]
            )
            / self.correction_factors_dict["CO2"]
        )

    def _calculate_real_volumetric_flow(self):

        self._real_volumetric_flow = self._volumetric_flow_mean*self._conversion_factor


    def _calculate_volumetric_flow_fractions(self):

        rename = {"Volumetric_fraction": "Volumetric_flow_fraction"}
        self._volumetric_flow_fractions_df = self._volumetric_fractions_df.multiply(
            self._real_volumetric_flow
        ).rename(columns=rename)


    def _calculate_material_flow(self):

        molecular_volume = const.physical_constants['molar volume of ideal gas (273.15 K, 101.325 kPa)'][0]*10**6
        rename = {"Volumetric_flow_fraction": "Material_flow"}
        self._material_flow_df = self._volumetric_flow_fractions_df.divide(
            molecular_volume
        ).rename(columns=rename)


    def _calculate_theoretical_material_flow(self):

        faraday_constant = const.physical_constants['Faraday constant'][0]
        absolute_initial_current = abs(self.experiment.initial_current)
        current_density = absolute_initial_current / self.electrode_surface_area
        factors = {
            "H2": 2,
            "CO": 2,
            "CO2": 2,
            "CH4": 8,
            "C2H4": 12,
            "C2H6": 16,
        }
        self._theoretical_material_flow_df = pd.DataFrame(
            index=[species for species in factors.keys()],
            columns=["Theoretical_material_flow"],
        )
        for species, factor in factors.items():
            self._theoretical_material_flow_df.loc[species] = (
                self.experiment.initial_time / 60 * current_density / 1000
            ) / (factor * faraday_constant)

    # def calculate_theoretical_amount_of_substance(self):


    def calculate_faraday_efficiency(self, gc_measurement: Measurement, mean_radius: int, assigned_peak_areas_dict:dict):

        self._calculate_volumetric_flow_mean(
            gc_measurement=gc_measurement,
            mean_radius=mean_radius
        )
        self._calculate_volumetric_fractions(
            assigned_peak_areas_dict=assigned_peak_areas_dict
        )
        self._calculate_conversion_factor()
        self._calculate_real_volumetric_flow()
        self._calculate_volumetric_flow_fractions()
        self._calculate_material_flow()
        self._calculate_theoretical_material_flow()
        return self._material_flow_df.divide(self._theoretical_material_flow_df['Theoretical_material_flow'], axis='index')
    
    @property
    def volumetric_fractions(self):
        return self._volumetric_fractions_df

    @property
    def conversion_factor(self):
        return self._conversion_factor
    
    @property
    def real_volumetric_flow(self):
        return self._real_volumetric_flow

    @property
    def volumetric_flow_fractions(self):
        return self._volumetric_flow_fractions_df

    @property
    def material_flow(self):
        return self._material_flow_df

    @property
    def theoretical_material_flow(self):
        return self._theoretical_material_flow_df

    # @property
    # def theoretical_amount_of_substance(self):
    #     self.theoretical_amount_of_substance
