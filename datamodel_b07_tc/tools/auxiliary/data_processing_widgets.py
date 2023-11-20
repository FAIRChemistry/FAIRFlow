import os
import ipywidgets as widgets
import pandas as pd
from pathlib import Path
from IPython.display import display, clear_output

# Import modified sdRDM objects #
from sdRDM import DataModel

# Import general tools and objects of this datamodel #

# Objects #
from datamodel_b07_tc.core.experiment import Experiment
from datamodel_b07_tc.core.measurement import Measurement
#from datamodel_b07_tc.core.plantsetup import PlantSetup

# Tools #
from datamodel_b07_tc.tools.auxiliary.librarian import Librarian
from datamodel_b07_tc.tools.calculus.calibrator import Calibrator
from datamodel_b07_tc.tools.calculus.faraday_efficiency_calculator import FaradayEfficiencyCalculator
from datamodel_b07_tc.tools.auxiliary.peak_assigner import PeakAssigner
from datamodel_b07_tc.tools.readers.gcparser import gc_parser
from datamodel_b07_tc.tools.readers.gstaticparser import gstatic_parser
from datamodel_b07_tc.tools.readers.mfmparser import mfm_parser
#from datamodel_b07_tc.tools.readers.DEXPI2sdRDM import DEXPI2sdRDM

class initialize_dataset:

    def init_datamodel(self,_):
        # Initialize the dataset #
        if Path(self.datamodels_dropdown.value).suffix == '.git':
            lib = DataModel.from_git( url=self.datamodels_dropdown.value )
        else:
            lib = DataModel.from_markdown( self.datamodels_dropdown.value )
            
        self.dataset = lib.Dataset()

    def save_dataset(self,_):

        print("Saving dataset!")
        
        # Add authors to the dataset #
        if self.authors.value and self.affiliations.value:
            authors      = [ s.strip() for s in self.authors.value.split(",") ]
            affiliations = [ s.strip() for s in self.affiliations.value.split(",") ]

        for aut,aff in zip(authors,affiliations):
            self.dataset.general_information.add_to_authors( name=aut, affiliation=aff )

        # Write dataset #
        os.makedirs( self.root / "datasets", exist_ok=True )
        with open( str(self.root) + "/datasets/%s.json"%self.dataset_text.value, "w") as f: f.write(self.dataset.json())

    def change_dataset(self,_):
        self.button_save.description = 'Save dataset as:  %s.json'%self.dataset_text.value
    
    def add_title(self,_):
        self.dataset.general_information.title       = self.title.value

    def add_description(self,_):
        self.dataset.general_information.description = self.description.value        

    def write_dataset(self,root: Path, git_path: str) -> None:
        
        self.root                = root
        self.librarian           = Librarian(root_directory=root)
        self.datamodels          = self.librarian.search_files_in_subdirectory(root_directory=root, directory_keys=["specifications"], file_filter="md", verbose=False)
                         
        self.datamodels_dropdown = widgets.Dropdown(options=[(path.parts[-1],path) for _,path in self.datamodels.items()]+[("git",git_path)],
                                                    description="Choose datamodel",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        self.title               = widgets.Text(description="Title of the project:",
                                                placeholder="Type the title of the project",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.description         = widgets.Textarea(description="Description of the project:",
                                                placeholder="Descripte the project",
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

        self.dataset_text        = widgets.Text(description="Dataset:",
                                                placeholder="Name the dataset for this project (will be saved as json file)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.button_save         = widgets.Button(description='Save dataset as:  %s.json'%self.dataset_text.value,
                                                  layout=widgets.Layout(width="30%"),
                                                  style={"button_color": 'lightblue'})
        
        # Initialize the dataset #
        if Path(self.datamodels_dropdown.value).suffix == '.git':
            lib = DataModel.from_git( url=self.datamodels_dropdown.value )
        else:
            lib = DataModel.from_markdown( self.datamodels_dropdown.value )

        self.dataset = lib.Dataset()
        
        # Handle on observing
        self.datamodels_dropdown.observe(self.init_datamodel,names="value")
        self.title.observe(self.add_title,names="value")
        self.description.observe(self.add_description,names="value")
        self.dataset_text.observe(self.change_dataset,names="value")
        
        # Handle button
        self.button_save.on_click(self.save_dataset)

        # Widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))

        widgets0  = self.datamodels_dropdown
        widgets1  = widgets.VBox([self.title, self.description, self.authors, self.affiliations])
        widgets2  = widgets.VBox([self.dataset_text, v_space, self.button_save])

        # Combine the layout
        full_layout = widgets.VBox([widgets0, widgets1, widgets2])

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

        experiment                   = Experiment()
        gc_experimental_data_df_list = []
        gc_metadata_df_list          = []
        gc_measurements_list         = []

        potentiostatic_metadata_df, potentiostatic_measurement = Measurement.from_parser( parser=gstatic_parser, metadata_path=self.Echem_files.value[0] )
        mfm_experimental_data_df, mfm_measurement              = Measurement.from_parser( parser=mfm_parser, experimental_data_path=self.MFM_files.value[0] )
        #experiment.plant_setup                                = PlantSetup.from_parser( parser=DEXPI2sdRDM, path=self.plant_setup_files[0] )

        for i in range(0,len(self.GC_files.value),2):
            gc_metadata_df, gc_experimental_data_df, gc_measurement = Measurement.from_parser(parser=gc_parser,metadata_path=self.GC_files.value[i],experimental_data_path=self.GC_files.value[i+1])
            gc_experimental_data_df_list.append(gc_experimental_data_df)
            gc_metadata_df_list.append(gc_metadata_df)
            gc_measurements_list.append(gc_measurement)

        experiment.measurements      = [potentiostatic_measurement, mfm_measurement, *gc_measurements_list]

        # Read in parameters such as calibration, correction factors and farraday coefficients and save it in Experiment class #
        experiment.species_data      = Calibrator.from_json_file(path_to_json_file=self.calib_files.value[0]).calibrate()
        experiment.read_correction_factors(self.correction_files.value[0])
        experiment.read_faraday_coefficients(self.faraday_files.value[0])

        # Append new experiment to current dataset #
        self.dataset.experiments.append(experiment)

        # Update experiment list #
        self.experiments.value = [ exp.id for exp in self.dataset.experiments if hasattr(exp,"id") ]

        # Empty files widget #
        self.Echem_files.value      = []
        self.GC_files.value         = []
        self.MFM_files.value        = []
        self.calib_files.value      = []
        self.correction_files.value = []
        self.faraday_files.value    = []

    def folder_dropdown_option_handler(self,_):
        # If no subdirectories exist, then the parent folder is simply the first parent, otherwise it is the 2nd parent
        # (because the current dropdown value is already )
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
            self.experiments.value = [ exp.id for exp in self.dataset.experiments if hasattr(exp,"id")]
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")
    
    def experiment_input_handler(self,change):
        # This function only updates the experiment list, if a experiment is deleted from the tags it self
        if len(change["old"]) > len(change["new"]) and not self.flag:
            dummy = [ idx for idx,val in enumerate(change["old"]) if val not in change["new"]][0]
            self.dataset.experiments.pop(dummy)
            self.experiments.value = [exp.id for exp in self.dataset.experiments]
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
            self.experiments.value = [exp.id for exp in self.dataset.experiments]
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")
        
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

        # Clear existing widgets
        clear_output(wait=True)

        # Display the layout for experiment and species
        display(self.full_layout)

        # Also display the peak assignment again
        self.gc_measurements = [gc for gc in self.dataset.experiments[self.experiments_dropdown.value].measurements if gc.measurement_type == 'GC measurement']
        self.peak_assignment = PeakAssigner.from_gc_measurement(self.gc_measurements, self.species_tags.value)
        self.peak_assignment.assign_peaks()
    
    def species_tags_input_handler(self,_):
        # If species are changed redo the ouput of widget one
        self.peak_assignment.modify_dropdown_options( self.species_tags.value )

    def do_postprocessing(self,_):

        print("\nStarting the postprocessing\n")

        fe_calculator = FaradayEfficiencyCalculator(experiment=self.dataset.experiments[self.experiments_dropdown.value],
                                                    electrode_surface_area=self.elec_surf_area.value,
                                                    mean_radius=self.mean_radius.value)

        faraday_efficiencies = []

        for i, (gc_measurement, assigned_peak_areas_dict) in enumerate(zip(self.gc_measurements, self.peak_assignment._assignment_dicts)):
            tmp = fe_calculator.calculate_faraday_efficiencies( gc_measurement=gc_measurement, assigned_peak_areas_dict=assigned_peak_areas_dict )
            faraday_efficiencies.append( tmp )
            print("Faraday effiencies of GC measurement n°%d"%i)
            print(tmp,"\n")

        mean_faraday_efficiency = pd.concat(faraday_efficiencies).groupby(level=0).mean()
        
        print("\nMean Faraday efficency over all GC measurements")
        print(mean_faraday_efficiency,"\n")

        for species_data in self.dataset.experiments[self.experiments_dropdown.value].species_data:
            if species_data.species in mean_faraday_efficiency.index:
                faraday_efficiency              = mean_faraday_efficiency.loc[species_data.species].values
                species_data.faraday_efficiency = self.lib.Data(quantity= 'Faraday efficiency', values = faraday_efficiency.tolist(), unit = '%')


    def choose_experiment(self,datamodel,dataset_path) -> None:
        
        # Common variables
        self.dataset_path      = dataset_path
        self.dataset, self.lib = datamodel

        self.experiments_dropdown = widgets.Dropdown(options=[(str(exp.id),idx) for idx,exp in enumerate( self.dataset.experiments) ],
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

        self.elec_surf_area   = widgets.FloatText(value=1.0,
                                                  description='Electrode surface area [cm^2]:',
                                                  style={'description_width': 'auto'})

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
        widgets2  = widgets.VBox([self.explanation_label,v_space,widgets.HBox([self.mean_radius,self.elec_surf_area])])
        widgets3  = self.display_button
        widgets4  = self.button_save


        # Combine the layout
        self.full_layout = widgets.VBox([widgets0,widgets1])

        # Display the layout
        display(self.full_layout)

        # Execute the peak assignment for the initial experiment value
        self.choose_experiment_input_handler(None)

        # Do postprocessing and save dataset
        layout = widgets.VBox([widgets.VBox([widgets2,v_space]),
                               widgets.VBox([widgets3,v_space,widgets4],
                               layout=widgets.Layout(align_items = 'center'))])
        
        display(layout)

