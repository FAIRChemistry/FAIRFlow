import sdRDM

from typing import Optional, Union, List
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from datetime import datetime as Datetime
from sdRDM.base.datatypes import Unit
from .quantity import Quantity


@forge_signature
class Data(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@db5f6da1081228bb92912b00a9cbad9be469320c#Data"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    quantity: Optional[Quantity] = element(
        description="quantity of a value.",
        default=None,
        tag="quantity",
        json_schema_extra=dict(),
    )

    values: List[Union[float, str, Datetime]] = wrapped(
        "values",
        element(
            description="values.",
            default_factory=ListPlus,
            tag="float",
            json_schema_extra=dict(multiple=True),
        ),
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
