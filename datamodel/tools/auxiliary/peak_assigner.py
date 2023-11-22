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

typical_retention_time = {"Hydrogen": 1.7, "Carbon dioxide": 3.0, "Carbon monoxide": 13.6, 
                          "Methane": 3.6, "Ethene": 6.0, "Ethane": 7.1}


class PeakAssigner(BaseModel):
    peak_areas_retention_time_dict: Dict[str, Dict[str, List[float]]]
    species: List[str]
    _assignment_dicts = []
    _selection_output = Output()
    _VBox_list = []
    _full_layout = VBox([])

    def save_assignments(self, _):
        """
        This functions create the assignment dict, after the button is clicked.
        The dict contains a dict per measurement which contains per species a list of assigned peak areas.
        """
        
        self._assignment_dicts.clear()

        for VBox in self._VBox_list:
            _assignment_dict = {}
            # Iterate through the dropdown menus and extract the species per peak area
            # Start from index 2 and following, as the first two entries are the measurement label 
            # and retention time, peak area and species label

            for widget in VBox.children[2:]:
                species   = widget.children[2].value
                peak_area = float( widget.children[1].value )
                if species != "":
                    if species in _assignment_dict:
                        _assignment_dict[species].append( peak_area )
                    else:
                        _assignment_dict[species] = [ peak_area ]

            self._assignment_dicts.append( _assignment_dict.copy() )

        with self._selection_output:
            self._selection_output.clear_output(wait=False)
            sleep(1)
            print("Assignments saved.")

    def assign_peaks(self):
        """
        Function that displays a widget with the GC measurements: Retention time, peak area, and one need to choose a corresponding species
        """
        # Set layout of widgets
        layout_button = Layout( align_items="center", width="30%" )
        layout_hbox   = Layout( align_items="stretch", width="100%", justify_content="center" )
        layout_vbox   = Layout( width="100%" )

        self._VBox_list.clear()

        for measurement_number, peak_areas_retention_time in self.peak_areas_retention_time_dict.items():
            
            # For each measurement create a horizontal box containing the retention time, peak area and species
            hbox_list = [ Label( value  = measurement_number, 
                                 layout = Layout(width="60%", height="30px", justify_content="center") ),

                          HBox( [ Label( value="Retention time",
                                         layout=Layout(width="30%", height="30px")),
                                  Label( value="Peak area",
                                         layout=Layout(width="20%", height="30px")),
                                  Label( value="Species",
                                         layout=Layout(width="40%", height="30px")) ] ) ]
        
            for peak_area, retention_time in zip(peak_areas_retention_time["peak_areas"], peak_areas_retention_time["retention_time"]):
                
                # Set default values with a given dict
                default_value = [trt[0] for trt in typical_retention_time.items() if (abs( trt[1] - retention_time ) < 0.6) and (trt[0] in self.species) ]
                default_value = default_value[0] if bool(default_value) else ""

                dropdown             = Dropdown( options = [""] + self.species,
                                                 layout  = Layout(width="40%", height="30px"),
                                                 style   = {"description_width": "initial"},
                                                 value   = default_value)
                
                retention_time_label = Label( value  = f"{retention_time:.2f}",
                                              layout = Layout(width="30%", height="30px"))

                peak_area_label      = Label( value  = f"{peak_area:.2f}",
                                              layout = Layout(width="20%", height="30px"))
                
                hbox_list.append( HBox( [ retention_time_label, peak_area_label, dropdown ] ) )

            # Append the bertical box for each measurement to the overall list with every vertical boxes
            self._VBox_list.append( VBox( children = hbox_list, layout = layout_vbox ) )

        # Create a button to save the assignments made
        display_button = Button( description="Save Assignments",
                                 layout=layout_button)
        
        # Handle button on click
        display_button.on_click(self.save_assignments)
        
        # Define the total layout
        widget0 = HBox(children=self._VBox_list, layout=layout_hbox)
        widget1 = HBox(children=[display_button],layout=Layout(justify_content="center"))
        widget2 = self._selection_output

        full_layout = VBox([widget0,widget1,widget2])

        display(full_layout)

    def modify_dropdown_options(self, new_options):
        """
        Function that takes new list of species and update the widget dropdowns

        Args:
            new_options (list): New species
        """

        for vbox in self._VBox_list:
            for hbox in vbox.children[2:]:
                # For each Hbox, the retention time is children 0, the peak area children 1 and the dropdown is the 2nd

                # Overwrite the dropdown the new options
                hbox.children[2].options = new_options

                # Set default values with a given dict
                retention_time           = float( hbox.children[0].value )
                default_value            = [trt[0] for trt in typical_retention_time.items() if (abs( trt[1] - retention_time ) < 0.6) and (trt[0] in new_options) ]
                default_value            = default_value[0] if bool(default_value) else ""

                hbox.children[2].value   = default_value