import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .material import Material
from .insulation import Insulation


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
        description="insulation of the tubing.",
        default_factory=Insulation,
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="9d5388aebe9c91e4babc159076b8b137651e2b53"
    )
