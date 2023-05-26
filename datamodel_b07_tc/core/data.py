import sdRDM

from typing import Optional, Union, List
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator

from datetime import datetime

from .quantity import Quantity
from .unit import Unit


@forge_signature
class Data(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("dataINDEX"),
        xml="@id",
    )

    quantity: Optional[Quantity] = Field(
        default=None,
        description="quantity of a value.",
    )

    values: List[Union[float, str, datetime]] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="values.",
    )

    unit: Optional[Unit] = Field(
        default=None,
        description="unit of the values.",
    )
