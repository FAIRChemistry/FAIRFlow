
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

    time: Optional[Data] = Field(
        default=None,
        description="time in seconds.",
    )

    flow_rate: Optional[Data] = Field(
        default=None,
        description="flow rate.",
    )

    second_test: Optional[str] = Field(
        default=None,
        description="second test.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="e243332d34aace2b933a1385915f3b8871a64409"
    )
