import sdRDM

import numpy as np
from typing import List, Optional
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from .data import Data


@forge_signature
class Calibration(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("calibrationINDEX"),
        xml="@id",
    )

    peak_areas: Optional[Data] = Field(
        default=Data(),
        description="Recorded peak areas of the individual calibration solutions.",
    )

    concentrations: Optional[Data] = Field(
        default=Data(),
        description="concentrations of the individual calibration solutions.",
    )

    regression_coefficients: List[float] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="Polynomial coefficients in order of increasing degree.",
    )

    degree: Optional[int] = Field(
        default=1,
        description="Degree of regression model.",
    )

    def calibrate(self):
        """
        Calibrate the regression model on seen data
        """

        self.regression_coefficients = np.polynomial.polynomial.polyfit(
            self.peak_areas.values, self.concentrations.values, self.degree
        ).tolist()

    def predict(self, x: list) -> np.ndarray:
        """
        Predict with regression model

        Args:
            x (1D list): New locations for which predictions should be made

        Returns:
           (1D numpy array): Predicted data at new locations
        """

        return np.polynomial.Polynomial(self.regression_coefficients)(np.array(x))
