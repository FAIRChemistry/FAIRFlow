import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from .material import Material
from .insulation import Insulation
from .pipingnetworksegment import PipingNetworkSegment
from .pipingcomponent import PipingComponent


@forge_signature
class PipingNetworkSystem(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("pipingnetworksystemINDEX"),
        xml="@id",
    )

    piping_component: List[PipingComponent] = Field(
        default_factory=ListPlus,
        multiple=True,
        description=(
            "Component of a piping network system that is not a pipe, e.g. a valve."
        ),
    )

    piping_network_segment: List[PipingNetworkSegment] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="A piping segment being part of a piping network system.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="07c15acdec1591bdb9141fd4b99f97b3fb251642"
    )

    def add_to_piping_component(
        self,
        manufacturer: Optional[str] = None,
        equipment_type: Optional[str] = None,
        series: Optional[str] = None,
        on_off: Optional[bool] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'PipingComponent' to attribute piping_component

        Args:
            id (str): Unique identifier of the 'PipingComponent' object. Defaults to 'None'.
            manufacturer (): name of the manufacturer of the Piping component.. Defaults to None
            equipment_type (): type given by the manufacturer of the Piping component.. Defaults to None
            series (): the series of the Piping component.. Defaults to None
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
        self.piping_component.append(PipingComponent(**params))
        return self.piping_component[-1]

    def add_to_piping_network_segment(
        self,
        material: Optional[Material] = None,
        inner_diameter: Optional[float] = None,
        outer_diameter: Optional[float] = None,
        length: Optional[int] = None,
        insulation: Optional[Insulation] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'PipingNetworkSegment' to attribute piping_network_segment

        Args:
            id (str): Unique identifier of the 'PipingNetworkSegment' object. Defaults to 'None'.
            material (): material with which the fluid flowing through comes into contact.. Defaults to None
            inner_diameter (): inner diameter of the tubing in mm.. Defaults to None
            outer_diameter (): outer diameter of the tubing in mm.. Defaults to None
            length (): length of the tubing in mm.. Defaults to None
            insulation (): insulation of the tubing.. Defaults to None
        """
        params = {
            "material": material,
            "inner_diameter": inner_diameter,
            "outer_diameter": outer_diameter,
            "length": length,
            "insulation": insulation,
        }
        if id is not None:
            params["id"] = id
        self.piping_network_segment.append(PipingNetworkSegment(**params))
        return self.piping_network_segment[-1]
