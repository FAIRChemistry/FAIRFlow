import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .data import Data


@forge_signature
class MassFlowRate(sdRDM.DataModel):

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

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="15c1628100dadc5d2ce53ff72a02f247fae78748"
    )
