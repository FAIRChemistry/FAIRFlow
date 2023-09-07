import json
from pydantic import BaseModel
from datamodel_b07_tc.tools.python_api.analysis import Analysis
from datamodel_b07_tc.tools.python_api.calibration import Calibration
from datamodel_b07_tc.tools.python_api.data import Data
from datamodel_b07_tc.tools.python_api.quantity import Quantity

from pathlib import Path

class Calibrator(BaseModel):

    analysis : Analysis

    @classmethod
    def from_json_file(cls, path_to_json: Path):
        """
        Load calibration data from a JSON file and store them in an Calibration object.

        Args:
            path_to_json (Path): Path to json-type file.

        """
        with open(path_to_json, 'r') as file:
            calibration_data = json.load(file)

        calibrations = []
        for value in calibration_data.values():
            calibration = Calibration(
                species=value['species'],
                peak_area=Data(
                    quantity=Quantity.PEAKAREA.value,
                    unit=None,
                    values=value['peak_areas'],
                ),
                concentrations=Data(
                    quantity=Quantity.CONCENTRATION.value,
                    unit='%',
                    values=value['concentrations']
                )
            )
            calibrations.append(calibration)
        analysis = Analysis()
        analysis.calibrations=calibrations
        return cls(analysis=analysis)


    def calibrate(self):
        """
        Perform calibration using the calibration data.
        Returns:
            Analysis: Calibration parameters.
        """

        return self.analysis.calibrate()
    
    @property
    def available_json_files(self) -> list[str]:

        path_list = list(Path(self.calibration_file_path).glob(".json"))
        _available_files = {
            count: file
            for count, file in enumerate(path_list)
            if file.is_file()
        }
        return _available_files
    
