import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .insulation import Insulation
from .material import Material


@forge_signature
class Tubing(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("tubingINDEX"),
        xml="@id",
    )

    material: Optional[Material] = Field(
        default=None,
        description="material with which the fluid flowing through comes into contact.",
    )

    inner_diameter: Optional[float] = Field(
        default=None,
        description="inner diameter of the tubing in mm.",
    )

    outer_diameter: Optional[float] = Field(
        default=None,
        description="outer diameter of the tubing in mm.",
    )

    length: Optional[int] = Field(
        default=None,
        description="length of the tubing in mm.",
    )

    insulation: Optional[Insulation] = Field(
        default=None,
        description="insulation of the tubing.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="e7fa7c7530bb346a7692be1c5baa472556377a9f"
    )
