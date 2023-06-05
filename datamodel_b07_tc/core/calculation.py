import sdRDM

from typing import Optional, Union, List
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator

from datetime import datetime

from .data import Data
from .species import Species
from .quantity import Quantity
from .unit import Unit
from .calibration import Calibration


@forge_signature
class Calculation(sdRDM.DataModel):

    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("calculationINDEX"),
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
        default="66a1a1ef8dfb8b8fa8af6dec408f57c5f13a37c7"
    )

    def add_to_calibrations(
        self,
        species: Optional[Species] = None,
        peak_area: List[Data] = ListPlus(),
        concentration: List[Data] = ListPlus(),
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
            peak_area (): Recorded peak areas of the individual calibration solutions.. Defaults to ListPlus()
            concentration (): concentrations of the individual calibration solutions.. Defaults to ListPlus()
            slope (): slopes of the (linear) calibration functions.. Defaults to None
            intercept (): intercept of the (linear) calibration functions.. Defaults to None
            coefficient_of_determination (): coefficients of the (linear) calibration functions.. Defaults to None
        """

        params = {
            "species": species,
            "peak_area": peak_area,
            "concentration": concentration,
            "slope": slope,
            "intercept": intercept,
            "coefficient_of_determination": coefficient_of_determination,
        }

        if id is not None:
            params["id"] = id

        self.calibrations.append(Calibration(**params))

    def add_to_faraday_coefficients(
        self,
        quantity: Optional[Quantity] = None,
        values: List[Union[float, str, datetime]] = ListPlus(),
        unit: Optional[Unit] = None,
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
