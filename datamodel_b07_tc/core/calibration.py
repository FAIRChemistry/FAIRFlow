import sdRDM

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
        description="Recorded peak areas of the individual calibration solutions.",
        default_factory=Data,
    )

    concentrations: Optional[Data] = Field(
        description="concentrations of the individual calibration solutions.",
        default_factory=Data,
    )

    slope: Optional[Data] = Field(
        description="slopes of the (linear) calibration functions.",
        default_factory=Data,
    )

    intercept: Optional[Data] = Field(
        description="intercept of the (linear) calibration functions.",
        default_factory=Data,
    )

    coefficient_of_determination: Optional[Data] = Field(
        description="coefficients of the (linear) calibration functions.",
        default_factory=Data,
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="fd42a62a670931da22ba364492bd185f7673ef73"
    )
