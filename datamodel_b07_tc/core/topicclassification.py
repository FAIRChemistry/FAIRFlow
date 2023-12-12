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

    vocab_url: Optional[str] = Field(
        default=None,
        description="Specifies the URL location for the full controlled vocabulary.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="a5c45be8f4f6032b87c9208d1accc55140d9fcd5"
    )
