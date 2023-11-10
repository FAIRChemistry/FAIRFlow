
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .parameter import Parameter
from .equipment import Equipment


@forge_signature
class MassFlowMeter(Equipment):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("massflowmeterINDEX"),
        xml="@id",
    )

    min_flow: Optional[Parameter] = Field(
        default=Parameter(),
        description="Minimum possible flow rate.",
    )

    max_flow: Optional[Parameter] = Field(
        default=Parameter(),
        description="Maximum possible flow rate.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="b33747e8292297d73d6fe56d3d49a006d78221ac"
    )
