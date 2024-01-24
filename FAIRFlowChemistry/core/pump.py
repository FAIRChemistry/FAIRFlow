
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
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@46cef31442ba9e52c957dc3a77a7bf5a64326c1e#Pump"
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
        default="46cef31442ba9e52c957dc3a77a7bf5a64326c1e"
    )
