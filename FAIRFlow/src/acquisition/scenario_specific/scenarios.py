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
        self.w_FileChooser_PID.observe(self.Handler_FileChooser_PID)
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
        print("Handler called")
        with self.w_Output_NewMeasurement:
            self.w_Output_NewMeasurement.clear_output()
            name = self.w_Text_MeasurementName.value.strip()
            if name:
                print(f"✅ New measurement added: {name}")
                # 
                # Here the logic for creating a new measurement!!!
                if name in self.measurement_objects_dict.keys():
                    self.w_Output_NewMeasurement.clear_output()
                    print("⚠️ Measurement of the same name already present! Choose a different name.")
                else:
                    self.measurement_objects_dict.update({name: Measurement(name)})
                    self.w_Dropdown_Measure.options = list(self.measurement_objects_dict.keys())
                # # What is a measurement object?
                # 
                self.w_Text_MeasurementName.value = ''
            else:
                print("⚠️ Please enter a name before adding.")
        self.w_Dropdown_Measure.value = name
        self.Handler_Measurement_Dropdown()


    def Handler_Measurement_Dropdown(self):
        '''
        Attached to the w_Dropdown_Measure widget. Clear the current output
        seen in the w_Output_DropdownMeasure widget and displays the selected
        measurement object 
        '''

        with self.w_Output_DropdownMeasure:
            self.w_Output_DropdownMeasure.clear_output(wait=False)
            # display(self.w_Gridbox_Measurement)
            display("Hallo du kleine Maus")
    
    def Handler_FileChooser_PID(self, _):
        if self.w_FileChooser_PID.selected:
            self.plant = DEXPI2sdRDM(self.w_FileChooser_PID.selected)

        with self.w_Output_ReadPID:
            self.w_Output_ReadPID.clear_output(wait=False)
            print("PID sucessfully parsed.\n")

        # Update component list
        self.component_list = [pl.component_id for pl in self.plant.components]


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


@register_scenario
class FaradayEfficiency(ScenarioBase):

    def __init__(self, dataset, root):

        self.categories = {
            "potentiostat":      "potentiostat",
            "gas chromatograph": "gas_chromatograph",
            "mass flow meter":   "mass_flow_meter",
            "species data":      "species_data",
            "P&ID":              "P_ID",
        }
        self.w_Dropdown_Categories = widgets.Dropdown(
            options=[opt for opt in self.categories.keys()],
            description="Category",
            layout=widgets.Layout(
                width="auto",
                grid_area ="dropdown_category"
            ),
            style={"description_width": "auto"},
        )


        # attach handlers

        self.w_Button_FileToMeasurement.on_click(self.Button_FileToMeasurement_handler)


        w_Gridbox_Specific = widgets.GridBox(
            children=[
                self.w_Dropdown_Categories,
                self.w_Button_FileToMeasurement,
                self.w_Output_FileToMeasurement,
            ],
            layout=widgets.Layout(
                width='auto',
                # border='2px solid' + "#000000",
                # padding='10px',
                # margin='5px',
                # background_color="#ff0000",
                grid_area = 'gridbox_specific',
                grid_template_rows='auto',
                grid_template_columns="20% 15% 15% 15% 15% 15%",
                grid_template_areas='''    
                "dropdown_category           dropdown_category           button_file_to_measurement              button_file_to_measurement           output_file_to_measurement           output_file_to_measurement"
                '''
            )
        )
        super().__init__(dataset, root, w_Gridbox_Specific)


    def Button_FileToMeasurement_handler(self, _=None):
        print("Handler called")
        with self.w_Output_FileToMeasurement:
            self.w_Output_FileToMeasurement.clear_output()
            name = self.w_Dropdown_Categories.value.strip()
            if name:
                print(f'✅ File of type "{name}" added to measurement')

                measurement = self.measurement_objects_dict[self.w_Dropdown_Measure.value]
                file        = self.w_FileChooser_Data.selected
                category    = self.categories[self.w_Dropdown_Categories.value]
                if hasattr(measurement, category):
                    getattr(measurement, category).append(file)
                else:
                    setattr(measurement, category, [file])

            else:
                print("⚠️ Please enter a name before adding.")


@register_scenario
class SelectiveOxidation(ScenarioBase):

    def __init__(self, dataset, root):

        style = self.style
        # Scenario-specific imports
        from FAIRFlow.src.acquisition.scenario_specific.readers import gc_parser_selective_oxidation
        from pathlib import PureWindowsPath

        self.GCParser = gc_parser_selective_oxidation
        self.PureWindowsPath = PureWindowsPath

        # selective oxidation-specific widgets

        self.w_label_precha_descr = widgets.Label(
            value="Choose prechannel:",
            style=super().style,
            layout=widgets.Layout(
                width='auto',
                # border='2px solid' + "#000000",
                # padding='10px',
                # margin='5px',
                # background_color="#ff0000",
                grid_area='label_precha_descr'
            ),
        )

        self.w_dropdown_choose_precha = widgets.Dropdown(

            layout = widgets.Layout(
                width='auto',
                grid_area='dropdown_choose_precha'
            ),
            style = style,
        )

        self.w_html_cha_description = widgets.HTML(
            value="<p style='line-height: 1.2;'>Choose channels <br> ('Ctrl' + 'Left Click' for multiple):</p>",
            # value= '<style>p{word-wrap: break-word}</style> <p>'+ "Choose channels <br> ('Ctrl' + 'Left Click' for multiple):" +' </p>',
            layout=widgets.Layout(
                width='auto',
                grid_area='html_cha_descr'
            ),
        )

        self.w_selectmultiple_choose_cha = widgets.SelectMultiple(
            disabled = False,
            layout = widgets.Layout(
                width='auto',
                grid_area='selectmultiple_choose_cha'
            ),
            style = style,
        )

        # attach observers

        self.w_selectmultiple_choose_cha.observe(
            self._channel_handler,
            names="value"
        )

        self.w_dropdown_choose_precha.observe(
            self._prechannel_handler,
            names="value"
        )

        # self.w_button_add_to_measure.on_click(
        #     self._add_measurement_handler
        #     lambda _: self._add_file(
        #         self.w_dropdown_choose_precha.value,
        #         self.w_selectmultiple_choose_cha.value,
        #     )
        # )

        # build the grid box using the scenario-specific widgets defined above

        w_Gridbox_Specific = widgets.GridBox(
            children=[
                self.w_label_precha_descr,
                self.w_dropdown_choose_precha,
                self.w_html_cha_description,
                self.w_selectmultiple_choose_cha,
            ],
            layout=widgets.Layout(
                width='auto',
                grid_area = 'gridbox_specific',
                grid_template_rows='auto auto auto',
                grid_template_columns='25% 25% 50%',
                grid_template_areas='''
                "label_precha_descr       dropdown_choose_precha     dropdown_choose_precha"
                "html_cha_descr           selectmultiple_choose_cha  selectmultiple_choose_cha"
                "html_cha_description     html_cha_description       html_cha_description"
                "output_dropdown_measure  output_dropdown_measure    output_dropdown_measure"
                '''
            )
        )

        # call the constructor of the parent class
        super().__init__(dataset, root, w_Gridbox_Specific)

    def _prechannel_handler(self, _):
        pass

    def _channel_handler(self, _):
        pass

    def _file_chooser_input_handler(self, _):
        if self.w_FileChooser_Data.selected:
            self.mydata_df = self.GCParser(self.w_FileChooser_Data.selected)
            self.mylist = self.mydata_df['datetime'].astype(str) + ' - ' + self.mydata_df['Filename'].apply(lambda x: self.PureWindowsPath(x).name).astype(str) + ' - ' + self.mydata_df['Vial'].astype(str)
            self.w_dropdown_choose_precha.options = self.mylist
            self.w_selectmultiple_choose_cha.options = self.mylist


class Measurement():
    pid_component = None

    def __init__(self, name):
        self.name = name