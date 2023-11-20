import sdRDM

from typing import Optional, Union, List
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator

from datetime import datetime as Datetime
from astropy.units import UnitBase

from .quantity import Quantity
from .data import Data
from .species import Species
from .calibration import Calibration


@forge_signature
class Analysis(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("analysisINDEX"),
        xml="@id",
    )

    calibrations: List[Calibration] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="Calibration measurement.",
    )

    faraday_coefficients: List[Data] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="Faraday coefficients.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="a4c50b26815a02cca2986380d5aeb8c023e877eb"
    )

    def add_to_calibrations(
        self,
        species: Optional[Species] = None,
        peak_areas: Optional[Data] = None,
        concentrations: Optional[Data] = None,
        slope: Optional[Data] = None,
        intercept: Optional[Data] = None,
        coefficient_of_determination: Optional[Data] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Calibration' to attribute calibrations

        Args:
            id (str): Unique identifier of the 'Calibration' object. Defaults to 'None'.
            species (): Species for which the calibration was performed.. Defaults to None
            peak_areas (): Recorded peak areas of the individual calibration solutions.. Defaults to None
            concentrations (): concentrations of the individual calibration solutions.. Defaults to None
            slope (): slopes of the (linear) calibration functions.. Defaults to None
            intercept (): intercept of the (linear) calibration functions.. Defaults to None
            coefficient_of_determination (): coefficients of the (linear) calibration functions.. Defaults to None
        """

        params = {
            "species": species,
            "peak_areas": peak_areas,
            "concentrations": concentrations,
            "slope": slope,
            "intercept": intercept,
            "coefficient_of_determination": coefficient_of_determination,
        }

        if id is not None:
            params["id"] = id

        self.calibrations.append(Calibration(**params))

        return self.calibrations[-1]

    def add_to_faraday_coefficients(
        self,
        quantity: Optional[Quantity] = None,
        values: List[Union[float, str, Datetime]] = ListPlus(),
        unit: Optional[UnitBase] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Data' to attribute faraday_coefficients

        Args:
            id (str): Unique identifier of the 'Data' object. Defaults to 'None'.
            quantity (): quantity of a value.. Defaults to None
            values (): values.. Defaults to ListPlus()
            unit (): unit of the values.. Defaults to None
        """

        params = {
            "quantity": quantity,
            "values": values,
            "unit": unit,
        }

        if id is not None:
            params["id"] = id

        self.faraday_coefficients.append(Data(**params))

        return self.faraday_coefficients[-1]