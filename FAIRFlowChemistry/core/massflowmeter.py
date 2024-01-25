
from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .device import Device
from .parameter import Parameter


@forge_signature
class MassFlowMeter(
    Device,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@fc10b75fe304b696b13fdc9d111bd0a4867177cd#MassFlowMeter"
    },
):
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
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="fc10b75fe304b696b13fdc9d111bd0a4867177cd"
    )
