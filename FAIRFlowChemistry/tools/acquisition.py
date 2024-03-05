#!~/miniconda3/bin/python

import ipywidgets as widgets
from pathlib import Path
from IPython.display import display

# Import general tools and objects of this datamodel #

# Objects #
from FAIRFlowChemistry.core import Dataset
from FAIRFlowChemistry.core import Experiment

# Tools #
from .auxiliary import Librarian
from .reader import gc_parser, gstatic_parser, mfm_parser

import ipywidgets as widgets
from typing import List, Callable
from FAIRFlowChemistry.tools.auxiliary import Librarian

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
        
        self.button_go_back   = widgets.Button(description='Change to parent diretory',
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

class measurement_object:
    """
    Class that stores widgets for measurement files
    """
    def __init__(self, name: str) -> None:

        self.name          = name
        self.galvano_files = widgets.TagsInput(allow_duplicates=False)
        self.GC_files      = widgets.TagsInput(allow_duplicates=False)
        self.MFM_files     = widgets.TagsInput(allow_duplicates=False)

        widgets0  = widgets.VBox([widgets.Label(value='Files for galvanostat:'), self.galvano_files])
        widgets1  = widgets.VBox([widgets.Label(value='Files for gas chromatography:'), self.GC_files])
        widgets2  = widgets.VBox([widgets.Label(value='Files for mass flow meter:'), self.MFM_files])

        # Combine the layout
        self.full_layout = widgets.VBox([widgets0,widgets1,widgets2])

class reading_raw_data_widget():
    
    def measurement_tabs(self):
        # Define tab widget
        self.tabs  = widgets.Tab( [obj.full_layout for obj in self.measurement_objects] )

        # Set title of the tabs
        for i,title in enumerate( [ obj.name for obj in self.measurement_objects ] ):
            self.tabs.set_title(i, title)

        heading = widgets.Label(value="Files for measurements:")

        self.tab_widget = widgets.VBox([ heading, self.tabs ])

    def save_dataset(self,_):
        # Function to save dataset
        with open(self.dataset_dropdown.value, "w") as f: f.write(self.dataset.json())
        print("Dataset saved.")
    
    def add_file(self, category: str, file: str ):
        # Function that adds a file to a chosen category
        # The file is added to the selected measurement tab to the selected children (galvanostat, gas chromatography, etc.)
        if category == "Galvanostat":
            self.tabs.children[self.tabs.selected_index].children[0].children[1].value = (
                self.tabs.children[self.tabs.selected_index].children[0].children[1].value +
                [file]
            )
        elif category == "Gas chromatography":
            self.tabs.children[self.tabs.selected_index].children[1].children[1].value = (
                self.tabs.children[self.tabs.selected_index].children[1].children[1].value +
                [file]
            )
        elif category == "Mass flow meter":
            self.tabs.children[self.tabs.selected_index].children[2].children[1].value = (
                self.tabs.children[self.tabs.selected_index].children[2].children[1].value +
                [file]
            )
        elif category == "Species data":
            self.species_file.value  = file

        elif category == "P&ID":
            self.pid_file.value      = file
        
    def add_experiment(self,_):

        ## Read in selected raw data and save it in Experiment class ##
        if not self.experiment_name.value:
            raise ValueError("Provide experiment name!\n")
        
        experiment                 = Experiment( id = self.experiment_name.value )
        
        potentiostatic_measurement = [ gstatic_parser( metadata_path = self.galvano_files.value[0] ) ]
        mfm_measurement            = [ mfm_parser( experimental_data_path = mfm_file ) for mfm_file in self.MFM_files.value ]
        gc_measurements_list       = [ gc_parser( metadata_path = self.GC_files.value[i], experimental_data_path = self.GC_files.value[i+1] ) for i in range( 0, len(self.GC_files.value), 2 ) ]

        experiment.measurements    = [ *potentiostatic_measurement, *mfm_measurement, *gc_measurements_list ]

        # Initialize species data such as calibration, correction factors and transfering eletron number
        experiment.initialize_species_from_yaml( self.species_file.value )

        # Append new experiment to current dataset
        self.dataset.experiments.append( experiment )
        
        # Update experiment list
        self.experiments.value = [ exp.id for exp in self.dataset.experiments ]

        # Empty files widget
        self.measurements.value    = []
        self.measurement_input_handler()
        self.experiment_name.value = ""
        
    def dataset_input_handler(self,_):
        try:
            self.flag              = True
            with open(self.dataset_dropdown.value) as f:
                self.dataset = Dataset.from_json(f)
            self.experiments.value = [ exp.id for exp in self.dataset.experiments ]
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")
    
    def measurement_input_handler(self,_):

        # Delete measurement object that are not in the measurements widget anymore
        del_idx = [ i for i,obj in enumerate(self.measurement_objects) if not obj.name in self.measurements.value ]
        del_idx.sort( reverse = True)

        for idx in del_idx:
            del self.measurement_objects[idx]

        # Get names of current experiments
        measurement_names = [ obj.name for obj in self.measurement_objects ]

        # Add new measurement objects if they are not already there
        for i, measurement in enumerate(self.measurements.value):
            if not measurement in measurement_names:
                self.measurement_objects.insert( i, measurement_object( name = measurement ) )

        # Call measurement tab widget
        self.measurement_tabs()
    
    def experiment_input_handler(self,change):
        # This function only updates the experiment list, if a experiment is deleted from the tags it self
        if len(change["old"]) > len(change["new"]) and not self.flag:
            dummy = [ idx for idx,val in enumerate(change["old"]) if val not in change["new"]][0]
            self.dataset.experiments.pop(dummy)
            self.experiments.value = [ exp.id for exp in self.dataset.experiments ]
        else:
            pass
        self.flag = False
    

    def choose_data(self, root: Path, dataset_directory: str) -> None:
        
        self.librarian        = Librarian(root_directory=root)
        datasets              = self.librarian.search_files_in_subdirectory(root_directory=root, directory_keys=[dataset_directory], file_filter="json", verbose=False)
        self.flag             = False

        # Call explorer widget
        self.explorer         = explorer()
        explorer_widget       = self.explorer.main( root = root, 
                                                    file_categories = ['Galvanostat', 'Gas chromatography', 'Mass flow meter', 'Species data', 'P&ID'], 
                                                    add_file_callalbe = self.add_file )

        self.dataset_dropdown = widgets.Dropdown( options=[(path.parts[-1],path) for _,path in datasets.items()],
                                                  description="Choose dataset",
                                                  layout=widgets.Layout(width='auto'),
                                                  style={'description_width': 'auto'})

        self.experiment_name  = widgets.Text( description='Experiment name:',
                                              placeholder='Provide a name for the experiment',
                                              layout=widgets.Layout(width='auto'),
                                              style={'description_width': 'auto'})

        self.button_save      = widgets.Button( description='Save dataset as:  %s'%self.dataset_dropdown.value.name,
                                                layout=widgets.Layout(width="30%"),
                                                style={"button_color": 'lightblue'})

        self.button_add_exp   = widgets.Button(description='Add experiment',
                                              layout=widgets.Layout(width='auto'))


        self.experiments      = widgets.TagsInput(allow_duplicates=False)
        self.pid_file         = widgets.Text(description='P&ID file:',
                                             placeholder="Provided as xml file using DEXPI standards",
                                             layout=widgets.Layout(width='auto'),
                                             style={'description_width': 'auto'})
        self.species_file     = widgets.Text(description='Species file:',
                                             placeholder="Provided as yaml file",
                                             layout=widgets.Layout(width='auto'),
                                             style={'description_width': 'auto'})
        
        self.measurements     = widgets.TagsInput(allow_duplicates=False)

        # Functions for the buttons
        self.button_add_exp.on_click(self.add_experiment)
        self.button_save.on_click(self.save_dataset)

        # Attach the event handler to the 'value' property change of the file type widget
        self.dataset_dropdown.observe(self.dataset_input_handler, names='value')
        self.measurements.observe(self.measurement_input_handler, names='value')
        self.experiments.observe(self.experiment_input_handler,names="value")

        # Initial value for dataset
        self.dataset_input_handler(None)

        # Initialize the measurements
        self.measurement_objects  = [ ]
        self.measurements.value   = ["Measurement 1"]

        # Display the widgets

        # Create the layout
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))
        v_space_s = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='15px'))

        widgets0  = widgets.HBox([self.dataset_dropdown])
        widgets1  = widgets.VBox([v_space_s,explorer_widget,v_space_s])
        widgets2  = widgets.VBox([self.pid_file,self.species_file,v_space_s])
        widgets3  = widgets.VBox([widgets.Label(value='Manually add/remove Measurements:'), self.measurements])
        widgets4  = widgets.VBox([v_space_s,self.tab_widget,v_space_s])
        
        widgets8 = widgets.VBox([widgets.VBox([widgets.Label(value='After selecting all necessary files for an experiment, add the experiment to the chosen dataset.'),
                                                self.experiment_name, self.button_add_exp]), 
                                  widgets.VBox([widgets.Label(value='Experiments:'),self.experiments])])
        widgets9 = widgets.VBox([self.button_save ],layout=widgets.Layout(align_items = 'center'))

        # Combine the layout
        full_layout = widgets.VBox([widgets0,v_space,widgets1,widgets2,widgets3,widgets4,v_space,v_space,widgets8,v_space,widgets9])

        # Display the layout
        display(full_layout)