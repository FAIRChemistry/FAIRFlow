import sdRDM

from typing import Optional, Union
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from sdRDM.base.datatypes import Unit
from datetime import datetime as Datetime
from .datatype import DataType


@forge_signature
class Metadata(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@ecaec8b83d4ad94b6d8a4d0f7be4b76ce6cfa92a#Metadata"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    parameter: Optional[str] = element(
        description="Name of the parameter.",
        default=None,
        tag="parameter",
        json_schema_extra=dict(),
    )

    value: Union[str, float, Datetime, None] = element(
        description="value of the parameter.",
        default=None,
        tag="value",
        json_schema_extra=dict(),
    )

    abbreviation: Optional[str] = element(
        description="abbreviation for the parameter.",
        default=None,
        tag="abbreviation",
        json_schema_extra=dict(),
    )

    data_type: Union[DataType, str, None] = element(
        description="type of the parameter.",
        default=None,
        tag="data_type",
        json_schema_extra=dict(),
    )

    mode: Optional[str] = element(
        description="mode of the parameter. E.g., on and off.",
        default=None,
        tag="mode",
        json_schema_extra=dict(),
    )

    unit: Optional[Unit] = element(
        description="unit of the parameter.",
        default=None,
        tag="unit",
        json_schema_extra=dict(),
    )

    description: Optional[str] = element(
        description="description of the parameter.",
        default=None,
        tag="description",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="ecaec8b83d4ad94b6d8a4d0f7be4b76ce6cfa92a"
    )
