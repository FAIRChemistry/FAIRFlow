import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .material import Material


@forge_signature
class Insulation(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("insulationINDEX"),
        xml="@id",
    )

    thickness: Optional[float] = Field(
        default=None,
        description="diameter of the insulating layer in mm.",
    )

    material: Optional[Material] = Field(
        default=None,
        description="insulating material",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="471329cc838d1776fca25a8ea45e5ff4708492f3"
    )
