
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .device import Device
from .measurement import Measurement
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
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="8872c248623884be3e946849d19313d400c3d949"
    )
