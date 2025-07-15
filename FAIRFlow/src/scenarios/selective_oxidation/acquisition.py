#!~/miniconda3/bin/python

import ipywidgets as widgets
from pathlib import PureWindowsPath

# Import FAIRFlow modules
from FAIRFlow.src.utils.registry import register_scenario
from FAIRFlow.src.acquisition.acquisition import ScenarioBase
from FAIRFlow.src.acquisition.acquisition import Measurement
from FAIRFlow.src.scenarios.selective_oxidation.readers import gc_parser_selective_oxidation

@register_scenario
class SelectiveOxidation(ScenarioBase):

    def __init__(self, dataset, root):

        style = self.style

        self.GCParser = gc_parser_selective_oxidation
        self.PureWindowsPath = PureWindowsPath

        # selective oxidation-specific widgets

        self.w_Label_PrechaDescr = widgets.Label(
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

        self.w_Dropdown_ChoosePrecha = widgets.Dropdown(

            layout = widgets.Layout(
                width='auto',
                grid_area='dropdown_choose_precha'
            ),
            style = style,
        )

        self.w_Html_ChaDescription = widgets.HTML(
            value="<p style='line-height: 1.2;'>Choose channels <br> ('Ctrl' + 'Left Click' for multiple):</p>",
            # value= '<style>p{word-wrap: break-word}</style> <p>'+ "Choose channels <br> ('Ctrl' + 'Left Click' for multiple):" +' </p>',
            layout=widgets.Layout(
                width='auto',
                grid_area='html_cha_descr'
            ),
        )

        self.w_Selectmultiple_ChooseCha = widgets.SelectMultiple(
            disabled = False,
            layout = widgets.Layout(
                width='auto',
                grid_area='selectmultiple_choose_cha'
            ),
            style = style,
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
                self.w_Label_PrechaDescr,                               # label_precha_descr
                self.w_Dropdown_ChoosePrecha,                           # dropdown_choose_precha
                self.w_Html_ChaDescription,                             # html_cha_descr
                self.w_Selectmultiple_ChooseCha,                        # selectmultiple_choose_cha
            ],
            layout=widgets.Layout(
                width='auto',
                grid_area = 'gridbox_specific',
                grid_template_rows='auto auto auto',
                grid_template_columns='25% 25% 50%',
                grid_template_areas='''
                "label_precha_descr       dropdown_choose_precha     dropdown_choose_precha"
                "html_cha_descr           selectmultiple_choose_cha  selectmultiple_choose_cha"
                "output_dropdown_measure  output_dropdown_measure    output_dropdown_measure"
                '''
            )
        )

        # call the constructor of the parent class
        super().__init__(dataset, root, w_Gridbox_Specific)

        # attach observers

        self.w_Selectmultiple_ChooseCha.observe(
            self._channel_handler,
            names="value"
        )

        self.w_Dropdown_ChoosePrecha.observe(
            self._prechannel_handler,
            names="value"
        )

        self.w_FileChooser_Data._select.on_click(
            self._file_chooser_input_handler,
        )
        
        self.w_Dropdown_Measure.observe(
            self.Handler_Measurement_Dropdown,
            names="value"
        )

    def _prechannel_handler(self, _):
        if not self.w_Dropdown_Measure.value == "":
            measurement = self.measurement_objects_dict[self.w_Dropdown_Measure.value]
            setattr(measurement, "prechannel", self.w_Dropdown_ChoosePrecha.value)

    def _channel_handler(self, _):
        if not self.w_Dropdown_Measure.value == "":
            measurement = self.measurement_objects_dict[self.w_Dropdown_Measure.value]
            setattr(measurement, "channels", self.w_Selectmultiple_ChooseCha.value)

    def _file_chooser_input_handler(self, _):
        if not self.w_FileChooser_Data._filename.value == "":
            self.mydata_df = self.GCParser(self.w_FileChooser_Data.selected)
            self.mylist = self.mydata_df['datetime'].astype(str) + ' - ' + self.mydata_df['Filename'].apply(lambda x: self.PureWindowsPath(x).name).astype(str) + ' - ' + self.mydata_df['Vial'].astype(str)
            self.w_Dropdown_ChoosePrecha.options = self.mylist
            self.w_Selectmultiple_ChooseCha.options = self.mylist
            setattr(self.w_FileChooser_Data._filename, "value", "")

    def Handler_Measurement_Dropdown(self, _=None):
        # Add additional updates ontop of what is done in every scenario
        super().Handler_Measurement_Dropdown()
        if not self.w_Dropdown_Measure.value == "":
            measurement = self.measurement_objects_dict[self.w_Dropdown_Measure.value]
            if hasattr(measurement, "prechannel"):
                self.w_Dropdown_ChoosePrecha.value = measurement.prechannel
            if hasattr(measurement, "channels"):
                self.w_Selectmultiple_ChooseCha.value = measurement.channels