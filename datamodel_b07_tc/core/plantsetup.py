import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .tubing import Tubing
from .insulation import Insulation
from .material import Material
from .device import Device
from .output import Output
from .input import Input
from .chemical import Chemical


@forge_signature
class PlantSetup(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("plantsetupINDEX"),
        xml="@id",
    )

    devices: List[Device] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="bla",
    )

    tubing: List[Tubing] = Field(
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
        default="f89366840d5168fcd2c896892a68b9d2b571126a"
    )

    def add_to_devices(
        self,
        manufacturer: Optional[str] = None,
        device_type: Optional[str] = None,
        series: Optional[str] = None,
        on_off: Optional[bool] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Device' to attribute devices

        Args:
            id (str): Unique identifier of the 'Device' object. Defaults to 'None'.
            manufacturer (): name of the manufacturer of the device.. Defaults to None
            device_type (): type given by the manufacturer of the device.. Defaults to None
            series (): the series of the device.. Defaults to None
            on_off (): operational mode of the flow module. True is on and False is off.. Defaults to None
        """

        params = {
            "manufacturer": manufacturer,
            "device_type": device_type,
            "series": series,
            "on_off": on_off,
        }

        if id is not None:
            params["id"] = id

        self.devices.append(Device(**params))

    def add_to_tubing(
        self,
        material: Optional[Material] = None,
        inner_diameter: Optional[float] = None,
        outer_diameter: Optional[float] = None,
        length: Optional[int] = None,
        insulation: Optional[Insulation] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Tubing' to attribute tubing

        Args:
            id (str): Unique identifier of the 'Tubing' object. Defaults to 'None'.
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

        self.tubing.append(Tubing(**params))

    def add_to_input(
        self, component: List[Chemical] = ListPlus(), id: Optional[str] = None
    ) -> None:
        """
        This method adds an object of type 'Input' to attribute input

        Args:
            id (str): Unique identifier of the 'Input' object. Defaults to 'None'.
            component (): component of the output fluid.. Defaults to ListPlus()
        """

        params = {
            "component": component,
        }

        if id is not None:
            params["id"] = id

        self.input.append(Input(**params))

    def add_to_output(
        self, component: List[Chemical] = ListPlus(), id: Optional[str] = None
    ) -> None:
        """
        This method adds an object of type 'Output' to attribute output

        Args:
            id (str): Unique identifier of the 'Output' object. Defaults to 'None'.
            component (): component of the output fluid.. Defaults to ListPlus()
        """

        params = {
            "component": component,
        }

        if id is not None:
            params["id"] = id

        self.output.append(Output(**params))
