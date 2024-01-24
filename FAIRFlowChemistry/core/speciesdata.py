import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .data import Data
from .calibration import Calibration
from .species import Species
from .chemicalformula import ChemicalFormula


@forge_signature
class SpeciesData(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@f7accf3054d687b0e59ef5bd04786fc2617e0353#SpeciesData"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    species: Optional[Species] = element(
        description="name of the species.",
        default=None,
        tag="species",
        json_schema_extra=dict(),
    )

    chemical_formula: Optional[ChemicalFormula] = element(
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

    faraday_coefficient: Optional[float] = element(
        description="Faraday coefficients of the individual species.",
        default=None,
        tag="faraday_coefficient",
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
        default="f7accf3054d687b0e59ef5bd04786fc2617e0353"
    )
