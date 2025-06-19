#!~/miniconda3/bin/python

'''

'''



from pathlib import Path, PureWindowsPath

from IPython.display import display, clear_output
import ipywidgets as widgets
from ipyfilechooser import FileChooser



# Data model objects
from FAIRFlow.core import Dataset, Experiment, PlantSetup

# Import general tools and objects of this datamodel
from FAIRFlow.src.acquisition.scenario_specific.scenarios import FaradayEfficiency, SelectiveOxidation # Not needed anymore?
from FAIRFlow.src.utils.auxiliary import Librarian

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
        if not hasattr(self.dataset, "general_information.scenario_name"):
            raise KeyError("\nChosen dataset does not contain information about the scenario type!\n")
        self.scenario_type = self.dataset.general_information.scenario_name

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

        self.w_Button_SaveDataset.description = f"Save dataset as:  {self.w_Dropdown_Dataset.value.name}"

        self.w_Label_ScenarioType =widgets.Label(
            value=f'Scenario type: "{self._scenario_type}"',
            layout=widgets.Layout(
                width='auto',
                grid_area='label_scenario_nr'
            ),
        )

        gridbox = widgets.GridBox(
            children=[
                self.w_Label_SelectedDataset,
                self.w_Dropdown_Dataset,
                self._scenario.w_Gridbox_Measurement,
                self.w_Label_MeasurementHeading, 
                # mybox,
                self.w_Button_SaveDataset,
                self.w_Label_ScenarioType,
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
                "dropdown_dataset           label_selected_dataset  label_scenario_nr"
                "label_measurement_heading  .                       ."
                "scenario_gridbox           scenario_gridbox        scenario_gridbox"
                ".                          button_save_dataset     ."
                '''
            )
        )
                # "mybox                      .                       ."
                # "button_save_dataset              button_save_dataset        button_save_dataset"

        display(gridbox)




#!~/miniconda3/bin/python

import ipywidgets as widgets
from ipyfilechooser import FileChooser
from pathlib import Path

from IPython.display import display, clear_output

# Objects
from FAIRFlow.core import Dataset, Experiment, PlantSetup

# Import FAIRFlow packages
from FAIRFlow.src.utils.registry import register_scenario, SCENARIO_REGISTRY
from FAIRFlow.src.utils.lookups import SCENARIO_MAPPING
from FAIRFlow.src.generic_readers.dexpi2sdrdm import DEXPI2sdRDM


class ScenarioBase:
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

        # try reading in the experiments and subsequently the plant and the plant components
        try:
            experiments_ids_list = [exp.id for exp in self.dataset.experiments]
            self.plant_setup = (self.dataset.experiments[0].plant_setup if self.dataset.experiments else PlantSetup())
            self.component_list = [pl.component_id for pl in self.plant_setup.components]
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")        

        self.w_Output_ReadPID = widgets.Output(
            layout=widgets.Layout(
                width= "auto",
                grid_area="output_read_pid"
            )
        )

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
        #         grid_area='label_scenario_nr'
        #     ),
        # )

        self.w_Label_BrowseToFile = widgets.Label(
            value="Browse to the file to be read in:",
            layout=widgets.Layout(
                width='auto',
                grid_area='label_browse_file'
            ),
        )

        self.w_Label_BrowseToPID = widgets.Label(
            value="Browse to the P&ID file to be read in:",
            layout=widgets.Layout(
                width='auto',
                grid_area='label_browse_pid'
            ),
        )

        self.w_FileChooser_Data = FileChooser(
            self.root / "scenarios" / SCENARIO_MAPPING[self.__class__.__name__]['dir_name'] / 'raw_data',
            layout = widgets.Layout(
                width='auto',
                grid_area='file_chooser_data'
            ),
        )

        self.w_FileChooser_PID = FileChooser(
            self.root / "scenarios" / SCENARIO_MAPPING[self.__class__.__name__]['dir_name'] / 'DEXPI',
            layout = widgets.Layout(
                width='auto',
                grid_area='file_chooser_pid'
            ),
        )

        self.w_Dropdown_Component = widgets.Dropdown(
            options=[""] + self.component_list,
            description="Component",
            tooltip="P&ID component of the currently loaded P&ID",
            layout = widgets.Layout(
                width='auto',
                grid_area='dropdown_component'
            ),
        )

        self.w_Dropdown_Measure = widgets.Dropdown(
            options=[""] + list(self.measurement_objects_dict.keys()),
            description="All measurements",
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

        self.w_Output_NewMeasurement = widgets.Output(
            layout=widgets.Layout(
                width='auto',
                grid_area='output_new_measurement'
            ),
        )

        self.w_Text_MeasurementName = widgets.Text(
            placeholder='Enter measurement name',
            description='Name:',
            style={'description_width': 'auto'},
            layout=widgets.Layout(
                width='auto',
                grid_area='text_measurement_name'
            ),
        )


        # Attach observers to the widgets
        # self.w_Button_NewMeasurement._click_handlers.callbacks.clear()
        self.w_Button_NewMeasurement.on_click(self.Handler_Button_NewMeasurement)
        self.w_Dropdown_Measure.observe(self.Handler_Measurement_Dropdown)
        self.w_FileChooser_PID.observe(self.Handler_FileChooser_PID)   # Not yet working, has to be changed
        # self.w_Dropdown_Measure.value # name of the currently selected measurement


        self.w_Gridbox_Measurement = widgets.GridBox(
            children = [
                self.w_Button_NewMeasurement,
                self.w_Dropdown_Measure,
                self.w_Dropdown_Component,
                self.w_FileChooser_Data,
                self.w_FileChooser_PID,
                self.w_Gridbox_Specific,
                self.w_Text_MeasurementName,
                self.w_Label_BrowseToFile,
                self.w_Label_BrowseToPID,
                self.w_Output_NewMeasurement,
                self.w_Output_DropdownMeasure,
                self.w_Output_ReadPID,
                self.w_Output_ComponentToMeasurement,
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
                grid_area = 'scenario_gridbox',
                grid_template_rows='auto, auto, auto, auto, auto, auto, auto, auto auto auto',
                grid_template_columns="20% 15% 15% 15% 15% 15%",
                grid_template_areas='''
                "text_measurement_name          text_measurement_name           button_new_measurement      button_new_measurement          output_new_measurement      output_new_measurement "
                "dropdown_measure               dropdown_measure                dropdown_measure            dropdown_measure                dropdown_measure            dropdown_measure       "
                "output_dropdown_measure        output_dropdown_measure         output_dropdown_measure     output_dropdown_measure         output_dropdown_measure     output_dropdown_measure"
                "output_read_pid                output_read_pid                 output_read_pid             output_read_pid                 output_read_pid             output_read_pid        "
                "label_browse_file              label_browse_file               label_browse_file           label_browse_file               label_browse_file           label_browse_file      "
                "file_chooser_data              file_chooser_data               file_chooser_data           file_chooser_data               file_chooser_data           file_chooser_data      "
                "label_browse_pid               label_browse_pid                label_browse_pid            label_browse_pid                label_browse_pid            label_browse_pid       "
                "file_chooser_pid               file_chooser_pid                file_chooser_pid            file_chooser_pid                file_chooser_pid            file_chooser_pid       "
                "dropdown_component             dropdown_component              dropdown_component          dropdown_component              dropdown_component          dropdown_component     "
                "gridbox_specific               gridbox_specific                gridbox_specific            gridbox_specific                gridbox_specific            gridbox_specific       "
                '''
            )
        )
#  auto auto auto auto auto


    def Handler_Button_NewMeasurement(self, _=None):
        with self.w_Output_NewMeasurement:
            self.w_Output_NewMeasurement.clear_output()
            name = self.w_Text_MeasurementName.value.strip()
            if name:
                # 
                # Here the logic for creating a new measurement!!!
                if name in self.measurement_objects_dict.keys():
                    self.w_Output_NewMeasurement.clear_output()
                    print("⚠️ Measurement of the same name already present! Choose a different name.")
                else:
                    self.measurement_objects_dict.update({name: Measurement(name)})
                    self.w_Dropdown_Measure.options = list(self.measurement_objects_dict.keys())
                    print(f"✅ New measurement added: {name}")
                # # What is a measurement object?
                # 
                self.w_Text_MeasurementName.value = ''
            else:
                print("⚠️ Please enter a name before adding.")
        self.w_Dropdown_Measure.value = name
        self.Handler_Measurement_Dropdown()


    def Handler_Measurement_Dropdown(self, _=None):
        '''
        Attached to the w_Dropdown_Measure widget. Clear the current output
        seen in the w_Output_DropdownMeasure widget and displays the selected
        measurement object 
        '''

        with self.w_Output_DropdownMeasure:
            self.w_Output_DropdownMeasure.clear_output(wait=False)
            # display(self.w_Gridbox_Measurement)
            display("Hallo du kleine Maus")
    
    def Handler_FileChooser_PID(self, _=None):
        with open('logging', 'w') as f:
            f.write('hallo')
        if self.w_FileChooser_PID.selected:
            self.plant = DEXPI2sdRDM(self.w_FileChooser_PID.selected)

        with self.w_Output_ReadPID:
            self.w_Output_ReadPID.clear_output(wait=False)
            print("PID sucessfully parsed.\n")

        # Update component list
        self.component_list = [pl.component_id for pl in self.plant.components]
        self.w_Dropdown_Component.options=[""] + self.component_list



    def Handler_Button_ComponentToMeasurement(self, _=None):
        component = self.w_Dropdown_Component.value
        measurement = self.w_Dropdown_Measure.value    
        with self.w_Output_ComponentToMeasurement:
            self.w_Output_ComponentToMeasurement.clear_output()
            print(f'✅ P&ID component {component}vadded to measurementv{measurement}')
        measurement.pid_component = component

    # def _measurement_input_handler(self, _= None):
    #     '''
    #     Updates the measuremnt objects according to what      
    #     '''

    #     # Delete measurement objects from the measurement_objects_dict list 
    #     # that are not in the w_TagsInput_Measure widget anymore
    #     del_idx = [
    #         i
    #         for i, obj in enumerate(self.measurement_objects_dict)
    #         if not obj.name in self.w_TagsInput_Measure.value
    #     ]
    #     del_idx.sort(reverse=True)

    #     for idx in del_idx:
    #         del self.measurement_objects_dict[idx]

    #     measurement_names = [obj.name for obj in self.measurement_objects_dict]


        # if self.dataset.general_information.scenario_nr == '1':
        #     for i, measurement in enumerate(self.w_TagsInput_Measure.value):
        #         if not measurement in measurement_names:
        #             self.measurement_objects_dict.insert(
        #                 i,
        #                 measurement_object_so(
        #                     name=measurement, component_list=self.component_list
        #                 ),
        #             )
        #     # Update component list of all exisiting measurements
        #     for obj in self.measurement_objects_dict:
        #         obj.update_component_list(self.component_list)
        #     self._measurement_dropdown()
            
        # elif self.dataset.general_information.scenario_nr == '2':
        #     for i, measurement in enumerate(self.w_TagsInput_Measure.value):
        #         if not measurement in measurement_names:
        #             self.measurement_objects_dict.insert(
        #                 i,
        #                 measurement_object_fe(
        #                     name=measurement, component_list=self.component_list
        #                 ),
        #             )
        #     # Call measurement tab widget
        #     self._measurement_tabs()
        #     # Update component list of all exisiting measurements
        #     for obj in self.measurement_objects_dict:
        #         obj.update_component_list(self.component_list)

    @property
    def w_scenario_gridbox(self):
        return self.w_Gridbox_Measurement


class Measurement():
    pid_component = None

    def __init__(self, name):
        self.name = name