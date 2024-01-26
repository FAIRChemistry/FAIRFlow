
from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .metadata import Metadata
from .measurement import Measurement
from .device import Device


@forge_signature
class Potentiostat(
    Device,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@ecaec8b83d4ad94b6d8a4d0f7be4b76ce6cfa92a#Potentiostat"
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
        default="ecaec8b83d4ad94b6d8a4d0f7be4b76ce6cfa92a"
    )
