import sdRDM

import json
import pandas as pd
from typing import List, Optional
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from pathlib import Path
from .measurement import Measurement
from .species import Species
from .measurementtype import MeasurementType
from .data import Data
from .calibration import Calibration
from .datatype import DataType
from .speciesdata import SpeciesData
from .metadata import Metadata
from .quantity import Quantity
from .chemicalformula import ChemicalFormula
from .plantsetup import PlantSetup


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
        id: Optional[str] = None,
    ) -> Measurement:
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

    def add_to_species_data(
        self,
        species: Optional[Species] = None,
        chemical_formula: Optional[ChemicalFormula] = None,
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

    def calibrate_from_json(self, path_to_json_file: Path, degree: int = 1):
        """
        Load calibration data (and with it chemical formula) from a JSON file and add them in the species data object.

        Args:
            path_to_json_file (Path): Path to json-type file.
            degree (int): Degree of polynomial regression on calibration data
        """
        with open(path_to_json_file, "r") as file:
            calibration_data = json.load(file)

        for species, data in calibration_data.items():
            # Create Calibration object and fit it to the given data
            calibration = Calibration(
                peak_areas=Data(
                    quantity="Peak area", unit="", values=data["peak_areas"]
                ),
                concentrations=Data(
                    quantity=Quantity.CONCENTRATION.value,
                    unit="%",
                    values=data["concentrations"],
                ),
                degree=degree,
            )
            calibration.calibrate()

            self.add_to_species_data(
                species=species,
                chemical_formula=data["chemical_formula"],
                calibration=calibration,
            )

    def read_correction_factors(self, path: Path):
        """
        Load correction factors for (existing) each species and add them in the species data object.

        Args:
            path (Path): Path to json-type file.
        """

        with open(path, "r") as f:
            correction_factors_dict = json.load(f)

        for species, correction_factor in correction_factors_dict.items():
            for species_data_object in self.species_data:
                if species_data_object.species == species:
                    species_data_object.correction_factor = correction_factor

    def read_faraday_coefficients(self, path: Path):
        """
        Load Faraday coefficients for (existing) each species and add them in the species data object.

        Args:
            path (Path): Path to json-type file.
        """

        with open(path, "r") as f:
            faraday_coefficients_dict = json.load(f)

        for species, faraday_coefficient in faraday_coefficients_dict.items():
            for species_data_object in self.species_data:
                if species_data_object.species == species:
                    species_data_object.faraday_coefficient = faraday_coefficient

    @property
    def volumetric_flow_time_course(self) -> list:
        """This property extracts the volumetric flow time as well as the flow it self from the experiment class

        Returns:
            list: Datetime list and flow value list
        """
        mfm_measurement = self.get(
            "measurements", "measurement_type", "MFM measurement"
        )[0][0]

        volumetric_flow_datetime_list = mfm_measurement.get(
            "experimental_data", "quantity", Quantity.DATETIME.value
        )[0][0].values
        volumetric_flow_values_list = mfm_measurement.get(
            "experimental_data", "quantity", Quantity.VOLUMETRICFLOWRATE.value
        )[0][0].values

        # If data is directly read in from the experiment, it is the correct format, if read from json dataset, it is a string and needs to be converted
        if not type(volumetric_flow_datetime_list[0]) == DataType.DATETIME.value:
            volumetric_flow_datetime_list = [
                pd.to_datetime(timestamp, format="%Y-%m-%dT%H:%M:%S").to_pydatetime()
                for timestamp in volumetric_flow_datetime_list
            ]

        return [volumetric_flow_datetime_list, volumetric_flow_values_list]
