#!~/miniconda3/bin/python

import os
import pandas as pd
import ipywidgets as widgets
from typing import List
from pathlib import Path
from datetime import datetime
from easyDataverse import Dataverse
from IPython.display import display, clear_output

# Import general tools and objects of this datamodel #
from FAIRFlowChemistry.core import Dataset

# Other #
# Mute the "libuv only supports millisecond timer resolution" warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="gevent.hub")

class DaRUS_upload:

    def add_file_dir(self,_):
        # Clear previous output and print the new message in the button's output area
        with self.button_output:
            clear_output(wait=True)
            if os.path.isfile(self.file_directoy_input.value) or os.path.isdir(self.file_directoy_input.value):
                self.file_directoy.value = self.file_directoy.value + [ self.file_directoy_input.value ]
                print(f"Added file / directory: {self.file_directoy_input.value }")
            else:
                print(f"The specified entry is neither a file nor a directory:\n {self.file_directoy_input.value}")
                
    def action_handler(self,_):
        with self.action_output:
            clear_output(wait=True)

            if len(self.api_token_text.value.split("-") )== 5:
                self.dataverse = Dataverse( server_url = 'https://darus.uni-stuttgart.de',
                                            api_token  = self.api_token_text.value )
            else:
                raise KeyError("Invalid API token presented\n")
            
            if self.action_dropdown.value == "Create new one":
                self.create_new()

            elif self.action_dropdown.value == "Edit existing one":
                self.edit_existing()
                
            else:
                # Display empty space to overwrite existing widget output
                display( widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px')) )

    def fill_citation(self):
        """
        Function that uses the provided dataset and map its general information to the DaRUS dataset
        """
        # Add project group
        self.DaRUS_data.citation.project = []
        self.DaRUS_data.citation.add_project( name = self.dataset.general_information.project, level=1 )
        
        # Add title
        self.DaRUS_data.citation.title = self.dataset.general_information.title
        
        # Add description
        self.DaRUS_data.citation.ds_description = []
        self.DaRUS_data.citation.add_ds_description( value = self.dataset.general_information.description )

        # Add authors
        self.DaRUS_data.citation.author = []
        for author in self.dataset.general_information.authors: 
            self.DaRUS_data.citation.add_author( **{k:author.__dict__[k] for k in author.__dict__.keys() if k!="id"} ) 

        # Add point of contact
        self.DaRUS_data.citation.dataset_contact = []
        self.DaRUS_data.citation.add_dataset_contact( **{k:self.dataset.general_information.contact.__dict__[k] for k in self.dataset.general_information.contact.__dict__.keys() if k!="id"} ) 

        # Add subjects
        self.DaRUS_data.citation.subject      = self.dataset.general_information.subject

        # Add depositor
        self.DaRUS_data.citation.depositor    = self.depositor_text.value.strip()
        self.DaRUS_data.citation.date_of_deposit = datetime.now().date().strftime("%Y-%m-%d")
        
        # Add generall SFB information
        self.DaRUS_data.citation.grant_number = []
        self.DaRUS_data.citation.add_grant_number( agency="DFG", value="358283783 - SFB 1333")

        # Add language
        self.DaRUS_data.citation.language     = [ "English" ]

        # Add related publication
        self.DaRUS_data.citation.publication = []
        self.DaRUS_data.citation.add_publication( **{k:self.dataset.general_information.related_publication.__dict__[k] for k in self.dataset.general_information.related_publication.__dict__.keys() if k!="id"})
        
        # Add topic classification
        self.DaRUS_data.citation.topic_classification = []
        for classification in self.dataset.general_information.topic_classification: 
            self.DaRUS_data.citation.add_topic_classification( **{k:classification.__dict__[k] for k in classification.__dict__.keys() if k!="id"} )

        # Add keywords
        self.DaRUS_data.citation.keyword = []
        for keyword in self.dataset.general_information.keywords:
            self.DaRUS_data.citation.add_keyword( **{k:keyword.__dict__[k] for k in keyword.__dict__.keys() if k!="id"} ) 
    
    def add_files_dir_to_dataset(self):
        # Add files and directories to DaRUS dataset
        for entry in self.file_directoy.value:
            if os.path.isfile(entry):
                self.DaRUS_data.add_file( dv_dir = entry, local_path = entry )
            elif os.path.isdir(entry):
               self.DaRUS_data.add_directory( dirpath = entry )
            else:
                print(f"The specified entry is neither a file nor a directory:\n {entry}")

    def create_new(self):
    
        self.dataverse_dropdown = widgets.Dropdown( options= self.dataverse_list,
                                                    description="Choose dataverse:",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        # Initialize  
        self.file_directoy.value = [ str(self.dataset_path) ]

        # Handle button
        self.button_upload.on_click( self.upload_to_DaRUS )

        # Widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))

        widgets0  = widgets.VBox([self.dataverse_dropdown, v_space])
        widgets1  = self.file_directoy_input
        widgets2  = widgets.VBox([self.button_add_file_dir, self.button_output], layout=widgets.Layout(align_items = 'center'))
        widgets3  = widgets.VBox([v_space,widgets.Label(value='Files / directories in DaRUS dataset:'), self.file_directoy])
        widgets4  = widgets.VBox([self.button_upload],layout=widgets.Layout(align_items = 'center'))

        # Combine the layout
        full_layout = widgets.VBox([widgets0, widgets1, widgets2, widgets3, widgets4])

        # Display the layout
        display(full_layout)

    def edit_existing(self):
        
        self.doi_text               = widgets.Text( description="DOI/PID for dataverse:",
                                                    placeholder="Doi of exisitng dataverse (e.g.: 'doi:xx.xxxxx/darus-xxxx)",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'} )

        self.button_download        = widgets.Button(description='Download dataset from DaRUS',
                                                     layout=widgets.Layout(width="30%"),
                                                     style={"button_color": 'lightblue'})

        self.file_directoy_text     = widgets.Text( description="Destination directory",
                                                    placeholder="Destination directory for DaRUS download. E.g: current directory with '.' ",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'} )
        
        # Handle button
        self.button_download.on_click( self.download_from_DaRUS )

        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))
        widgets0  = widgets.VBox([self.doi_text, self.file_directoy_text, v_space, self.button_download],layout=widgets.Layout(align_items = 'center'))

        # Combine the layout
        full_layout = widgets.VBox([widgets0, v_space,self.download_output])

        # Display the layout
        display(full_layout)

    def download_from_DaRUS(self,_):
        
        # Create folder where DaRUS data is saved
        os.makedirs( os.path.dirname(self.file_directoy_text), exist_ok=True )

        # Load existing DaRUS dataset
        self.DaRUS_data = self.dataverse.load_dataset( self.doi_text.value )
        
        # Initialize (remove all files from current dataset and reupload them if wanted)
        self.file_directoy.value = [ f.local_path for f in self.DaRUS_data.files ]
        self.DaRUS_data.files    = []

        # Handle button
        self.button_upload.on_click( self.update_to_DaRUS )

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

    def update_to_DaRUS(self,_):

        # Update citation metadata with provided dataset
        self.fill_citation()

        # Add files and directories
        self.add_files_dir_to_dataset()
        
        # Update dataset
        self.DaRUS_data.update( )

    def upload_to_DaRUS(self,_):
        """
        Function that uses the provided sdRDM dataset to extract all necessary information to upload a dataset to DaRUS.
        """
        
        # Create new DaRUS dataset
        self.DaRUS_data = self.dataverse.create_dataset()

        # Fill in citation metadata from general information object
        self.fill_citation()

        # Add files and directories
        self.add_files_dir_to_dataset()

        # Upload dataset
        self.DaRUS_data.upload( dataverse_name = self.dataverse_dropdown.value )


    def DaRUS(self, dataset: Dataset, dataset_path: Path | str, dataverse_list: List):
        
        # Common variables
        self.dataset                = Dataset(**dataset.__dict__)
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


        # Define output spaces
        self.button_output          = widgets.Output()  
        self.download_output        = widgets.Output()
        self.action_output          = widgets.Output()

        # Handle buttons
        self.button_add_file_dir.on_click(self.add_file_dir)


        ## Main widgets ##

        self.action_dropdown        = widgets.Dropdown(options= ["","Create new one", "Edit existing one"],
                                                       description="Choose whether you want to create a new data record or edit an existing one:",
                                                       layout=widgets.Layout(width='auto'),
                                                       style={'description_width': 'auto'})
        
        self.depositor_text         = widgets.Text( description="Depositor:",
                                                placeholder="Name of the person uploading this dataset (e.g.: Max Mustermann)",
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
        display( widgets.VBox([self.action_dropdown, self.depositor_text, self.api_token_text, v_space, self.action_output]) )