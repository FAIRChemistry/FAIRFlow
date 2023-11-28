import sdRDM

from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class TopicClassification(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("topicclassificationINDEX"),
        xml="@id",
    )

    term: Optional[str] = Field(
        default=None,
        description="Topic or Subject term that is relevant to this Dataset.",
    )

    vocabulary: Optional[str] = Field(
        default=None,
        description=(
            "Provided for specification of the controlled vocabulary in use, e.g.,"
            " LCSH, MeSH, etc."
        ),
    )

    vocabulary_url: Optional[str] = Field(
        default=None,
        description="Specifies the URL location for the full controlled vocabulary.",
    )
