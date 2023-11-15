
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from astropy.units import UnitBase
from .chemical import Chemical
from .equipment import Equipment


@forge_signature
class GasCylinder(Equipment):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("gascylinderINDEX"),
        xml="@id",
    )

    volume: Optional[UnitBase] = Field(
        default=None,
        description="Volume of the Gas cylinder.",
    )

    pressure: Optional[UnitBase] = Field(
        default=None,
        description="Maximum operating pressure of the gas cylinder.",
    )

    Content: Optional[Chemical] = Field(
        default=Chemical(),
        description="Content of the Gas cylinder.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="1acc70cc802e268e3f749491b735d3b53a462c96"
    )
