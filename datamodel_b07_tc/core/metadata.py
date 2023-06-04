import sdRDM

from typing import Optional, Union
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator

from datetime import datetime

from .unit import Unit
from .datatype import DataType


@forge_signature
class Metadata(sdRDM.DataModel):

    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("metadataINDEX"),
        xml="@id",
    )

    parameter: Optional[str] = Field(
        default=None,
        description="Name of the parameter.",
    )

    value: Union[str, float, datetime, None] = Field(
        default=None,
        description="value of the parameter.",
    )

    abbreviation: Optional[str] = Field(
        default=None,
        description="abbreviation for the parameter.",
    )

    data_type: Union[DataType, str, None] = Field(
        default=None,
        description="type of the parameter.",
    )

    mode: Optional[str] = Field(
        default=None,
        description="mode of the parameter. E.g., on and off.",
    )

    unit: Union[Unit, str, None] = Field(
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
        default="5fdd27504705d8dfabdb6a1210039f98b4e65bbb"
    )
