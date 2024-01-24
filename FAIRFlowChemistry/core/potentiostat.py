
from typing import Optional
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .device import Device
from .measurement import Measurement
from .metadata import Metadata


@forge_signature
class Potentiostat(Device):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    measurement: Optional[Measurement] = element(
        description="Measuring Data.",
        default_factory=Measurement,
        tag="measurement",
        json_schema_extra=dict(),
    )

    metadata: Optional[Metadata] = element(
        description="Metadata of the Potentiostat.",
        default_factory=Metadata,
        tag="metadata",
        json_schema_extra=dict(),
    )
