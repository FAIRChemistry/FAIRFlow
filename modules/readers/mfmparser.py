import pandas as pd
import os

from pathlib import Path
from datamodel_b07_tc.core.data import Data
from datamodel_b07_tc.core.quantity import Quantity
from datamodel_b07_tc.core.unit import Unit


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

        record = mfm_exp_data_df.to_dict(orient="list")
        mapping = [
            {"values": "Datetime"},
            {"values": "Time"},
            {"values": "Signal"},
            {"values": "Flow_rate"},
        ]
        units_formulae = {
            "datetime": {
                "quantity": Quantity.DATETIME.value,
                "unit": Unit.YEARSMONTHSDAYSHOURSMINUTESSECONDS.value,
            },
            "time": {
                "quantity": Quantity.TIME.value,
                "unit": Unit.SECONDS.value,
            },
            "signal": {
                "quantity": Quantity.SIGNAL.value,
                "unit": Unit.NONE.value,
            },
            "flow_rate": {
                "quantity": Quantity.MASSFLOWRATE.value,
                "unit": Unit.MILLILITERPERSECOND.value,
            },
        }
        mfm_exp_data = {}
        for i, (param, dict) in enumerate(units_formulae.items()):
            if param == "datetime":
                mfm_exp_data[param] = Data(
                    **{key: value for key, value in dict.items()},
                    **{
                        key: [
                            timestamp.to_pydatetime()
                            for timestamp in record[value]
                        ]
                        for key, value in mapping[i].items()
                    }
                )
            else:
                mfm_exp_data[param] = Data(
                    **{key: value for key, value in dict.items()},
                    **{key: record[value] for key, value in mapping[i].items()}
                )
        return mfm_exp_data_df, mfm_exp_data

    @property
    def available_files(self) -> list[str]:
        return self._available_files
