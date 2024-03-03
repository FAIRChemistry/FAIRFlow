import sdRDM

from typing import Dict, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict
from .material import Material


@forge_signature
class Insulation(sdRDM.DataModel):
    """Small type for attribute 'insulation'"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )
    thickness: Optional[float] = element(
        default=None, tag="thickness", json_schema_extra=dict()
    )
    material: Optional[str] = element(
        default=None, tag="material", json_schema_extra=dict()
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="f8cdbee59156292c0dda1a7171efeb7a002d7a55"
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


@forge_signature
class Tubing(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    material: Optional[Material] = element(
        description="material with which the fluid flowing through comes into contact.",
        default=None,
        tag="material",
        json_schema_extra=dict(),
    )

    inner_diameter: Optional[float] = element(
        description="inner diameter of the tubing in mm.",
        default=None,
        tag="inner_diameter",
        json_schema_extra=dict(),
    )

    outer_diameter: Optional[float] = element(
        description="outer diameter of the tubing in mm.",
        default=None,
        tag="outer_diameter",
        json_schema_extra=dict(),
    )

    length: Optional[int] = element(
        description="length of the tubing in mm.",
        default=None,
        tag="length",
        json_schema_extra=dict(),
    )

    insulation: Optional[Insulation] = element(
        description="insulation of the tubing.",
        default_factory=Insulation,
        tag="insulation",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="f8cdbee59156292c0dda1a7171efeb7a002d7a55"
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
