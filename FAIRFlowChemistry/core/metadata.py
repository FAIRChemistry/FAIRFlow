import sdRDM

from typing import Dict, Optional, Union
from uuid import uuid4
from pydantic import PrivateAttr, model_validator
from pydantic_xml import attr, element
from lxml.etree import _Element

from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.base.datatypes import Unit
from sdRDM.tools.utils import elem2dict


from sdRDM.base.datatypes import Unit
from datetime import datetime as Datetime

from .datatype import DataType


@forge_signature
class Metadata(
    sdRDM.DataModel,
    search_mode="unordered",
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    parameter: Optional[str] = element(
        description="name of the parameter.",
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

    data_type: Optional[DataType] = element(
        description="type of the parameter.",
        default=None,
        tag="data_type",
        json_schema_extra=dict(),
    )

    mode: Optional[str] = element(
        description="mode of the parameter. e.g., on and off.",
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
        default="https://github.com/FAIRChemistry/FAIRFlow"
    )
    _commit: Optional[str] = PrivateAttr(
        default="e8eb42f3ed30a3b47a5f17238ca156f6ff6d5e4b"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                isinstance(i, _Element) for i in value
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)

        return self
