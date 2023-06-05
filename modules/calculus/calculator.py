import os
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from datamodel_b07_tc.core.dataset import Dataset
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
        dataset: Dataset,
    ) -> pd.DataFrame:
        d = dataset
        c = d.experiments[-1].calculations

        _col = ["slope", "intercept", "coef_det"]
        # _n = [n for n in _cali.keys()]
        cali_result_df = pd.DataFrame(
            # index=_n,
            columns=_col,
        )

        for calibration in c.calibrations:
            species = calibration.species
            peak_areas = calibration.peak_area[0].values
            concentrations = calibration.concentration[0].values
            f = linear_model.LinearRegression(fit_intercept=True)
            f.fit(
                np.array(peak_areas).reshape(-1, 1),
                np.array(concentrations),
            )
            slope, intercept = f.coef_[0], f.intercept_
            coef_det = f.score(
                np.array(peak_areas).reshape(-1, 1),
                np.array(concentrations),
            )
            cali_result_df.loc[species] = [slope, intercept, coef_det]
            calibration.slope = Data(
                quantity=Quantity.SLOPE, values=[slope], unit=Unit.PERCENTAGE
            )
            calibration.intercept = Data(
                quantity=Quantity.INTERCEPT,
                values=[intercept],
                unit=Unit.PERCENTAGE,
            )
            calibration.coefficient_of_determination = Data(
                quantity=Quantity.COEFFDET, values=[coef_det], unit=Unit.NONE
            )

        return cali_result_df, d

    def calc_vol_frac(
        self,
        peak_area_dict: dict,
        calibration_result_df: pd.DataFrame,
    ) -> pd.DataFrame:
        _r_df = calibration_result_df
        _p = peak_area_dict
        _vol_frac_df = pd.DataFrame(
            index=_r_df.index, columns=["volume_fraction"]
        )
        for key, value in _p.items():
            _vol_frac_df.loc[key] = (
                value * _r_df.loc[key][0] + _r_df.loc[key][1]
            )
        return _vol_frac_df

    def calculate_conversion_factor(
        self,
        volume_fractions: pd.DataFrame,
        correction_factors: dict,
    ) -> pd.DataFrame:
        _vol_frac_df = volume_fractions
        f_corr_dict = correction_factors
        f_conv = (
            1
            / (
                (_vol_frac_df.loc["H2"][0] / 100) / f_corr_dict["H2"]
                + (
                    1
                    - (_vol_frac_df.loc["H2"][0] / 100)
                    + (_vol_frac_df.loc["CO"][0]) / 100
                )
                / f_corr_dict["CO2"]
                + (_vol_frac_df.loc["CO"][0] / 100) / f_corr_dict["CO"]
            )
            / f_corr_dict["CO2"]
        )

        # for key, value in f_corr_dict.items():
        # conversion_factors_df = pd.DataFrame(index=columns='conversion_factors')

        return f_conv

    def calculate_vol_flow_r(
        self, conversion_factor: float, volumetric_flow_measured: pd.DataFrame
    ) -> pd.DataFrame:
        f_conv = conversion_factor
        _vol_flow_m = volumetric_flow_measured
        _vol_flow_r = _vol_flow_m.multiply(f_conv)
        return _vol_flow_r

    def plot(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.regplot(
            x=self._p,
            y=self.c,
            ci=95,
            order=1,
            line_kws={
                "label": "Linear regression line: r'$f(x)=' f'{intercept} r'$x+$'f'{sclope}'",
                "color": "m",
            },
            seed=1,
            truncate=False,
            label="Original data",
        )
        ax.set_xlabel("Peak area")
        ax.set_ylabel("Concentration")
        # ax.set_xticks([1000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000])
        # ax.set_yticks(np.arange(3.0, 10.5, 0.5))
        ax.legend(loc="upper left")
        fig.savefig(self.path_to_dataset + "/" + f"calib_plot_{self._n}.png")
