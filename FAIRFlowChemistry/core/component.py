import sdRDM

from typing import Dict, List, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict
from .componenttype import ComponentType


@forge_signature
class Component(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    component_type: Optional[ComponentType] = element(
        description="equipment or piping component.",
        default=None,
        tag="component_type",
        json_schema_extra=dict(),
    )

    id: Optional[str] = element(
        description="id used to unambiguously identify the component.",
        default=None,
        tag="id",
        json_schema_extra=dict(),
    )

    component_class: Optional[str] = element(
        description="class of the component.",
        default=None,
        tag="component_class",
        json_schema_extra=dict(),
    )

    component_class_uri: Optional[str] = element(
        description="uri of the component.",
        default=None,
        tag="component_class_uri",
        json_schema_extra=dict(),
    )

    component_name: Optional[str] = element(
        description=(
            "name of the component used to link between the abstract component and its"
            " shape."
        ),
        default=None,
        tag="component_name",
        json_schema_extra=dict(),
    )

    generic_attribute: List[str] = element(
        description="a generic attribute as defined by DEXPI.",
        default_factory=ListPlus,
        tag="generic_attribute",
        json_schema_extra=dict(multiple=True),
    )

    connections: List["Component"] = element(
        description=(
            "other component this component is connected to via pipes, wires or"
            " similar."
        ),
        default_factory=ListPlus,
        tag="connections",
        json_schema_extra=dict(multiple=True),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="c0afa15b3139d198065f3824cc2033e5ab02f73a"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                (isinstance(i, _Element) for i in value)
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)
        return self

    def add_to_connections(
        self,
        component_type: Optional[ComponentType] = None,
        id: Optional[str] = None,
        component_class: Optional[str] = None,
        component_class_uri: Optional[str] = None,
        component_name: Optional[str] = None,
        generic_attribute: List[str] = ListPlus(),
        connections: List["Component"] = ListPlus(),
        id: Optional[str] = None,
    ) -> Component:
        """
        This method adds an object of type 'Component' to attribute connections

        Args:
            id (str): Unique identifier of the 'Component' object. Defaults to 'None'.
            component_type (): equipment or piping component.. Defaults to None
            id (): id used to unambiguously identify the component.. Defaults to None
            component_class (): class of the component.. Defaults to None
            component_class_uri (): uri of the component.. Defaults to None
            component_name (): name of the component used to link between the abstract component and its shape.. Defaults to None
            generic_attribute (): a generic attribute as defined by DEXPI.. Defaults to ListPlus()
            connections (): other component this component is connected to via pipes, wires or similar.. Defaults to ListPlus()
        """
        params = {
            "component_type": component_type,
            "id": id,
            "component_class": component_class,
            "component_class_uri": component_class_uri,
            "component_name": component_name,
            "generic_attribute": generic_attribute,
            "connections": connections,
        }
        if id is not None:
            params["id"] = id
        self.connections.append(Component(**params))
        return self.connections[-1]
