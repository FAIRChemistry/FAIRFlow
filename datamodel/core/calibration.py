import numpy as np
import sdRDM

from sklearn.linear_model import LinearRegression
from typing import Optional
from pydantic import Field, PrivateAttr
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

    regression_model: Optional[LinearRegression] = Field(
        default=LinearRegression(fit_intercept=True),
        description="Linear regression model.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="48482b81b482e9464bf050b2490e5f461bbf3497"
    )

    def calibrate(self):
        """
        Calibrate the regression model on seen data
        """
        self.regression_model.fit( np.array(self.peak_areas.values).reshape(-1, 1), np.array(self.concentrations.values) )