import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from .output import Output
from .input import Input
from .pipingnetworksystem import PipingNetworkSystem
from .chemical import Chemical
from .equipment import Equipment


@forge_signature
class PlantSetup(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("plantsetupINDEX"),
        xml="@id",
    )

    equipment: List[Equipment] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="bla",
    )

    piping_network_system: Optional[PipingNetworkSystem] = Field(
        default=PipingNetworkSystem(),
        description="bla",
    )

    input: List[Input] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="bla",
    )

    output: List[Output] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="bla",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="b33747e8292297d73d6fe56d3d49a006d78221ac"
    )

    def add_to_equipment(
        self,
        manufacturer: Optional[str] = None,
        equipment_type: Optional[str] = None,
        series: Optional[str] = None,
        on_off: Optional[bool] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Equipment' to attribute equipment

        Args:
            id (str): Unique identifier of the 'Equipment' object. Defaults to 'None'.
            manufacturer (): name of the manufacturer of the equipment.. Defaults to None
            equipment_type (): type given by the manufacturer of the equipment.. Defaults to None
            series (): the series of the equipment.. Defaults to None
            on_off (): operational mode of the flow module. True is on and False is off.. Defaults to None
        """
        params = {
            "manufacturer": manufacturer,
            "equipment_type": equipment_type,
            "series": series,
            "on_off": on_off,
        }
        if id is not None:
            params["id"] = id
        self.equipment.append(Equipment(**params))
        return self.equipment[-1]

    def add_to_input(
        self, component: List[Chemical] = ListPlus(), id: Optional[str] = None
    ) -> None:
        """
        This method adds an object of type 'Input' to attribute input

        Args:
            id (str): Unique identifier of the 'Input' object. Defaults to 'None'.
            component (): component of the output fluid.. Defaults to ListPlus()
        """
        params = {"component": component}
        if id is not None:
            params["id"] = id
        self.input.append(Input(**params))
        return self.input[-1]

    def add_to_output(
        self, component: List[Chemical] = ListPlus(), id: Optional[str] = None
    ) -> None:
        """
        This method adds an object of type 'Output' to attribute output

        Args:
            id (str): Unique identifier of the 'Output' object. Defaults to 'None'.
            component (): component of the output fluid.. Defaults to ListPlus()
        """
        params = {"component": component}
        if id is not None:
            params["id"] = id
        self.output.append(Output(**params))
        return self.output[-1]
