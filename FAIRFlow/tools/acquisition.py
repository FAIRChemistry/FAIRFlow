#!~/miniconda3/bin/python

import ipywidgets as widgets

from pathlib import Path
from typing import List
from IPython.display import display, clear_output

# Import general tools and objects of this datamodel

# Objects
from FAIRFlow.core import Dataset, Experiment, PlantSetup

# Tools
from .auxiliary import Librarian, explorer
from .reader import gc_parser, gstatic_parser, mfm_parser, DEXPI2sdRDM


class measurement_object:
    """
    Stores the measurement widgets.
    """

    def __init__(self, name: str, component_list: List[str]) -> None:

        # Safe name
        self.name = name

        # Define portion of component dropdown to path tags
        portion = 3

        self.potentio_component = widgets.Dropdown(
            options=[""] + component_list,
            description="Corresponding plant component",
            layout=widgets.Layout(flex=str(portion)),
            style={"description_width": "auto"},
        )

        self.gc_component = widgets.Dropdown(
            options=[""] + component_list,
            description="Corresponding plant component",
            layout=widgets.Layout(flex=str(portion)),
            style={"description_width": "auto"},
        )

        self.mfm_component = widgets.Dropdown(
            options=[""] + component_list,
            description="Corresponding plant component",
            layout=widgets.Layout(flex=str(portion)),
            style={"description_width": "auto"},
        )

        self.potentio_files = widgets.TagsInput(
            allow_duplicates=False, layout=widgets.Layout(flex=str(10 - portion))
        )
        self.GC_files = widgets.TagsInput(
            allow_duplicates=False, layout=widgets.Layout(flex=str(10 - portion))
        )
        self.MFM_files = widgets.TagsInput(
            allow_duplicates=False, layout=widgets.Layout(flex=str(10 - portion))
        )

        widgets0 = widgets.VBox(
            [
                widgets.Label(value="Files for potentiostat:"),
                widgets.HBox([self.potentio_files, self.potentio_component]),
            ]
        )
        widgets1 = widgets.VBox(
            [
                widgets.Label(value="Files for gas chromatograph:"),
                widgets.HBox([self.GC_files, self.gc_component]),
            ]
        )
        widgets2 = widgets.VBox(
            [
                widgets.Label(value="Files for mass flow meter:"),
                widgets.HBox([self.MFM_files, self.mfm_component]),
            ]
        )

        # Combine the layout
        self.full_layout = widgets.VBox([widgets0, widgets1, widgets2])

    def update_component_list(self, component_list: List[str]):
        self.potentio_component.options = [""] + component_list
        self.gc_component.options = [""] + component_list
        self.mfm_component.options = [""] + component_list


class reading_raw_data_widget:

    def _dataset_input_handler(self, _):
        try:
            with open(self.dataset_dropdown.value) as f:
                self.dataset = Dataset.from_json(f)
            self.experiments.value = [exp.id for exp in self.dataset.experiments]
            self.plant = (
                self.dataset.experiments[0].plant_setup
                if self.dataset.experiments
                else PlantSetup()
            )

            # Update component list
            self.component_list = [pl.component_id for pl in self.plant.components]

            if self.component_list:
                with self.pid_output:
                    clear_output(wait=False)
                    print("PID taken from first experiment of dataset!\n")
            else:
                with self.pid_output:
                    clear_output(wait=False)
                    print("")

            # Call measurement input handler to update
            self._measurement_input_handler(None)

            # Update button description
            self.button_save.description = f"Save dataset as:  {self.dataset_dropdown.value.name}"
            
        except:
            raise KeyError("\nChoosen dataset cannot be interpreted!\n")

    def _add_file(self, category: str, file: str):
        # Function that adds a file to a chosen category
        # The file is added to the selected measurement tab to the selected children (potentiostat, gas chromatograph, etc.)
        if category == "potentiostat":
            self.tabs.children[self.tabs.selected_index].children[0].children[
                1
            ].value = self.tabs.children[self.tabs.selected_index].children[0].children[
                1
            ].value + [
                file
            ]
        elif category == "gas chromatograph":
            self.tabs.children[self.tabs.selected_index].children[1].children[
                1
            ].value = self.tabs.children[self.tabs.selected_index].children[1].children[
                1
            ].value + [
                file
            ]
        elif category == "mass flow meter":
            self.tabs.children[self.tabs.selected_index].children[2].children[
                1
            ].value = self.tabs.children[self.tabs.selected_index].children[2].children[
                1
            ].value + [
                file
            ]
        elif category == "species data":
            self.species_file.value = file

        elif category == "P&ID":
            self.pid_file.value = file

    def _read_pid(self, _):
        # Function that reads in DEXPI PID file and generates the PlantSetup
        self.plant = DEXPI2sdRDM(self.pid_file.value)

        with self.pid_output:
            self.pid_output.clear_output(wait=False)
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

    def _measurement_input_handler(self, _):

        # Delete measurement objects that are not in the measurements widget anymore
        del_idx = [
            i
            for i, obj in enumerate(self.measurement_objects)
            if not obj.name in self.measurements.value
        ]
        del_idx.sort(reverse=True)

        for idx in del_idx:
            del self.measurement_objects[idx]

        # Get names of current experiments
        measurement_names = [obj.name for obj in self.measurement_objects]

        # Add new measurement objects if they are not already there
        for i, measurement in enumerate(self.measurements.value):
            if not measurement in measurement_names:
                self.measurement_objects.insert(
                    i,
                    measurement_object(
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

        with self.tab_output:
            self.tab_output.clear_output(wait=False)
            display(widgets.VBox([heading, self.tabs]))

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

    def _experiment_input_handler(self, _):

        # Delete experiment objects that are not in the experiment widget anymore
        del_idx = [
            i
            for i, exp in enumerate(self.dataset.experiments)
            if not exp.id in self.experiments.value
        ]
        del_idx.sort(reverse=True)

        for idx in del_idx:
            del self.dataset.experiments[idx]

    def _save_dataset(self, _):
        # Function to save dataset
        with open(self.dataset_dropdown.value, "w") as f:
            f.write(self.dataset.json())
        print("Dataset saved.")



    def choose_data(self, root: Path, dataset_directory: str) -> None:

        self.librarian = Librarian(root_directory=root)
        datasets = self.librarian.search_files_in_subdirectory(
            root_directory=root,
            directory_keys=[dataset_directory],
            file_filter="json",
            verbose=False,
        )

        # Define ouput for some widgets
        self.pid_output = widgets.Output()
        self.tab_output = widgets.Output()

        # Call explorer widget
        self.explorer = explorer()
        explorer_widget = self.explorer.main(
            root=root,
            file_categories=[
                "Potentiostat",
                "Gas chromatograph",
                "Mass flow meter",
                "Species data",
                "P&ID",
            ],
            add_file_callalbe=self._add_file,
        )

        # Define all widgets
        self.dataset_dropdown = widgets.Dropdown(
            options=[("", Path(""))]
            + [(path.parts[-1], path) for _, path in datasets.items()],
            description="Choose dataset",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.experiment_name = widgets.Text(
            description="Experiment name:",
            placeholder="Provide a name for the experiment",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.pid_file = widgets.Text(
            description="P&ID file:",
            placeholder="Provided as xml file using the DEXPI standard",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.species_file = widgets.Text(
            description="Species file:",
            placeholder="Provided as yaml file",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.experiments = widgets.TagsInput(allow_duplicates=False)

        self.measurements = widgets.TagsInput(allow_duplicates=False)

        self.button_save = widgets.Button(
            description=f"Save dataset as:  {self.dataset_dropdown.value.name}",
            layout=widgets.Layout(width="30%"),
            style={"button_color": "lightblue"},
        )

        self.button_add_exp = widgets.Button(
            description="Add experiment", layout=widgets.Layout(width="auto")
        )

        self.button_read_pid = widgets.Button(
            description="Read PID", layout=widgets.Layout(width="auto")
        )

        self.button_vis_pid = widgets.Button(
            description="Visualize PID", layout=widgets.Layout(width="auto")
        )

        # Functions for the buttons
        self.button_add_exp.on_click(self._add_experiment)
        self.button_save.on_click(self._save_dataset)
        self.button_read_pid.on_click(self._read_pid)
        self.button_vis_pid.on_click(self._visualize_pid)

        # Attach the event handler to the 'value' property change of the file type widget
        self.dataset_dropdown.observe(self._dataset_input_handler, names="value")
        self.measurements.observe(self._measurement_input_handler, names="value")
        self.experiments.observe(self._experiment_input_handler, names="value")

        # Initialize several objects
        self.measurement_objects = []

        # Display the widgets

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

        widgets0 = widgets.HBox([self.dataset_dropdown])
        widgets1 = widgets.VBox(
            [
                widgets.Label(value="Manually add/remove Measurements:"),
                self.measurements,
            ]
        )
        widgets2 = widgets.VBox([explorer_widget, v_space_s])
        widgets3 = widgets.VBox([self.tab_output, v_space_s])
        widgets4 = widgets.VBox(
            [
                v_space_s,
                self.pid_file,
                v_space_ss,
                widgets.HBox([self.button_read_pid, self.button_vis_pid]),
                self.pid_output,
                v_space_ss,
                self.species_file,
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
                        self.experiment_name,
                        self.button_add_exp,
                    ]
                ),
                widgets.VBox([widgets.Label(value="Experiments:"), self.experiments]),
            ]
        )
        widgets6 = widgets.VBox(
            [self.button_save], layout=widgets.Layout(align_items="center")
        )

        # Combine the layout
        full_layout = widgets.VBox(
            [
                widgets0,
                v_space,
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

        # Display the layout
        display(full_layout)
