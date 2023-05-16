
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .measurement import Measurement


@forge_signature
class GCMeasurement(Measurement):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("gcmeasurementINDEX"),
        xml="@id",
    )

    peak_number: Optional[int] = Field(
        default=None,
        description="peak number.",
    )

    retention_time: Optional[float] = Field(
        default=None,
        description="retention time.",
    )

    signal: Optional[float] = Field(
        default=None,
        description="signal of the peak.",
    )

    peak_area: Optional[float] = Field(
        default=None,
        description="peak area.",
    )

    peak_height: Optional[float] = Field(
        default=None,
        description="peak height.",
    )

    peak_area_percentage: Optional[float] = Field(
        default=None,
        description="peak area in percent.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="cc74206c0fc92ce0d0ee24128eddbe51fa614d6a"
    )
