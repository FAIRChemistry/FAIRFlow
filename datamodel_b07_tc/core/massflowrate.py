
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .measurement import Measurement
from .data import Data


@forge_signature
class MassFlowRate(Measurement):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("massflowrateINDEX"),
        xml="@id",
    )

    datetime: Optional[float] = Field(
        default=None,
        description="date and time of the mass flow rate measurement.",
    )

    time: Optional[Data] = Field(
        default=None,
        description="time in seconds.",
    )

    signal: Optional[Data] = Field(
        default=None,
        description="signal of the mass flow rate measurement.",
    )

    flow_rate: Optional[Data] = Field(
        default=None,
        description="flow rate.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="f89366840d5168fcd2c896892a68b9d2b571126a"
    )
