import sdRDM

from datetime import datetime
from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .data import Data
from .analysis import Analysis
from .measurement import Measurement
from .measurementtype import MeasurementType
from .metadata import Metadata
from .plantsetup import PlantSetup


@forge_signature
class Experiment(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("experimentINDEX"),
        xml="@id",
    )

    plant_setup: Optional[PlantSetup] = Field(
        default=PlantSetup(),
        description="the individual plant setup that is used in this one experiment.",
    )

    measurements: List[Measurement] = Field(
        default_factory=ListPlus,
        multiple=True,
        description=(
            "different measurements that are made within the scope of one experiment."
        ),
    )

    analysis: Optional[Analysis] = Field(
        default=Analysis(),
        description=(
            "all the calculations that are done within the scope of one experiment."
        ),
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="a4c50b26815a02cca2986380d5aeb8c023e877eb"
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

        return self.measurements[-1]
    

    # def get_injection_date(self) -> datetime:

    #     injection_date_string = self.gc_measurements.get(
    #         "metadata", "parameter", "Injection Date"
    #     )[0][0].value
    #     inj_date_datetime = datetime.strptime(
    #         injection_date_string, "%d-%b-%y, %H:%M:%S"
    #     )
    #     return injection_date_string

    @property
    def volumetric_flow_time_course(self) ->list:

        mfm_measurement = (
            self.get("measurements", "measurement_type", "MFM Measurement")
            [0][0]
        )
        volumetric_flow_datetime_list = mfm_measurement.get("experimental_data", "quantity", "Date time")[0][0].values
        volumetric_flow_values_list = mfm_measurement.get("experimental_data", "quantity", "Volumetric flow rate")[0][0].values
        return [volumetric_flow_datetime_list, volumetric_flow_values_list]
    
    @property
    def initial_time(self) -> float:

        initial_time = float(
            self.get("measurements/metadata", "parameter", "TINIT")[0][0].value
        )
        return initial_time
    
    @property
    def initial_current(self) -> float:

        initial_current = float(
            self.get("measurements/metadata", "parameter", "IINIT")[0][0].value
        )
        return initial_current
