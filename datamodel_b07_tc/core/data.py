import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .unit import Unit
from .quantity import Quantity
from .datatype import DataType


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

    values: List[DataType] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="values.",
    )

    unit: Optional[Unit] = Field(
        default=None,
        description="unit of the values.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="cfa50a71b09fa2d5fb0c474c7a62a01f2acacf98"
    )
