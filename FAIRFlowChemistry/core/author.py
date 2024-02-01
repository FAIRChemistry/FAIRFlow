import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class Author(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@1fe8cd09b86dc6043d0966423f3cb52d5025050d#Author"
    },
):
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
        description="Name of the identifier scheme (ORCID, ISNI).",
        default=None,
        tag="identifier_scheme",
        json_schema_extra=dict(),
    )

    identifier: Optional[str] = element(
        description=(
            "Uniquely identifies an individual author or organization, according to"
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
        default="1fe8cd09b86dc6043d0966423f3cb52d5025050d"
    )
