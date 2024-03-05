import sdRDM

import yaml
import pandas as pd
from typing import List, Optional
from pydantic import model_validator
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from lxml.etree import _Element
from .measurementtype import MeasurementType
from .quantity import Quantity
from .plantsetup import PlantSetup
from .calibration import Calibration
from .data import Data
from .component import Component
from .metadata import Metadata
from .measurement import Measurement
from .datatype import DataType
from .speciesdata import SpeciesData


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

    measurements: List[Measurement] = wrapped(
        "measurements",
        element(
            description=(
                "different measurements that are made within the scope of one"
                " experiment."
            ),
            default_factory=ListPlus,
            tag="Measurement",
            json_schema_extra=dict(multiple=True),
        ),
    )

    species_data: List[SpeciesData] = wrapped(
        "species_data",
        element(
            description="all provided and calculated data about a specific species.",
            default_factory=ListPlus,
            tag="SpeciesData",
            json_schema_extra=dict(multiple=True),
        ),
    )

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
        electron_transfer: Optional[float] = None,
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
            electron_transfer (): Number of transfered electrons of the individual species.. Defaults to None
            faraday_efficiency (): Faraday efficiencies of the individual species.. Defaults to None
        """
        params = {
            "species": species,
            "chemical_formula": chemical_formula,
            "calibration": calibration,
            "correction_factor": correction_factor,
            "electron_transfer": electron_transfer,
            "faraday_efficiency": faraday_efficiency,
        }
        if id is not None:
            params["id"] = id
        self.species_data.append(SpeciesData(**params))
        return self.species_data[-1]

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
        electron_transfer: Optional[float] = None,
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
            electron_transfer (): Number of transfered electrons of the individual species.. Defaults to None
            faraday_efficiency (): Faraday efficiencies of the individual species.. Defaults to None
        """
        params = {
            "species": species,
            "chemical_formula": chemical_formula,
            "calibration": calibration,
            "correction_factor": correction_factor,
            "electron_transfer": electron_transfer,
            "faraday_efficiency": faraday_efficiency,
        }
        if id is not None:
            params["id"] = id
        self.species_data.append(SpeciesData(**params))
        return self.species_data[-1]

    def initialize_species_from_yaml(self, yaml_file: str):
        """
        Function that initializes species from a yaml file

        Args:
            yaml_file (str): Path to the yaml file
        """

        with open(yaml_file) as f:
            species_data = yaml.safe_load(f)

        for species, item in species_data.items():

            if not "calibration" in item.keys():
                raise KeyError(f"No calibration data provided for species: {species}!")
            else:
                if not "peak_areas" in item["calibration"].keys():
                    raise KeyError(
                        f"No peak areas provided for calibration of species: {species}!"
                    )
                if not "concentrations" in item["calibration"].keys():
                    raise KeyError(
                        "No concentrations provided for calibration of species:"
                        f" {species}!"
                    )

            if not "chemical_formula" in item.keys():
                raise KeyError(f"No chemical formula provided for species: {species}!")

            if not "correction_factor" in item.keys():
                raise KeyError(f"No correction factor provided for species: {species}!")

            if not "electron_transfer" in item.keys():
                raise KeyError(f"No electron transfer provided for species: {species}!")

            # Create Calibration object and fit it to the given data
            calibration = Calibration(
                peak_areas=Data(
                    quantity="Peak area", values=item["calibration"]["peak_areas"]
                ),
                concentrations=Data(
                    quantity=Quantity.CONCENTRATION.value,
                    values=item["calibration"]["concentrations"],
                ),
            )
            calibration.calibrate()

            # Add species
            self.add_to_species_data(
                species=species,
                chemical_formula=item["chemical_formula"],
                calibration=calibration,
                correction_factor=item["correction_factor"],
                electron_transfer=item["electron_transfer"],
            )

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
