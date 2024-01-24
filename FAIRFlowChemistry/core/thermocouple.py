
from typing import Optional
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .thermocoupletype import ThermocoupleType
from .device import Device


@forge_signature
class Thermocouple(Device):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    thermocouple_type: Optional[ThermocoupleType] = element(
        description="type of thermocouple like J, K and so on.",
        default=None,
        tag="thermocouple_type",
        json_schema_extra=dict(),
    )
