
from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .device import Device
from .massflowrate import MassFlowRate
from .parameter import Parameter
from .data import Data


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

    mass_flow_rates: List[MassFlowRate] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="Mass flow rate.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="15c1628100dadc5d2ce53ff72a02f247fae78748"
    )

    def add_to_mass_flow_rates(
        self,
        time: Optional[Data] = None,
        flow_rate: Optional[Data] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'MassFlowRate' to attribute mass_flow_rates

        Args:
            id (str): Unique identifier of the 'MassFlowRate' object. Defaults to 'None'.
            time (): time in seconds.. Defaults to None
            flow_rate (): flow rate.. Defaults to None
        """

        params = {
            "time": time,
            "flow_rate": flow_rate,
        }

        if id is not None:
            params["id"] = id

        self.mass_flow_rates.append(MassFlowRate(**params))
