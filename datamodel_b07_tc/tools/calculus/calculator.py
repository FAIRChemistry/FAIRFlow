from pydantic import BaseModel
from datamodel_b07_tc.core import Experiment

class Calculator(BaseModel):
    experiment: Experiment

    def calibrate(self):
        self.experiment.analysis.calibrate()
        
    
        def from_json(self, calibration_file):

        return self.experiment
    
        load_calibration_file
    