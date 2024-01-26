
from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .pumptype import PumpType
from .device import Device


@forge_signature
class Pump(
    Device,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@ecaec8b83d4ad94b6d8a4d0f7be4b76ce6cfa92a#Pump"
    },
):
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
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="ecaec8b83d4ad94b6d8a4d0f7be4b76ce6cfa92a"
    )
