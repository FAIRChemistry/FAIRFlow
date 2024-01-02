
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
        default="8b7eacb04935747b31b603de5a7dd9dc8a26d3f7"
    )
