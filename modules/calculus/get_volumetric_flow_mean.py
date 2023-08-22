from datetime import datetime
from datamodel_b07_tc.core.experiment import Experiment


def get_volumetric_flow_mean(
    experiment: Experiment, averaging_radius: int = 10
) -> float:
    injection_date_string = experiment.get(
        "measurements/metadata", "parameter", "Injection Date"
    )[0].value
    inj_date_datetime = datetime.strptime(
        injection_date_string, "%d-%b-%y, %H:%M:%S"
    )

    volumetric_flow_datetime_list = (
        experiment.get("measurements", "measurement_type", "MFM Measurement")[
            0
        ]
        .experimental_data[0]
        .values
    )
    volumetric_flow = (
        experiment.get("measurements", "measurement_type", "MFM Measurement")[
            0
        ]
        .experimental_data[3]
        .values
    )
    volumetric_flows = []
    for i, datetime_ in enumerate(volumetric_flow_datetime_list):
        if datetime_ == inj_date_datetime:
            for j in range(i - averaging_radius, i + averaging_radius + 1):
                volumetric_flows.append(volumetric_flow[j])
    volumetric_flows_mean = sum(volumetric_flows) / (averaging_radius * 2 + 1)
    return volumetric_flows_mean
