import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class RelatedPublication(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@2142e14e0bb639468af89bac2b4b7b5dbd2087b1#RelatedPublication"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    citation: Optional[str] = element(
        description="The full bibliographic citation for this related publication.",
        default=None,
        tag="citation",
        json_schema_extra=dict(),
    )

    id_type: Optional[str] = element(
        description=(
            "The type of digital identifier used for this publication (e.g., Digital"
            " Object Identifier (DOI))."
        ),
        default=None,
        tag="id_type",
        json_schema_extra=dict(),
    )

    id_number: Optional[str] = element(
        description="'The identifier for the selected ID type.'",
        default=None,
        tag="id_number",
        json_schema_extra=dict(),
    )

    url: Optional[str] = element(
        description=(
            "'Link to the publication web page (e.g., journal article page, archive"
            " record page, or other)."
        ),
        default=None,
        tag="url",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="2142e14e0bb639468af89bac2b4b7b5dbd2087b1"
    )
