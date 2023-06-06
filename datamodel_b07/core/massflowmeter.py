
from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator


from .parameter import Parameter
from .device import Device


@forge_signature
class MassFlowMeter(Device):

    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("massflowmeterINDEX"),
        xml="@id",
    )

    min_flow: Optional[Parameter] = Field(
        default=None,
        description="Minimum possible flow rate.",
    )

    max_flow: Optional[Parameter] = Field(
        default=None,
        description="Maximum possible flow rate.",
    )
