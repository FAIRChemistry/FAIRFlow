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

    parameter: Optional[str] = Field(
        default=None,
        description="Name of the parameter.",
    )

    abbreviation: Optional[str] = Field(
        default=None,
        description="abbreviation for the parameter.",
    )

    data_type: Optional[DataType] = Field(
        default=None,
        description="type of the parameter.",
    )

    mode: Optional[str] = Field(
        default=None,
        description="mode of the parameter. E.g., on and off.",
    )

    size: Optional[float] = Field(
        default=None,
        description="size of the parameter.",
    )

    unit: Optional[Unit] = Field(
        default=None,
        description="unit of the parameter.",
    )

    description: Optional[str] = Field(
        default=None,
        description="description of the parameter.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="e824f185724b28508edb41513f76000bd0fe3798"
    )
