from datamodel_b07_tc.core.experiment import Experiment


def assign_peaks(experiment: Experiment, peak_assign_dict: dict) -> dict:

    peak_area_dict = {}
    for key, value in peak_assign_dict.items():
        for number in value:
            for i, peak in enumerate(
                experiment.measurements[2].experimental_data[0].values
            ):
                if number == peak:
                    peak_area_dict[key] = (
                        experiment
                        .measurements[2]
                        .experimental_data[4]
                        .values[i]
                    )
    return peak_area_dict
