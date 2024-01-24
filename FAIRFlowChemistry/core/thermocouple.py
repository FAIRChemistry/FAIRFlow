
from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .device import Device
from .thermocoupletype import ThermocoupleType


@forge_signature
class Thermocouple(
    Device,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@f7accf3054d687b0e59ef5bd04786fc2617e0353#Thermocouple"
    },
):
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
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="f7accf3054d687b0e59ef5bd04786fc2617e0353"
    )
