
from typing import Optional
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .device import Device
from .pumptype import PumpType


@forge_signature
class Pump(Device):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    pump_type: Optional[PumpType] = element(
        description="type of the pump.",
        default=None,
        tag="pump_type",
        json_schema_extra=dict(),
    )
