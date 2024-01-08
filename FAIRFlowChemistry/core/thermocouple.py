
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .thermocoupletype import ThermocoupleType
from .device import Device


@forge_signature
class Thermocouple(Device):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("thermocoupleINDEX"),
        xml="@id",
    )

    thermocouple_type: Optional[ThermocoupleType] = Field(
        default=None,
        description="type of thermocouple like J, K and so on.",
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="b43287a9337e1abbe0f20892f8911c112fccc4f3"
    )
