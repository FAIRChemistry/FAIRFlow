import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class PipingComponent(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("pipingcomponentINDEX"),
        xml="@id",
    )

    manufacturer: Optional[str] = Field(
        default=None,
        description="name of the manufacturer of the Piping component.",
    )

    equipment_type: Optional[str] = Field(
        default=None,
        description="type given by the manufacturer of the Piping component.",
    )

    series: Optional[str] = Field(
        default=None,
        description="the series of the Piping component.",
    )

    on_off: Optional[bool] = Field(
        default=None,
        description="operational mode of the flow module. True is on and False is off.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="3155c0b011acb68ca77bec7fc9616c770158e2a9"
    )
