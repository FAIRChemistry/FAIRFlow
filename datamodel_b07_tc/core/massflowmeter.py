
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
        default="cddc89d9dbce3fa43a4452496cfe853bc838a6ed"
    )
