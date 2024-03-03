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
class RelatedPublication(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    citation: Optional[str] = element(
        description="full bibliographic citation for this related publication.",
        default=None,
        tag="citation",
        json_schema_extra=dict(),
    )

    id_type: Optional[str] = element(
        description=(
            "type of digital identifier used for this publication, e.g., digital object"
            " identifier (DOI)."
        ),
        default=None,
        tag="id_type",
        json_schema_extra=dict(),
    )

    id_number: Optional[str] = element(
        description="identifier for the selected ID type.",
        default=None,
        tag="id_number",
        json_schema_extra=dict(),
    )

    url: Optional[str] = element(
        description=(
            "link to the publication web page, e.g., journal article page, archive"
            " record page, or other."
        ),
        default=None,
        tag="url",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="776c01c6d4f826efbd50d299dde774d1201156d1"
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
