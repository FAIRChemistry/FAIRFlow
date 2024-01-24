import sdRDM

from typing import Optional
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


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
