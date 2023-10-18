import sdRDM

from typing import Optional, Union
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from datetime import datetime as Datetime
from astropy.units import UnitBase
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

    value: Union[str, float, Datetime, None] = Field(
        default=None,
        description="value of the parameter.",
    )

    abbreviation: Optional[str] = Field(
        default=None,
        description="abbreviation for the parameter.",
    )

    type: Optional[str] = Field(
        default=None,
        description="type of the parameter, e.g. a quantity, a toggle, a label.",
    )

    data_type: Optional[DataType] = Field(
        default=None,
        description="type of the data, e.g. string, float, bool.",
    )

    mode: Optional[str] = Field(
        default=None,
        description="mode of the parameter. E.g., on and off.",
    )

    unit: Optional[UnitBase] = Field(
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
        default="3155c0b011acb68ca77bec7fc9616c770158e2a9"
    )
