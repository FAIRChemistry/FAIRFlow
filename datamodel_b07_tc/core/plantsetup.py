import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from .pipingnetworksystem import PipingNetworkSystem
from .equipment import Equipment
from .pipingnetworksegment import PipingNetworkSegment
from .input import Input
from .output import Output
from .pipingcomponent import PipingComponent
from .chemical import Chemical


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

    piping_network_system: List[PipingNetworkSystem] = Field(
        default_factory=ListPlus,
        multiple=True,
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
        default="3155c0b011acb68ca77bec7fc9616c770158e2a9"
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

    def add_to_piping_network_system(
        self,
        piping_component: List[PipingComponent] = ListPlus(),
        piping_network_segment: List[PipingNetworkSegment] = ListPlus(),
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'PipingNetworkSystem' to attribute piping_network_system

        Args:
            id (str): Unique identifier of the 'PipingNetworkSystem' object. Defaults to 'None'.
            piping_component (): Component of a piping network system that is not a pipe, e.g. a valve.. Defaults to ListPlus()
            piping_network_segment (): A piping segment being part of a piping network system.. Defaults to ListPlus()
        """
        params = {
            "piping_component": piping_component,
            "piping_network_segment": piping_network_segment,
        }
        if id is not None:
            params["id"] = id
        self.piping_network_system.append(PipingNetworkSystem(**params))
        return self.piping_network_system[-1]

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
