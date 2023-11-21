import pandas as pd
import numpy as np

from pydantic import BaseModel
from pydantic import PrivateAttr
from datetime import datetime
from datamodel_b07_tc.test import Experiment
from datamodel_b07_tc.test import Measurement

import scipy.constants as const

class FaradayEfficiencyCalculator(BaseModel):
    experiment: Experiment
    mean_radius: int = 10
    volumetric_flow_mean: float = None
    volumetric_fractions_df: pd.DataFrame = None
    conversion_factor: float = None
    real_volumetric_flow: float = None
    volumetric_flow_fractions_df: pd.DataFrame = None
    material_flow_df: pd.DataFrame = None
    theoretical_material_flow_df: pd.DataFrame = None

    class Config:
        # allow panda dataframe
        arbitrary_types_allowed = True

    def _calculate_volumetric_flow_mean(self, gc_measurement: Measurement) -> float:
        """
        Function checks the GC injection time and search the corresponding time in the mass flow meter recordings.
        The times are matched and the mean mass flow is computed as an average over the x steps bevore and after
        the GC injection.

        Args:
            gc_measurement (Measurement): Object containing meta data as well as data from GC measurement

        Returns:
            float: Averaged volumetric flow
        """

        volumetric_flow_datetime_list, volumetric_flow_values_list = self.experiment.volumetric_flow_time_course
        
        inj_date_datetime          = gc_measurement.get("metadata","parameter","Injection Date")[0][0].value
        index_match                = np.argmin( [abs(dt - inj_date_datetime) for dt in volumetric_flow_datetime_list] )
        self.volumetric_flow_mean  = np.mean( np.array( volumetric_flow_values_list )[ range(index_match - self.mean_radius, index_match + self.mean_radius + 1) ] )

    def _calculate_volumetric_fractions(self, assigned_peak_areas_dict: dict):
        """
        Function that uses the fited linear regresion model on calibration data to compute the volume fraction given the assigned peak area

        Args:
            assigned_peak_areas_dict (dict): Dictionary containing the species and the associated peak area.
        """
        self.volumetric_fractions_df = pd.DataFrame( index=[species for species in assigned_peak_areas_dict.keys()], columns=["Volumetric_fraction"] )

        for species, peak_areas in assigned_peak_areas_dict.items():
            self.volumetric_fractions_df.loc[species] = self.experiment.get("species_data", "species", species)[0][0].calibration.regression_model.predict( np.atleast_2d( peak_areas[0] ) ) / 100
            

    def _get_correction_factor(self, species):
        """
        Function that extracts the correction factor of a given species

        Args:
            species (string): Name of the species

        Returns:
            float: Correction factor to account for real circumstances
        """
        return self.experiment.get("species_data", "species", species)[0][0].correction_factor


    def _calculate_real_volumetric_flow(self):
        """
        Function that computes the correction factor to account that the mass flow meter is only calibrated on CO2, thus correction of the volumetric flow needs to be done.
        Furthermore the real volumetric flow is computed
        """
        self.conversion_factor    = ( 1 / ( self.volumetric_fractions_df.loc["Hydrogen"].values[0] / self._get_correction_factor("Hydrogen")
                                        + ( 1 - self.volumetric_fractions_df.loc["Hydrogen"].values[0]  + self.volumetric_fractions_df.loc["Carbon monoxide"].values[0]  ) / self._get_correction_factor("Carbon dioxide")
                                        + self.volumetric_fractions_df.loc["Carbon monoxide"].values[0] / self._get_correction_factor("Carbon monoxide")
                                        ) / self._get_correction_factor("Carbon dioxide") )
        
        self.real_volumetric_flow = self.volumetric_flow_mean * self.conversion_factor

    def _calculate_material_flow(self):
        """
        Function that computes the real material flow of every component.
        """
        molecular_volume                  = const.physical_constants["molar volume of ideal gas (273.15 K, 101.325 kPa)"][0] * 10**6
        rename                            = {"Volumetric_fraction": "Material_flow"}
        self.volumetric_flow_fractions_df = self.volumetric_fractions_df.multiply( self.real_volumetric_flow ).divide( molecular_volume ).rename ( columns = rename )
            
    def _calculate_theoretical_material_flow(self):
        faraday_constant                   = const.physical_constants["Faraday constant"][0]
        factors                            = { esd.species: esd.faraday_coefficient for esd in self.experiment.species_data }
        self.theoretical_material_flow_df  = pd.DataFrame( index=[species for species in factors.keys()], columns = ["Theoretical_material_flow"] )

        # Time provided in seconds
        initial_time                       = self.experiment.get("measurements/metadata", "parameter", "Time")[0][0].value

        # Current_density i provided in mA/cm^2; Electrode surface A is given as cm^2 --> current I = i*A_surface [A]
        initial_current                    = abs( self.experiment.get("measurements/metadata", "parameter", "Current")[0][0].value ) * self.experiment.get("measurements/metadata", "parameter", "Electrode surface area")[0][0].value

        # Faraday constant is C/mol, with C = A*s --> t_init * I_init = Q_init [As=C]
        # theoretical flow [mol/s]: mA * 1A / 1000mA / ( C/mol ) = mol / s
        for species, factor in factors.items():
            self.theoretical_material_flow_df.loc[species] = initial_current / 1000 / ( factor * faraday_constant )

    # def calculate_theoretical_amount_of_substance(self):

    def calculate_faraday_efficiencies(self, gc_measurement: Measurement, assigned_peak_areas_dict: dict):
        self._calculate_volumetric_flow_mean( gc_measurement=gc_measurement )
        self._calculate_volumetric_fractions( assigned_peak_areas_dict=assigned_peak_areas_dict )
        self._calculate_conversion_factor()
        self._calculate_real_volumetric_flow()
        self._calculate_volumetric_flow_fractions()
        self._calculate_material_flow()
        self._calculate_theoretical_material_flow()
        rename = {"Material_flow": "Faraday_efficiency"}
        faraday_efficiency_df = self.material_flow_df.divide( self.theoretical_material_flow_df["Theoretical_material_flow"], axis="index", ).rename(columns=rename)
        faraday_efficiency_df.dropna(inplace=True)
        return faraday_efficiency_df