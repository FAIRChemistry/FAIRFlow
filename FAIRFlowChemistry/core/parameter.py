import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from astropy.units import UnitBase


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

    unit: Optional[UnitBase] = Field(
        default=None,
        description="unit of the values.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="b280844bc9acb4b64bd3d16d0996bffcd6087e9e"
    )
