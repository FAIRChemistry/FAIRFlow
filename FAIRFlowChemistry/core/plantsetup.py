import sdRDM

from typing import List, Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from .reactantrole import ReactantRole
from .device import Device
from .stoichiometry import Stoichiometry
from .tubing import Tubing, Insulation
from .chemical import Chemical
from .material import Material


@forge_signature
class PlantSetup(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@3a00657a27b163e6872492862513e86c0040689d#PlantSetup"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    devices: List[Device] = wrapped(
        "devices",
        element(
            description="bla",
            default_factory=ListPlus,
            tag="Device",
            json_schema_extra=dict(multiple=True),
        ),
    )

    tubing: List[Tubing] = wrapped(
        "tubing",
        element(
            description="bla",
            default_factory=ListPlus,
            tag="Tubing",
            json_schema_extra=dict(multiple=True),
        ),
    )

    input: List[Chemical] = wrapped(
        "input",
        element(
            description="bla",
            default_factory=ListPlus,
            tag="Chemical",
            json_schema_extra=dict(multiple=True),
        ),
    )

    output: List[Chemical] = wrapped(
        "output",
        element(
            description="bla",
            default_factory=ListPlus,
            tag="Chemical",
            json_schema_extra=dict(multiple=True),
        ),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="3a00657a27b163e6872492862513e86c0040689d"
    )

    def add_to_devices(
        self,
        manufacturer: Optional[str] = None,
        device_type: Optional[str] = None,
        series: Optional[str] = None,
        on_off: Optional[bool] = None,
        id: Optional[str] = None,
    ) -> Device:
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
        return self.devices[-1]

    def add_to_tubing(
        self,
        material: Optional[Material] = None,
        inner_diameter: Optional[float] = None,
        outer_diameter: Optional[float] = None,
        length: Optional[int] = None,
        insulation: Optional[Insulation] = None,
        id: Optional[str] = None,
    ) -> Tubing:
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
        return self.tubing[-1]

    def add_to_input(
        self,
        name: Optional[str] = None,
        formula: Optional[str] = None,
        pureness: Optional[float] = None,
        supplier: Optional[str] = None,
        stoichiometry: Optional[Stoichiometry] = None,
        state_of_matter: Optional[str] = None,
        reactant_role: Optional[ReactantRole] = None,
        id: Optional[str] = None,
    ) -> Chemical:
        """
        This method adds an object of type 'Chemical' to attribute input

        Args:
            id (str): Unique identifier of the 'Chemical' object. Defaults to 'None'.
            name (): IUPAC name of the compound.. Defaults to None
            formula (): molecular formula of the compound.. Defaults to None
            pureness (): pureness of the compound in percent.. Defaults to None
            supplier (): name of the supplier of the compound.. Defaults to None
            stoichiometry (): stoichiometric information like equivalents, mass, amount of substance, volume. Defaults to None
            state_of_matter (): s for solid, l for liquid and g for gaseous. Defaults to None
            reactant_role (): Role that a reactand plays in a chemical reaction or  in a process.. Defaults to None
        """
        params = {
            "name": name,
            "formula": formula,
            "pureness": pureness,
            "supplier": supplier,
            "stoichiometry": stoichiometry,
            "state_of_matter": state_of_matter,
            "reactant_role": reactant_role,
        }
        if id is not None:
            params["id"] = id
        self.input.append(Chemical(**params))
        return self.input[-1]

    def add_to_output(
        self,
        name: Optional[str] = None,
        formula: Optional[str] = None,
        pureness: Optional[float] = None,
        supplier: Optional[str] = None,
        stoichiometry: Optional[Stoichiometry] = None,
        state_of_matter: Optional[str] = None,
        reactant_role: Optional[ReactantRole] = None,
        id: Optional[str] = None,
    ) -> Chemical:
        """
        This method adds an object of type 'Chemical' to attribute output

        Args:
            id (str): Unique identifier of the 'Chemical' object. Defaults to 'None'.
            name (): IUPAC name of the compound.. Defaults to None
            formula (): molecular formula of the compound.. Defaults to None
            pureness (): pureness of the compound in percent.. Defaults to None
            supplier (): name of the supplier of the compound.. Defaults to None
            stoichiometry (): stoichiometric information like equivalents, mass, amount of substance, volume. Defaults to None
            state_of_matter (): s for solid, l for liquid and g for gaseous. Defaults to None
            reactant_role (): Role that a reactand plays in a chemical reaction or  in a process.. Defaults to None
        """
        params = {
            "name": name,
            "formula": formula,
            "pureness": pureness,
            "supplier": supplier,
            "stoichiometry": stoichiometry,
            "state_of_matter": state_of_matter,
            "reactant_role": reactant_role,
        }
        if id is not None:
            params["id"] = id
        self.output.append(Chemical(**params))
        return self.output[-1]
