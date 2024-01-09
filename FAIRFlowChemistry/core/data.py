import sdRDM

from typing import Optional, Union, List
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from astropy.units import UnitBase, Unit
from sdRDM.base.datatypes import UnitType
from datetime import datetime as Datetime
from .quantity import Quantity


@forge_signature
class Data(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("dataINDEX"),
        xml="@id",
    )

    quantity: Optional[Quantity] = Field(
        default=None,
        description="quantity of a value.",
    )

    values: List[Union[float, str, Datetime]] = Field(
        default_factory=ListPlus,
        multiple=True,
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
        default="ef81b78015477a06bc88e5dd78879b337a8d9c2e"
    )
