import sdRDM

import numpy as np
from typing import Dict, List, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict
from .data import Data


@forge_signature
class Calibration(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    peak_areas: Optional[Data] = element(
        description="recorded peak areas of the individual calibration solutions.",
        default_factory=Data,
        tag="peak_areas",
        json_schema_extra=dict(),
    )

    concentrations: Optional[Data] = element(
        description="concentrations of the individual calibration solutions.",
        default_factory=Data,
        tag="concentrations",
        json_schema_extra=dict(),
    )

    regression_coefficients: List[float] = element(
        description="polynomial coefficients in order of increasing degree.",
        default_factory=ListPlus,
        tag="regression_coefficients",
        json_schema_extra=dict(multiple=True),
    )

    degree: Optional[int] = element(
        description="degree of regression model.",
        default=1,
        tag="degree",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="347b27d91bdf446180753173ad51b018302abcb6"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                (isinstance(i, _Element) for i in value)
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)
        return self

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
