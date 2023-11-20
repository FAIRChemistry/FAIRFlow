
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
<<<<<<< HEAD
from .device import Device
from .thermocoupletype import ThermocoupleType
=======


from .thermocoupletype import ThermocoupleType
from .device import Device
>>>>>>> 5e18871 (updated core)


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
<<<<<<< HEAD
        default="01b5fdc2e92add8386e9d335f576018888635f17"
=======
        default="466366e7b75450efb6b154eca033fc469f36e2a4"
>>>>>>> 5e18871 (updated core)
    )
