from datetime import datetime
from datamodel_b07_tc.core.dataset import Dataset


def get_mfr(dataset: Dataset, average_count: int = 10) -> float:
    m = average_count
    d = dataset

    inj_date = d.get(
        "experiments/measurements/metadata", "parameter", "Injection Date"
    )[0].value
    inj_date_dt = datetime.strptime(inj_date, "%d-%b-%y, %H:%M:%S")

    mf_dt_list = (
        d.get(
            "experiments/measurements", "measurement_type", "MFM Measurement"
        )[0]
        .experimental_data[0]
        .values
    )
    mfr_list = (
        d.get(
            "experiments/measurements", "measurement_type", "MFM Measurement"
        )[0]
        .experimental_data[3]
        .values
    )
    mfr = []
    for i, time in enumerate(mf_dt_list):
        if time == inj_date_dt:
            for j in range(i - m, i + m + 1):
                mfr.append(mfr_list[j])
    mfr_mean = sum(mfr) / (m * 2 + 1)
    return inj_date_dt, mf_dt_list, mfr_list, mfr_mean
