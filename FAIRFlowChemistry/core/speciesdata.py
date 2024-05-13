import sdRDM

from typing import Dict, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict
from .data import Data
from .calibration import Calibration


@forge_signature
class SpeciesData(sdRDM.DataModel, search_mode="unordered"):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    species: Optional[str] = element(
        description="name of the species.",
        default=None,
        tag="species",
        json_schema_extra=dict(),
    )

    chemical_formula: Optional[str] = element(
        description="chemical formula of the species.",
        default=None,
        tag="chemical_formula",
        json_schema_extra=dict(),
    )

    calibration: Optional[Calibration] = element(
        description="calibration measurement.",
        default_factory=Calibration,
        tag="calibration",
        json_schema_extra=dict(),
    )

    correction_factor: Optional[float] = element(
        description="correction factors of the individual species.",
        default=None,
        tag="correction_factor",
        json_schema_extra=dict(),
    )

    electron_transfer: Optional[float] = element(
        description="Number of transfered electrons of the individual species.",
        default=None,
        tag="electron_transfer",
        json_schema_extra=dict(),
    )

    faraday_efficiency: Optional[Data] = element(
        description="Faraday efficiencies of the individual species.",
        default_factory=Data,
        tag="faraday_efficiency",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="2db1d881b230dff78178a78a2360339d1bc95946"
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
