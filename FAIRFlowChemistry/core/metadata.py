import sdRDM

from typing import Optional, Union
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from astropy.units import UnitBase, Unit
from sdRDM.base.datatypes import UnitType
from datetime import datetime as Datetime
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

    data_type: Union[DataType, str, None] = Field(
        default=None,
        description="type of the parameter.",
    )

    mode: Optional[str] = Field(
        default=None,
        description="mode of the parameter. E.g., on and off.",
    )

    unit: Optional[Union[UnitBase, str, UnitType, Unit]] = Field(
        default=None,
        description="unit of the parameter.",
    )

    description: Optional[str] = Field(
        default=None,
        description="description of the parameter.",
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="b43287a9337e1abbe0f20892f8911c112fccc4f3"
    )
