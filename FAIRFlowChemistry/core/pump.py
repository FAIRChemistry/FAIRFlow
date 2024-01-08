
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
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="b43287a9337e1abbe0f20892f8911c112fccc4f3"
    )
