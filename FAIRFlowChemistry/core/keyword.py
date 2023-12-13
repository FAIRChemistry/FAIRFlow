import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class Keyword(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("keywordINDEX"),
        xml="@id",
    )

    value: Optional[str] = Field(
        default=None,
        description="Key terms that describe important aspects of the Dataset.",
    )

    vocabulary: Optional[str] = Field(
        default=None,
        description=(
            "For the specification of the keyword controlled vocabulary in use, such as"
            " LCSH, MeSH, or others."
        ),
    )

    vocabulary_uri: Optional[str] = Field(
        default=None,
        description=(
            "Keyword vocabulary URI points to the web presence that describes the"
            " keyword vocabulary, if appropriate."
        ),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="9d5388aebe9c91e4babc159076b8b137651e2b53"
    )
