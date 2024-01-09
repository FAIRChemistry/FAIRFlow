#!~/miniconda3/bin/python

import os
import ipywidgets as widgets
from typing import List
from pathlib import Path
from IPython.display import display, clear_output

# Import modified sdRDM objects #
from sdRDM import DataModel

# Import general tools and objects of this datamodel #

# Tools #
from .auxiliary import Librarian

class initialize_dataset:

    def init_datamodel(self,_):
        # Initialize the dataset #
        if Path(self.datamodels_dropdown.value).suffix == '.git':
            lib = DataModel.from_git( url=self.datamodels_dropdown.value, tag=self.git_branch ) if self.git_branch else DataModel.from_git( url=self.datamodels_dropdown.value )
        elif Path(self.datamodels_dropdown.value).suffix == '.md':
            lib = DataModel.from_markdown( self.datamodels_dropdown.value )
        else:
            pass
        
        self.dataset = lib.Dataset()

    def save_dataset(self,_):

        with self.button_output:
            clear_output(wait=True)

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

        self.dataset.general_information.contact = dict( name = self.contact_text.value.split(",")[0].strip(), 
                                                         email = self.contact_text.value.split(",")[1].strip(), 
                                                         affiliation = affili )

        # Add subject
        self.dataset.general_information.subject = list( self.subject_selection.value )

        # Add related publication
        self.dataset.general_information.related_publication  = dict( citation = self.related_publication.value.split(",")[0].strip(),
                                                                      url      = self.related_publication.value.split(",")[1].strip() )

        # Add topic classifications
        for i in range(0, len(self.topic_classification.value.split(",")), 2):
            self.dataset.general_information.add_to_topic_classification( value     = self.topic_classification.value.split(",")[i].strip() , 
                                                                          vocab_uri = self.topic_classification.value.split(",")[i + 1].strip() )

        # Add keywords
        for i in range(0, len(self.keywords.value.split(",")), 2):
            self.dataset.general_information.add_to_keywords( value          = self.keywords.value.split(",")[i].strip() , 
                                                              vocabulary_uri = self.keywords.value.split(",")[i + 1].strip() )
            
        # Write dataset #
        os.makedirs( self.root / "datasets", exist_ok=True )
        with open( str(self.root) + "/datasets/%s.json"%self.dataset_text.value, "w") as f: f.write(self.dataset.json())

    def change_dataset(self,_):
        self.button_save.description = 'Save dataset as:  %s.json'%self.dataset_text.value
               
    def write_dataset(self,root: Path, git_path: str, git_branch: str="", subjects: List=[]) -> None:
        
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

        self.subject_selection   = widgets.SelectMultiple( options=subjects,
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
        
        # Initialize the datamodel
        self.init_datamodel(None)
        
        # Handle on observing
        self.datamodels_dropdown.observe(self.init_datamodel,names="value")
        self.dataset_text.observe(self.change_dataset,names="value")
        
        # Handle button
        self.button_save.on_click(self.save_dataset)

        # Output spaces
        self.button_output = widgets.Output()

        # Widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))
        h_space   = widgets.HBox([widgets.Label(value='')], layout=widgets.Layout(width='30px'))

        widgets0  = widgets.HBox([self.datamodels_dropdown, h_space, self.identifier_scheme])
        widgets1  = widgets.VBox([v_space, self.title, self.description, self.project,v_space])
        widgets2  = widgets.VBox([self.authors, self.affiliations, self.identifier, self.contact_text, v_space])
        widgets3  = widgets.VBox([self.subject_selection, self.related_publication, self.topic_classification, self.keywords, v_space])
        widgets4  = widgets.VBox([self.dataset_text, v_space])
        widgets5  = widgets.VBox([self.button_save, self.button_output], layout=widgets.Layout(align_items = 'center') )

        # Combine the layout
        full_layout = widgets.VBox([widgets0, widgets1, widgets2, widgets3, widgets4, widgets5])

        # Display the layout
        display(full_layout)

        return
