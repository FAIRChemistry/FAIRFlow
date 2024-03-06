import sdRDM

from typing import List, Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from .genericattibute import GenericAttibute
from .componenttype import ComponentType
from .component import Component


@forge_signature
class PlantSetup(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@c41a0c1e08586e8cb4deff5d7a6e8b76d1e12ca7#PlantSetup"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    components: List[Component] = wrapped(
        "components",
        element(
            description="bla.",
            default_factory=ListPlus,
            tag="Component",
            json_schema_extra=dict(multiple=True),
        ),
    )

    input: List[str] = wrapped(
        "input",
        element(
            description="bla.",
            default_factory=ListPlus,
            tag="string",
            json_schema_extra=dict(multiple=True),
        ),
    )

    output: List[str] = wrapped(
        "output",
        element(
            description="bla.",
            default_factory=ListPlus,
            tag="string",
            json_schema_extra=dict(multiple=True),
        ),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="c41a0c1e08586e8cb4deff5d7a6e8b76d1e12ca7"
    )

    def add_to_components(
        self,
        component_type: Optional[ComponentType] = None,
        component_id: Optional[str] = None,
        component_class: Optional[str] = None,
        component_class_uri: Optional[str] = None,
        component_name: Optional[str] = None,
        generic_attributes: List[GenericAttibute] = ListPlus(),
        connections: List[str] = ListPlus(),
        id: Optional[str] = None,
    ) -> Component:
        """
        This method adds an object of type 'Component' to attribute components

        Args:
            id (str): Unique identifier of the 'Component' object. Defaults to 'None'.
            component_type (): equipment or piping component.. Defaults to None
            component_id (): id used to unambiguously identify the component.. Defaults to None
            component_class (): class of the component.. Defaults to None
            component_class_uri (): uri of the component.. Defaults to None
            component_name (): name of the component used to link between the abstract component and its shape.. Defaults to None
            generic_attributes (): a generic attribute as defined by DEXPI.. Defaults to ListPlus()
            connections (): component id of other component this component is connected to via pipes, wires or similar.. Defaults to ListPlus()
        """
        params = {
            "component_type": component_type,
            "component_id": component_id,
            "component_class": component_class,
            "component_class_uri": component_class_uri,
            "component_name": component_name,
            "generic_attributes": generic_attributes,
            "connections": connections,
        }
        if id is not None:
            params["id"] = id
        self.components.append(Component(**params))
        return self.components[-1]
