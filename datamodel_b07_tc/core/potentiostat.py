
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
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="aaa02c13eb4aa0bc5b011edd3375aa60ea3c8955"
    )
