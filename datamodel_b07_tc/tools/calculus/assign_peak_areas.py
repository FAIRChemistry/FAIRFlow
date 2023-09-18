from pydantic import BaseModel
from pydantic import PrivateAttr
from datamodel_b07_tc.core.measurement import Measurement


class PeakAreaAssignment(BaseModel):

    peak_areas_index_dict: dict

    @classmethod
    def from_gc_measurement(cls, gc_measurement: Measurement):
        _gc_peak_areas: list = gc_measurement.get("experimental_data", "quantity", "Peak area")[0][0].values
        _gc_peak_numbers: list = gc_measurement.get("experimental_data", "quantity", "Peak number")[0][0].values
        peak_areas_index_dict = {index:peak for peak, index in zip(_gc_peak_areas, list(map(int, _gc_peak_numbers)))}
        return cls(peak_areas_index_dict=peak_areas_index_dict)


    def assign(self, peak_assignment_dict: dict) -> dict:

        assigned_peak_areas_dict = {}
        for species, index_list in peak_assignment_dict.items():
            for index in index_list:
                for i, peak in enumerate(
                    self.peak_areas_index_dict.keys()
                ):
                    if index == peak:
                        assigned_peak_areas_dict[species] = (
                            list(self.peak_areas_index_dict.values())[i]
                        )
        return assigned_peak_areas_dict

    @property
    def get_peak_areas_index_dict(self) -> dict:
        return self.peak_areas_index_dict














    # peak_area_dict = {}
    # for key, value in peak_assign_dict.items():
    #     for number in value:
    #         for i, peak in enumerate(
    #             experiment.measurements[2].experimental_data[0].values
    #         ):
    #             if number == peak:
    #                 peak_area_dict[key] = (
    #                     experiment
    #                     .measurements[2]
    #                     .experimental_data[4]
    #                     .values[i]
    #                 )
    # return peak_area_dict
