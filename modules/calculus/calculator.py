import os
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from datamodel_b07_tc.core.experiment import Experiment
from datamodel_b07_tc.core.calibration import Calibration
from datamodel_b07_tc.core.data import Data
from datamodel_b07_tc.core.unit import Unit
from datamodel_b07_tc.core.quantity import Quantity


# from datamodel_b07_tc.core import


class Calculator:
    def __init__(
        self,
        path_to_dataset: str | bytes | os.PathLike,
    ):
        self._path_to_dataset = path_to_dataset

    def calibrate(
        self,
        calibration_input_dict: dict,
    ) -> pd.DataFrame:
        column_names = [
            "Peak_areas",
            "Concentrations",
            "Slope",
            "Intercept",
            "Coefficient_of_determination",
        ]
        self.calibration_df = pd.DataFrame(
            columns=column_names,
            index=[species for species in calibration_input_dict.keys()],
        )
        self.models_dict = {}
        calibration_dict = {}
        for key, value in calibration_input_dict.items():
            calibration = Calibration(
                species=value[0].value,
                peak_area=Data(values=value[1], unit=Unit.NONE),
                concentration=Data(values=value[2], unit=Unit.PERCENTAGE),
            )
            function = linear_model.LinearRegression(fit_intercept=True)
            function.fit(
                np.array(calibration.peak_area.values).reshape(-1, 1),
                np.array(calibration.concentration.values),
            )
            slope, intercept = function.coef_[0], function.intercept_
            coefficient_of_determination = function.score(
                np.array(calibration.peak_area.values).reshape(-1, 1),
                np.array(calibration.concentration.values),
            )
            calibration.slope = Data(
                quantity=Quantity.SLOPE, values=[slope], unit=Unit.PERCENTAGE
            )
            calibration.intercept = Data(
                quantity=Quantity.INTERCEPT,
                values=[intercept],
                unit=Unit.PERCENTAGE,
            )
            calibration.coefficient_of_determination = Data(
                quantity=Quantity.COEFFDET,
                values=[coefficient_of_determination],
                unit=Unit.NONE,
            )
            calibration_dict[key] = calibration
            self.models_dict[key] = function
            self.calibration_df.loc[calibration.species] = [
                calibration.peak_area.values,
                calibration.concentration.values,
                calibration.slope.values[0],
                calibration.intercept.values[0],
                calibration.coefficient_of_determination.values[0],
            ]

        return self.calibration_df, calibration_dict

    # def plot_calibration(self):
    #     i = 1
    #     j = 0
    #     for count, index, row in enumerate(self.calibration_df.iterrows()):
    #         if count % 2 == 0:
    #             j = 2
    #         else:
    #             j = 1
    #         fig, ax = plt.subplots(i, j, figsize=(10, 6))
    #         sns.regplot(
    #             x=row["Concentrations"],
    #             y=row["Peak_areas"],
    #             ci=95,
    #             order=1,
    #             line_kws={
    #                 "label": "Linear regression line: r'$f(x)=' f'{intercept} r'$x+$'f'{sclope}'",
    #                 "color": "m",
    #             },
    #             seed=1,
    #             truncate=False,
    #             label="Original data",
    #             ax=ax[i, j],
    #         )
    #         i += 1

    #         ax.set_xlabel("Peak area")
    #         ax.set_ylabel("Concentration")
    #         # ax.set_xticks([1000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000])
    #         # ax.set_yticks(np.arange(3.0, 10.5, 0.5))
    #         ax.legend(loc="upper left")
    #     file_name = f"calib_plot_{index}.png"
    #     file_path = self._path_to_dataset / file_name
    #     fig.savefig(file_path)

    def calculate_volumetric_fractions(
        self,
        peak_area_dict: dict,
        calibration_df: pd.DataFrame,
    ) -> pd.DataFrame:
        volumetric_fractions_df = pd.DataFrame(
            index=calibration_df.index, columns=["Volumetric_fraction"]
        )
        for species, peak_area in peak_area_dict.items():
            volumetric_fractions_df.loc[species] = (
                peak_area * calibration_df.loc[species][2]
                + calibration_df.loc[species][3]
            )
        return volumetric_fractions_df

    def calculate_conversion_factor(
        self,
        volumetric_fractions_df: pd.DataFrame,
        correction_factors_dict: dict,
    ) -> pd.DataFrame:
        conversion_factor = (
            1
            / (
                (volumetric_fractions_df.loc["H2"][0] / 100)
                / correction_factors_dict["H2"]
                + (
                    1
                    - (volumetric_fractions_df.loc["H2"][0] / 100)
                    + (volumetric_fractions_df.loc["CO"][0]) / 100
                )
                / correction_factors_dict["CO2"]
                + (volumetric_fractions_df.loc["CO"][0] / 100)
                / correction_factors_dict["CO"]
            )
            / correction_factors_dict["CO2"]
        )

        # for key, value in f_corr_dict.items():
        # conversion_factors_df = pd.DataFrame(index=columns='conversion_factors')

        return conversion_factor

    def calculate_real_volumetric_flow(
        self,
        conversion_factor: float,
        measured_volumetric_flow_df: pd.DataFrame,
    ) -> pd.DataFrame:
        real_volumetric_flow_df = measured_volumetric_flow_df["Flow"].multiply(
            conversion_factor
        )
        return real_volumetric_flow_df

    def calculate_volumetric_flow_fractions(
        self,
        real_volumetric_flow: float,
        volumetric_fractions_df: pd.DataFrame,
    ) -> pd.DataFrame:
        rename = {"Volumetric_fraction": "Volumetric_flow_fraction"}
        volumetric_flow_fractions_df = volumetric_fractions_df.multiply(
            real_volumetric_flow
        ).rename(columns=rename)
        return volumetric_flow_fractions_df

    def calcualte_material_flow(
        self,
        volumetric_flow_fractions_df: pd.DataFrame,
    ):
        molecular_volume = 22.41396954
        rename = {"Volumetric_flow_fraction": "Material_flow"}
        material_flow_df = volumetric_flow_fractions_df.divide(
            molecular_volume
        ).rename(columns=rename)
        return material_flow_df

    def calculate_theoretical_material_flow(
        self, initial_current, initial_time, electrode_surface_area
    ):
        positive_initial_current = abs(initial_current)
        current_density = positive_initial_current / electrode_surface_area
        faraday_constant = 96485.3321
        factors = {
            "H2": 2,
            "CO": 2,
            "CO2": 2,
            "CH4": 8,
            "C2H4": 12,
            "C2H6": 16,
        }
        theoretical_material_flow_df = pd.DataFrame(
            index=[species for species in factors.keys()],
            columns=["Theoretical_material_flow"],
        )
        for species, factor in factors.items():
            theoretical_material_flow_df.loc[species] = (
                initial_time / 60 * current_density / 1000
            ) / (factor * faraday_constant)
        return theoretical_material_flow_df

    def calculate_theoretical_amount_of_substance(
        self, initial_current, initial_time, electrode_surface_area
    ):
        positive_initial_current = abs(initial_current)
        current_density = positive_initial_current / electrode_surface_area
        faraday_constant = 96485.3321
        factors = {
            "H2": 2,
            "CO": 2,
            "CO2": 2,
            "CH4": 8,
            "C2H4": 12,
            "C2H6": 16,
        }
        theoretical_theoretical_amount_of_substance_df = pd.DataFrame(
            index=[species for species in factors.keys()],
            columns=["Theoretical_theoretical_amount_of_substance"],
        )
        for species, factor in factors.items():
            theoretical_theoretical_amount_of_substance_df.loc[species] = (
                initial_time * current_density / 1000 * factor
            ) / (2 * faraday_constant)
        return theoretical_theoretical_amount_of_substance_df
