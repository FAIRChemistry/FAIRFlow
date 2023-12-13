import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class TopicClassification(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("topicclassificationINDEX"),
        xml="@id",
    )

    value: Optional[str] = Field(
        default=None,
        description="Topic or Subject term that is relevant to this Dataset.",
    )

    vocab: Optional[str] = Field(
        default=None,
        description=(
            "Provided for specification of the controlled vocabulary in use, e.g.,"
            " LCSH, MeSH, etc."
        ),
    )

    vocab_uri: Optional[str] = Field(
        default=None,
        description="Specifies the URI location for the full controlled vocabulary.",
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="bf557ce8e1909bacc11454021c872d74be597f4f"
    )
