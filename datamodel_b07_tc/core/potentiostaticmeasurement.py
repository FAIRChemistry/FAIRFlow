
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .measurement import Measurement
from .data import Data


@forge_signature
class PotentiostaticMeasurement(Measurement):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("potentiostaticmeasurementINDEX"),
        xml="@id",
    )

    time: Optional[Data] = Field(
        default=None,
        description="time.",
    )

    voltage: Optional[Data] = Field(
        default=None,
        description="voltage.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="bc26f8048a0681cc23e8e4cf35b3c8bf22fcf044"
    )
