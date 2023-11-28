
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .device import Device
from .pumptype import PumpType


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
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="e71182674108fd2e5c98cc34924822982a11ad53"
    )
