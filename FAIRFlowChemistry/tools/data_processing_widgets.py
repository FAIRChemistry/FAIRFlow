import os
import ipywidgets as widgets
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List
from IPython.display import display, clear_output

# Import modified sdRDM objects #
from sdRDM import DataModel

# Import general tools and objects of this datamodel #

# Objects #
from FAIRFlowChemistry.core import Experiment
from FAIRFlowChemistry.core import MeasurementType
from FAIRFlowChemistry.core import Quantity
from FAIRFlowChemistry.core import Contact
from FAIRFlowChemistry.core import RelatedPublication
from pyDaRUS import Citation
from pyDaRUS import Dataset as DaRUS_dataset
from pyDaRUS.metadatablocks.citation import SubjectEnum, Language

# Tools #
from .auxiliary import Librarian, PeakAssigner
from .reader import gc_parser, gstatic_parser, mfm_parser
from .calculator import FaradayEfficiencyCalculator

class initialize_dataset:

    def init_datamodel(self,_):
        # Initialize the dataset #
        if Path(self.datamodels_dropdown.value).suffix == '.git':
            lib = DataModel.from_git( url=self.datamodels_dropdown.value, tag=self.git_branch )
        else:
            lib = DataModel.from_markdown( self.datamodels_dropdown.value )
            
        self.dataset = lib.Dataset()

    def save_dataset(self,_):

        print("Saving dataset!")
        
        # Add title
        self.dataset.general_information.title       = self.title.value
        
        # Add description
        self.dataset.general_information.description = self.description.value 

        # Add project group
        self.dataset.general_information.project     = self.project.value

        # Add authors to the dataset 
        for aut,aff,ident in zip( self.authors.value.split(","), self.affiliations.value.split(","), self.identifier.value.split(",") ):
            self.dataset.general_information.add_to_authors( name = aut.strip(), 
                                                             affiliation = aff.strip(), 
                                                             identifier_scheme = self.identifier_scheme.value,
                                                             identifier = ident.strip() )

        # Add contact (search contact in provided authors)
        affili = [ aff for aut,aff in zip(self.authors.value.split(","), self.affiliations.value.split(",")) if aut.strip() == self.contact_text.value.split(",")[0].strip() ]
        affili = affili[0] if bool(affili) else None

        self.dataset.general_information.contact = Contact( name = self.contact_text.value.split(",")[0].strip(), 
                                                            email = self.contact_text.value.split(",")[1].strip(), 
                                                            affiliation = affili )

        # Add subject
        self.dataset.general_information.subject = list( self.subject_selection.value )

        # Add related publication
        self.dataset.general_information.related_publication  = RelatedPublication( citation = self.related_publication.value.split(",")[0].strip(),
                                                                                    url      = self.related_publication.value.split(",")[1].strip() )

        # Add topic classifications
        for i in range(0, len(self.topic_classification.value.split(",")), 2):
            self.dataset.general_information.add_to_topic_classification( term           = self.topic_classification.value.split(",")[i].strip() , 
                                                                          vocabulary_url = self.topic_classification.value.split(",")[i + 1].strip() )

        # Add keywords
        for i in range(0, len(self.keywords.value.split(",")), 2):
            self.dataset.general_information.add_to_keywords( term           = self.keywords.value.split(",")[i].strip() , 
                                                              vocabulary_url = self.keywords.value.split(",")[i + 1].strip() )
            
        # Write dataset #
        os.makedirs( self.root / "datasets", exist_ok=True )
        with open( str(self.root) + "/datasets/%s.json"%self.dataset_text.value, "w") as f: f.write(self.dataset.json())

    def change_dataset(self,_):
        self.button_save.description = 'Save dataset as:  %s.json'%self.dataset_text.value
               
    def write_dataset(self,root: Path, git_path: str, git_branch: str) -> None:
        
        self.git_branch          = git_branch    
        self.root                = root
        self.librarian           = Librarian(root_directory=root)
        self.datamodels          = self.librarian.search_files_in_subdirectory(root_directory=root, directory_keys=["specifications"], file_filter="md", verbose=False)
                         
        self.datamodels_dropdown = widgets.Dropdown(options= [("git",git_path)] + [(path.parts[-1],path) for _,path in self.datamodels.items()],
                                                    description="Choose datamodel",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        self.title               = widgets.Text(description="Title of the project:",
                                                placeholder="Type the title of the project",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.description         = widgets.Text(description="Description of the project:",
                                                placeholder="Describe the project",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.project             = widgets.Text(description="Project:",
                                                placeholder="Name of the project group (e.g.: Project B07)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.authors             = widgets.Text(description="Author list:",
                                                placeholder="Name the authors of the project (e.g.: author1, author2, ...)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.affiliations        = widgets.Text(description="Affiliations:",
                                                placeholder="Name the affiliation fo each author (e.g.: University of Stuttgart, TUM, ...)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})


        self.identifier_scheme   = widgets.Dropdown(options= ["ORCID"],
                                                    description="Choose unique identifier scheme:",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        self.identifier          = widgets.Text(description="Unique identifier:",
                                                placeholder="Provide identifier according to choosen identifier scheme (e.g. for ORCID: xxxx-xxxx-xxxx-xxxx)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.contact_text      = widgets.Text(description="Contact:",
                                                placeholder="Name the contact of the project (e.g.: Max Mustermann, max.mustermann@universityofstuttgart.de)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.subject_selection   = widgets.SelectMultiple( options=[ subject.value for subject in SubjectEnum ],
                                                          description="Choose subjects (press and hold 'strg' to select several):",
                                                          value=["Chemistry"],
                                                          layout=widgets.Layout(width='auto'),
                                                           style={'description_width': 'auto'} )
        
        self.related_publication  = widgets.Text (description="Related publication:",
                                                    placeholder="The full bibliographic citation for this related publication and link to the publication web page, separated by a comma (e.g.: M. Mustermann Publication: Test. J. Chem. Phys. xxx, xxx (xxx), https://doi.org/xxx )",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        

        self.topic_classification = widgets.Text (description="Topic classification:",
                                                    placeholder="The classification and the url, seperated by a comma (e.g.: homogeneous catalysis (LCSH), https://xxx, polyethers (LCSH), https://xxx, ... )",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})

        self.keywords             = widgets.Text (description="Keywords:",
                                                    placeholder="The keywords and the url, seperated by a comma (e.g.: polymer chemistry (Loterre Chemistry Vocabulary), https://xxx )",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})


        self.dataset_text        = widgets.Text(description="Dataset:",
                                                placeholder="Name the dataset for this project (will be saved as json file)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.button_save         = widgets.Button(description='Save dataset as:  %s.json'%self.dataset_text.value,
                                                  layout=widgets.Layout(width="30%"),
                                                  style={"button_color": 'lightblue'})
        
        # Initialize the dataset #
        if Path(self.datamodels_dropdown.value).suffix == '.git':
            lib = DataModel.from_git( url=self.datamodels_dropdown.value, tag=self.git_branch )
        else:
            lib = DataModel.from_markdown( self.datamodels_dropdown.value )

        self.dataset = lib.Dataset()
        
        # Handle on observing
        self.datamodels_dropdown.observe(self.init_datamodel,names="value")
        self.dataset_text.observe(self.change_dataset,names="value")
        
        # Handle button
        self.button_save.on_click(self.save_dataset)

        # Widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))
        h_space   = widgets.HBox([widgets.Label(value='')], layout=widgets.Layout(width='30px'))

        widgets0  = widgets.HBox([self.datamodels_dropdown, h_space, self.identifier_scheme])
        widgets1  = widgets.VBox([v_space, self.title, self.description, self.project,v_space])
        widgets2  = widgets.VBox([self.authors, self.affiliations, self.identifier, self.contact_text, v_space])
        widgets3  = widgets.VBox([self.subject_selection, self.related_publication, self.topic_classification, self.keywords, v_space])
        widgets4  = widgets.VBox([self.dataset_text, v_space])
        widgets5  = widgets.VBox([self.button_save], layout=widgets.Layout(align_items = 'center') )

        # Combine the layout
        full_layout = widgets.VBox([widgets0, widgets1, widgets2, widgets3, widgets4, widgets5])

        # Display the layout
        display(full_layout)

        return


class reading_raw_data_widget():
    
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

        experiment                 = Experiment()
        
        potentiostatic_measurement = gstatic_parser( metadata_path = self.Echem_files.value[0] )
        mfm_measurement            = mfm_parser( experimental_data_path = self.MFM_files.value[0] )
        gc_measurements_list       = [ gc_parser( metadata_path = self.GC_files.value[i], experimental_data_path = self.GC_files.value[i+1] ) for i in range( 0, len(self.GC_files.value), 2 ) ]

        experiment.measurements    = [ potentiostatic_measurement, mfm_measurement, *gc_measurements_list ]

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
            self.datamodel         = DataModel.parse( self.dataset_dropdown.value )
            self.dataset, self.lib = self.datamodel
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
    

    def choose_data(self,root: Path) -> None:
        
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

        self.button_go_for    = widgets.Button(description='Move into directory',
                                              layout=widgets.Layout(width='auto'))
        
        self.button_go_back   = widgets.Button(description='Move one diretory back',
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
        try:
            self.datamodel         = DataModel.parse( self.dataset_dropdown.value )
            self.dataset, self.lib = self.datamodel
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")
        
        # List of experiments
        self.experiments.value = [ exp.id for exp in self.dataset.experiments ]

        # Functions for the buttons #
        self.button_go_for.on_click(self.go_to_subfolder)
        self.button_go_back.on_click(self.go_to_parentfolder)
        self.button_select.on_click(self.add_file)
        self.button_add_exp.on_click(self.add_experiment)

        # Attach the event handler to the 'value' property change of the file type widget
        self.file_type_text.observe(self.file_type_input_handler, names='value')
        self.folder_dropdown.observe(self.folder_dropdown_option_handler, names='options')
        self.file_category.observe(self.file_category_input_handler, names='value')
        self.dataset_dropdown.observe(self.dataset_input_handler, names='value')
        self.experiments.observe(self.experiment_input_handler,names="value")

        # Display the widgets

        # Create the layout
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
        widgets10 = widgets.VBox([widgets.VBox([widgets.Label(value='After selecting all necessary files of one experiment, add experiment to choosen dataset'),self.button_add_exp]), 
                                  widgets.VBox([widgets.Label(value='Experiments:'),self.experiments])])
        
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))

        # Combine the layout
        full_layout = widgets.VBox([widgets0,v_space,widgets1,widgets2,widgets3,widgets4,v_space,widgets5,widgets6,widgets7,widgets8,widgets9,
                                    v_space,widgets10])

        # Display the layout
        display(full_layout)


class analyzing_raw_data_widget:

    def save_dataset(self,_):
        with open(self.dataset_path, "w") as f: f.write(self.dataset.json())
        print("Dataset saved.")

    def choose_experiment_input_handler(self,_):
        """
        This function provides the peaks of the GC measurement inheritend in the choosen experiment
        """

        # Clear every widget output and make new ones
        clear_output(wait=True)

        # Display the experiment widget
        display(self.full_layout)
        
        # Also display the peak assignment again (input is the choosen experiment and the current species)
        self.peak_assignment = PeakAssigner( experiment             = self.dataset.experiments[self.experiments_dropdown.value], 
                                             species                = self.species_tags.value,
                                             typical_retention_time = self.typical_retention_time )
        self.peak_assignment.assign_peaks()

        # Display the postprocessing
        display(self.full_layout2)
    
    def species_tags_input_handler(self,_):
        # If species are changed redo the ouput of widget one
        self.peak_assignment.modify_dropdown_options( self.species_tags.value )

    def do_postprocessing(self,_):

        # Clear existing output (in case several post processing are done, remove the print output )
        with self.postprocessing_output:
            clear_output(wait=True)
            print("\nStarting the postprocessing\n")

            fe_calculator = FaradayEfficiencyCalculator(experiment  = self.dataset.experiments[self.experiments_dropdown.value],
                                                        mean_radius = self.mean_radius.value)

            faraday_efficiencies = []

            # Extract the GC measurements from the choosen experiment
            gc_measurements      = self.dataset.experiments[self.experiments_dropdown.value].get("measurements", "measurement_type", MeasurementType.GC.value)[0]

            for i, gc_measurement in enumerate( gc_measurements ):
                tmp = fe_calculator.calculate_faraday_efficiencies( gc_measurement = gc_measurement )
                faraday_efficiencies.append( tmp )
                print("Faraday effiencies of GC measurement n°%d"%i)
                print(tmp,"\n")

            mean_faraday_efficiency = pd.concat(faraday_efficiencies).groupby(level=0).mean()
            
            print("\nMean Faraday efficency over all GC measurements")
            print(mean_faraday_efficiency,"\n")

            for species_data in self.dataset.experiments[self.experiments_dropdown.value].species_data:
                if species_data.species in mean_faraday_efficiency.index:
                    faraday_efficiency              = mean_faraday_efficiency.loc[species_data.species].values
                    species_data.faraday_efficiency = self.lib.Data(quantity= Quantity.FARADAYEFFIECENCY.value, values = faraday_efficiency.tolist(), unit = '%')


    def choose_experiment(self,datamodel,dataset_path,typical_retention_time={}) -> None:
        
        # Common variables
        self.typical_retention_time = typical_retention_time 
        self.dataset_path           = dataset_path
        self.dataset, self.lib      = datamodel

        if not bool( self.dataset.experiments  ): raise ValueError("Dataset contains no experiments!\n")

        self.experiments_dropdown = widgets.Dropdown(options=[(str(exp.id),idx) for idx,exp in enumerate( self.dataset.experiments ) ],
                                                    description="Choose experiment:",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})

        self.species_tags         = widgets.TagsInput(allow_duplicates=False,
                                                      value=['Hydrogen', 'Carbon monoxide', 'Carbon dioxide', 'Methane', 'Ethene', 'Ethane'])

        self.mean_radius          = widgets.IntSlider(value=10,  # Initial value
                                                      min=0,    # Minimum value
                                                      max=20,   # Maximum value
                                                      step=1,   # Step size
                                                      description='Mean radius:')

        self.display_button       = widgets.Button(description="Start posprocessing", 
                                                   layout=widgets.Layout(width="30%"),
                                                   style={"button_color": 'green'})
        
        self.button_save          = widgets.Button(description='Save dataset as:  %s'%dataset_path.name,
                                                   layout=widgets.Layout(width="30%"),
                                                   style={"button_color": 'lightblue'})
        
        self.explanation_label    = widgets.HTML(value='The mass flow at the time of the GC measurement is determined by matching the time of the gc measurement\
                                                        with the corresponding times of the mass flow measurements. Errors in the mass flows due to strong fluctuations\
                                                        are minimized by calculating the mean by averaging over a certain number (=radius) of measuring points before and\
                                                        after the time of the GC measurement. The radius has to be specified in accordance with the strength of fluctuations.')

        # Output areas
        self.postprocessing_output = widgets.Output()

        # Handle switch of experiment
        self.experiments_dropdown.observe(self.choose_experiment_input_handler,names="value")
        self.species_tags.observe(self.species_tags_input_handler,names="value")

        # Handle buttons
        self.display_button.on_click(self.do_postprocessing)
        self.button_save.on_click(self.save_dataset)

        # Widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))

        widgets0  = widgets.HBox([self.experiments_dropdown])
        widgets1  = widgets.VBox([widgets.Label(value='Species in GC analysis:'), self.species_tags])
        widgets2  = widgets.VBox([self.explanation_label, v_space, self.mean_radius, v_space])
        widgets3  = widgets.VBox([self.display_button, v_space, self.postprocessing_output], layout=widgets.Layout(align_items = 'center'))
        widgets4  = widgets.VBox([v_space,self.button_save], layout=widgets.Layout(align_items = 'center') )


        # Combine the experiment layout
        self.full_layout = widgets.VBox([widgets0,widgets1])

        # Do postprocessing and save dataset
        self.full_layout2 = widgets.VBox([widgets2, widgets3, widgets4] )

        # Execute the peak assignment for the initial experiment value and thus visualize the widgets
        self.choose_experiment_input_handler(None)




class DaRUS_upload:

    def action_handler(self,_):
        with self.action_output:
            clear_output(wait=True)

            if self.action_dropdown.value == "Create new one":
                self.create_new()
            elif self.action_dropdown.value == "Edit existing one":
                self.edit_existing()
            else:
                pass
        
    def add_file_dir(self,_):
        # Clear previous output and print the new message in the button's output area
        with self.button_output:
            clear_output(wait=True)
            if os.path.isfile(self.file_directoy_input.value) or os.path.isdir(self.file_directoy_input.value):
                self.file_directoy.value = self.file_directoy.value + [ self.file_directoy_input.value ]
                print(f"Added file / directory: {self.file_directoy_input.value }")
            else:
                print(f"The specified entry is neither a file nor a directory:\n {self.file_directoy_input.value}")
            

    def upload_to_DaRUS(self,_):

        #### Initialize and write DaRUS dataset ####

        self.DaRUS_data    = DaRUS_dataset()

        ## Get citation metadata from the general information object of the provided dataset ##

        citation      = Citation()

        # Add project group
        citation.add_project( name = self.dataset.general_information.project, level=1 )
        
        # Add title
        citation.title = self.dataset.general_information.title
        
        # Add description
        citation.add_description( text = self.dataset.general_information.description )

        # Add authors
        for author in self.dataset.general_information.authors: 
            citation.add_author( **{k:author.__dict__[k] for k in author.__dict__.keys() if k!="id"} ) 

        # Add point of contact
        citation.add_contact( **{k:self.dataset.general_information.contact.__dict__[k] for k in self.dataset.general_information.contact.__dict__.keys() if k!="id"} ) 

        # Add subjects
        citation.subject      = self.dataset.general_information.subject

        # Add depositor
        citation.depositor    = self.depositor_text.value.strip()
        citation.deposit_date = datetime.now().date().strftime("%Y-%m-%d")
        
        # Add generall SFB information
        citation.add_grant_information( grant_agency="DFG", grant_number="358283783 - SFB 1333")

        # Add language
        citation.language     = [ Language.english ]

        # Add related publication
        citation.add_related_publication( **{k:self.dataset.general_information.related_publication.__dict__[k] for k in self.dataset.general_information.related_publication.__dict__.keys() if k!="id"})
        
        # Add topic classification
        for classification in self.dataset.general_information.topic_classification: 
            citation.add_topic_classification( **{k:classification.__dict__[k] for k in classification.__dict__.keys() if k!="id"} )

        # Add keywords
        for keyword in self.dataset.general_information.keywords:
            citation.add_keyword( **{k:keyword.__dict__[k] for k in keyword.__dict__.keys() if k!="id"} ) 

        # Add the citation metadata to the DaRUS dataset
        self.DaRUS_data.add_metadatablock(citation)


        ## Add files and directories ##

        for entry in self.file_directoy.value:
            if os.path.isfile(entry):
                self.DaRUS_data.add_file( dv_path = entry, local_path = entry )
            elif os.path.isdir(entry):
               self.DaRUS_data.add_directory( dirpath = entry )
            else:
                print(f"The specified entry is neither a file nor a directory:\n {entry}")

        ## Upload ##

        self.DaRUS_data.upload( dataverse_name = self.dataverse_dropdown.value,
                           DATAVERSE_URL  = "https://darus.uni-stuttgart.de",
                           API_TOKEN      = self.api_token_text.value)


    def update_to_DaRUS(self,_):

        ## Add files and directories ##

        for entry in self.file_directoy.value:
            if os.path.isfile(entry):
                self.DaRUS_data.add_file( dv_path = entry, local_path = entry )
            elif os.path.isdir(entry):
               self.DaRUS_data.add_directory( dirpath = entry )
            else:
                print(f"The specified entry is neither a file nor a directory:\n {entry}")

        ## Add editor information and upload

        self.DaRUS_data.update( contact_name  = self.contact_text.value.split(",")[0].strip(), 
                                contact_mail  = self.contact_text.value.split(",")[1].strip(),
                                dataverse_url = 'https://darus.uni-stuttgart.de',
                                api_token     = self.api_token_text.value )

    def download_from_DaRUS(self,_):
        #self.DaRUS_data = DaRUS_dataset.from_dataverse_doi( doi           = self.doi_text.value, 
        #                                                    dataverse_url = 'https://darus.uni-stuttgart.de',
        #                                                    api_token     = self.api_token_text.value )
        
        self.DaRUS_data = DaRUS_dataset()

        # Initialize  
        self.file_directoy.value = self.DaRUS_data.files

        # Handle button
        self.button_upload.on_click(self.update_to_DaRUS)

        with self.download_output:
            clear_output(wait=True)
            v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))
            
            widgets0  = self.file_directoy_input
            widgets1  = widgets.VBox([self.button_add_file_dir, self.button_output], layout=widgets.Layout(align_items = 'center'))
            widgets2  = widgets.VBox([v_space,widgets.Label(value='Files / directories in DaRUS dataset:'), self.file_directoy])
            widgets3  = widgets.VBox([self.button_upload],layout=widgets.Layout(align_items = 'center'))

            # Combine the layout
            full_layout = widgets.VBox([widgets0, widgets1, widgets2, widgets3])

            # Display the layout
            display(full_layout)

    def create_new(self):
        
        self.dataverse_dropdown     = widgets.Dropdown(options= self.dataverse_list,
                                                    description="Choose dataverse:",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        self.depositor_text         = widgets.Text (description="Depositor:",
                                                    placeholder="Name of the person uploading this dataset (e.g.: Max Mustermann)",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        # Initialize  
        self.file_directoy.value = [ str(self.dataset_path) ]

        # Handle button
        self.button_upload.on_click(self.upload_to_DaRUS)

        # Widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))

        widgets0  = widgets.VBox([self.dataverse_dropdown, v_space])
        widgets1  = widgets.VBox([self.depositor_text,v_space])
        widgets2  = self.file_directoy_input
        widgets3  = widgets.VBox([self.button_add_file_dir, self.button_output], layout=widgets.Layout(align_items = 'center'))
        widgets4  = widgets.VBox([v_space,widgets.Label(value='Files / directories in DaRUS dataset:'), self.file_directoy])
        widgets5  = widgets.VBox([self.button_upload],layout=widgets.Layout(align_items = 'center'))

        # Combine the layout
        full_layout = widgets.VBox([widgets0, widgets1, widgets2, widgets3, widgets4, widgets5])

        # Display the layout
        display(full_layout)


    def edit_existing(self):

        self.contact_text           = widgets.Text( description="Contact of editing person:",
                                                    placeholder="Name of the person editing this dataverse (e.g.: Max Mustermann, maxmustermann@web.de)",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'} )
        
        self.doi_text               = widgets.Text( description="DOI/PID for dataverse:",
                                                    placeholder="Doi of exisitng dataverse (e.g.: 'doi:xx.xxxxx/darus-xxxx)",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'} )

        self.button_download        = widgets.Button(description='Download dataset from DaRUS',
                                                     layout=widgets.Layout(width="30%"),
                                                     style={"button_color": 'lightblue'})

        # Handle button
        self.button_download.on_click(self.download_from_DaRUS)

        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))
        widgets0  = widgets.VBox([self.contact_text,self.doi_text,v_space])
        widgets1  = widgets.VBox([self.button_download],layout=widgets.Layout(align_items = 'center'))

        # Combine the layout
        full_layout = widgets.VBox([widgets0, widgets1,v_space,self.download_output])

        # Display the layout
        display(full_layout)

    def upload(self,datamodel: DataModel, dataset_path: Path | str, dataverse_list: List):
        
        # Common variables
        self.dataset, self.lib      = datamodel
        self.dataverse_list         = dataverse_list
        self.dataset_path           = dataset_path

        # Common widgets
        self.file_directoy_input    = widgets.Text (description="Path to file / directory (can be absolut or relative):",
                                                    placeholder="Addiotional directories or paths that should be uploaded, only one entry allowed (e.g.: ./data/Rohdaten, ./data/calibration/calibration.json, ... )",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        self.file_directoy          = widgets.TagsInput(allow_duplicates=False)
        
        self.button_add_file_dir    = widgets.Button(description='Add file / directory to DaRUS dataset',
                                                     layout=widgets.Layout(width="20%"))
        
        self.button_upload          = widgets.Button(description='Upload dataset to DaRUS',
                                                     layout=widgets.Layout(width="30%"),
                                                     style={"button_color": 'lightblue'})
        
        self.button_output          = widgets.Output()  
        self.download_output        = widgets.Output()

        # Handle buttons
        self.button_add_file_dir.on_click(self.add_file_dir)

        self.action_output         = widgets.Output()

        ## Main widgets ##

        self.action_dropdown        = widgets.Dropdown(options= ["","Create new one", "Edit existing one"],
                                                       description="Choose whether you want to create a new data record or edit an existing one:",
                                                       layout=widgets.Layout(width='auto'),
                                                       style={'description_width': 'auto'})
        
        self.api_token_text         = widgets.Text( description="API token:",
                                                    placeholder="Provide personal API token for DaRUS (e.g.: xxx-xxx-xxx-xxx-xxx)",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        # Handle effects
        self.action_dropdown.observe(self.action_handler)

        # Display general widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))
        display( widgets.VBox([self.action_dropdown, self.api_token_text, v_space, self.action_output]) )