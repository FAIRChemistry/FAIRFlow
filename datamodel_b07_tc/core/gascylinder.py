
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
        description="Content of the Gas cylinder.",
        default_factory=Chemical,
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="fd42a62a670931da22ba364492bd185f7673ef73"
    )
