
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
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="fd42a62a670931da22ba364492bd185f7673ef73"
    )
