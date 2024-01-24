import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from sdRDM.base.datatypes import Unit


@forge_signature
class Parameter(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@db5f6da1081228bb92912b00a9cbad9be469320c#Parameter"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    value: Optional[float] = element(
        description="values.",
        default=None,
        tag="value",
        json_schema_extra=dict(),
    )

    unit: Optional[Unit] = element(
        description="unit of the values.",
        default=None,
        tag="unit",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="db5f6da1081228bb92912b00a9cbad9be469320c"
    )
