import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class Device(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@3206d61a7ef1fb8aaa8971863b6ab25925c3e134#Device"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    manufacturer: Optional[str] = element(
        description="name of the manufacturer of the device.",
        default=None,
        tag="manufacturer",
        json_schema_extra=dict(),
    )

    device_type: Optional[str] = element(
        description="type given by the manufacturer of the device.",
        default=None,
        tag="device_type",
        json_schema_extra=dict(),
    )

    series: Optional[str] = element(
        description="the series of the device.",
        default=None,
        tag="series",
        json_schema_extra=dict(),
    )

    on_off: Optional[bool] = element(
        description="operational mode of the flow module. True is on and False is off.",
        default=None,
        tag="on_off",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="3206d61a7ef1fb8aaa8971863b6ab25925c3e134"
    )
