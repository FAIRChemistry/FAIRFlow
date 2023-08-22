import sdRDM

from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator


from .data import Data
from .species import Species


@forge_signature
class Calibration(sdRDM.DataModel):

    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("calibrationINDEX"),
        xml="@id",
    )

    species: Optional[Species] = Field(
        default=None,
        description="Species for which the calibration was performed.",
    )

    peak_area: Optional[Data] = Field(
        default=Data(),
        description="Recorded peak areas of the individual calibration solutions.",
    )

    concentration: Optional[Data] = Field(
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
<<<<<<< Updated upstream

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="8f3ba22c83330e0532dcb7cdb12b205c1f881980"
    )
=======
>>>>>>> Stashed changes
