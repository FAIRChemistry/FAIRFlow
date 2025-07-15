#!~/miniconda3/bin/python

'''

'''

# Third-party python packages
import ipywidgets as widgets
from ipyfilechooser import FileChooser
from IPython.display import display, clear_output
from pathlib import Path

from abc import ABC, abstractmethod

# FAIRFlow data model objects
from FAIRFlow.core import Dataset, Experiment, Measurement, PlantSetup

# FAIRFlow imports
from FAIRFlow.src.utils.auxiliary import Librarian
from FAIRFlow.src.utils.registry import SCENARIO_REGISTRY
from FAIRFlow.src.utils.factory import create_scenario

# from FAIRFlow.src.utils.lookups import SCENARIO_MAPPING
from FAIRFlow.src.acquisition.generic_readers.dexpi2sdrdm import DEXPI2sdRDM


### Here we need logic to load the scenario-specific code



class AcquireData:
    '''
    Class that creates a widget for reading in raw data and saving it as
    a dataset.

    Attributes
    ----------
    None

    Methods
    -------
    choose_data(root: Path) -> None:
        Method that lets the user choose the dataset to be read in and
        displays the data acquisition widget.
    '''

    experiment_objects_dict = {}

    
    def choose_data(self, root: Path) -> None:
        '''
        Only public method of the class. It searches all datasets in the
        directory "./datasets/" and displays the "w_Dropdown_Dataset" widget,
        which let's the user choose a dataset.
        
        Parameters
        ----------
        root : Path
            Path to the root directory (current working directory).

        Returns:
        None
        
        '''
        self.root = root
        self.librarian = Librarian(root_directory=self.root)
        datasets_dict = self.librarian.search_files_in_subdirectory(
            root_directory=self.root,
            directory_keys=['datasets'],
            file_filter="json",
            verbose=False,
        )

        self.w_Dropdown_Dataset = widgets.Dropdown(
            options=[("", Path(""))]
            + [(path.parts[-1], path) for _, path in datasets_dict.items()],
            description="Choose dataset",
            layout=widgets.Layout(
                width="auto",
                grid_area ="dropdown_dataset"
            ),
            style={"description_width": "auto"},
        )

        self.w_Dropdown_Dataset.observe(self._dataset_input_handler, names="value")
        
        display(self.w_Dropdown_Dataset)


    def _dataset_input_handler(self, _):
        '''
        Observer that is attached to the "w_Dropdown_Dataset" widget.
        It reads in a selected dataset and depending on the scenario_nr 
        instantiates the respective class.   
        
        Parameters
        ----------
        root : Path
            Path to the root directory (current working directory).

        Returns:
        None
        
        '''
        clear_output(wait=True)

        self.dataset_path = self.w_Dropdown_Dataset.value
        try:
            with open(self.w_Dropdown_Dataset.value) as f:
                self.dataset = Dataset.from_json(f)
        except:
            raise KeyError("\nChoosen dataset cannot be read!\n")
        if (
            not hasattr(self.dataset, "general_information")
            or self.dataset.general_information is None
            or not hasattr(self.dataset.general_information, "scenario_name")
            or not self.dataset.general_information.scenario_name
        ):
            raise KeyError("\nChosen dataset does not contain information about the scenario type!\n")
        else:
            self.scenario_name = self.dataset.general_information.scenario_name
        # if self.scenario_name not in SCENARIO_REGISTRY.keys():
        #     raise KeyError(
        #         f"\nScenario '{self.scenario_name}' not recognized!\n"
        #         f"Available scenarios are: {list(SCENARIO_REGISTRY.keys())}\n"
        #     )
        
        
        # else:
        self._scenario = create_scenario(
            scenario_name=self.scenario_name,
            stage=Path(__file__).stem,
            dataset=self.dataset,
            root=self.root,
        )


        
        self.w_Button_SaveDataset = widgets.Button(
            description=f"Save dataset as:  {self.dataset_path.name}",
            layout=widgets.Layout(
                width="auto",
                # justify_self="center",  # horizontal alignment of items
                align_self="center",  # horizontal alignment of items
                grid_area = "button_save_dataset"
                ),
            style={"button_color": "lightgrey"},
        )
        self.w_Button_SaveDataset.description = f'Save dataset as:  "{self.w_Dropdown_Dataset.value.name}"'

        self.w_Label_SelectedDataset = widgets.Label(

            value=f'Selected dataset: "{self.w_Dropdown_Dataset.value.name}"',
            layout=widgets.Layout(
                width='auto',
                grid_area='label_selected_dataset'
            ),
        )

        self.w_Label_MeasurementHeading = widgets.Label(
            value="Files for measurements:",
            layout=widgets.Layout(
                width='auto',
                grid_area='label_measurement_heading',
                # border='2px solid' + "#000000",
                # padding='10px',
                # margin='5px',
                # background_color="#0008FF",
            ),
        )

        self.w_Label_ScenarioName =widgets.Label(
            value=f'Scenario name: "{self.dataset.general_information.scenario_name}"',
            layout=widgets.Layout(
                width='auto',
                grid_area='label_scenario_name'
            ),
        )

        self.w_Output_ReadPID = widgets.Output(
            layout=widgets.Layout(
                width= "auto",
                grid_area="output_read_pid"
            )
        )

        self.w_Label_BrowseToPID = widgets.Label(
            value="Browse to the P&ID file to be read in:",
            layout=widgets.Layout(
                width='auto',
                grid_area='label_browse_pid'
            ),
        )

        self.w_FileChooser_PID = FileChooser(
            self.root / "data" / self.dataset.general_information.scenario_name / 'DEXPI',
            layout = widgets.Layout(
                width='auto',
                grid_area='file_chooser_pid'
            ),
        )

        self.w_Dropdown_Experiment = widgets.Dropdown(
            options=[""] + list(self.experiment_objects_dict.keys()),
            description="Currently selected experiment",
            style={'description_width': 'auto'},
            layout = widgets.Layout(
                width='auto',
                grid_area='dropdown_experiment'
            ),
        )

        self.w_Button_NewExperiment = widgets.Button(
            description = 'Add new experiment',
            layout = widgets.Layout(
                width='auto',
                grid_area='button_new_experiment'
            ),
            style={"button_color": "lightgrey"},
            button_style='success',
            tooltip='Click to add a new experiment',
            icon='plus',
        )

        self.w_Button_DeleteExperiment = widgets.Button(
            description = 'Delete currently selected experiment',
            layout = widgets.Layout(
                width='auto',
                grid_area='button_delete_experiment'
            ),
            style={"button_color": "red"},
            button_style='success',
            tooltip='Click to the experiment currently selected',
            icon='minus',
        )

        self.w_Output_ModExperiment = widgets.Output(
            layout=widgets.Layout(
                width='auto',
                grid_area='output_mod_experiment'
            ),
        )

        self.w_Text_ExperimentId   = widgets.Text(
            placeholder='Enter experiment id',
            description='Name:',
            style={'description_width': 'auto'},
            layout=widgets.Layout(
                width='auto',
                grid_area='text_experiment_id'
            ),
        )
        self.w_Output_DropdownExperiment = widgets.Output(          # This is widgets that displays one whole experiment
            layout=widgets.Layout(                                  # it should be called whenever w_Dropdown_Measure changes
                width = "auto",
                grid_area="output_dropdown_experiment"
            )
        )


        self.w_Gridbox_Experiment = widgets.GridBox(
            children = [
                self.w_Text_ExperimentId,                              # textexperiment_id
                self.w_Button_NewExperiment,                           # button_new_experiment
                self.w_Button_DeleteExperiment,                        # button_delete_experiment
                self.w_Output_ModExperiment,                           # output_mod_experiment
                self.w_Dropdown_Experiment,                            # dropdown_experiment
                self.w_Output_DropdownExperiment,                      # output_dropdown_experiment
            ],
            layout=widgets.Layout(
                width='auto',
                # justify_items="center",  # horizontal alignment of items
                # align_items="center",  # horizontal alignment of items
                # width='90%',
                # border='2px solid' + "#000000",
                # padding='10px',
                # margin='5px',
                # background_color="#0008FF",
                grid_area = 'experiment_gridbox',
                grid_template_rows='auto, auto, auto, auto, auto, auto, auto, auto auto auto',
                grid_template_columns="20% 15% 15% 15% 15% 15%",
                grid_template_areas='''
                "text_experiment_id        button_new_experiment       button_new_experiment       button_delete_experiment    button_delete_experiment    output_mod_experiment     "
                "dropdown_experiment         dropdown_experiment         dropdown_experiment         dropdown_experiment         dropdown_experiment         dropdown_experiment       "
                "output_dropdown_experiment  output_dropdown_experiment  output_dropdown_experiment  output_dropdown_experiment  output_dropdown_experiment  output_dropdown_experiment"
                '''
            )
        )

        gridbox = widgets.GridBox(
            children=[
                self.w_Dropdown_Dataset,                                # dropdown_dataset
                self.w_Label_SelectedDataset,                           # label_selected_dataset
                self.w_Label_ScenarioName,                              # label_scenario_name
                self.w_Label_MeasurementHeading,                        # label_measurement_heading
                self.w_Label_BrowseToPID,                               # label_browse_pid
                self.w_FileChooser_PID,                                 # file_chooser_pid
                self.w_Output_ReadPID,                                  # output_read_pid
                self._scenario.w_Gridbox_Measurement,                   # measurement_gridbox
                self.w_Gridbox_Experiment,                              # experiment_gridbox
                self.w_Button_SaveDataset,                              # button_save_dataset
            ],
            layout=widgets.Layout( 
                # justify_items="center",  # horizontal alignment of items
                # align_items="center",  # horizontal alignment of items
                width='auto',
                # width='90%',
                # gap="10px 20px",          # optional spacing
                grid_template_rows='auto auto auto auto',
                # grid_template_rows='auto auto auto',
                grid_template_columns='25% 50% 25%',
                grid_template_areas='''
                "dropdown_dataset           label_selected_dataset  label_scenario_name"
                "experiment_gridbox         experiment_gridbox      experiment_gridbox "
                "label_browse_pid           label_browse_pid        label_browse_pid   "
                "file_chooser_pid           file_chooser_pid        file_chooser_pid   "
                "output_read_pid            output_read_pid         output_read_pid    "
                "label_measurement_heading  .                       .                  "
                "measurement_gridbox        measurement_gridbox     measurement_gridbox"
                ".                          button_save_dataset     .                  "
                '''
            )
        )

        # try reading in the experiments and subsequently the plant and the plant components
        if hasattr(self.dataset, "experiments"):
            if len(self.dataset.experiments) > 0:
                self.experiment_objects_dict = {exp.id: exp for exp in self.dataset.experiments}
                with open("logging", "a") as f:
                    f.write("hallo\n")
                    f.write("\n".join([key for key in self.experiment_objects_dict.keys() if key is not None]))
                self.w_Dropdown_Experiment.options = [""] + list(self.experiment_objects_dict)
                self.w_Dropdown_Experiment.value = list(self.experiment_objects_dict)[-1]
                self.update_plant()
                self.update_measurements()


        # We need methods that update certains widgets or list/dicts

        # handlers should only be called in case of events, they typically change internal lists/dicts
        # updating methods typically work the other way round. They update widgets according to the internal lists/dicts
        self.w_FileChooser_PID._select.on_click(self.Handler_FileChooser_PID)   # Not yet working, has to be changed
        self.w_Button_NewExperiment.on_click(self.Handler_Button_NewExperiment)
        self.w_Button_DeleteExperiment.on_click(self.Handler_Button_DeleteExperiment)

        display(gridbox)
    
    def Handler_FileChooser_PID(self, _=None):
        '''
        
        '''
        if not self.w_FileChooser_PID._filename.value == "" and not self.w_Dropdown_Experiment.value == "":
            plant = DEXPI2sdRDM(self.w_FileChooser_PID.selected)
            experiment_object = self.experiment_objects_dict[self.w_Dropdown_Experiment.value]
            with open("logging", "a") as f:
                if experiment_object.plant_setup is not None:
                    if experiment_object.plant_setup.id is not None:
                        f.write(experiment_object.plant_setup.id)
            if not hasattr(experiment_object, "plant_setup"):
                setattr(experiment_object, "plant", plant)
            else:
                experiment_object.pid_component = plant
            setattr(self.w_FileChooser_PID._filename, "value",  "")
            with self.w_Output_ReadPID:
                self.w_Output_ReadPID.clear_output(wait=False)
                print("PID sucessfully parsed.\n")
            # Update component list
            self.component_list = [pl.component_id for pl in experiment_object.plant_setup.components if experiment_object.plant_setup is not None]
            self._scenario.w_Dropdown_Component.options=[""] + self.component_list

    def Handler_Button_NewExperiment(self, _=None):
        with self.w_Output_ModExperiment:
            self.w_Output_ModExperiment.clear_output()
            new_experiment_id = self.w_Text_ExperimentId.value.strip()
            if new_experiment_id:
                if new_experiment_id in self.experiment_objects_dict.keys():
                    self.w_Output_ModExperiment.clear_output()
                    print("⚠️ Experiment of the same id already present! Choose a different id.")
                else:
                    experiment_object = Experiment()
                    experiment_object.id = new_experiment_id
                    self.experiment_objects_dict.update({new_experiment_id: experiment_object})
                    self.w_Dropdown_Experiment.options = [""] + list(self.experiment_objects_dict.keys())
                    print(f"✅ New experiment added: {new_experiment_id}")
                # # What is a measurement object?
                # 
                self.w_Text_ExperimentId.  value = ''
            else:
                print("⚠️ Please enter an id before adding.")
        self.w_Dropdown_Experiment.value = new_experiment_id
        self.Handler_Experiment_Dropdown()

    def Handler_Button_DeleteExperiment(self, _=None):
        with self.w_Output_ModExperiment:
            self.w_Output_ModExperiment.clear_output()
            current_experiment_id = self.w_Dropdown_Experiment.value
            if not current_experiment_id == "" and current_experiment_id in self.experiment_objects_dict.keys():
                del self.experiment_objects_dict[current_experiment_id]
                self.w_Dropdown_Experiment.options = [""]
                if self.experiment_objects_dict:
                    self.w_Dropdown_Experiment.options += list(self.experiment_objects_dict.keys())
                    self.w_Dropdown_Experiment.value = list(self.experiment_objects_dict)[-1]
                else:
                    self.w_Dropdown_Experiment.value = ""
                self.Handler_Experiment_Dropdown()
                print(f"✅ Experiment {current_experiment_id} successfully deleted.")
            elif current_experiment_id == "":
                print("⚠️ No experiment selected to delete.")



    def Handler_Experiment_Dropdown(self, _=None):
        '''
        Attached to the w_Dropdown_Experiment widget. Clear the current output
        seen in the w_Output_DropdownExperiment widget and displays the selected
        experiment object 
        '''

        if not self.w_Dropdown_Experiment.value == "":
            current_experiment_id = self.w_Dropdown_Experiment.value
            experiment_object = self.experiment_objects_dict[current_experiment_id]
            if hasattr(experiment_object, "plant"):
                self.w_FileChooser_PID.selected = experiment_object.plant


    def update_plant(self):
        current_experiment_object = self.experiment_objects_dict[self.w_Dropdown_Experiment.value]
        if hasattr(current_experiment_object, "plant"):
            self.w_FileChooser_PID.selected = current_experiment_object.plant.id
    def update_measurements(self):
        current_experiment_object = self.experiment_objects_dict[self.w_Dropdown_Experiment.value]
        if hasattr(current_experiment_object, "measurements"):
            self._scenario.w_Dropdown_Measurement.options = [""] + [measure.id for measure in current_experiment_object.measurements]


class ScenarioBase(ABC):
    # style = {'description_width': '15%'}
    style = {'description_width': 'auto'}
    component_list = [] # components of the currently selected PID
    measurement_objects_dict = {}

    w_Button_FileToMeasurement = widgets.Button(
        description = 'Add file to measurement',
        layout = widgets.Layout(
            width='auto',
            grid_area='button_file_to_measurement'
        ),
        style={"button_color": "lightgrey"},
        button_style='success',
        tooltip='Click to add the selected file to the currently open measurement',
        icon='plus',
    )
    w_Output_FileToMeasurement = widgets.Output(
        layout=widgets.Layout(
            width='auto',
            grid_area='output_file_to_measurement'
        ),
    )
    
    def __init__(self, dataset, root, gridbox_specific):

        # make arguments class-wide available
        self.dataset            = dataset
        self.root               = root
        self.w_Gridbox_Specific = gridbox_specific      

        self.w_Output_ComponentToMeasurement = widgets.Output(
            layout=widgets.Layout(
                width= "auto",
                grid_area="output_component_to_measurement"
            )
        )
        
        # if self.component_list:
        #     with self.w_Output_PID:
        #         clear_output(wait=False)
        #         print("PID taken from first experiment of dataset!\n")
        # else:
        #     with self.w_Output_PID:
        #         clear_output(wait=False)
        #         print("")

        # Define the generic scenario widgets

        self.w_Output_DropdownMeasure = widgets.Output(             # This is widgets that displays one whole measurement
            layout=widgets.Layout(                                  # it should be called whenever w_Dropdown_Measure changes
                width = "auto",
                grid_area="output_dropdown_measure"
            )
        )

        # self.w_TagsInput_Measure = widgets.TagsInput(
        #     allow_duplicates=False,
        #     layout=widgets.Layout(
        #         width="auto",
        #         grid_area="tagsinput_measure"
        #     ),
        # )

        # self.w_Label_ScenarioNr =widgets.Label(
        #     value=f'Scenario number: "{self.dataset.general_information.scenario_nr}"',
        #     layout=widgets.Layout(
        #         width='auto',
        #         grid_area='label_scenario_name'
        #     ),
        # )

        self.w_Label_BrowseToFile = widgets.Label(
            value="Browse to the file to be read in:",
            layout=widgets.Layout(
                width='auto',
                grid_area='label_browse_file'
            ),
        )

        self.w_FileChooser_Data = FileChooser(
            self.root / "data" / self.dataset.general_information.scenario_name / 'raw_data',
            layout = widgets.Layout(
                width='auto',
                grid_area='file_chooser_data'
            ),
        )

        self.w_Dropdown_Component = widgets.Dropdown(
            options=[""] + self.component_list,
            description="Component:",
            tooltip="P&ID component of the currently loaded P&ID",
            layout = widgets.Layout(
                width='auto',
                grid_area='dropdown_component'
            ),
        )

        self.w_Dropdown_Measure = widgets.Dropdown(
            options=[""] + list(self.measurement_objects_dict.keys()),
            description="Currently selected measurements:",
            style={'description_width': 'auto'},
            layout = widgets.Layout(
                width='auto',
                grid_area='dropdown_measure'
            ),
        )

        self.w_Button_NewMeasurement = widgets.Button(
            description = 'Add new measurement',
            layout = widgets.Layout(
                width='auto',
                grid_area='button_new_measurement'
            ),
            style={"button_color": "lightgrey"},
            button_style='success',
            tooltip='Click to add a new measurement',
            icon='plus',
        )

        self.w_Button_DeleteMeasurement = widgets.Button(
            description = 'Delete currently selected measurement',
            layout = widgets.Layout(
                width='auto',
                grid_area='button_delete_measurement'
            ),
            style={"button_color": "red"},
            button_style='success',
            tooltip='Click to the measurement currently selected',
            icon='minus',
        )

        self.w_Output_ModMeasurement = widgets.Output(
            layout=widgets.Layout(
                width='auto',
                grid_area='output_mod_measurement'
            ),
        )

        self.w_Text_MeasurementId = widgets.Text(
            placeholder='Enter measurement id',
            description='Name:',
            style={'description_width': 'auto'},
            layout=widgets.Layout(
                width='auto',
                grid_area='text_measurement_id'
            ),
        )


        # Attach observers to the widgets
        # self.w_Button_NewMeasurement._click_handlers.callbacks.clear()
        self.w_Button_NewMeasurement.on_click(self.Handler_Button_NewMeasurement)
        self.w_Button_DeleteMeasurement.on_click(self.Handler_Button_DeleteMeasurement)
        # self.w_Dropdown_Measure.observe(self.Handler_Measurement_Dropdown)
        self.w_Dropdown_Component.observe(self.Handler_DropdownComponent)
        # self.w_Dropdown_Measure.value # name of the currently selected measurement
            # Do not attach a handler here; child classes should attach their own handler if needed
            # self.w_Dropdown_Measure.value # name of the currently selected measurement

        self.w_Gridbox_Measurement = widgets.GridBox(
            children = [
                self.w_Text_MeasurementId,                            # text_measurement_id
                self.w_Button_NewMeasurement,                           # button_new_measurement
                self.w_Button_DeleteMeasurement,                        # button_delete_measurement
                self.w_Output_ModMeasurement,                           # output_mod_measurement
                self.w_Dropdown_Measure,                                # dropdown_measure
                self.w_Output_DropdownMeasure,                          # output_dropdown_measure
                self.w_Dropdown_Component,                              # dropdown_component
                self.w_Label_BrowseToFile,                              # label_browse_file
                self.w_FileChooser_Data,                                # file_chooser_data
                self.w_Gridbox_Specific,                                # gridbox_specific
                # self.w_Output_ComponentToMeasurement,                   # 
            ],
            layout=widgets.Layout(
                width='auto',
                # justify_items="center",  # horizontal alignment of items
                # align_items="center",  # horizontal alignment of items
                # width='90%',
                border='2px solid' + "#000000",
                # padding='10px',
                # margin='5px',
                # background_color="#0008FF",
                grid_area = 'measurement_gridbox',
                grid_template_rows='auto, auto, auto, auto, auto, auto, auto, auto auto auto',
                grid_template_columns="20% 15% 15% 15% 15% 15%",
                grid_template_areas='''
                "text_measurement_id          button_new_measurement          button_new_measurement      button_delete_measurement       button_delete_measurement   output_mod_measurement  "
                "dropdown_measure               dropdown_measure                dropdown_measure            dropdown_measure                dropdown_measure            dropdown_measure        "
                "output_dropdown_measure        output_dropdown_measure         output_dropdown_measure     output_dropdown_measure         output_dropdown_measure     output_dropdown_measure "
                "dropdown_component             dropdown_component              dropdown_component          dropdown_component              dropdown_component          dropdown_component      "
                "label_browse_file              label_browse_file               label_browse_file           label_browse_file               label_browse_file           label_browse_file       "
                "file_chooser_data              file_chooser_data               file_chooser_data           file_chooser_data               file_chooser_data           file_chooser_data       "
                "gridbox_specific               gridbox_specific                gridbox_specific            gridbox_specific                gridbox_specific            gridbox_specific        "
                '''
            )
        )

    @abstractmethod
    def _file_chooser_input_handler(self, _=None):
        # Placeholder handler for file chooser; implement logic as needed
        pass

    def Handler_Button_NewMeasurement(self, _=None):
        with self.w_Output_ModMeasurement:
            self.w_Output_ModMeasurement.clear_output()
            new_measurement_id = self.w_Text_MeasurementId.value.strip()
            if new_measurement_id:
                # 
                # Here the logic for creating a new measurement!!!
                if new_measurement_id in self.measurement_objects_dict.keys():
                    self.w_Output_ModMeasurement.clear_output()
                    print("⚠️ Measurement of the same ID already present! Choose a different ID.")
                else:
                    measurement_object = Measurement()
                    measurement_object.id = new_measurement_id
                    self.measurement_objects_dict.update({new_measurement_id: measurement_object})
                    self.w_Dropdown_Measure.options = [""] + list(self.measurement_objects_dict.keys())
                    print(f"✅ New measurement added: {new_measurement_id}")
                # # What is a measurement object?
                # 
                self.w_Text_MeasurementId.value = ''
            else:
                print("⚠️ Please enter an ID before adding.")
        self.w_Dropdown_Measure.value = new_measurement_id
        self.Handler_Measurement_Dropdown()

    def Handler_Button_DeleteMeasurement(self, _=None):
        with self.w_Output_ModMeasurement:
            self.w_Output_ModMeasurement.clear_output()
            current_measurement_id = self.w_Dropdown_Measure.value
            if not current_measurement_id == "" and current_measurement_id in self.measurement_objects_dict.keys():
                del self.measurement_objects_dict[current_measurement_id]
                self.w_Dropdown_Measure.options = [""]
                if self.measurement_objects_dict:
                    self.w_Dropdown_Measure.options += list(self.measurement_objects_dict.keys())
                    self.w_Dropdown_Measure.value = list(self.measurement_objects_dict)[-1]
                else:
                    self.w_Dropdown_Measure.value = ""
                self.Handler_Measurement_Dropdown()
                print(f"✅ Measurement {current_measurement_id} successfully deleted.")
            elif current_measurement_id == "":
                print("⚠️ No measurement selected to delete.")
            # elif not current_measurement_id == "" and not current_measurement_id in self.measurement_objects_dict.keys():
            #     print("⚠️ Selected measurement does not exist.")



    def Handler_Measurement_Dropdown(self, _=None):
        '''
        Attached to the w_Dropdown_Measure widget. Clear the current output
        seen in the w_Output_DropdownMeasure widget and displays the selected
        measurement object 
        '''

        # with self.w_Output_DropdownMeasure:
        #     self.w_Output_DropdownMeasure.clear_output(wait=False)
        #     # display(self.w_Gridbox_Measurement)
        #     display("Hallo du kleine Maus")
            # Here wee need to update everything to the new selected measurement object !!!
        if not self.w_Dropdown_Measure.value == "":
            with open("logging.log", "a") as f:
                f.write(f'measurement objects dict: { self.measurement_objects_dict}')
            current_measurement_id = self.w_Dropdown_Measure.value
            measurement_object = self.measurement_objects_dict[current_measurement_id]
            if hasattr(measurement_object, "pid_component"):
                self.w_Dropdown_Component.value = measurement_object.pid_component
            # if hasattr(measurement, "filepath"):
            #     self.w_FileChooser_Data.filename = measurement.filepath

    def Handler_DropdownComponent(self, _=None):
        if not self.w_Dropdown_Component.value == "":
            component = self.w_Dropdown_Component.value
            measurement = self.measurement_objects_dict[self.w_Dropdown_Measure.value]    
            # with self.w_Output_ComponentToMeasurement:
            #     self.w_Output_ComponentToMeasurement.clear_output()
            #     print(f'✅ P&ID component {component}vadded to measurementv{measurement}')
            if not hasattr(measurement, "pid_component"):
                setattr(measurement, "pid_component", component)
            else:
                measurement.pid_component = component

    @property
    def w_measurement_gridbox(self):
        return self.w_Gridbox_Measurement


# ### Experiment

# - plant_setup
#   - Type: PlantSetup
#   - Description: the individual plant setup that is used in this one experiment.
# - measurements
#   - Type: Measurement[]
#   - Description: different measurements that are made within the scope of one experiment.
# - species_data
#   - Type: SpeciesData[]
#   - Description: all provided and calculated data about a specific species.


# ### PlantSetup

# - components
#   - Type: Component[]
#   - Description: bla.
# - input
#   - Type: string[]
#   - Description: bla.
# - output
#   - Type: string[]
#   - Description: bla.

# ### Measurement

# - _measurement_type_
#   - Type: MeasurementType
#   - Description: type of a measurement, e.g. potentiostatic or gas chromatography.
# - metadata
#   - Type: Metadata[]
#   - Description: metadata of a measurement.
# - experimental_data
#   - Type: Data[]
#   - Description: experimental data of a measurement.
# - source
#   - Type: Component
#   - Description: measuring device the data stems from.