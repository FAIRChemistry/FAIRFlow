import sdRDM

from typing import Optional
from pydantic import Field
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
