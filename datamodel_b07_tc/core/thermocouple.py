
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
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="bb0e745ce48c41c1231aa5de1f300ce63fd7a450"
    )
