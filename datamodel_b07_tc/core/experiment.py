import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .metadata import Metadata
from .measurementtype import MeasurementType
from .data import Data
from .plantsetup import PlantSetup
from .calculation import Calculation
from .measurement import Measurement


@forge_signature
class Experiment(sdRDM.DataModel):

    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("experimentINDEX"),
        xml="@id",
    )

    plant_setup: Optional[PlantSetup] = Field(
        default=None,
        description="the individual plant setup that is used in this one experiment.",
    )

    measurements: List[Measurement] = Field(
        default_factory=ListPlus,
        multiple=True,
        description=(
            "different measurements that are made within the scope of one experiment."
        ),
    )

    calculations: Optional[Calculation] = Field(
        default=None,
        description=(
            "all the calculations that are done within the scope of one experiment."
        ),
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="7dd708753549b0c2433a72463c1d653249635979"
    )

    def add_to_measurements(
        self,
        measurement_type: Optional[MeasurementType] = None,
        metadata: List[Metadata] = ListPlus(),
        experimental_data: List[Data] = ListPlus(),
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Measurement' to attribute measurements

        Args:
            id (str): Unique identifier of the 'Measurement' object. Defaults to 'None'.
            measurement_type (): type of a measurement, e.g. potentiostatic or gas chromatography.. Defaults to None
            metadata (): metadata of a measurement.. Defaults to ListPlus()
            experimental_data (): experimental data of a measurement.. Defaults to ListPlus()
        """

        params = {
            "measurement_type": measurement_type,
            "metadata": metadata,
            "experimental_data": experimental_data,
        }

        if id is not None:
            params["id"] = id

        self.measurements.append(Measurement(**params))
