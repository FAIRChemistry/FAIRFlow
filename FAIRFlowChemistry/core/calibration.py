import sdRDM

import numpy as np
from typing import List, Optional
from pydantic import Field, PrivateAttr
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
        description="Recorded peak areas of the individual calibration solutions.",
        default_factory=Data,
    )

    concentrations: Optional[Data] = Field(
        description="concentrations of the individual calibration solutions.",
        default_factory=Data,
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
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="b43287a9337e1abbe0f20892f8911c112fccc4f3"
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
