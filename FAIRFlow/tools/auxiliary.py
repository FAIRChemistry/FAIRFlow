import logging
import numpy as np
import ipywidgets as widgets

from pathlib import Path
from typing import List, Dict, Callable
from pydantic import BaseModel
from IPython.display import display
from FAIRFlow.core import Experiment
from FAIRFlow.core import Quantity
from FAIRFlow.core import MeasurementType
from ipywidgets import (
    VBox,  # Vertical container for widgets (called its children)
    HBox,  # Horizontal container for widgets
    Output,  # Widget for displaying output from other widgets
    Label,  # Simple string label widget, useful for displaying text
    Dropdown,  # Classic dropdown menu
    Button,  # Classic button
    Layout,  # Layout specification object
    TagsInput
)

logger = logging.getLogger("main")

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
        
        if len(directory_keys) == 1 and directory_keys[0] == ".":
            subdirectory_files = self.enumerate_files(directory=root_directory, filter=file_filter, verbose=verbose)   

            if not bool(subdirectory_files): 
                raise KeyError("No files with filter: '%s' found in the given directory: %s"%(file_filter,root_directory))
        
        else:
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
                raise KeyError("No files with filter: '%s' found in the given sub directory: %s"%(file_filter,root[idx_sub_directory]))
        
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

class explorer:
    """
    This class is a widget that allows to scroll through folders and select files
    """
    # Function to navigate into the selected subfolder
    def go_to_subfolder(self,_):
        self.current_dir.value       = str(self.folder_dropdown.value)
        subroot                      = self.librarian.enumerate_subdirectories(directory=self.folder_dropdown.value)
        self.folder_dropdown.options = [ (path.parts[-1],path) for _,path in subroot.items() ] if bool(subroot) else [ ("No subdirectories",self.folder_dropdown.value) ]

    # Function to navigate back from the selected subfolder
    def go_to_parentfolder(self,_):
        parentfolder                 = self.parent
        self.current_dir.value       = str(parentfolder)
        parentroot                   = self.librarian.enumerate_subdirectories(directory=parentfolder)
        self.folder_dropdown.options = [(path.parts[-1],path) for _,path in parentroot.items()]

    def folder_dropdown_option_handler(self,_):
        # If no subdirectories exist, then the parent folder is simply the first parent, otherwise it is the 2nd parent
        # (because the current dropdown value is already one deeper than the actual directory )
        if str(self.folder_dropdown.value.parent) == self.current_dir.value:
            self.parent                  = self.folder_dropdown.value.parent.parent
            self.file_folder             = self.folder_dropdown.value.parent
        else:
            self.parent                  = self.folder_dropdown.value.parent
            self.file_folder             = self.folder_dropdown.value

        # Reset file type after chaning dropdown

        self.file_type_text.value        = ""
        self.file_dropdown.options       = []

    def file_type_input_handler(self,_):
        if self.file_type_text.value:
            file_filter                  = self.file_type_text.value
            subdirectory_files           = self.librarian.enumerate_files(directory=self.file_folder, filter=file_filter)
            
            # Show all available files and show the first initially that they know if file are available
            try:
                self.file_dropdown.options   = [(file.parts[-1],file) for _,file in subdirectory_files.items()]
                self.file_dropdown.value     = subdirectory_files[0]
            except:
                self.file_dropdown.options   = ["No files with specified suffix"]
                self.file_dropdown.value     = "No files with specified suffix"
    
    def file_category_input_handler(self,_):
        self.button_select.description = 'Add file to %s'%(self.file_category.value)

    def add_file(self,_):
        self.add_file_callalbe( self.file_category.value, str(self.file_dropdown.value) )
    
    def main(self, root: str, file_categories: List[str], add_file_callalbe: Callable[[str,str], None]):

        self.librarian         = Librarian(root_directory=root)
        sub_directories        = self.librarian.enumerate_subdirectories(directory=root)
        self.file_folder       = root
        self.add_file_callalbe = add_file_callalbe


        self.folder_dropdown  = widgets.Dropdown(description='Select directory:',
                                                options=[(path.parts[-1],path) for _,path in sub_directories.items()],
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.file_dropdown    = widgets.Dropdown(description='Select file:',
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})
        
        self.file_category    = widgets.Dropdown(options=file_categories,
                                                value=file_categories[0],
                                                description='for category:',
                                                style={'description_width': 'auto'})
        
        self.file_type_text   = widgets.Text(description='File type:',
                                            placeholder='Enter type here (e.g.: csv, json, ... or * for all files)',
                                            layout=widgets.Layout(width='auto'),
                                            style={'description_width': 'auto'})
        
        self.current_dir      = widgets.Text(description='Current directory:',
                                            disabled=True,
                                            value=str(root),
                                            layout=widgets.Layout(width='auto'),
                                            style={'description_width': 'auto'})

        self.button_go_for    = widgets.Button(description='Change into selected directory',
                                              layout=widgets.Layout(width='auto'))
        
        self.button_go_back   = widgets.Button(description='Change into parent diretory',
                                              layout=widgets.Layout(width='auto'))
        
        self.button_select    = widgets.Button(description='Add file to %s'%(self.file_category.value),
                                              layout=widgets.Layout(width='auto'))
        

        # Attach the event handler to the 'value' property change of the file type widget
        self.file_type_text.observe(self.file_type_input_handler, names='value')
        self.folder_dropdown.observe(self.folder_dropdown_option_handler, names='options')
        self.file_category.observe(self.file_category_input_handler, names='value')
        
        # Functions for the buttons
        self.button_go_for.on_click(self.go_to_subfolder)
        self.button_go_back.on_click(self.go_to_parentfolder)
        self.button_select.on_click(self.add_file)

        # Display the widgets

        # Create the layout
        v_space_s = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='15px'))

        widgets0  = widgets.VBox([self.current_dir,v_space_s,self.folder_dropdown])
        widgets1  = widgets.HBox([self.button_go_for, self.button_go_back])
        widgets2  = widgets.VBox([v_space_s,self.file_type_text])
        widgets3  = widgets.HBox([self.file_dropdown,self.file_category])
        widgets4  = widgets.VBox([v_space_s,self.button_select])

        # Combine the layout
        full_layout = widgets.VBox([widgets0,widgets1,widgets2,widgets3,widgets4])

        # Return the layout
        return full_layout

class PeakAssigner:
    """
    Class that assign peaks of given GC measurements within a given experiment object
    """

    def __init__(self, experiment: Experiment, species: List[str], typical_retention_time: Dict = {}, lower_assignment_bound: float=0.1 ):
        """
        Args:
            experiment (Experiment): Experiment object contain the GC measurements
            species (List): List with possible species that should be matched to the GC results
            typical_retention_time (dict, optional): Dictionary with typical retenion times to pre assign peak values. Defaults to {}.
            lower_assignment_bound (float, optional): Preassignment boundary for typical retention time dictionary and measured retetion time values. Defaults to 0.1.
        """
        self.experiment = experiment
        self.species    = species
        self.typical_retention_time = typical_retention_time
        self.lower_assignment_bound = lower_assignment_bound
        self._assignment_dicts = []
        self._selection_output = Output()
        self._VBox_list = []
        self._full_layout = VBox([])
        self.signal_types = []

        self.peak_areas_retention_time_dict = {}

        # Get the GC measurements and make a dictionary for each measurement
        gc_measurements = self.experiment.get("measurements", "measurement_type", MeasurementType.GC.value)

        if len(gc_measurements) > 0:

            # Get signal types
            self.signal_types = [ md.value for md in gc_measurements[0][0].metadata if "Signal" in md.parameter ]
            
            for i, gc_measurement in enumerate(gc_measurements[0]):
                peak_areas     = gc_measurement.get("experimental_data", "quantity", Quantity.PEAKAREA.value)[0][0].values
                retention_time = gc_measurement.get("experimental_data", "quantity", Quantity.RETENTIONTIME.value)[0][0].values
                signal_type    = gc_measurement.get("experimental_data", "quantity", Quantity.SIGNAL.value)[0][0].values

                self.peak_areas_retention_time_dict[f"Measurement number {i}"] = { "peak_areas": peak_areas, 
                                                                                   "retention_time": retention_time,
                                                                                    "signal_type": signal_type }
        else:
            logger.info("\n!!! Warning: Given experiment doesn't contain GC measurements !!!\n")


        # Check if the GC measurement already has a assignment and use this instead of the typical retention time dictionary
        try:
            assigned_retention_time_dict = {}

            peak_assignments = gc_measurement.get("experimental_data","quantity",Quantity.PEAKASSIGNMENT.value)[0][0].values
            retention_time   = gc_measurement.get("experimental_data","quantity",Quantity.RETENTIONTIME.value)[0][0].values

            for species,ret_time in zip( peak_assignments, retention_time):
                # Prevent that not assigned peak will be used for analysis
                if species :
                    assigned_retention_time_dict[species] = ret_time

            self.typical_retention_time = assigned_retention_time_dict
            logger.info("\nGC measurement already contains an assignment. Use this assignment rather than the default dictionary.\n")
        except:
            pass

        
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
                peak_area = float( widget.children[1].value.split("(")[0].strip() )

                if species in _assignment_dict:
                    _assignment_dict[species].append( peak_area )
                else:
                    _assignment_dict[species] = [ peak_area ]

            ## Add the assigned peaks as experimental data to the GC measurement ##

            gc_measurement = self.experiment.get("measurements", "measurement_type", MeasurementType.GC.value)[0][i]

            # Add the species in the order the peak areas are saved
            tmp2 = np.round( gc_measurement.get("experimental_data","quantity",Quantity.PEAKAREA.value)[0][0].values, 2 ).tolist()

            # Sort the tuples based on peak values
            sorted_species_peak_tuples = sorted( [(key, value) for key, values in _assignment_dict.items() for value in values], key=lambda x: tmp2.index(x[1]) )
            
            # check if there is already an exisiting entry, if yes overwrite
            if all( gc_measurement.get("experimental_data","quantity",Quantity.PEAKASSIGNMENT.value) ):
                
                # Extract the species names in the sorted order --> if a peak has no species assignment its saved as: ""
                gc_measurement.get("experimental_data","quantity",Quantity.PEAKASSIGNMENT.value)[0][0].values = [ item[0] for item in sorted_species_peak_tuples ]

            # if not then add
            else:
                gc_measurement.add_to_experimental_data( quantity = Quantity.PEAKASSIGNMENT.value,
                                                         values   = [ item[0] for item in sorted_species_peak_tuples ],
                                                         unit     = ""
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
        
            for peak_area, retention_time, signal_type in zip( peak_areas_retention_time["peak_areas"], 
                                                               peak_areas_retention_time["retention_time"],
                                                               peak_areas_retention_time["signal_type"]):
                
                try:
                    # Set default values with a given dict (search for the species with the closest retention time and pick it as standard value)
                    diff          = [ abs( trt[1] - retention_time ) for trt in self.typical_retention_time.items() if trt[0] in self.species ]
                    if np.min(diff) < self.lower_assignment_bound:
                        idx           = np.argmin( diff )
                        default_value = list( self.typical_retention_time.items() )[idx][0]
                    else:
                        default_value = ""
                except:
                    default_value = ""

                dropdown             = Dropdown( options = [""] + self.species,
                                                 layout  = Layout(width="40%", height="30px"),
                                                 style   = {"description_width": "initial"},
                                                 value   = default_value)
                
                retention_time_label = Label( value  = f"{retention_time:.2f} (Signal: {signal_type:.0f})",
                                              layout = Layout(width="30%", height="30px"))

                peak_area_label      = Label( value  = f"{peak_area:.2f}",
                                              layout = Layout(width="20%", height="30px"))
                
                hbox_list.append( HBox( [ retention_time_label, peak_area_label, dropdown ] ) )

            # Append the vertical box for each measurement to the overall list with every vertical boxes
            self._VBox_list.append( VBox( children = hbox_list, layout = layout_vbox ) )

        # Create a button to save the assignments made
        display_button = Button( description="Save Assignments",
                                 layout=layout_button)
        
        # Handle button on click
        display_button.on_click(self.save_assignments)
        v_space   = VBox([Label(value='')], layout=Layout(height='30px'))

        # Description of signals:
        signal_descripton = TagsInput(allow_duplicates=False,
                                      layout = Layout(width="30%", height="30px")  
                                )
        
        signal_descripton.value = [ f'{i}: {stype}' for i,stype in enumerate(self.signal_types) ]

        signal_widget = widgets.VBox(
            [
                widgets.Label(value="GC Signal:"),
                signal_descripton,
            ]
        )


        # Define the total layout
        widget0 = [ HBox(children=self._VBox_list[i:i+3], layout=layout_hbox) for i in range( 0, len(self._VBox_list), 3 ) ]
        widget1 = HBox(children=[display_button],layout=Layout(justify_content="center"))
        widget2 = self._selection_output

        full_layout = VBox([signal_widget,v_space,*widget0,v_space,widget1,widget2])

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

                try:
                    # Set default values with a given dict (search for the species with the closest retention time and pick it as standard value)
                    diff          = [ abs( trt[1] - retention_time ) for trt in self.typical_retention_time.items() if trt[0] in self.species ]
                    if np.min(diff) < self.lower_assignment_bound:
                        idx           = np.argmin( diff )
                        default_value = list( self.typical_retention_time.items() )[idx][0]
                    else:
                        default_value = ""
                except:
                    default_value = ""

                hbox.children[2].value   = default_value