import sdRDM
import numpy as np

from typing import Optional, Union, List
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator

from datetime import datetime as Datetime
from astropy.units import UnitBase
from sklearn import linear_model

from .quantity import Quantity
from .calibration import Calibration
from .species import Species
from .data import Data


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
        default="c74e880ad947ad85af07e386502a19026786a4b7"
    )

    def add_to_calibrations(
        self,
        species: Optional[Species] = None,
        peak_area: Optional[Data] = None,
        concentration: Optional[Data] = None,
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
            peak_area (): Recorded peak areas of the individual calibration solutions.. Defaults to None
            concentration (): concentrations of the individual calibration solutions.. Defaults to None
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
    
    def calibrate(self):

        for cali in self.calibrations:
            peak_area = np.array(cali.peak_area.values).reshape(-1, 1)
            concentration = np.array(cali.concentration.values)

            function = linear_model.LinearRegression(fit_intercept=True)
            function.fit(peak_area, concentration)
            slope, intercept = function.coef_[0], function.intercept_
            coefficient_of_determination = function.score(
                peak_area,
                concentration
            )
            cali.slope = Data(
                quantity=Quantity.SLOPE.value, values=[slope], unit='%'
            )
            cali.intercept = Data(
                quantity=Quantity.INTERCEPT.value,
                values=[intercept],
                unit='%',
            )
            cali.coefficient_of_determination = Data(
                quantity=Quantity.COEFFDET.value,
                values=[coefficient_of_determination],
                unit=None,
            )


        # @property
        # def calibration_parameters():
        #     return 
