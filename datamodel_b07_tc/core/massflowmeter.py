
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .parameter import Parameter
from .device import Device


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
        default="0c60f2b0a6c35d66c401c995ad1e9a5a8c126b0f"
    )
