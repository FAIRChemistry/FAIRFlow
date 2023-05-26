
from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator


from .device import Device
from .thermocoupletype import ThermocoupleType


@forge_signature
class Thermocouple(Device):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("thermocoupleINDEX"),
        xml="@id",
    )

    thermocouple_type: Optional[ThermocoupleType] = Field(
        default=None,
        description="type of thermocouple like J, K and so on.",
    )
