import sdRDM

import numpy as np
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
from sklearn import linear_model
from .species import Species
from .chemicalformula import ChemicalFormula
from .data import Data
from .quantity import Quantity
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
        default=Calibration(),
        description="calibration measurement.",
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
        default=Data(),
        description="Faraday efficiencies of the individual species.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="b85d0314fec4cf3ed24720facf3bb92a91badc0b"
    )

    def calibrate(self):
        peak_areas = np.array(self.calibration.peak_areas.values).reshape(-1, 1)
        concentration = np.array(self.calibration.concentrations.values)
        function = linear_model.LinearRegression(fit_intercept=True)
        function.fit(peak_areas, concentration)
        slope, intercept = function.coef_[0], function.intercept_
        coefficient_of_determination = function.score(peak_areas, concentration)
        self.calibration.slope = Data(
            quantity=Quantity.SLOPE.value, values=[slope], unit="%"
        )
        self.calibration.intercept = Data(
            quantity=Quantity.INTERCEPT.value,
            values=[intercept],
            unit="%",
        )
        self.calibration.coefficient_of_determination = Data(
            quantity=Quantity.COEFFDET.value,
            values=[coefficient_of_determination],
            unit=None,
        )
