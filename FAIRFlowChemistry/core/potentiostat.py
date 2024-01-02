
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .measurement import Measurement
from .metadata import Metadata
from .device import Device


@forge_signature
class Potentiostat(Device):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("potentiostatINDEX"),
        xml="@id",
    )

    measurement: Optional[Measurement] = Field(
        description="Measuring Data.",
        default_factory=Measurement,
    )

    metadata: Optional[Metadata] = Field(
        description="Metadata of the Potentiostat.",
        default_factory=Metadata,
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="ddc41b4baadaf8dd1dec5234b201c6f1b4ca8902"
    )
