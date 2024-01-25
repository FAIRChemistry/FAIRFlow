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


class reading_raw_data_widget():
    
    # Function to save dataset
    def save_dataset(self,_):
        with open(self.dataset_dropdown.value, "w") as f: f.write(self.dataset.json())
        print("Dataset saved.")
    
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
    
    def add_file(self,_):
        if self.file_category.value == "EChem":
            self.Echem_files.value      = self.Echem_files.value + [str(self.file_dropdown.value)]

        elif self.file_category.value == "GC":
            self.GC_files.value         = self.GC_files.value + [str(self.file_dropdown.value)]

        elif self.file_category.value == "MFM":
            self.MFM_files.value        = self.MFM_files.value + [str(self.file_dropdown.value)]
        
        elif self.file_category.value == "Calibration":
            self.calib_files.value      = self.calib_files.value + [str(self.file_dropdown.value)]

        elif self.file_category.value == "Correction factors":
            self.correction_files.value = self.correction_files.value + [str(self.file_dropdown.value)]
        
        elif self.file_category.value == "Faraday coefficients":
            self.faraday_files.value    = self.faraday_files.value + [str(self.file_dropdown.value)]

    def add_experiment(self,_):

        ## Read in selected raw data and save it in Experiment class ##
        if not self.experiment_name.value:
            raise ValueError("Provide experiment name!\n")
        
        experiment                 = Experiment( id = self.experiment_name.value )
        
        potentiostatic_measurement = [ gstatic_parser( metadata_path = self.Echem_files.value[0] ) ]
        mfm_measurement            = [ mfm_parser( experimental_data_path = mfm_file ) for mfm_file in self.MFM_files.value ]
        gc_measurements_list       = [ gc_parser( metadata_path = self.GC_files.value[i], experimental_data_path = self.GC_files.value[i+1] ) for i in range( 0, len(self.GC_files.value), 2 ) ]

        experiment.measurements    = [ *potentiostatic_measurement, *mfm_measurement, *gc_measurements_list ]

        # Read in parameters such as calibration, correction factors and farraday coefficients and save it in Experiment class #
        experiment.calibrate_from_json( self.calib_files.value[0], degree=1 )
        experiment.read_correction_factors( self.correction_files.value[0] )
        experiment.read_faraday_coefficients( self.faraday_files.value[0] )

        # Append new experiment to current dataset #
        self.dataset.experiments.append( experiment )
        
        # Update experiment list #
        self.experiments.value = [ exp.id for exp in self.dataset.experiments ]

        # Empty files widget #
        self.Echem_files.value      = []
        self.GC_files.value         = []
        self.MFM_files.value        = []
        self.calib_files.value      = []
        self.correction_files.value = []
        self.faraday_files.value    = []
        self.experiment_name.value  = ""
        
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
        
    def dataset_input_handler(self,_):
        try:
            self.flag              = True
            with open(self.dataset_dropdown.value) as f:
                self.dataset = Dataset.from_json(f)
            self.experiments.value = [ exp.id for exp in self.dataset.experiments ]
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")
    
    def experiment_input_handler(self,change):
        # This function only updates the experiment list, if a experiment is deleted from the tags it self
        if len(change["old"]) > len(change["new"]) and not self.flag:
            dummy = [ idx for idx,val in enumerate(change["old"]) if val not in change["new"]][0]
            self.dataset.experiments.pop(dummy)
            self.experiments.value = [ exp.id for exp in self.dataset.experiments ]
        else:
            pass
        self.flag = False
    

    def choose_data(self, root: Path) -> None:
        
        self.librarian        = Librarian(root_directory=root)
        datasets              = self.librarian.search_files_in_subdirectory(root_directory=root, directory_keys=["datasets"], file_filter="json", verbose=False)
        sub_directories       = self.librarian.enumerate_subdirectories(directory=root)

        self.dataset_dropdown = widgets.Dropdown(options=[(path.parts[-1],path) for _,path in datasets.items()],
                                                description="Choose dataset",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.folder_dropdown  = widgets.Dropdown(description='Select folder:',
                                                options=[(path.parts[-1],path) for _,path in sub_directories.items()],
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.file_dropdown    = widgets.Dropdown(description='Select file:',
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})
        
        self.file_category    = widgets.Dropdown(options=['EChem', 'GC', 'MFM',"Calibration","Correction factors","Faraday coefficients"],
                                                value='EChem',
                                                description='for category:',
                                                style={'description_width': 'auto'})

        self.experiment_name  = widgets.Text(description='Experiment name:',
                                            placeholder='Enter the name of the experiment (e.g.: experiment1)',
                                            layout=widgets.Layout(width='auto'),
                                            style={'description_width': 'auto'})

        self.button_save          = widgets.Button(description='Save dataset as:  %s'%self.dataset_dropdown.value.name,
                                                   layout=widgets.Layout(width="30%"),
                                                   style={"button_color": 'lightblue'})
        
        self.button_go_for    = widgets.Button(description='Change into selected directory',
                                              layout=widgets.Layout(width='auto'))
        
        self.button_go_back   = widgets.Button(description='Change to parent diretory',
                                              layout=widgets.Layout(width='auto'))
        
        self.button_select    = widgets.Button(description='Add file to %s'%(self.file_category.value),
                                              layout=widgets.Layout(width='auto'))

        self.button_add_exp   = widgets.Button(description='Add experiment',
                                              layout=widgets.Layout(width='auto'))

        self.file_type_text   = widgets.Text(description='File type:',
                                            placeholder='Enter type here (e.g.: csv, json, ... or * for all files)',
                                            layout=widgets.Layout(width='auto'),
                                            style={'description_width': 'auto'})
        
        self.current_dir      = widgets.Text(description='Current directory:',
                                            disabled=True,
                                            value=str(root),
                                            layout=widgets.Layout(width='auto'),
                                            style={'description_width': 'auto'})

        self.Echem_files      = widgets.TagsInput(allow_duplicates=False)
        self.GC_files         = widgets.TagsInput(allow_duplicates=False)
        self.MFM_files        = widgets.TagsInput(allow_duplicates=False)
        self.calib_files      = widgets.TagsInput(allow_duplicates=False)
        self.correction_files = widgets.TagsInput(allow_duplicates=False)
        self.faraday_files    = widgets.TagsInput(allow_duplicates=False)
        self.experiments      = widgets.TagsInput(allow_duplicates=False)

        self.file_folder      = root
        self.flag             = False

        # Initial value for datamodel
        self.dataset_input_handler(None)

        # Functions for the buttons #
        self.button_go_for.on_click(self.go_to_subfolder)
        self.button_go_back.on_click(self.go_to_parentfolder)
        self.button_select.on_click(self.add_file)
        self.button_add_exp.on_click(self.add_experiment)
        self.button_save.on_click(self.save_dataset)

        # Attach the event handler to the 'value' property change of the file type widget
        self.file_type_text.observe(self.file_type_input_handler, names='value')
        self.folder_dropdown.observe(self.folder_dropdown_option_handler, names='options')
        self.file_category.observe(self.file_category_input_handler, names='value')
        self.dataset_dropdown.observe(self.dataset_input_handler, names='value')
        self.experiments.observe(self.experiment_input_handler,names="value")

        # Display the widgets

        # Create the layout
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))

        widgets0  = widgets.HBox([self.dataset_dropdown])
        widgets1  = widgets.VBox([self.current_dir,self.folder_dropdown])
        widgets2  = widgets.HBox([self.button_go_for, self.button_go_back])
        widgets3  = widgets.VBox([self.file_type_text])
        widgets4  = widgets.HBox([self.file_dropdown,self.file_category])
        widgets5  = widgets.VBox([self.button_select])
        widgets6  = widgets.VBox([widgets.Label(value='Files for EChem evaluation:'), self.Echem_files])
        widgets7  = widgets.VBox([widgets.Label(value='Files for GC evaluation:'), self.GC_files])
        widgets8  = widgets.VBox([widgets.Label(value='Files for MFM evaluation:'), self.MFM_files])
        widgets9  = widgets.HBox([widgets.VBox([widgets.Label(value='Files for calibration:'), self.calib_files]),
                                  widgets.VBox([widgets.Label(value='Files for correction factors:'), self.correction_files]),
                                  widgets.VBox([widgets.Label(value='Files for Farraday coefficients:'), self.faraday_files])])
        widgets10 = widgets.VBox([widgets.VBox([widgets.Label(value='After selecting all necessary files of one experiment, add experiment to choosen dataset'),
                                                self.experiment_name, self.button_add_exp]), 
                                  widgets.VBox([widgets.Label(value='Experiments:'),self.experiments])])
        widgets11 = widgets.VBox([self.button_save ])

        # Combine the layout
        full_layout = widgets.VBox([widgets0,v_space,widgets1,widgets2,widgets3,widgets4,v_space,widgets5,widgets6,widgets7,widgets8,widgets9,
                                    v_space,widgets10,v_space,widgets11])

        # Display the layout
        display(full_layout)