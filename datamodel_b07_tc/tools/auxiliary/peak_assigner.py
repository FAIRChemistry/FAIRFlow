import logging

from time import sleep
from pydantic import BaseModel
from typing import List, Dict
from IPython.display import display
from ipywidgets import (
    VBox,  # Vertical container for widgets (called its children)
    HBox,  # Horizontal container for widgets
    Output,  # Widget for displaying output from other widgets
    Label,  # Simple string label widget, useful for displaying text
    Dropdown,  # Classic dropdown menu
    Button,  # Classic button
    Layout,  # Layout specification object
)

logger = logging.getLogger(__name__)


class PeakAssigner(BaseModel):
    peak_areas_retention_time_dict: Dict[str, Dict[str, List[float]]]
    species: List[str]
    _assignment_dicts = []  # List[Dict[str, List[float]]]
    _selection_output = Output()
    _VBox_list = []
    _full_layout = VBox([])

    @classmethod
    def from_gc_measurement(cls, gc_measurements, species):
        peak_areas_retention_time_dict = {}
        for i, gc_measurement in enumerate(gc_measurements):
            if gc_measurement.measurement_type == "GC measurement":
                peak_areas = gc_measurement.get(
                    "experimental_data", "quantity", "Peak area"
                )[0][0].values
                peak_areas = [float(peak_area) for peak_area in peak_areas]
                retention_time = gc_measurement.get(
                    "experimental_data", "quantity", "Retention time"
                )[0][0].values
            else:
                raise TypeError(f"{gc_measurement} is not a GC measurement")
            peak_areas_retention_time_dict[f"Measurement number {i}"] = {
                "peak_areas": peak_areas,
                "retention_time": retention_time,
            }
        return cls(
            peak_areas_retention_time_dict=peak_areas_retention_time_dict,
            species=species,
        )

    def save_assignments(self, button):
        _assignment_dict = {}
        self._assignment_dicts.clear()
        for _VBox in self._VBox_list:
            hbox_list = _VBox.children
            _assignment_dict.clear()
            for widget in hbox_list[2:]:
                species = widget.children[2].value
                peak_area = float(widget.children[1].value)
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
            align_items="center",
            width="30%",
        )
        layout_hbox = Layout(
            align_items="stretch",
            width="100%",
            justify_content="center",
        )
        layout_vbox = Layout(
            width="100%",
        )
        self._VBox_list.clear()
        for (
            measurement_number,
            peak_areas_retention_time,
        ) in self.peak_areas_retention_time_dict.items():
            peak_areas = peak_areas_retention_time["peak_areas"]
            retention_time = peak_areas_retention_time["retention_time"]
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
                            value="Retention time",
                            layout=Layout(width="30%", height="30px"),
                        ),
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
            for peak_area, retention_time in zip(peak_areas, retention_time):
                dropdown = Dropdown(
                    options=[""] + self.species,
                    layout=Layout(width="40%", height="30px"),
                    style={"description_width": "initial"},
                )
                retention_time_label = Label(
                    value=f"{retention_time:.2f}",
                    layout=Layout(width="30%", height="30px"),
                )

                peak_area_label = Label(
                    value=f"{peak_area:.2f}",
                    layout=Layout(width="20%", height="30px"),
                )
                hbox = HBox([retention_time_label, peak_area_label, dropdown])
                hbox_list.append(hbox)
            self._VBox_list.append(
                VBox(children=hbox_list, layout=layout_vbox)
            )
            display_button = Button(
                description="Save Assignments", layout=layout_button
            )
            display_button.on_click(self.save_assignments)
        

        widget0 = HBox(children=self._VBox_list, layout=layout_hbox)
        widget1 = HBox(children=[display_button],layout=Layout(justify_content="center"))
        widget2 = self._selection_output

        full_layout = VBox([widget0,widget1,widget2])

        display(full_layout)

    def modify_dropdown_options(self, new_options):

            for vbox in self._VBox_list:
                for hbox in vbox.children[2:]:
                    dropdown = hbox.children[2]
                    # Assuming the Dropdown is always at index 2, modify its options
                    dropdown.options = new_options
                    # Preventing value to be first entry of new options
                    dropdown.value = None


    @property
    def get_assignment_dicts(self):
        return self._assignment_dicts
