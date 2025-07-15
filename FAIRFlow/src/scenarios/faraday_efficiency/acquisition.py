#!~/miniconda3/bin/python

import ipywidgets as widgets

# Import FAIRFlow modules
from FAIRFlow.src.utils.registry import register_scenario
from FAIRFlow.src.acquisition.acquisition import ScenarioBase

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
