
from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator
from .device import Device
from .parameter import Parameter


@forge_signature
class MassFlowMeter(Device):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("massflowmeterINDEX"),
        xml="@id",
    )

    min_flow: Optional[Parameter] = Field(
        default=Parameter(),
        description="Minimum possible flow rate.",
    )

    max_flow: Optional[Parameter] = Field(
        default=Parameter(),
        description="Maximum possible flow rate.",
    )
