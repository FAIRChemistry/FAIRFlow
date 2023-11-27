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

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="8872c248623884be3e946849d19313d400c3d949"
    )
