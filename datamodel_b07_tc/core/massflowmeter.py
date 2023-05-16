
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .device import Device
from .parameter import Parameter


@forge_signature
class MassFlowMeter(Device):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("massflowmeterINDEX"),
        xml="@id",
    )

    min_flow: Optional[Parameter] = Field(
        default=None,
        description="Minimum possible flow rate.",
    )

    max_flow: Optional[Parameter] = Field(
        default=None,
        description="Maximum possible flow rate.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="daa7338c6c1e84bf8cf2e7b2a6e61d55c7eab98d"
    )
