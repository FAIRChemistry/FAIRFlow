from datetime import datetime
from datamodel_b07_tc.core.experiment import Experiment


def get_initial_time_and_current(
    experiment: Experiment,
) -> tuple[float, float]:
    initial_current = float(
        experiment.get("measurements/metadata", "parameter", "IINIT")[0].value
    )
    inital_time = float(
        experiment.get("measurements/metadata", "parameter", "TINIT")[0].value
    )
    return initial_current, inital_time
