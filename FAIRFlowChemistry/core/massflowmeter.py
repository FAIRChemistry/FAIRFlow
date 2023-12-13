
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .parameter import Parameter
from .device import Device


@forge_signature
class MassFlowMeter(Device):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("massflowmeterINDEX"),
        xml="@id",
    )

    min_flow: Optional[Parameter] = Field(
        description="Minimum possible flow rate.",
        default_factory=Parameter,
    )

    max_flow: Optional[Parameter] = Field(
        description="Maximum possible flow rate.",
        default_factory=Parameter,
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="9d5388aebe9c91e4babc159076b8b137651e2b53"
    )
