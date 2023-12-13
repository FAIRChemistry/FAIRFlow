import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class Author(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("authorINDEX"),
        xml="@id",
    )

    name: Optional[str] = Field(
        default=None,
        description="full name including given and family name.",
    )

    affiliation: Optional[str] = Field(
        default=None,
        description="organization the author is affiliated to.",
    )

    identifier_scheme: Optional[str] = Field(
        default=None,
        description="Name of the identifier scheme (ORCID, ISNI).",
    )

    identifier: Optional[str] = Field(
        default=None,
        description=(
            "Uniquely identifies an individual author or organization, according to"
            " various schemes."
        ),
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="1bfa14eeb39e4bc915f2ec015be812f5dd1b4bb7"
    )
