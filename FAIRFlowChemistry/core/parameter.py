import sdRDM

from typing import Optional, Union
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from astropy.units import UnitBase, Unit
from sdRDM.base.datatypes import UnitType


@forge_signature
class Parameter(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("parameterINDEX"),
        xml="@id",
    )

    value: Optional[float] = Field(
        default=None,
        description="values.",
    )

    unit: Optional[Union[UnitBase, str, UnitType, Unit]] = Field(
        default=None,
        description="unit of the values.",
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="d3517c29138cd9ea80b6c4eb1ceab8a4277254ef"
    )
