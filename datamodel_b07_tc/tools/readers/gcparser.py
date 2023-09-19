import pandas as pd
import os

from pathlib import Path
from datamodel_b07_tc.core.data import Data
from datamodel_b07_tc.core.data import Quantity
from datamodel_b07_tc.core.metadata import Metadata


class GCParser:
    def __init__(
        self,
        directory_paths: str | bytes | os.PathLike | Path,
        filename_meta: str,
        filename_exp: str,
    ):
        """Pass the path to a directory containing CSV-type files of the MFM to be
        read.

        Args:
            path_to_directory (str | bytes | os.PathLike): Path to a directory containing CSV-type files.
        """
        path_list_meta = []
        for path in directory_paths:
            path_list_meta.extend(Path(path).glob(filename_meta))
        self._available_files_meta = {
            count: file
            for count, file in enumerate(path_list_meta)
            if file.is_file()
        }
        path_list_exp = []
        for path in directory_paths:
            path_list_exp.extend(Path(path).glob(filename_exp))
        self._available_files_exp = {
            count: file
            for count, file in enumerate(path_list_exp)
            if file.is_file()
        }


    def __repr__(self):
        return "GC experimental data parser"

    def extract_exp_data(self, file_index: int) -> pd.DataFrame:
        """Extract only data block as a `pandas.DataFrame`.

        Args:
            filestem (str): Name of the file (only stem) of which the data is to be extracted.

        Returns:
            pandas.DataFrame: DataFrame containing only the data from the file.
        """
        exp_data_df_gc = pd.read_csv(
            self._available_files_exp[file_index],
            sep=",",
            names=[
                "Peak_number",
                "Retention_time",
                "Signal",
                "Peak_type",
                "Peak_area",
                "Peak_height",
                "Peak_area_percentage",
            ],
            engine="python",
            encoding="utf-16_le",
        )

        record = exp_data_df_gc.to_dict(orient="list")
        mapping = [
            {"values": "Peak_number"},
            {"values": "Retention_time"},
            {"values": "Signal"},
            {"values": "Peak_type"},
            {"values": "Peak_area"},
            {"values": "Peak_height"},
            {"values": "Peak_area_percentage"},
        ]
        units_formulae = {
            "peak_number": {
                "quantity": Quantity.PEAKNUMBER.value,
                "unit": None,
            },
            "retention_time": {
                "quantity": Quantity.RETENTIONTIME.value,
                "unit": 's',
            },
            "signal": {
                "quantity": Quantity.SIGNAL.value,
                "unit": None,
            },
            "peak_type": {
                "quantity": Quantity.PEAKTYPE.value,
                "unit": None,
            },
            "peak_area": {
                "quantity": Quantity.PEAKAREA.value,
                "unit": None,
            },
            "peak_height": {
                "quantity": Quantity.PEAKHEIGHT.value,
                "unit": None,
            },
            "peak_area_percentage": {
                "quantity": Quantity.PEAKAREAPERCENTAGE.value,
                "unit": '%',
            },
        }

        gc_exp_data = {}
        for i, (param, dict) in enumerate(units_formulae.items()):
            gc_exp_data[param] = Data(
                **{key: value for key, value in dict.items()},
                **{key: record[value] for key, value in mapping[i].items()}
            )
        return exp_data_df_gc, gc_exp_data

    def extract_metadata(self, file_index: int) -> pd.DataFrame:
        """Extract only data block as a `pandas.DataFrame`.

        Args:
            filestem (str): Name of the file (only stem) of which the data is to be extracted.

        Returns:
            pandas.DataFrame: DataFrame containing only the data from the file.
        """
        gc_metadata_df = pd.read_csv(
            self._available_files_meta[file_index],
            sep=",",
            names=[
                "parameter",
                "value",
                "description",
            ],
            engine="python",
            encoding="utf-16_le",
        )
        # rename = {
        #     "Parameter": "parameter",
        #     "Value": "value",
        #     "Description": "description",
        # }
        # rename(rename).
        record = gc_metadata_df.to_dict(orient="records")
        gc_metadata = {}
        for i, entry in enumerate(record):
            gc_metadata[i] = Metadata(**entry)
        return gc_metadata_df, gc_metadata

    @property
    def available_meta_files(self) -> list[str]:
        return self._available_files_meta
    @property
    def available_exp_files(self) -> list[str]:
        return self._available_files_exp
    # def enumerate_available_files(self) -> dict[int, str]:
    #     """Enumerate the CSV files available in the given directory and
    #     return a dictionary with their index and name.

    #     Returns:
    #         dict[int, str]: Indices and names of available files.
    #     """
    #     return {
    #         count: value for count, value in enumerate(self.available_files)
    #     }
