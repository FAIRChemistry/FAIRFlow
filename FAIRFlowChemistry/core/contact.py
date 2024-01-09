import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class Contact(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("contactINDEX"),
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

    email: Optional[str] = Field(
        default=None,
        description="The e-mail address of the contact for the Dataset",
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="e456339bee79514bdb0b05626b283e99762b3e06"
    )
