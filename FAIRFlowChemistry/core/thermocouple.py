
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .device import Device
from .thermocoupletype import ThermocoupleType


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
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="b280844bc9acb4b64bd3d16d0996bffcd6087e9e"
    )
