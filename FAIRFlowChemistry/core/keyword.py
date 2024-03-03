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
class Keyword(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    value: Optional[str] = element(
        description="Key terms that describe important aspects of the Dataset.",
        default=None,
        tag="value",
        json_schema_extra=dict(),
    )

    vocabulary: Optional[str] = element(
        description=(
            "For the specification of the keyword controlled vocabulary in use, such as"
            " LCSH, MeSH, or others."
        ),
        default=None,
        tag="vocabulary",
        json_schema_extra=dict(),
    )

    vocabulary_uri: Optional[str] = element(
        description=(
            "Keyword vocabulary URI points to the web presence that describes the"
            " keyword vocabulary, if appropriate."
        ),
        default=None,
        tag="vocabulary_uri",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="f8cdbee59156292c0dda1a7171efeb7a002d7a55"
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
