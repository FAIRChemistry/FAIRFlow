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
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@f4f90b698573ebe018bb7f96d10be4877e4643b3#GenericAttibute"
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
        default="f4f90b698573ebe018bb7f96d10be4877e4643b3"
    )
