import sdRDM
import pandas as pd

from typing import Dict, List, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict
from .speciesdata import SpeciesData
from .data import Data
from .measurementtype import MeasurementType
from .component import Component
from .measurement import Measurement
from .plantsetup import PlantSetup
from .metadata import Metadata
from .calibration import Calibration
from .quantity import Quantity
from .datatype import DataType

@forge_signature
class Experiment(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    plant_setup: Optional[PlantSetup] = element(
        description="the individual plant setup that is used in this one experiment.",
        default_factory=PlantSetup,
        tag="plant_setup",
        json_schema_extra=dict(),
    )

    measurements: List[Measurement] = element(
        description=(
            "different measurements that are made within the scope of one experiment."
        ),
        default_factory=ListPlus,
        tag="measurements",
        json_schema_extra=dict(multiple=True),
    )

    species_data: List[SpeciesData] = element(
        description="all provided and calculated data about a specific species.",
        default_factory=ListPlus,
        tag="species_data",
        json_schema_extra=dict(multiple=True),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="baba9828ada6ed6f008c2c2fa0dc6c11f0d0c41c"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                (isinstance(i, _Element) for i in value)
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)
        return self

    def add_to_measurements(
        self,
        measurement_type: Optional[MeasurementType] = None,
        metadata: List[Metadata] = ListPlus(),
        experimental_data: List[Data] = ListPlus(),
        source: Optional[Component] = None,
        id: Optional[str] = None,
    ) -> Measurement:
        """
        This method adds an object of type 'Measurement' to attribute measurements

        Args:
            id (str): Unique identifier of the 'Measurement' object. Defaults to 'None'.
            measurement_type (): type of a measurement, e.g. potentiostatic or gas chromatography.. Defaults to None
            metadata (): metadata of a measurement.. Defaults to ListPlus()
            experimental_data (): experimental data of a measurement.. Defaults to ListPlus()
            source (): measuring device the data stems from.. Defaults to None
        """
        params = {
            "measurement_type": measurement_type,
            "metadata": metadata,
            "experimental_data": experimental_data,
            "source": source,
        }
        if id is not None:
            params["id"] = id
        self.measurements.append(Measurement(**params))
        return self.measurements[-1]

    def add_to_species_data(
        self,
        species: Optional[str] = None,
        chemical_formula: Optional[str] = None,
        calibration: Optional[Calibration] = None,
        correction_factor: Optional[float] = None,
        faraday_coefficient: Optional[float] = None,
        faraday_efficiency: Optional[Data] = None,
        id: Optional[str] = None,
    ) -> SpeciesData:
        """
        This method adds an object of type 'SpeciesData' to attribute species_data

        Args:
            id (str): Unique identifier of the 'SpeciesData' object. Defaults to 'None'.
            species (): name of the species.. Defaults to None
            chemical_formula (): chemical formula of the species.. Defaults to None
            calibration (): calibration measurement.. Defaults to None
            correction_factor (): correction factors of the individual species.. Defaults to None
            faraday_coefficient (): Faraday coefficients of the individual species.. Defaults to None
            faraday_efficiency (): Faraday efficiencies of the individual species.. Defaults to None
        """
        params = {
            "species": species,
            "chemical_formula": chemical_formula,
            "calibration": calibration,
            "correction_factor": correction_factor,
            "faraday_coefficient": faraday_coefficient,
            "faraday_efficiency": faraday_efficiency,
        }
        if id is not None:
            params["id"] = id
        self.species_data.append(SpeciesData(**params))
        return self.species_data[-1]

    @property
    def volumetric_flow_time_course(self) -> list:
        """This property extracts the volumetric flow time as well as the flow it self from the experiment class

        Returns:
            list: Datetime list and flow value list
        """
        volumetric_flow_datetime_list = []
        volumetric_flow_values_list = []

        mfm_measurements = self.get(
            "measurements", "measurement_type", "MFM measurement"
        )[0]
        for mfm_measurement in mfm_measurements:
            volumetric_flow_datetime_list.extend(
                mfm_measurement.get(
                    "experimental_data", "quantity", Quantity.DATETIME.value
                )[0][0].values
            )
            volumetric_flow_values_list.extend(
                mfm_measurement.get(
                    "experimental_data", "quantity", Quantity.VOLUMETRICFLOWRATE.value
                )[0][0].values
            )

        # If data is directly read in from the experiment, it is the correct format, if read from json dataset, it is a string and needs to be converted
        if not type(volumetric_flow_datetime_list[0]) == DataType.DATETIME.value:
            volumetric_flow_datetime_list = [
                pd.to_datetime(timestamp, format="%Y-%m-%dT%H:%M:%S").to_pydatetime()
                for timestamp in volumetric_flow_datetime_list
            ]

        return [volumetric_flow_datetime_list, volumetric_flow_values_list]