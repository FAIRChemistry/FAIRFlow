import regex as re
import pandas as pd
import pint_pandas
import os
from pathlib import Path
from datetime import datetime
from datamodel_b07_tc.core import Unit
from datamodel_b07_tc.core.data import Data
from datamodel_b07_tc.core.metadata import Metadata
from datamodel_b07_tc.core.massflowrate import (
    MassFlowRate,
)


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

    def extract_exp_data(self, filestem: str) -> dict:
        #     with open(self._available_files[filestem], "r") as f:
        #         Lines = f.readlines()
        #         for i, line in enumerate(Lines):
        #             if line.strip() == "Time,Value":
        #                 name_column = line.strip().split(sep=",")
        #                 num_line = i + 1

        names_column = [
            "datetime",
            "time",
            "signal",
            "flow",
        ]
        # ["/ (yyyy-mm-dd hh:mm:ss)", "/ (s)", "/ (1)", "/ (ml per s)"],
        exp_data_df = pd.read_csv(
            self._available_files[filestem],
            sep=",",
            names=names_column,
            engine="python",
            encoding="utf-8",
            skiprows=1
            # skiprows=[j for j in range(num_line)],
        )
        exp_data_df["datetime"] = pd.to_datetime(
            exp_data_df["datetime"], format="%d.%m.%Y ; %H:%M:%S"
        )
        # exp_data_df.columns = name_column
        datetime = Data(
            values=list(exp_data_df["datetime"].dt.to_pydatetime()),
            unit=Unit.DATETIME,
        )
        time = Data(values=list(exp_data_df["time"]), unit=Unit.SECONDS)
        signal = Data(values=list(exp_data_df["signal"]), unit=Unit.NONE)
        flow_rate = Data(
            values=list(exp_data_df["flow_rate"]),
            unit=Unit.MILLILITERPERSECOND,
        )
        mfr = MassFlowRate(
            datetime=datetime,
            time=time,
            signal=signal,
            flow_rate=flow_rate,
        )

        return exp_data_df, mfr

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
