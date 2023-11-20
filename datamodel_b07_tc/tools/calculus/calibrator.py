import json
from pydantic import BaseModel
from typing import List
from datamodel_b07_tc.test.speciesdata import SpeciesData
from datamodel_b07_tc.test.calibration import Calibration
from datamodel_b07_tc.test.data import Data
from datamodel_b07_tc.test.quantity import Quantity

from pathlib import Path


class Calibrator(BaseModel):
    species_data_list: List[SpeciesData]

    @classmethod
    def from_json_file(cls, path_to_json_file: Path):
        """
        Load calibration data from a JSON file and store them in an Calibration object.

        Args:
            path_to_json_file (Path): Path to json-type file.

        """
        with open(path_to_json_file, "r") as file:
            calibration_data = json.load(file)

        species_data_list = []
        for species, data in calibration_data.items():
            species_data = SpeciesData(species=species,
                                       chemical_formula=data["chemical_formula"],
                                       calibration=Calibration(peak_areas=Data(quantity="Peak area",unit=None,values=data["peak_areas"]),
                                       concentrations=Data(quantity="Concentration",unit="%",values=data["concentrations"])),
            )
            species_data_list.append(species_data)
        return cls(species_data_list=species_data_list)

    def calibrate(self):
        """
        Perform calibration using the calibration data.
        Returns:
            analysis (Analysis): Analysis-type object tha contains the computed calibration data.
        """
        for species_data in self.species_data_list:
            species_data.calibration.calibrate()
        return self.species_data_list
