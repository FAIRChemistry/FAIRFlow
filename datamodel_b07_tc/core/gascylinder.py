
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator

from astropy.units import UnitBase

from .equipment import Equipment
from .chemical import Chemical


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
        default="3155c0b011acb68ca77bec7fc9616c770158e2a9"
    )
