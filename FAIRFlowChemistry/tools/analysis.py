#!~/miniconda3/bin/python

import pandas as pd
import logging
import ipywidgets as widgets
from IPython.display import display, clear_output

# Import general tools and objects of this datamodel #

# Objects #
#from easyDataverse import Dataverse
from FAIRFlowChemistry.core import Data
from FAIRFlowChemistry.core import Dataset
from FAIRFlowChemistry.core import Experiment
from FAIRFlowChemistry.core import MeasurementType
from FAIRFlowChemistry.core import Quantity

# Tools #
from .auxiliary import PeakAssigner
from .calculator import FaradayEfficiencyCalculator

logger = logging.getLogger("main")

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
        self.peak_assignment = PeakAssigner( experiment             = Experiment( **self.dataset.experiments[self.experiments_dropdown.value].__dict__ ), 
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

            logger.info("\nStarting the postprocessing for experiment: %s\n"%(self.dataset.experiments[self.experiments_dropdown.value].id))

            fe_calculator = FaradayEfficiencyCalculator(experiment  = self.dataset.experiments[self.experiments_dropdown.value],
                                                        mean_radius = self.mean_radius.value)

            faraday_efficiencies = []

            # Extract the GC measurements from the choosen experiment
            gc_measurements      = self.dataset.experiments[self.experiments_dropdown.value].get("measurements", "measurement_type", MeasurementType.GC.value)[0]

            for i, gc_measurement in enumerate( gc_measurements ):
                tmp = fe_calculator.calculate_faraday_efficiencies( gc_measurement = gc_measurement )
                faraday_efficiencies.append( tmp )
                print("Faraday effiencies of GC measurement n°%d"%(i+1))
                print(tmp,"\n")

            mean_faraday_efficiency = pd.concat(faraday_efficiencies).groupby(level=0).mean()
            
            print("\nMean Faraday efficency over all GC measurements")
            print(mean_faraday_efficiency,"\n")

            for species_data in self.dataset.experiments[self.experiments_dropdown.value].species_data:
                if species_data.species in mean_faraday_efficiency.index:
                    faraday_efficiency              = mean_faraday_efficiency.loc[species_data.species].values
                    species_data.faraday_efficiency = Data( quantity = Quantity.FARADAYEFFIECENCY.value, values = faraday_efficiency.tolist())


    def choose_experiment(self, dataset: Dataset, dataset_path: str, typical_retention_time: dict={}) -> None:
        """
        Function that shows widgets to analyse faraday effiencies using GC measurements.

        Args:
            dataset (Dataset): Dataset containing all the necessary information.
            dataset_path (str): Path where the dataset should be saved to.
            typical_retention_time (dict, optional): If wanted, a dictionary containing species and typical retention times to do the pre assigment of the GC measurement peaks. Defaults to {}.

        """
        
        # Common variables
        self.typical_retention_time = typical_retention_time 
        self.dataset_path           = dataset_path
        self.dataset                = Dataset(**dataset.model_dump())

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