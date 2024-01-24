
from typing import Optional
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .device import Device
from .parameter import Parameter


@forge_signature
class MassFlowMeter(Device):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    min_flow: Optional[Parameter] = element(
        description="Minimum possible flow rate.",
        default_factory=Parameter,
        tag="min_flow",
        json_schema_extra=dict(),
    )

    max_flow: Optional[Parameter] = element(
        description="Maximum possible flow rate.",
        default_factory=Parameter,
        tag="max_flow",
        json_schema_extra=dict(),
    )
