import sdRDM

from typing import Optional, Union, List
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from datetime import datetime as Datetime
from astropy.units import UnitBase
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

    unit: Optional[UnitBase] = Field(
        default=None,
        description="unit of the values.",
    )
