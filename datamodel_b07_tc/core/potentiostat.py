
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
        default=Measurement(),
        description="Measuring Data.",
    )

    metadata: Optional[Metadata] = Field(
        default=Metadata(),
        description="Metadata of the Potentiostat.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="4b36a4f7384315a81558843c6cc801b24c0c950f"
    )
