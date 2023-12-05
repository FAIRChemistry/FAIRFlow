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
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="fd42a62a670931da22ba364492bd185f7673ef73"
    )
