import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from .chemicalformula import ChemicalFormula
from .data import Data
from .species import Species
from .calibration import Calibration


@forge_signature
class SpeciesData(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("speciesdataINDEX"),
        xml="@id",
    )

    species: Optional[Species] = Field(
        default=None,
        description="name of the species.",
    )

    chemical_formula: Optional[ChemicalFormula] = Field(
        default=None,
        description="chemical formula of the species.",
    )

    calibration: Optional[Calibration] = Field(
        description="calibration measurement.",
        default_factory=Calibration,
    )

    correction_factor: Optional[float] = Field(
        default=None,
        description="correction factors of the individual species.",
    )

    faraday_coefficient: Optional[float] = Field(
        default=None,
        description="Faraday coefficients of the individual species.",
    )

    faraday_efficiency: Optional[Data] = Field(
        description="Faraday efficiencies of the individual species.",
        default_factory=Data,
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="ef81b78015477a06bc88e5dd78879b337a8d9c2e"
    )
