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
class Author(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    name: Optional[str] = element(
        description="full name including given and family name.",
        default=None,
        tag="name",
        json_schema_extra=dict(),
    )

    affiliation: Optional[str] = element(
        description="organization the author is affiliated to.",
        default=None,
        tag="affiliation",
        json_schema_extra=dict(),
    )

    identifier_scheme: Optional[str] = element(
        description="name of the identifier scheme (ORCID, ISNI).",
        default=None,
        tag="identifier_scheme",
        json_schema_extra=dict(),
    )

    identifier: Optional[str] = element(
        description=(
            "unique identifier of an individual author or organization, according to"
            " various schemes."
        ),
        default=None,
        tag="identifier",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="c0afa15b3139d198065f3824cc2033e5ab02f73a"
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
