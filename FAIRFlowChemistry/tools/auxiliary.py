import logging
import numpy as np

from FAIRFlowChemistry.core import Experiment
from FAIRFlowChemistry.core import Measurement
from FAIRFlowChemistry.core import Quantity
from FAIRFlowChemistry.core import MeasurementType
from sdRDM.base.listplus import ListPlus

from pydantic import BaseModel, Field, validator
from typing import List, Dict
from pathlib import Path
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
logger.propagate = True

class DirectoryNotFoundError(Exception):
    def __init__(self, directory):
        super().__init__(f"Directory not found: {directory}")

class Librarian(BaseModel):
    """
    Class that manages directoy and file browsing

    Args:
        BaseModel (_type_): _description_

    Raises:
        KeyError: _description_
        KeyError: _description_

    Returns:
        _type_: _description_
    """
    root_directory: Path

    def enumerate_subdirectories(self, directory: Path, verbose: bool = None):
        dir_dict = {
            index: dir
            for index, dir in enumerate(
                [x for x in directory.iterdir() if x.is_dir()]
            )
        }
        if verbose:
            print(f"Parent directory: \n {directory} \nAvailable subdirectories:")
            for index, dir in dir_dict.items():
                print(f"{index}: .../{dir.name}")

        return dir_dict

    def enumerate_files(
        self,
        directory: Path,
        filter: str = None,
        verbose: bool = None
    ):
        """
        Directory is set to the root directory.
        If no value is passed for filter, all file types will be considered.
        """

        suffix = "*." + filter if filter != None else "*"

        file_dict = { index: file for index, file in enumerate(directory.glob(suffix)) if file.is_file() }

        if verbose: 
            print(f"Directory: \n {directory} \nAvailable files:")
            for index, file in file_dict.items():
                print(f"{index}: {file.name}")

        return file_dict

    def search_files_in_subdirectory(self,root_directory: Path, directory_keys: list[str], file_filter: str, verbose: bool = None) -> Path:
        """
        Function that loobs through Path objects containing a main directory. In this directory it is recoursevly searched for sub directories. 
        In the last sub directory files with the suffix 'file_filter' are searched and returned

        Args:
            root_directory (Path): Root directory
            directory_keys (list[str]): List of subdirectories that should be recoursevly searched
            file_filter (str): Suffix of files that should be found in last given sub directory
            verbose (bool, optional): Possiblity to printout all subdirectories in each directory listed. Defaults to None.

        Raises:
            KeyError: If either the specified sub directory or file could not be found

        Returns:
            subdirectory_files (Path): Path object containing all files found in the subdirectory
        """

        # First search for every nested sub directory in provided root directory #
        
        root = self.enumerate_subdirectories(root_directory)
        for j,directory_key in enumerate(directory_keys):
            try:
                idx_sub_directory = [i for i in range(len(root)) if root[i].parts[-1] == directory_key ][0]
                if j < len(directory_keys)-1: 
                    root          = self.enumerate_subdirectories(directory=root[idx_sub_directory])
            except:
                raise KeyError("Defined key: '%s' cannot be found in the given root directory: %s"%(directory_key,root[0].parent))

        # Search for all files that match the given filter in the specified sub directory #
        subdirectory_files = self.enumerate_files(directory=root[idx_sub_directory], filter=file_filter, verbose=verbose)   
        if not bool(subdirectory_files): 
            raise KeyError("No files with filter: '%s' found in the given sub directory: %s"%(file_filter,root_directory[idx_sub_directory]))
        
        return subdirectory_files


    def visualize_directory_tree(
        self, directory: Path, indent=0, skip_directories=None
    ):
        if skip_directories is None:
            skip_directories = []

        if directory.is_dir():
            if directory.name in skip_directories:
                return

            print("  " * indent + f"[{directory.name}]")

            for item in directory.iterdir():
                if item.is_dir():
                    self.visualize_directory_tree(
                        item, indent + 1, skip_directories
                    )
                else:
                    print("  " * (indent + 1) + item.name)
        else:
            print("Directory not found.")

    @property
    def get_root_directory(self):
        return self.root_directory


class PeakAssigner(BaseModel):
    """
    Class that assign peaks of given GC measurements within a given experiment object

    Args:
        experiment (Experiment): Experiment object contain the GC measurements
        species (List): List with possible species that should be matched to the GC results
    """
    experiment: Experiment
    species: List[str]
    gc_measurements: ListPlus[Measurement] = Field(default_factory=ListPlus)
    peak_areas_retention_time_dict: Dict[str, Dict[str, List[float]]] = Field(default_factory=dict)
    typical_retention_time: Dict = Field(default_factory=dict)
    _assignment_dicts = []
    _selection_output = Output()
    _VBox_list = []
    _full_layout = VBox([])

    # The validator objects are used to give the variables during the initialisation a value.
    # This is normaly done in __init__, but this conflicts with Pydantic

    @validator("gc_measurements", pre=True, always=True)
    def validate_gc_measurements(cls,value, values):
        experiment = values.get("experiment")
        if experiment:
            return experiment.get("measurements", "measurement_type", MeasurementType.GC.value)[0]
        else:
            print("\n!!! Warning: Given experiment doesn't contain GC measurements !!!\n")
            return None
    
    @validator("peak_areas_retention_time_dict", pre=True, always=True)
    def valdiate_peak_areas_retention_time_dict(cls,value, values):
        tmp = {}
        for i, gc_measurement in enumerate(values.get("gc_measurements")):
            peak_areas     = gc_measurement.get("experimental_data", "quantity", Quantity.PEAKAREA.value)[0][0].values
            retention_time = gc_measurement.get("experimental_data", "quantity", Quantity.RETENTIONTIME.value)[0][0].values
            
            tmp[f"Measurement number {i}"] = { "peak_areas": peak_areas, "retention_time": retention_time }

        return tmp
    
    def save_assignments(self, _):
        """
        This functions create the assignment dict, after the button is clicked.
        The dict contains a dict per measurement which contains per species a list of assigned peak areas.
        """
        
        self._assignment_dicts.clear()

        # Iterate through every GC measurement
        for i,VBox in enumerate(self._VBox_list):
            _assignment_dict = {}

            # Iterate through the dropdown menus and extract the species per peak area
            # Start from index 2 and following, as the first two entries are labels
            for widget in VBox.children[2:]:

                # Dropdown in the last entry in each children
                species   = widget.children[2].value
                peak_area = float( widget.children[1].value )
                if species != "":
                    if species in _assignment_dict:
                        _assignment_dict[species].append( peak_area )
                    else:
                        _assignment_dict[species] = [ peak_area ]

            ## Add the assigned peaks as experimental data to the GC measurement ##

            # Add the species in the order the peak areas are saved
            tmp2 = np.round( self.gc_measurements[i].get("experimental_data","quantity",Quantity.PEAKAREA.value)[0][0].values, 2 ).tolist()

            # Sort the tuples based on peak values
            sorted_species_peak_tuples = sorted([(key, value) for key, values in _assignment_dict.items() for value in values], key=lambda x: tmp2.index(x[1]))

            # check if there is already an exisiting entry, if yes overwrite
            if bool(self.gc_measurements[i].get("experimental_data","quantity",Quantity.PEAKASSIGNMENT.value)):
                # Extract the species names in the sorted order
                self.gc_measurements[i].get("experimental_data","quantity",Quantity.PEAKASSIGNMENT.value)[0][0].values = [ item[0] for item in sorted_species_peak_tuples ]

            # if not then add
            else:
                self.gc_measurements[i].add_to_experimental_data( quantity= Quantity.PEAKASSIGNMENT.value,
                                                             values= [ item[0] for item in sorted_species_peak_tuples ]
                                                            )                   

            self._assignment_dicts.append( _assignment_dict.copy() )

        with self._selection_output:
            self._selection_output.clear_output(wait=False)
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
                
                # Set default values with a given dict (search for the species with the closest retention time and pick it as standard value)
                idx           = np.argmin( [ abs( trt[1] - retention_time ) for trt in self.typical_retention_time.items() if trt[0] in self.species ] )
                default_value = list( self.typical_retention_time.items() )[idx][0]

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
                hbox.children[2].options = [""]+new_options

                # Set default values with a given dict
                retention_time           = float( hbox.children[0].value )
                # Set default values with a given dict (search for the species with the closest retention time and pick it as standard value)
                idx                      = np.argmin( [ abs( trt[1] - retention_time ) for trt in self.typical_retention_time.items() if trt[0] in new_options ] )
                default_value            = list( self.typical_retention_time.items() )[idx][0]

                hbox.children[2].value   = default_value