import pandas as pd
import numpy as np

from datetime import datetime
from pydantic import BaseModel

from datamodel.core import Experiment
from datamodel.core import Measurement
from datamodel.core import Species
from datamodel.core import Quantity

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
    initial_current: float = None

    class Config:
        # allow panda dataframe
        arbitrary_types_allowed = True

    def _calculate_volumetric_flow_mean(self, inj_date_datetime: datetime) -> float:
        """
        Function checks the GC injection time and search the corresponding time in the mass flow meter recordings.
        The times are matched and the mean mass flow is computed as an average over the x steps bevore and after
        the GC injection.

        Args:
            Injection time of gc_measurement

        Returns:
            float: Averaged volumetric flow [ml/s]
        """

        volumetric_flow_datetime_list, volumetric_flow_values_list = self.experiment.volumetric_flow_time_course
        
        index_match                = np.argmin( [abs(dt - inj_date_datetime) for dt in volumetric_flow_datetime_list] )
        self.volumetric_flow_mean  = np.mean( np.array( volumetric_flow_values_list )[ range(index_match - self.mean_radius, index_match + self.mean_radius + 1) ] )

    def _calculate_volumetric_fractions(self, assigned_peak_areas_dict: dict):
        """
        Function that uses the on calibration data fited linear regresion model to compute the volume fraction given the assigned peak area
        If several peak areas are specified for a component, these are added together. 
        The GC measurement object inheritets the peak areas as well as the matched species

        Args:
            assigned_peak_areas_dict (dict): Dictionary containing the species and the associated peak area.
        """
        self.volumetric_fractions_df = pd.DataFrame( index=[species for species in assigned_peak_areas_dict.keys()], columns=["Volumetric_fraction"] )

        # peak areas are given as list, as it is possible for one component to have several assigned peaks
        for species, peak_areas in assigned_peak_areas_dict.items():
            self.volumetric_fractions_df.loc[species] = self.experiment.get("species_data", "species", species)[0][0].calibration.predict( [ np.sum(peak_areas) ] ) / 100

        if self.volumetric_fractions_df["Volumetric_fraction"].sum() < 0.99: print("\n!!! Warning: Volume fractions doesn't add up to 1.0 !!!\n")

    def _calculate_real_volumetric_flow(self):
        """
        Function that computes the correction factor to account that the mass flow meter is only calibrated on CO2, thus correction of the volumetric flow needs to be done.
        With the correction factor, the real mean voulmetric flow of the mixture is computed
        """

        correction_factor_H   = self.experiment.get("species_data", "species", Species.HYDROGEN.value)[0][0].correction_factor
        correction_factor_CO  = self.experiment.get("species_data", "species", Species.CARBONMONOXIDE.value)[0][0].correction_factor
        correction_factor_CO2 = self.experiment.get("species_data", "species", Species.CARBONDIOXIDE.value)[0][0].correction_factor

        self.conversion_factor    = ( 1 / ( self.volumetric_fractions_df.loc[Species.HYDROGEN.value].values[0] / correction_factor_H
                                        + ( 1 - self.volumetric_fractions_df.loc[Species.HYDROGEN.value].values[0]  + self.volumetric_fractions_df.loc[Species.CARBONMONOXIDE.value].values[0]  ) / correction_factor_CO2
                                        + self.volumetric_fractions_df.loc[Species.CARBONMONOXIDE.value].values[0] / correction_factor_CO
                                        ) / correction_factor_CO2 )
        
        self.real_volumetric_flow = self.volumetric_flow_mean * self.conversion_factor

    def _calculate_material_flow(self):
        """
        Function that computes the real material flow of every component [mol/s].
        Given the real volumetric flow and the volumetric fractions (computed from GC measurement and calibration data)
        """
        ## molecular volume of ideal Gas at 1 atm and 273.15 K: 22.414 l/mol --> 22414 ml/mol (scipy gives m^3/mol = 10^-6*ml^3/mol)
        molecular_volume                  = const.physical_constants["molar volume of ideal gas (273.15 K, 101.325 kPa)"][0] * 10**6
        rename                            = {"Volumetric_fraction": "Material_flow"}

        # Material flow [mol/s] = vol_fraction [vol_% / vol_%] * real_vol_flow [ml/s] / mol_volume_id_gas [ml/mol]
        self.material_flow_df             = self.volumetric_fractions_df.rename ( columns = rename ) * self.real_volumetric_flow  / molecular_volume
            
    def _calculate_theoretical_material_flow(self):
        faraday_constant                   = const.physical_constants["Faraday constant"][0]
        factors                            = { esd.species: esd.faraday_coefficient for esd in self.experiment.species_data }
        self.theoretical_material_flow_df  = pd.DataFrame( index=[species for species in factors.keys()], columns = ["Theoretical_material_flow"] )

        # Current_density i provided in mA/cm^2; Electrode surface A is given as cm^2 --> current I = i*A_surface [A]
        self.initial_current               = abs( self.experiment.get("measurements/metadata", "parameter", "Current")[0][0].value ) * self.experiment.get("measurements/metadata", "parameter", "Electrode surface area")[0][0].value

        # Faraday constant is C/mol, with C = A*s
        # theoretical flow [mol/s]: mA * 1A / 1000mA / ( C/mol ) = mol * A/C = mol * A/(A*s) = mol / s
        for species, factor in factors.items():
            self.theoretical_material_flow_df.loc[species] = self.initial_current / 1000 / ( factor * faraday_constant )


    def calculate_faraday_efficiencies(self, gc_measurement: Measurement):
        """
        This function uses the injection time  as well as the assinged peak areas of the given GC measurement to compute the Faraday effiency.
        This is done by matching the injection to the provided mass flow meter measurements to obtain the mass flow.
        This is further used to compute the measured material flow (mol/s) and compare it with the expected material flow 
        under ideal conditions. The ratio between the measured and the theoretical material flow is the Faraday efficency.

        Args:
            gc_measurement (Measurement): GC measurement, containing the assigned peak areas and the injection time

        Returns:
            DataFrame: Faraday effiency for each species
        """

        # Extract the injection time out of the given GC measurement
        inj_date_datetime = gc_measurement.get("metadata", "parameter", "Injection Date")[0][0].value 

        # Extract the peak areas dict out of the given gc_measurement
        assigned_peak_areas_dict = {}

        peak_assignments = gc_measurement.get("experimental_data","quantity",Quantity.PEAKASSIGNMENT.value)[0][0].values
        peak_areas       = gc_measurement.get("experimental_data","quantity",Quantity.PEAKAREA.value)[0][0].values

        for species,peak_area in zip( peak_assignments, peak_areas):
            if species in assigned_peak_areas_dict.keys():
                assigned_peak_areas_dict[species].append(peak_area)
            else:
                assigned_peak_areas_dict[species] = [peak_area]

        # Compute the theoretical material flow (several substeps are performed to do so)
        self._calculate_volumetric_flow_mean( inj_date_datetime = inj_date_datetime )
        self._calculate_volumetric_fractions( assigned_peak_areas_dict = assigned_peak_areas_dict)
        self._calculate_real_volumetric_flow()
        self._calculate_material_flow()
        self._calculate_theoretical_material_flow()

        rename = {"Material_flow": "Faraday_efficiency"}

        # Compute the Faraday efficency by diving the real by the theoretical material flow
        faraday_efficiency_df = self.material_flow_df.divide( self.theoretical_material_flow_df["Theoretical_material_flow"], axis="index", ).rename(columns=rename)
        faraday_efficiency_df.dropna(inplace=True)

        return faraday_efficiency_df