import sdRDM
import networkx as nx
import matplotlib.pyplot as plt

from typing import List, Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from .genericattibute import GenericAttibute
from .component import Component
from .componenttype import ComponentType


@forge_signature
class PlantSetup(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@f4f90b698573ebe018bb7f96d10be4877e4643b3#PlantSetup"
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
        default="f4f90b698573ebe018bb7f96d10be4877e4643b3"
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

    def visualize(self, save_path: str=""):
        """
        Function that visualize the plantsetup as graph. 

        Args:
            save_path (str, optional): Path to save the graph (if wanted). Defaults to "".
        """
        # Create a directed graph
        G = nx.DiGraph()

        # Add nodes and edges
        for component in self.components:
            G.add_node(component.component_id)
            for connection in component.connections:
                G.add_edge(component.component_id, connection)

        # Draw the graph
        plt.figure()
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20, linewidths=2)
        plt.title('Plantsetup')
        if save_path: plt.savefig( save_path )
        plt.show()
        plt.close()