
from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .metadata import Metadata
from .device import Device
from .measurement import Measurement


@forge_signature
class Potentiostat(
    Device,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@1fe8cd09b86dc6043d0966423f3cb52d5025050d#Potentiostat"
    },
):
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
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="1fe8cd09b86dc6043d0966423f3cb52d5025050d"
    )
