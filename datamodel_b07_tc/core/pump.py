
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .pumptype import PumpType
from .device import Device


@forge_signature
class Pump(Device):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("pumpINDEX"),
        xml="@id",
    )

    pump_type: Optional[PumpType] = Field(
        default=None,
        description="type of the pump.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="a471134fc95f6210b145affe01f705a766fd9b50"
    )
