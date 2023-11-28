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
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="f26c9c00f26a15d920f294f65218aa200dbad222"
    )
