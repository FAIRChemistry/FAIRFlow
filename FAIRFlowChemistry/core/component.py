import sdRDM

from typing import List, Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from .componenttype import ComponentType
from .genericattibute import GenericAttibute


@forge_signature
class Component(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@c41a0c1e08586e8cb4deff5d7a6e8b76d1e12ca7#Component"
    },
):
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

    component_id: Optional[str] = element(
        description="id used to unambiguously identify the component.",
        default=None,
        tag="component_id",
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

    generic_attributes: List[GenericAttibute] = wrapped(
        "generic_attributes",
        element(
            description="a generic attribute as defined by DEXPI.",
            default_factory=ListPlus,
            tag="GenericAttibute",
            json_schema_extra=dict(multiple=True),
        ),
    )

    connections: List[str] = wrapped(
        "connections",
        element(
            description=(
                "component id of other component this component is connected to via"
                " pipes, wires or similar."
            ),
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

    def add_to_generic_attributes(
        self,
        name: Optional[str] = None,
        attribute_uri: Optional[str] = None,
        value: Optional[str] = None,
        format: Optional[str] = None,
        units: Optional[str] = None,
        units_uri: Optional[str] = None,
        id: Optional[str] = None,
    ) -> GenericAttibute:
        """
        This method adds an object of type 'GenericAttibute' to attribute generic_attributes

        Args:
            id (str): Unique identifier of the 'GenericAttibute' object. Defaults to 'None'.
            name (): bla.. Defaults to None
            attribute_uri (): bla.. Defaults to None
            value (): bla.. Defaults to None
            format (): bla.. Defaults to None
            units (): bla.. Defaults to None
            units_uri (): bla. Defaults to None
        """
        params = {
            "name": name,
            "attribute_uri": attribute_uri,
            "value": value,
            "format": format,
            "units": units,
            "units_uri": units_uri,
        }
        if id is not None:
            params["id"] = id
        self.generic_attributes.append(GenericAttibute(**params))
        return self.generic_attributes[-1]
