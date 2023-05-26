import pandas as pd
import os

from pathlib import Path
from datetime import datetime
from datamodel_b07_tc.core.data import Data
from datamodel_b07_tc.core.quantity import Quantity
from datamodel_b07_tc.core.unit import Unit
from datamodel_b07_tc.core.measurement import Measurement
from datamodel_b07_tc.core.measurementtype import MeasurementType


class MFMParser:
    def __init__(self, path_to_directory: str | bytes | os.PathLike):
        """Pass the path to a directory containing CSV-type files of the GC to be
        read.

        Args:
            path_to_directory (str | bytes | os.PathLike): Path to a directory containing CSV-type files.
        """
        path = list(Path(path_to_directory).glob("*.csv"))
        self._available_files = {
            file.stem: file for file in path if file.is_file()
        }

    def __repr__(self):
        return "MFM parser"

    def enumerate_available_files(self) -> dict[int, str]:
        """Enumerate the CSV files available in the given directory and
        return a dictionary with their index and name.

        Returns:
            dict[int, str]: Indices and names of available files.
        """
        return {
            count: value for count, value in enumerate(self.available_files)
        }

    def extract_exp_data(self, filestem: str):
        names_column = [
            "Datetime",
            "Time",
            "Signal",
            "Flow_rate",
        ]
        mfm_exp_data_df = pd.read_csv(
            self._available_files[filestem],
            sep=",",
            names=names_column,
            engine="python",
            encoding="utf-8",
            skiprows=1,
        )
        mfm_exp_data_df = mfm_exp_data_df.dropna()
        mfm_exp_data_df["Datetime"] = pd.to_datetime(
            mfm_exp_data_df["Datetime"], format="%d.%m.%Y ; %H:%M:%S"
        )
        # record = mfm_exp_data_df.to_dict(orient="list")
        # mapping = [
        #     {"values": "Datetime"},
        #     {"values": "Time"},
        #     {"values": "Signal"},
        #     {"values": "flow_rate"},
        # ]
        # units_formulae = [
        #     {
        #         "datetime": {
        #             "quantity": Quantity.DATETIME.value,
        #             "unit": Unit.YEARSMONTHSDAYSHOURSMINUTESSECONDS.value,
        #         }
        #     },
        #     {
        #         "time": {
        #             "quantity": Quantity.TIME.value,
        #             "unit": Unit.SECONDS.value,
        #         }
        #     },
        #     {
        #         "signal": {
        #             "quantity": Quantity.SIGNALvalue,
        #             "unit": Unit.NONE.value,
        #         }
        #     },
        #     {
        #         "flow_rate": {
        #             "quantity": Quantity.MASSFLOWRATE.value,
        #             "unit": Unit.MILLILITERPERSECOND.value,
        #         },
        #     },
        # ]
        # exp_data = {}
        # for dict in units_formulae.items():
        #     exp_data[dict.keys()[0]] = Data(
        #         *{key: value for key, value in dict.values()},
        #         **{key: record[value] for key, value in mapping.items()}
        #     )
        # mfm = Measurement(
        #     measurement_type=MeasurementType.MFM.value,
        #     experimental_data=[value for value in exp_data.values()],
        # )
        return mfm_exp_data_df  # , mfm

    @property
    def available_files(self) -> list[str]:
        return self._available_files

        # for line in open(self.file, 'r'):
        #     line = line.strip()
        #     if '=' in line:
        #         key_value = re.split('=', line.strip(r'_'))
        #         try:
        #             self.meta_data[key_value[0]] = float(key_value[1].strip("'"))
        #         except ValueError:
        #             self.meta_data[key_value[0]] = key_value[1].strip("'")
        # meta_data = self.meta_data
        # self.convert_datetime(meta_data)
        # self.rename_2theta(meta_data)
        # self.concatinate_wls(meta_data)
        # return meta_data

    # def extract_metadata(self, filestem: str) -> dict:
    #     with open(self._available_files[filestem], "r") as f:
    #         Lines = f.readlines()
    #         for i, line in enumerate(Lines):
    #             if line.strip() == "Time,Value":
    #                 num_line = i - 1
    #     metadata = pd.read_csv(
    #         self._available_files[filestem],
    #         sep=",",
    #         names=["Key", "Value"],
    #         engine="python",
    #         encoding="utf-8",
    #         skiprows=[j for j in range(num_line, i + 1)],
    #     )
    #     return metadata
