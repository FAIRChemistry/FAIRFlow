import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .calculation import Calculation
from .measurement import Measurement
from .listofmeasurements import ListOfMeasurements
from .metadata import Metadata
from .plantsetup import PlantSetup
from .data import Data


@forge_signature
class Experiment(sdRDM.DataModel):

    """"""

    id: str = Field(
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
        default="087d97eb5882e9a8535a8faaabe6baaea7a85f78"
    )

    def add_to_measurements(
        self,
        experimental_data: Optional[Data] = None,
        metadata: Optional[Metadata] = None,
        list_of_measurements: Optional[ListOfMeasurements] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Measurement' to attribute measurements

        Args:
            id (str): Unique identifier of the 'Measurement' object. Defaults to 'None'.
            experimental_data (): experimental data of a measurement.. Defaults to None
            metadata (): metadata of a measurement.. Defaults to None
            list_of_measurements (): list of measurements, that do not need any further quantities explanation. E.g., only metadata are of interest.. Defaults to None
        """

        params = {
            "experimental_data": experimental_data,
            "metadata": metadata,
            "list_of_measurements": list_of_measurements,
        }

        if id is not None:
            params["id"] = id

        self.measurements.append(Measurement(**params))
