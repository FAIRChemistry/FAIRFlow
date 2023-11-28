
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .measurement import Measurement
from .device import Device
from .metadata import Metadata


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
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="6b0b3acd5369750be57859b9eea7d22a6f4a02e5"
    )
