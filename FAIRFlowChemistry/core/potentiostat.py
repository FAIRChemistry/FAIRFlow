
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .device import Device
from .metadata import Metadata
from .measurement import Measurement


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
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="bf557ce8e1909bacc11454021c872d74be597f4f"
    )
