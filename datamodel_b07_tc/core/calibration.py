import sdRDM

from typing import Optional, Union, List
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator

from datetime import datetime

from .quantity import Quantity
from .species import Species
from .data import Data
from .unit import Unit


@forge_signature
class Calibration(sdRDM.DataModel):

    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("calibrationINDEX"),
        xml="@id",
    )

    species: Optional[Species] = Field(
        default=None,
        description="Species for which the calibration was performed.",
    )

    peak_area: List[Data] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="Recorded peak areas of the individual calibration solutions.",
    )

    concentration: List[Data] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="concentrations of the individual calibration solutions.",
    )

    slope: Optional[Data] = Field(
        default=None,
        description="slopes of the (linear) calibration functions.",
    )

    intercept: Optional[Data] = Field(
        default=None,
        description="intercept of the (linear) calibration functions.",
    )

    coefficient_of_determination: Optional[Data] = Field(
        default=None,
        description="coefficients of the (linear) calibration functions.",
    )

    def add_to_peak_area(
        self,
        quantity: Optional[Quantity] = None,
        values: List[Union[float, str, datetime]] = ListPlus(),
        unit: Optional[Unit] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Data' to attribute peak_area

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

        self.peak_area.append(Data(**params))

    def add_to_concentration(
        self,
        quantity: Optional[Quantity] = None,
        values: List[Union[float, str, datetime]] = ListPlus(),
        unit: Optional[Unit] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Data' to attribute concentration

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

        self.concentration.append(Data(**params))
