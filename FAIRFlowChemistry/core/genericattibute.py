import sdRDM

from typing import Dict, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict


@forge_signature
class GenericAttibute(sdRDM.DataModel):
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
        default="0ac4b46fc7efe83957d1676773cd61495bf1cdbd"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                (isinstance(i, _Element) for i in value)
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)
        return self
