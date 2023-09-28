import logging

from datamodel_b07_tc.modified.measurement import Measurement
from time import sleep
from pydantic import BaseModel
from typing import List, Dict

from ipywidgets import (
    VBox,  # Vertical container for widgets (called its children)
    HBox,  # Horizontal container for widgets
    Output,  # Widget for displaying output from other widgets
    Label,  # Simple string label widget, useful for displaying text
    Dropdown,  # Classic dropdown menu
    Button,  # Classic button
    Layout,
)

logger = logging.getLogger(__name__)


class PeakAssigner(BaseModel):
    peak_areas_dict: Dict[str, List[float]]
    species: List[str]
    _assignment_dicts = []  # List[Dict[str, List[float]]]
    _selection_output = Output()
    # _assignments_dicts_of_measurements = List[getattr(_assignment_dicts, "type")]
    _VBox_list = []

    @classmethod
    def from_gc_measurement(cls, gc_measurements, species):
        peak_areas_dict = {}
        for i, gc_measurement in enumerate(gc_measurements):
            if gc_measurement.measurement_type == "GC measurement":
                peak_areas = gc_measurement.get(
                    "experimental_data", "quantity", "Peak area"
                )[0][0].values
                peak_areas = [float(peak_area) for peak_area in peak_areas]
            else:
                raise TypeError(f"{gc_measurement} is not a GC measurement")
            peak_areas_dict[f"Measurement number {i}"] = peak_areas
        return cls(peak_areas_dict=peak_areas_dict, species=species)

    def save_assignments(self, button):
        _assignment_dict = {}
        self._assignment_dicts.clear()
        for _VBox in self._VBox_list:
            hbox_list = _VBox.children
            _assignment_dict.clear()
            for widget in hbox_list[2:]:
                species = widget.children[1].value
                peak_area = float(widget.children[0].value)
                if species != "":
                    if species in _assignment_dict:
                        _assignment_dict[species].append(peak_area)
                    else:
                        _assignment_dict[species] = [peak_area]
            self._assignment_dicts.append(_assignment_dict.copy())

        with self._selection_output:
            self._selection_output.clear_output(wait=False)
            sleep(1)
            print("Assignments saved.")

    def assign_peaks(self):
        layout_button = Layout(
            # display="flex",
            # flex_flow="column",
            align_items="center",
            width="30%",
        )
        layout_hbox = Layout(
            # display="flex",
            # flex_flow="column",
            align_items="stretch",
            width="100%",
            justify_content="center",
        )
        layout_vbox = Layout(
            # display="flex",
            # flex_flow="column",
            # align_items="stretch",
            width="100%",
        )
        self._VBox_list.clear()
        for measurement_number, peak_areas in self.peak_areas_dict.items():
            hbox_list = [
                Label(
                    value=measurement_number,
                    layout=Layout(
                        width="60%", height="30px", justify_content="center"
                    ),
                )
            ]
            hbox_list.append(
                HBox(
                    [
                        Label(
                            value="Peak area",
                            layout=Layout(width="20%", height="30px"),
                        ),
                        Label(
                            value="Species",
                            layout=Layout(width="40%", height="30px"),
                        ),
                    ]
                )
            )
            for peak_area in peak_areas:
                dropdown = Dropdown(
                    options=[""] + self.species,
                    layout=Layout(width="40%", height="30px"),
                    style={"description_width": "initial"},
                )
                label = Label(
                    value=f"{peak_area:.2f}",
                    layout=Layout(width="20%", height="30px"),
                )
                hbox = HBox([label, dropdown])
                hbox_list.append(hbox)
            self._VBox_list.append(
                VBox(children=hbox_list, layout=layout_vbox)
            )
            display_button = Button(
                description="Save Assignments", layout=layout_button
            )
            display_button.on_click(self.save_assignments)

        # display(HBox(children=VBox_list, layout=layout_hbox))
        display(HBox(children=self._VBox_list, layout=layout_hbox))
        display(
            HBox(
                children=[display_button],
                layout=Layout(justify_content="center"),
            )
        )
        display(self._selection_output)

    # def assign_peaks(self):
    #     VBox_list = []
    #     for peak_areas in self.peak_areas_dict.values():
    #         # hbox_list.clear()
    #         hbox_list.append(
    #             HBox(
    #                 [
    #                     Label(
    #                         value="Peak area",
    #                         layout=Layout(width="10%", height="20px"),
    #                     ),
    #                     Label(
    #                         value="Species", layout={"width": "max-content"}
    #                     ),
    #                 ]
    #             )
    #         )
    #         for peak_area in peak_areas:
    #             dropdown = Dropdown(
    #                 options=[""] + self.species,
    #                 layout={"width": "max-content"},
    #                 style={"description_width": "initial"},
    #             )
    #             label = Label(
    #                 value=f"{peak_area:.2f}",
    #                 layout=Layout(width="5%", height="20px"),
    #             )
    #             hbox = HBox([label, dropdown])
    #             hbox_list.append(hbox)
    #     VBox_list.append(VBox(hbox_list))
    #     display_button = Button(description="Save Assignments")
    #     display_button.on_click(self.save_assignments)

    #     display(HBox(VBox_list))
    #     # display(display_button)
    #     # display(self._selection_output)
