import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class GenericAttibute(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@2430ed60950545d51f2fa235656907e21e8d3ac4#GenericAttibute"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    name: Optional[str] = element(
        description="bla.",
        default=None,
        tag="name",
        json_schema_extra=dict(),
    )

    attribute_uri: Optional[str] = element(
        description="bla.",
        default=None,
        tag="attribute_uri",
        json_schema_extra=dict(),
    )

    value: Optional[str] = element(
        description="bla.",
        default=None,
        tag="value",
        json_schema_extra=dict(),
    )

    format: Optional[str] = element(
        description="bla.",
        default=None,
        tag="format",
        json_schema_extra=dict(),
    )

    units: Optional[str] = element(
        description="bla.",
        default=None,
        tag="units",
        json_schema_extra=dict(),
    )

    units_uri: Optional[str] = element(
        description="bla",
        default=None,
        tag="units_uri",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="2430ed60950545d51f2fa235656907e21e8d3ac4"
    )
