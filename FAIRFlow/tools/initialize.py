#!~/miniconda3/bin/python

import os
import ipywidgets as widgets
from IPython.display import display, clear_output

# Import Dataset
from FAIRFlow.core import Dataset


class initialize_dataset:

    def _save_dataset(self,_):

        with self.button_output:
            clear_output(wait=True)

            print("Saving dataset!")
            
            # Add title
            self.dataset.general_information.title       = self.title.value
            
            # Add description
            self.dataset.general_information.description = self.description.value 

            # Add project group
            self.dataset.general_information.project     = self.project.value

            # Add purpose
            self.dataset.general_information.purpose     = self.purpose.value

        # Write dataset
        os.makedirs( f"{os.getcwd()}/{os.path.dirname(self.dataset_text.value)}", exist_ok=True )
        with open( f"{os.getcwd()}/{self.dataset_text.value}.json", "w") as f: f.write(self.dataset.json())

    def _change_dataset(self,_):
        self.button_save.description = 'Save dataset as:  %s.json'%self.dataset_text.value
               
    def write_dataset(self) -> None:
        
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

        self.purpose            = widgets.Text(description="Purpose:",
                                                placeholder="Purpose of this dataset",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.dataset_text        = widgets.Text(description="Dataset destination:",
                                                placeholder="Provide a relative path to save the dataset (e.g. datasets/dummy will be saved as datasets/dummy.json).",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.button_save         = widgets.Button(description='Save dataset as:  %s.json'%self.dataset_text.value,
                                                  layout=widgets.Layout(width="30%"),
                                                  style={"button_color": 'lightblue'})
        
        # Initialize the datamodel
        self.dataset = Dataset()
        
        # Handle on observing
        self.dataset_text.observe(self._change_dataset,names="value")
        
        # Handle button
        self.button_save.on_click(self._save_dataset)

        # Output spaces
        self.button_output = widgets.Output()

        # Widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))

        widgets0  = widgets.VBox([self.title, self.description, self.project, self.purpose, v_space, self.dataset_text, v_space])
        widgets1  = widgets.VBox([self.button_save, self.button_output], layout=widgets.Layout(align_items = 'center') )

        # Combine the layout
        full_layout = widgets.VBox([widgets0, widgets1])

        # Display the layout
        display(full_layout)

        return
