import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .material import Material


@forge_signature
class Insulation(sdRDM.DataModel):

    """"""

    id: str = Field(
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
        default="daa7338c6c1e84bf8cf2e7b2a6e61d55c7eab98d"
    )
