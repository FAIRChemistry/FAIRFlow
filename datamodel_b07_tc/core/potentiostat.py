
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .equipment import Equipment
from .measurement import Measurement
from .metadata import Metadata


@forge_signature
class Potentiostat(Equipment):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("potentiostatINDEX"),
        xml="@id",
    )

    measurement: Optional[Measurement] = Field(
        default=Measurement(),
        description="Measuring Data.",
    )

    metadata: Optional[Metadata] = Field(
        default=Metadata(),
        description="Metadata of the Potentiostat.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="753f0527c5fbcbed77c29fa79bfd166eb495c1d8"
    )
