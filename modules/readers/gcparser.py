import pandas as pd
import os

from pathlib import Path
from datamodel_b07_tc.core.unit import Unit
from datamodel_b07_tc.core.data import Data
from datamodel_b07_tc.core.data import Quantity
from datamodel_b07_tc.core.measurement import MeasurementType
from datamodel_b07_tc.core.measurement import Measurement
from datamodel_b07_tc.core.metadata import Metadata


class GCParser:
    def __init__(self, path_to_directory: str | bytes | os.PathLike):
        """Pass the path to a directory containing CSV-type files of the GC to be
        read.

        Args:
            path_to_directory (str | bytes | os.PathLike): Path to a directory containing CSV-type files.
        """
        path = list(Path(path_to_directory).glob("*.CSV"))
        self._available_files = {
            file.stem: file for file in path if file.is_file()
        }

    def __repr__(self):
        return "GC experimental data parser"

    def enumerate_available_files(self) -> dict[int, str]:
        """Enumerate the CSV files available in the given directory and
        return a dictionary with their index and name.

        Returns:
            dict[int, str]: Indices and names of available files.
        """
        return {
            count: value for count, value in enumerate(self.available_files)
        }

    def extract_exp_data(self, filestem: str) -> pd.DataFrame:
        """Extract only data block as a `pandas.DataFrame`.

        Args:
            filestem (str): Name of the file (only stem) of which the data is to be extracted.

        Returns:
            pandas.DataFrame: DataFrame containing only the data from the file.
        """
        gc_exp_data_df = pd.read_csv(
            self._available_files[filestem],
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

        record = gc_exp_data_df.to_dict(orient="list")
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
                "unit": Unit.NONE.value,
            },
            "retention_time": {
                "quantity": Quantity.RETENTIONTIME.value,
                "unit": Unit.SECONDS.value,
            },
            "signal": {
                "quantity": Quantity.SIGNAL.value,
                "unit": Unit.NONE.value,
            },
            "peak_type": {
                "quantity": Quantity.PEAKTYPE.value,
                "unit": Unit.NONE.value,
            },
            "peak_area": {
                "quantity": Quantity.PEAKAREA.value,
                "unit": Unit.NONE.value,
            },
            "peak_height": {
                "quantity": Quantity.PEAKHEIGHT.value,
                "unit": Unit.NONE.value,
            },
            "peak_area_percentage": {
                "quantity": Quantity.PEAKAREAPERCENTAGE.value,
                "unit": Unit.PERCENTAGE.value,
            },
        }

        gc_exp_data = {}
        for i, (param, dict) in enumerate(units_formulae.items()):
            gc_exp_data[param] = Data(
                **{key: value for key, value in dict.items()},
                **{key: record[value] for key, value in mapping[i].items()}
            )
        return gc_exp_data_df, gc_exp_data

    def extract_metadata(self, filestem: str) -> pd.DataFrame:
        """Extract only data block as a `pandas.DataFrame`.

        Args:
            filestem (str): Name of the file (only stem) of which the data is to be extracted.

        Returns:
            pandas.DataFrame: DataFrame containing only the data from the file.
        """
        gc_metadata_df = pd.read_csv(
            self._available_files[filestem],
            sep=",",
            names=[
                "parameter",
                "value",
                "description",
            ],
            engine="python",
            encoding="utf-16_le",
        )
        record = gc_metadata_df.to_dict(orient="records")
        gc_metadata = {}
        for i, entry in enumerate(record):
            gc_metadata[i] = Metadata(**entry)
        return gc_metadata_df, gc_metadata

    @property
    def available_files(self) -> list[str]:
        return self._available_files
