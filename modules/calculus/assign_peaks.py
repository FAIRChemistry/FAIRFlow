from datamodel_b07_tc.core.dataset import Dataset


def assign_peaks(dataset: Dataset, peak_assign_dict: dict) -> dict:
    d = dataset
    p = peak_assign_dict

    peak_area_dict = {}
    for key, value in p.items():
        for number in value:
            for i, peak in enumerate(
                d.experiments[0].measurements[2].experimental_data[0].values
            ):
                if number == peak:
                    peak_area_dict[key] = (
                        d.experiments[0]
                        .measurements[2]
                        .experimental_data[4]
                        .values[i]
                    )
    return peak_area_dict
