from datetime import datetime
from datamodel_b07_tc.core.dataset import Dataset


def get_mfm(dataset: Dataset) -> float:
    d = dataset

    query_inj_date = (
        '{measurements {metadata (parameter: "Injection Date") {value}}}'
    )

    inj_date = d.query(query_inj_date)["measurements"][1]["metadata"][0][
        "value"
    ]

    inj_date_datetime = datetime.strptime(inj_date, "%d-%b-%y, %H:%M:%S")
    inj_date_datetime
    vol_flows = []
    m = 10
    for i, time in enumerate(mfm_exp_data_df["datetime"]):
        if time.to_pydatetime() == inj_date_datetime:
            for j in range(i - m, i + m + 1):
                vol_flows.append(mfm_exp_data_df.at[j, "flow"])
    vol_flow_mean = sum(vol_flows) / (m * 2 + 1)
    return vol_flow_mean
