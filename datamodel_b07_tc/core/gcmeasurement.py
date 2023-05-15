
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .data import Data
from .measurement import Measurement


@forge_signature
class GCMeasurement(Measurement):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("gcmeasurementINDEX"),
        xml="@id",
    )

    retention_times: Optional[Data] = Field(
        default=None,
        description="retention time.",
    )

    peak_areas: Optional[Data] = Field(
        default=None,
        description="peak area.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="a92cd7e4d0326d4eafac9c6c2b73ea481e0b61b8"
    )
