import sdRDM

from typing import Optional, Union, List
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.base.datatypes import Unit
from datetime import datetime as Datetime
from lxml.etree import _Element
from .quantity import Quantity


@forge_signature
class Data(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@d957c6074b70fafa6e197b474ff403e15b0f7142#Data"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    quantity: Optional[Quantity] = element(
        description="quantity of a value.",
        default=None,
        tag="quantity",
        json_schema_extra=dict(),
    )

    values: List[Union[float, str, Datetime]] = wrapped(
        "values",
        element(
            description="values.",
            default_factory=ListPlus,
            tag="float",
            json_schema_extra=dict(multiple=True),
        ),
    )

    unit: Optional[Unit] = element(
        description="unit of the values.",
        default=None,
        tag="unit",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="d957c6074b70fafa6e197b474ff403e15b0f7142"
    )

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
