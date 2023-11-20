
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .pipingcomponent import PipingComponent


@forge_signature
class Valve(PipingComponent):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("valveINDEX"),
        xml="@id",
    )

    valve_type: Optional[str] = Field(
        default=None,
        description="Type of valve, e.g. 3-way ball valve.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="1acc70cc802e268e3f749491b735d3b53a462c96"
    )
