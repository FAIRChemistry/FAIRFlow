#!~/miniconda3/bin/python

import ipywidgets as widgets
from ipyfilechooser import FileChooser

from pathlib import Path, PureWindowsPath
from typing import List
from IPython.display import display, clear_output

# Import general tools and objects of this datamodel

# Objects
from FAIRFlow.core import Dataset, Experiment, PlantSetup

# Tools
from .auxiliary import Librarian, explorer
from .reader import gc_parser_faraday_efficiency, gc_parser_selective_oxidation, gstatic_parser, mfm_parser, DEXPI2sdRDM






class Person:
    """
    A class to represent a person.

    ...

    Attributes
    ----------
    name : str
        first name of the person
    surname : str
        family name of the person
    age : int
        age of the person

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """

    def __init__(self, name, surname, age):
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        ----------
            name : str
                first name of the person
            surname : str
                family name of the person
            age : int
                age of the person
        """

        self.name = name
        self.surname = surname
        self.age = age

    def info(self, additional=""):
        """
        Prints the person's name and age.

        If the argument 'additional' is passed, then it is appended after the main info.

        Parameters
        ----------
        additional : str, optional
            More info to be displayed (default is None)

        Returns
        -------
        None
        """

        print(f'My name is {self.name} {self.surname}. I am {self.age} years old.' + additional)


class reading_raw_data_widget_new:
    '''
    Class that creates a widget for reading in raw data and saving it as
    a dataset.

    Attributes
    ----------
    None

    Methods
    -------
    choose_data(root: Path, dataset_directory: str) -> None:
        Method that lets the user choose the dataset to be read in and
        displays the data acquisition widget.
    '''

    def choose_data(self, root: Path, dataset_directory: str) -> None:
        '''
        Method that lets the user choose the dataset to be read in and
        displays the data acquisition widget.
        
        Parameters
        ----------
        root : Path
            Path to the root directory of the dataset.
        dataset_directory : str
            Name of the directory where the datasets are stored.

        Returns:
        None
        
        '''
        self.root = root
        self.librarian = Librarian(root_directory=self.root)
        datasets = self.librarian.search_files_in_subdirectory(
            root_directory=self.root,
            directory_keys=[dataset_directory],
            file_filter="json",
            verbose=False,
        )

        self.w_dropdown_dataset = widgets.Dropdown(
            options=[("", Path(""))]
            + [(path.parts[-1], path) for _, path in datasets.items()],
            description="Choose dataset",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        widgets0 = widgets.HBox([self.w_dropdown_dataset])

        initial_layout = widgets.VBox(
            [
                widgets0,
            ]
        )
        self.w_dropdown_dataset.observe(self._dataset_input_handler, names="value")
        display(initial_layout)


    def _dataset_input_handler(self, _):
        clear_output(wait=True)

        self.dataset_path = self.w_dropdown_dataset.value
        try:
            with open(self.w_dropdown_dataset.value) as f:
                self.dataset = Dataset.from_json(f)
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")
        if self.dataset.general_information.scenario_nr == '1':
            self._scenario_selective_oxidation()
        elif self.dataset.general_information.scenario_nr == '2':
            self._scenario_faraday_efficiency()
        else:
            raise ValueError("\nScenario number not implemented!\n")

    def _scenario_faraday_efficiency(self):
        self.w_tagsinput_exp = widgets.TagsInput(allow_duplicates=False)

        self.w_button_save_dataset = widgets.Button(
            description=f"Save dataset as:  {self.w_dropdown_dataset.value.name}",
            layout=widgets.Layout(width="30%"),
            style={"button_color": "lightblue"},
        )

        try:
            self.w_tagsinput_exp.value = [exp.id for exp in self.dataset.experiments]
            self.plant = (
                self.dataset.experiments[0].plant_setup
                if self.dataset.experiments
                else PlantSetup()
            )

            # Define ouput for some widgets
            self.w_output_pid = widgets.Output()
            self.w_output_tab = widgets.Output()

            # Update component list
            self.component_list = [pl.component_id for pl in self.plant.components]

            # Initialize several objects
            self.measurement_objects = []
            self.w_tagsinput_measure = widgets.TagsInput(allow_duplicates=False)
            if self.component_list:
                with self.w_output_pid:
                    clear_output(wait=False)
                    print("PID taken from first experiment of dataset!\n")
            else:
                with self.w_output_pid:
                    clear_output(wait=False)
                    print("")
                    

            # Call measurement input handler to update
            self._measurement_input_handler(None)

            # Update button description
            self.w_button_save_dataset.description = f"Save dataset as:  {self.w_dropdown_dataset.value.name}"
            
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")


        self.w_button_add_exp = widgets.Button(
            description="Add experiment", layout=widgets.Layout(width="auto")
        )

        self.w_button_read_pid = widgets.Button(
            description="Read PID", layout=widgets.Layout(width="auto")
        )

        self.w_button_vis_pid = widgets.Button(
            description="Visualize PID", layout=widgets.Layout(width="auto")
        )
        # Call explorer widget
        self.explorer = explorer()
        w_explorer = self.explorer.main(
            root=self.root,
            file_categories=[
                "Potentiostat",
                "Gas chromatograph",
                "Mass flow meter",
                "Species data",
                "P&ID",
            ],
            add_file_callalbe=self._add_file,
        )

        self.w_text_exp_name = widgets.Text(
            description="Experiment name:",
            placeholder="Provide a name for the experiment",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.w_text_pid_file = widgets.Text(
            description="P&ID file:",
            placeholder="Provided as xml file using the DEXPI standard",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.w_text_species_file = widgets.Text(
            description="Species file:",
            placeholder="Provided as yaml file",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )


        # Functions for the buttons
        self.w_button_add_exp.on_click(self._add_experiment)
        self.w_button_save_dataset.on_click(self._save_dataset)
        self.w_button_read_pid.on_click(self._read_pid)
        self.w_button_vis_pid.on_click(self._visualize_pid)

        # Attach the event handler to the 'value' property change of the file type widget
        self.w_dropdown_dataset.observe(self._dataset_input_handler, names="value")
        self.w_tagsinput_measure.observe(self._measurement_input_handler, names="value")
        self.w_tagsinput_exp.observe(self._experiment_input_handler, names="value")



        # Create the layout
        v_space = widgets.VBox(
            [widgets.Label(value="")], layout=widgets.Layout(height="30px")
        )
        v_space_s = widgets.VBox(
            [widgets.Label(value="")], layout=widgets.Layout(height="15px")
        )
        v_space_ss = widgets.VBox(
            [widgets.Label(value="")], layout=widgets.Layout(height="7.5px")
        )
        widgets0 = widgets.VBox(
            [
                widgets.Label(value=f'Selected dataset: "{self.w_dropdown_dataset.value.name}"'),
            ]
        )
        widgets0_5 = widgets.VBox(
            [
                widgets.Label(value=f'Scenario number: "{self.dataset.general_information.scenario_nr}"'),
            ]
        )
        widgets1 = widgets.VBox(
            [
                widgets.Label(value="Manually add/remove Measurements:"),
                self.w_tagsinput_measure,
            ]
        )
        widgets2 = widgets.VBox([w_explorer, v_space_s])
        widgets3 = widgets.VBox([self.w_output_tab, v_space_s])
        widgets4 = widgets.VBox(
            [
                v_space_s,
                self.w_text_pid_file,
                v_space_ss,
                widgets.HBox([self.w_button_read_pid, self.w_button_vis_pid]),
                self.w_output_pid,
                v_space_ss,
                self.w_text_species_file,
                v_space_s,
            ]
        )
        widgets5 = widgets.VBox(
            [
                widgets.VBox(
                    [
                        widgets.Label(
                            value="After selecting all necessary files for an experiment, add the experiment to the chosen dataset."
                        ),
                        self.w_text_exp_name,
                        self.w_button_add_exp,
                    ]
                ),
                widgets.VBox([widgets.Label(value="Experiments:"), self.w_tagsinput_exp]),
            ]
        )
        widgets6 = widgets.VBox(
            [self.w_button_save_dataset], layout=widgets.Layout(align_items="center")
        )

        # Combine the layout
        full_layout = widgets.VBox(
            [
                widgets0,
                v_space_s,
                widgets0_5,
                v_space_s,
                widgets1,
                v_space_s,
                widgets2,
                widgets3,
                widgets4,
                v_space,
                widgets5,
                v_space,
                widgets6,
            ]
        )

        display(full_layout)

    def _scenario_selective_oxidation(self):
        self.date_time_list = []

        self.w_tagsinput_exp = widgets.TagsInput(allow_duplicates=False)

        self.w_button_save_dataset = widgets.Button(
            description=f"Save dataset as:  {self.w_dropdown_dataset.value.name}",
            layout=widgets.Layout(width="30%"),
            style={"button_color": "lightblue"},
        )

        try:
            self.w_tagsinput_exp.value = [exp.id for exp in self.dataset.experiments]
            self.plant = (
                self.dataset.experiments[0].plant_setup
                if self.dataset.experiments
                else PlantSetup()
            )

            # Define ouput for some widgets
            self.w_output_pid = widgets.Output(
                layout=widgets.Layout(grid_area="output_pid")
            )
            self.w_output_tab = widgets.Output(
                layout=widgets.Layout(grid_area="output_tab")
            )

            # Update component list
            self.component_list = [pl.component_id for pl in self.plant.components]

            self.measurement_objects = []
            self.w_tagsinput_measure = widgets.TagsInput(
                allow_duplicates=False,
                layout=widgets.Layout(
                    width="auto",
                    grid_area="tagsinput_measure"),
            )
            if self.component_list:
                with self.w_output_pid:
                    clear_output(wait=False)
                    print("PID taken from first experiment of dataset!\n")
            else:
                with self.w_output_pid:
                    clear_output(wait=False)
                    print("")
                    

            # Call measurement input handler to update
            self._measurement_input_handler(None)

            # Update button description
            self.w_button_save_dataset.description = f"Save dataset as:  {self.w_dropdown_dataset.value.name}"
            
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")


        scenario_mapping = {
            '1': 'selective_oxidation',
            '2': 'faraday_efficiency'
        }
        style = {'description_width': '15%'}

        # Define widgets
        self.w_button_add_exp = widgets.Button(
            description="Add experiment",
            layout=widgets.Layout(
                width="auto",
                grid_area="button_add_exp",
            ),
        )

        self.w_button_read_pid = widgets.Button(
            description="Read PID",
            layout=widgets.Layout(
                width="auto",
                grid_area="button_read_pid",
            )
        )

        self.w_button_vis_pid = widgets.Button(
            description="Visualize PID",
            layout=widgets.Layout(
                width="auto",
                grid_area="button_vis_pid",
            )
        )

        self.w_text_exp_name = widgets.Text(
            description="Experiment name:",
            placeholder="Provide a name for the experiment",
            layout=widgets.Layout(
                width="auto",
                grid_area="text_exp_name",
            ),
            style={"description_width": "auto"},
        )

        self.w_text_pid_file = widgets.Text(
            description="P&ID file:",
            placeholder="Provided as xml file using the DEXPI standard",
            layout=widgets.Layout(
                width="auto",
                grid_area="text_pid_file",
            ),
            style={"description_width": "auto"},
        )

        
        self.w_label_select_dataset = widgets.Label(
            value=f'Selected dataset: "{self.w_dropdown_dataset.value.name}"',
            layout=widgets.Layout(
                width='auto',
                grid_area='label_select_dataset'
            ),
        )

        self.w_label_scenario_nr =widgets.Label(
            value=f'Scenario number: "{self.dataset.general_information.scenario_nr}"',
            layout=widgets.Layout(
                width='auto',
                grid_area='label_scenario_nr'
            ),
        )

        self.w_label_select_path = widgets.Label(
            value="Browse to the file to be read in:",
            layout=widgets.Layout(
                width='auto',
                grid_area='label_select_path'
            ),
        )

        self.w_file_chooser = FileChooser(
            self.root / "data" / f'{scenario_mapping[self.dataset.general_information.scenario_nr]}' / 'raw_data',
            layout = widgets.Layout(
                width='auto',
                grid_area='file_chooser'
            ),
        )

        self.w_label_precha_descr = widgets.Label(
            value="Choose prechannel:",
            style=style,
            layout=widgets.Layout(
                width='auto',
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

        self.w_label_add_rm_measure = widgets.Label(
            value="Manually add/remove Measurements:",
            layout=widgets.Layout(
                width='auto',
                grid_area='label_add_rm_measure'
            ),
        )

        self.w_button_add_to_measure = widgets.Button(
            description="Add to measurement",
            layout=widgets.Layout(
                width="auto",
                grid_area='add_to_measure'
            ),
        )

        self.w_label_add_exp = widgets.Label(
            value='''After selecting all necessary files for an 
            experiment, add the experiment to the chosen dataset.''',
            layout=widgets.Layout(
                width='auto',
                grid_area='label_add_exp'
            ),
        )

        # Attach event handler
        self.w_button_add_exp.on_click(
            self._add_experiment
        )
        self.w_button_save_dataset.on_click(
            self._save_dataset
        )
        self.w_button_read_pid.on_click(
            self._read_pid
        )
        self.w_button_vis_pid.on_click(
            self._visualize_pid
        )
        self.w_file_chooser._filename.observe(
            self._file_chooser_input_handler,
            names="value"
        )
        self.w_file_chooser._select.on_click(
            self._file_chooser_input_handler
        )
        self.w_tagsinput_measure.observe(
            self._measurement_input_handler,
            names="value"
        )

        # self.w_button_add_to_measure.on_click(
        #     self._add_measurement_handler
        #     # lambda _: self._add_file(
        #     #     self.w_dropdown_choose_precha.value,
        #     #     self.w_selectmultiple_choose_cha.value,
        #     # )
        # )

        # self.w_tagsinput_exp.observe(
        #     self._experiment_input_handler,
        #     names="value"
        # )

        # Set up grid layout
        gridbox = widgets.GridBox(
            children=[
                self.w_label_select_dataset,
                self.w_label_scenario_nr,
                self.w_label_select_path,
                self.w_file_chooser,
                self.w_label_add_rm_measure,
                self.w_tagsinput_measure,


                self.w_output_tab,
                self.w_text_pid_file,
                self.w_button_read_pid,
                self.w_button_vis_pid,
                self.w_output_pid,
                self.w_label_precha_descr,
                self.w_dropdown_choose_precha,
                self.w_html_cha_description,
                self.w_selectmultiple_choose_cha,
                self.w_button_add_to_measure,
            ],
            layout=widgets.Layout(
                width='100%',
                grid_template_rows='auto auto auto auto auto auto',
                grid_template_columns='25% 25% 50%',
                grid_template_areas='''
                "label_select_dataset    label_select_dataset      label_scenario_nr"
                "label_select_path       label_select_path         label_select_path"
                "file_chooser            file_chooser              file_chooser"
                "label_add_rm_measure    label_add_rm_measure      label_add_rm_measure"
                "tagsinput_measure       tagsinput_measure         tagsinput_measure"


                "output_tab              output_tab                output_tab"
                "text_pid_file           text_pid_file             text_pid_file"
                "button_read_pid         button_read_pid           button_read_pid"
                "button_vis_pid          button_vis_pid            button_vis_pid"
                "output_pid              output_pid                output_pid"
                "label_precha_descr      dropdown_choose_precha    dropdown_choose_precha"
                "html_cha_descr          selectmultiple_choose_cha selectmultiple_choose_cha"
                '''
            )
        )
                # add_to_measure           add_to_measure           add_to_measure"


        display(gridbox)

    def _file_chooser_input_handler(self, _):
        if self.w_file_chooser.selected:
            self.mydata_df = gc_parser_selective_oxidation(self.w_file_chooser.selected)
            self.mylist = self.mydata_df['datetime'].astype(str) + ' - ' + self.mydata_df['Filename'].apply(lambda x: PureWindowsPath(x).name).astype(str) + ' - ' + self.mydata_df['Vial'].astype(str)
            self.w_dropdown_choose_precha.options = self.mylist
            self.w_selectmultiple_choose_cha.options = self.mylist


    def _measurement_input_handler(self, _):
        '''
        Function that handles the measurement input. It updates the
        measurement objects and the tabs in the measurement tab widget.
        It is called when the user adds or removes measurements in the
        measurement tagsinput widget.
        It also updates the component list of the measurement objects
        and the component dropdowns in the measurement tab widget.
        Diplays the measurement tab widget.

        Parameters
        ----------
        _ : None
            Not used, but required for the observer function.
        Returns
        -------
        None        
        '''

        # Delete measurement objects from the measurement_objects list 
        # that are not in the w_tagsinput_measure widget anymore
        del_idx = [
            i
            for i, obj in enumerate(self.measurement_objects)
            if not obj.name in self.w_tagsinput_measure.value
        ]
        del_idx.sort(reverse=True)

        for idx in del_idx:
            del self.measurement_objects[idx]


        # Add new measurement objects if they are not yet there
        # Depending on the scenario number, different measurement objects are created
        measurement_names = [obj.name for obj in self.measurement_objects]
        for i, measurement in enumerate(self.w_tagsinput_measure.value):
            if not measurement in measurement_names:
                if self.dataset.general_information.scenario_nr == '1':
                    self.measurement_objects.insert(
                        i,
                        measurement_object_so(
                            name=measurement, component_list=self.component_list
                        ),
                    )
                elif self.dataset.general_information.scenario_nr == '2':
                    self.measurement_objects.insert(
                        i,
                        measurement_object_fe(
                            name=measurement, component_list=self.component_list
                        ),
                    )

        # Update component list of all exisiting measurements
        for obj in self.measurement_objects:
            obj.update_component_list(self.component_list)

        # Call measurement tab widget
        self._measurement_tabs()

    def _measurement_tabs(self):

        # Define tab widget
        self.tabs = widgets.Tab([obj.full_layout for obj in self.measurement_objects])

        # Set title of the tabs
        for i, title in enumerate([obj.name for obj in self.measurement_objects]):
            self.tabs.set_title(i, title)

        heading = widgets.Label(value="Files for measurements:")

        with self.w_output_tab:
            self.w_output_tab.clear_output(wait=False)
            display(widgets.VBox([heading, self.tabs]))

    def _add_file(self, category: str, file: str):
        # Function that adds a file to a chosen category
        # The file is added to the selected measurement tab to the selected children (potentiostat, gas chromatograph, etc.)

        def _add(index_children, file):
            self.tabs.children[self.tabs.selected_index].children[index_children].children[
                1
            ].value = self.tabs.children[self.tabs.selected_index].children[index_children].children[
                1
            ].value + [
                file
            ]
        if category == "potentiostat":
            _add(0, file)
        elif category == "gas chromatograph":
            _add(1, file)
        elif category == "mass flow meter":
            _add(2, file)
        elif category == "species data":
            self.w_text_species_file.value = file
        elif category == "P&ID":
            self.pid_file.value = file

    def _read_pid(self, _):
        # Function that reads in DEXPI PID file and generates the PlantSetup
        self.plant = DEXPI2sdRDM(self.w_text_pid_file.value)

        with self.w_output_pid:
            self.w_output_pid.clear_output(wait=False)
            print("PID sucessfully read out!\n")

        # Update component list
        self.component_list = [pl.component_id for pl in self.plant.components]

        # Call tab widget
        self._measurement_input_handler(None)

    def _visualize_pid(self, _):
        # Function that visualizes the PID as graph
        # If plant is just initialized read in PID first
        if not self.plant.components:
            self._read_pid(None)
        self.plant.visualize()


    def _add_experiment(self, _):

        ## Read in selected raw data and save it in Experiment class ##
        if not self.experiment_name.value:
            raise ValueError("Provide experiment name!\n")

        # Define experiment object
        experiment = Experiment(id=self.experiment_name.value)

        # Add plant setup
        experiment.plant_setup = self.plant

        # Get all measurements and add to experiment
        for measurement in self.measurement_objects:

            pot_measurements = [
                gstatic_parser(metadata_path=potentiostat_file)
                for potentiostat_file in measurement.potentio_files.value
            ]
            mfm_measurements = [
                mfm_parser(experimental_data_path=mfm_file)
                for mfm_file in measurement.MFM_files.value
            ]
            gc_measurements = [
                gc_parser(
                    metadata_path=measurement.GC_files.value[i],
                    experimental_data_path=measurement.GC_files.value[i + 1],
                )
                for i in range(0, len(measurement.GC_files.value), 2)
            ]

            # Add corresponding DEXPI component for each measurement
            for i, pm in enumerate(pot_measurements):
                pm.id = f'{measurement.name.replace(" ", "")}_potentiostat_{i}'

                # Add defined source of measurement
                if measurement.potentio_component.value in self.component_list:
                    pm.source = self.plant.components[
                        self.component_list.index(measurement.potentio_component.value)
                    ]

            for i, mm in enumerate(mfm_measurements):
                mm.id = f'{measurement.name.replace(" ", "")}_massflowmeter_{i}'

                # Add defined source of measurement
                if measurement.mfm_component.value in self.component_list:
                    mm.source = self.plant.components[
                        self.component_list.index(measurement.mfm_component.value)
                    ]

            for i, gm in enumerate(gc_measurements):
                gm.id = f'{measurement.name.replace(" ", "")}_gaschromatograph{i}'

                # Add defined source of measurement
                if measurement.gc_component.value in self.component_list:
                    gm.source = self.plant.components[
                        self.component_list.index(measurement.gc_component.value)
                    ]

            for measurement in [*pot_measurements, *mfm_measurements, *gc_measurements]:
                experiment.add_to_measurements(**measurement.model_dump())

        # Initialize species data such as calibration, correction factors and transfering eletron number
        experiment.initialize_species_from_yaml(self.species_file.value)

        # Append new experiment to current dataset
        self.dataset.experiments.append(experiment)

        # Update experiment list
        self.experiments.value = [exp.id for exp in self.dataset.experiments]

        # Empty files widget
        self.measurements.value = []
        self.experiment_name.value = ""




    # def _add_experiment2(self, _):

    #     ## Read in selected raw data and save it in Experiment class ##
    #     if not self.w_text_exp_name.value:
    #         raise ValueError("Provide experiment name!\n")

    #     # Define experiment object
    #     experiment = Experiment(id=self.w_text_exp_name.value)

    #     # Add plant setup
    #     experiment.plant_setup = self.plant

    #     # Get all measurements and add to experiment
    #     for measurement in self.measurement_objects:

    #         if self.dataset.general_information.scenario_nr == '2':
    #             pot_measurements = [
    #                 gstatic_parser(metadata_path=potentiostat_file)
    #                 for potentiostat_file in measurement.potentio_files.value
    #             ]
    #             mfm_measurements = [
    #                 mfm_parser(experimental_data_path=mfm_file)
    #                 for mfm_file in measurement.MFM_files.value
    #             ]
    #             gc_measurements = [
    #                 gc_parser_faraday_efficiency(
    #                     metadata_path=measurement.GC_files.value[i],
    #                     experimental_data_path=measurement.GC_files.value[i + 1],
    #                 )
    #                 for i in range(0, len(measurement.GC_files.value), 2)
    #             ]

    #             # Add corresponding DEXPI component for each measurement
    #             for i, pm in enumerate(pot_measurements):
    #                 pm.id = f'{measurement.name.replace(" ", "")}_potentiostat_{i}'

    #                 # Add defined source of measurement
    #                 if measurement.potentio_component.value in self.component_list:
    #                     pm.source = self.plant.components[
    #                         self.component_list.index(measurement.potentio_component.value)
    #                     ]

    #             for i, mm in enumerate(mfm_measurements):
    #                 mm.id = f'{measurement.name.replace(" ", "")}_massflowmeter_{i}'

    #                 # Add defined source of measurement
    #                 if measurement.mfm_component.value in self.component_list:
    #                     mm.source = self.plant.components[
    #                         self.component_list.index(measurement.mfm_component.value)
    #                     ]

    #             for i, gm in enumerate(gc_measurements):
    #                 gm.id = f'{measurement.name.replace(" ", "")}_gaschromatograph{i}'

    #                 # Add defined source of measurement
    #                 if measurement.gc_component.value in self.component_list:
    #                     gm.source = self.plant.components[
    #                         self.component_list.index(measurement.gc_component.value)
    #                     ]

    #         elif self.dataset.general_information.scenario_nr == '1':

    #             gc_measurements = [
    #                 n_channel_measurements = len(measurement.GC_files.value) - 1
    #                 gc_parser_selective_oxidation(
    #                     prechannel_data_path=measurement.GC_files.value[i],
    #                     channel_data_paths = []
    #                     channel_data_path=measurement.GC_files.value[i + 1],
    #                 )
    #                 for i in range(0, len(measurement.GC_files.value))
    #             ]

    #             # Add corresponding DEXPI component for each measurement
    #             for i, gm in enumerate(gc_measurements):
    #                 gm.id = f'{measurement.name.replace(" ", "")}_gaschromatograph{i}'

    #                 # Add defined source of measurement
    #                 if measurement.gc_component.value in self.component_list:
    #                     gm.source = self.plant.components[
    #                         self.component_list.index(measurement.gc_component.value)
    #                     ]

    #         for measurement in [*pot_measurements, *mfm_measurements, *gc_measurements]:
    #             experiment.add_to_measurements(**measurement.model_dump())

    #     # Initialize species data such as calibration, correction factors and transfering eletron number
    #     experiment.initialize_species_from_yaml(self.w_text_species_file.value)

    #     # Append new experiment to current dataset
    #     self.dataset.experiments.append(experiment)

    #     # Update experiment list
    #     self.w_tagsinput_exp.value = [exp.id for exp in self.dataset.experiments]

    #     # Empty files widget
    #     self.w_tagsinput_measure.value = []
    #     self.w_text_exp_name.value = ""

    def _experiment_input_handler(self, _):

        # Delete experiment objects that are not in the experiment widget anymore
        del_idx = [
            i
            for i, exp in enumerate(self.dataset.experiments)
            if not exp.id in self.w_tagsinput_exp.value
        ]
        del_idx.sort(reverse=True)

        for idx in del_idx:
            del self.dataset.experiments[idx]

    def _save_dataset(self, _):
        # Function to save dataset
        with open(self.w_dropdown_dataset.value, "w") as f:
            f.write(self.dataset.json())
        print("Dataset saved.")

class measurement_object_fe:
    """
    Stores the measurement widgets.
    """

    def __init__(self, name: str, component_list: List[str]) -> None:

        # Safe name
        self.name = name

        # Define portion of component dropdown to path tags
        portion = 3

        self.w_dropdown_potentio_component = widgets.Dropdown(
            options=[""] + component_list,
            description="Corresponding plant component",
            layout=widgets.Layout(flex=str(portion)),
            style={"description_width": "auto"},
        )

        self.w_dropdown_gc_component = widgets.Dropdown(
            options=[""] + component_list,
            description="Corresponding plant component",
            layout=widgets.Layout(flex=str(portion)),
            style={"description_width": "auto"},
        )

        self.w_dropdown_mfm_component = widgets.Dropdown(
            options=[""] + component_list,
            description="Corresponding plant component",
            layout=widgets.Layout(flex=str(portion)),
            style={"description_width": "auto"},
        )

        self.w_tagsinput_potentio_files = widgets.TagsInput(
            allow_duplicates=False, layout=widgets.Layout(flex=str(10 - portion))
        )
        self.w_tagsinput_GC_files = widgets.TagsInput(
            allow_duplicates=False, layout=widgets.Layout(flex=str(10 - portion))
        )
        self.w_tagsinput_MFM_files = widgets.TagsInput(
            allow_duplicates=False, layout=widgets.Layout(flex=str(10 - portion))
        )

        widgets0 = widgets.VBox(
            [
                widgets.Label(value="Files for potentiostat:"),
                widgets.HBox([
                    self.w_tagsinput_potentio_files,
                    self.w_dropdown_potentio_component
                ]),
            ]
        )
        widgets1 = widgets.VBox(
            [
                widgets.Label(value="Files for gas chromatograph:"),
                widgets.HBox([
                    self.w_tagsinput_GC_files,
                    self.w_dropdown_gc_component
                ]),
            ]
        )
        widgets2 = widgets.VBox(
            [
                widgets.Label(value="Files for mass flow meter:"),
                widgets.HBox([
                    self.w_tagsinput_MFM_files,
                    self.w_dropdown_mfm_component
                ]),
            ]
        )

        # Combine the layout
        self.full_layout = widgets.VBox([widgets0, widgets1, widgets2])


    def update_component_list(self, component_list: List[str]):
        
        self.w_dropdown_potentio_component.options = [""] + component_list
        self.w_dropdown_gc_component.options = [""] + component_list
        self.w_dropdown_mfm_component.options = [""] + component_list

class measurement_object_so:
    """
    Stores the measurement widgets.
    """

    def __init__(self, name: str, component_list: List[str]) -> None:

        # Safe name
        self.name = name

        # Define portion of component dropdown to path tags
        portion = 3

        self.w_dropdown_gc_component = widgets.Dropdown(
            options=[""] + component_list,
            description="Corresponding plant component",
            layout=widgets.Layout(flex=str(portion)),
            style={"description_width": "auto"},
        )

        self.w_tagsinput_GC_files = widgets.TagsInput(
            allow_duplicates=False, layout=widgets.Layout(flex=str(10 - portion))
        )

        widgets1 = widgets.VBox(
            [
                widgets.Label(value="Files for gas chromatograph:"),
                widgets.HBox([
                    self.w_tagsinput_GC_files,
                    self.w_dropdown_gc_component
                ]),
            ]
        )

        # Combine the layout
        self.full_layout = widgets.VBox([widgets1])



    def update_component_list(self, component_list: List[str]):

        self.w_dropdown_gc_component.options = [""] + component_list
