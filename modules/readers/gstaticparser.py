import regex as re
import pandas as pd
import os
from pathlib import Path
from datamodel_b07_tc.core import Unit
from datamodel_b07_tc.core.data import Data
from datamodel_b07_tc.core.metadata import Metadata
from datamodel_b07_tc.core.potentiostaticmeasurement import (
    PotentiostaticMeasurement,
)


class GstaticParser:
    def __init__(
        self,
        path_to_directory: str | bytes | os.PathLike,
    ):
        """Pass the path to a directory containing CSV-type files of the GC to be
        read.

        Args:
            path_to_directory (str | bytes | os.PathLike): Path to a directory containing CSV-type files.
        """
        path = list(Path(path_to_directory).glob("*.DTA"))
        self._available_files = {
            file.stem: file for file in path if file.is_file()
        }

    def __repr__(self):
        return "Gstatic parser"

    def enumerate_available_files(self) -> dict[int, str]:
        """Enumerate the CSV files available in the given directory and
        return a dictionary with their index and name.

        Returns:
            dict[int, str]: Indices and names of available files.
        """
        return {
            count: value for count, value in enumerate(self.available_files)
        }

    def extract_metadata(self, filestem: str) -> dict:
        metadata = pd.read_csv(
            self._available_files[filestem],
            sep="\t",
            names=[
                "Abbreviation",
                "Type",
                "Parameter",
                "Description_or_unit",
            ],
            engine="python",
            encoding="utf-8",
            skiprows=[0, 1, *[i for i in range(55, 3658)]],
        )
        # metadata_list = []
        # for index, row in metadata.iterrows():
        #     abbreviation = row[0]
        #     type = row[1]
        #     parameter = row[2]
        #     description = row[3]
        #     metadata_list.append(
        #         Metadata(
        #             abbreviation=abbreviation,
        #             type=type,
        #             parameter=parameter,
        #             description=description,
        #         )
        #     )
        # pot = PotentiostaticMeasurement(metadata=metadata_list)
        return metadata  # , pot

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

    # def convert_datetime(self, meta_data):
    #     datemeasured = meta_data["DATEMEASURED"]
    #     pattern_date = r"([0-9]{1,2})\-([A-Za-z]*)\-([0-9]{4})\s([0-9]{2})\:([0-9]{2})\:([0-9]{2})"
    #     months = [
    #         "jan",
    #         "feb",
    #         "mar",
    #         "apr",
    #         "may",
    #         "jun",
    #         "jul",
    #         "aug",
    #         "sep",
    #         "oct",
    #         "nov",
    #         "dec",
    #     ]
    #     date_raw = re.findall(pattern_date, datemeasured)[0]
    #     datum = []
    #     for part in date_raw:
    #         try:
    #             datum.append(int(part))
    #         except ValueError:
    #             datum.append(months.index(part.lower()) + 1)
    #     date = datetime(
    #         datum[2], datum[1], datum[0], datum[3], datum[4], datum[5]
    #     )
    #     meta_data["DATEMEASURED"] = date
