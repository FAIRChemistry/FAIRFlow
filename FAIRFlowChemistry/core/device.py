import sdRDM

from typing import Dict, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict


@forge_signature
class Device(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    manufacturer: Optional[str] = element(
        description="name of the manufacturer of the device.",
        default=None,
        tag="manufacturer",
        json_schema_extra=dict(),
    )

    device_type: Optional[str] = element(
        description="type given by the manufacturer of the device.",
        default=None,
        tag="device_type",
        json_schema_extra=dict(),
    )

    series: Optional[str] = element(
        description="the series of the device.",
        default=None,
        tag="series",
        json_schema_extra=dict(),
    )

    on_off: Optional[bool] = element(
        description="operational mode of the flow module. True is on and False is off.",
        default=None,
        tag="on_off",
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
