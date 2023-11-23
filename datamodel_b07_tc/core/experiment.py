import sdRDM

import json
from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from pathlib import Path
from .measurementtype import MeasurementType
from .speciesdata import SpeciesData
from .measurement import Measurement
from .metadata import Metadata
from .data import Data
from .plantsetup import PlantSetup
from .chemicalformula import ChemicalFormula
from .species import Species
from .calibration import Calibration


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

    species_data: List[SpeciesData] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="all provided and calculated data about a specific species.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="7504f503d8e4455500cbff7d193b9d959161556a"
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

    def add_to_species_data(
        self,
        species: Optional[Species] = None,
        chemical_formula: Optional[ChemicalFormula] = None,
        calibration: Optional[Calibration] = None,
        correction_factor: Optional[float] = None,
        faraday_coefficient: Optional[float] = None,
        faraday_efficiency: Optional[Data] = None,
        id: Optional[str] = None,
    ) -> None:
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

    def calibrate_from_json(path_to_json_file: Path):
        """
        Load calibration data (and with it chemical formula) from a JSON file and store them in the species data object.

        Args:
            path_to_json_file (Path): Path to json-type file.

        """
        with open(path_to_json_file, "r") as file:
            calibration_data = json.load(file)

        species_data_list = []

        for species, data in calibration_data.items():
            species_data = SpeciesData(
                species=species,
                chemical_formula=data["chemical_formula"],
                calibration=Calibration(
                    peak_areas=Data(
                        quantity="Peak area", unit=None, values=data["peak_areas"]
                    ),
                    concentrations=Data(
                        quantity="Concentration",
                        unit="%",
                        values=data["concentrations"],
                    ),
                ),
            )
            species_data_list.append(species_data)
        return cls(species_data_list=species_data_list)
