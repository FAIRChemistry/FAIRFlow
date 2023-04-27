import pandas as pd
import os
from pathlib import Path


class GCMDParser:
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
        return "gc metadata parser"

    def enumerate_available_files(self) -> dict[int, str]:
        """Enumerate the CSV files available in the given directory and
        return a dictionary with their index and name.

        Returns:
            dict[int, str]: Indices and names of available files.
        """
        return {
            count: value for count, value in enumerate(self.available_files)
        }

    def extract_metadata(self, filestem: str) -> pd.DataFrame:
        """Extract only data block as a `pandas.DataFrame`.

        Args:
            filestem (str): Name of the file (only stem) of which the data is to be extracted.

        Returns:
            pandas.DataFrame: DataFrame containing only the data from the file.
        """
        metadata_df = pd.read_csv(
            self._available_files[filestem],
            sep=",",
            names=[
                "column_1",
                "column_2",
                "column_3"
                #     "Peak_Number",
                #     "Retention_Time",
                #     "Signal",
                #     "Peak_Type",
                #     "Area",
                #     "Height",
                #     "Area_Percentage",
            ],
            engine="python",
            encoding="utf-16_le",
        )
        return metadata_df

    @property
    def available_files(self) -> list[str]:
        return self._available_files
