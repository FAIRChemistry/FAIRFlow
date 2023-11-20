import sdRDM

import numpy as np
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from sklearn import linear_model
from .quantity import Quantity
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

    slope: Optional[Data] = Field(
        default=Data(),
        description="slopes of the (linear) calibration functions.",
    )

    intercept: Optional[Data] = Field(
        default=Data(),
        description="intercept of the (linear) calibration functions.",
    )

    coefficient_of_determination: Optional[Data] = Field(
        default=Data(),
        description="coefficients of the (linear) calibration functions.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="01b5fdc2e92add8386e9d335f576018888635f17"
    )

    def calibrate(self):
        peak_areas = np.array(self.peak_areas.values).reshape(-1, 1)
        concentration = np.array(self.concentrations.values)
        function = linear_model.LinearRegression(fit_intercept=True)
        function.fit(peak_areas, concentration)
        slope, intercept = function.coef_[0], function.intercept_
        coefficient_of_determination = function.score(peak_areas, concentration)
        self.slope = Data(quantity=Quantity.SLOPE.value, values=[slope], unit="%")
        self.intercept = Data(
            quantity=Quantity.INTERCEPT.value,
            values=[intercept],
            unit="%",
        )
        self.coefficient_of_determination = Data(
            quantity=Quantity.COEFFDET.value,
            values=[coefficient_of_determination],
            unit=None,
        )
        # def calibration_parameters():
        #     return
