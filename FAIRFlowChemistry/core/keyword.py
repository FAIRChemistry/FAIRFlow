import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class Keyword(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@fc10b75fe304b696b13fdc9d111bd0a4867177cd#Keyword"
    },
):
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
        default="fc10b75fe304b696b13fdc9d111bd0a4867177cd"
    )
