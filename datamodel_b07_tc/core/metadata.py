import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .unit import Unit
from .datatype import DataType


@forge_signature
class Metadata(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("metadataINDEX"),
        xml="@id",
    )

    quantity: Optional[str] = Field(
        default=None,
        description="Name of the quantity.",
    )

    data_type: Optional[DataType] = Field(
        default=None,
        description="type of the quantity.",
    )

    mode: Optional[str] = Field(
        default=None,
        description="mode of the qantity.",
    )

    size: Optional[float] = Field(
        default=None,
        description="size of the quantity.",
    )

    unit: Optional[Unit] = Field(
        default=None,
        description="unit of the quantity.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="087d97eb5882e9a8535a8faaabe6baaea7a85f78"
    )
