from datetime import datetime
from datamodel_b07_tc.core.dataset import Dataset


def get_initial_time_current(dataset: Dataset) -> tuple[float, float]:
    d = dataset

    I_init = float(
        d.get("experiments/measurements/metadata", "parameter", "IINIT")[
            0
        ].value
    )
    t_init = float(
        d.get("experiments/measurements/metadata", "parameter", "TINIT")[
            0
        ].value
    )
    return I_init, t_init
