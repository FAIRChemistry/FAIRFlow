
from typing import Optional
from pydantic import Field
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
<<<<<<< Updated upstream

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="8f3ba22c83330e0532dcb7cdb12b205c1f881980"
    )
=======
>>>>>>> Stashed changes
