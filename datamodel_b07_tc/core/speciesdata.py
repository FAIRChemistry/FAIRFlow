import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .data import Data
from .species import Species
from .calibration import Calibration
from .chemicalformula import ChemicalFormula


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
        default=Calibration(),
        description="calibration measurement.",
    )

    correction_factor: Optional[Data] = Field(
        default=Data(),
        description="correction factors of the individual species.",
    )

    faraday_coefficient: Optional[Data] = Field(
        default=Data(),
        description="Faraday coefficients of the individual species.",
    )

    faraday_efficiency: Optional[Data] = Field(
        default=Data(),
        description="Faraday efficiencies of the individual species.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="19fe6530748ba481b5060171bf6a43a81cab90d7"
    )
