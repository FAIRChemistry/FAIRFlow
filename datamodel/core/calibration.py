import numpy as np
import sdRDM

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator

from .data import Data


@forge_signature
class Calibration(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("calibrationINDEX"),
        xml="@id",
    )

    peak_areas: Optional[Data] = Field(
        default=Data(),
        description="Recorded peak areas of the individual calibration solutions.",
    )

    concentrations: Optional[Data] = Field(
        default=Data(),
        description="concentrations of the individual calibration solutions.",
    )

    regression_model: Optional[LinearRegression] = Field(
        default=LinearRegression(),
        description="(Linear) Regression model.",
    )

    degree: Optional[int] = Field(
        default=2,
        description="Degree of regression model.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="48482b81b482e9464bf050b2490e5f461bbf3497"
    )

    class Config:
        # allow LinearRegression
        arbitrary_types_allowed = True

    def calibrate(self):
        """
        Calibrate the regression model on seen data
        """
  
        x_train     = PolynomialFeatures(degree=self.degree).fit_transform( np.array(self.peak_areas.values).reshape(-1, 1) )
        y_train     = np.array( self.concentrations.values )
        self.regression_model.fit( x_train, y_train )
    
    def predict(self, x: list) -> np.ndarray:
        """
        Predict with regression model

        Args:
            x (1D list): New locations for which predictions should be made

        Returns:
           (1D numpy array): Predicted data at new locations
        """

        x_predict = PolynomialFeatures(degree=self.degree).fit_transform( np.array(x).reshape(-1,1) )

        return self.regression_model.predict( x_predict )