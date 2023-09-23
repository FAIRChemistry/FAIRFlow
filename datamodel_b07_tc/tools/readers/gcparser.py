import pandas as pd

from pathlib import Path
from pydantic import BaseModel

from datamodel_b07_tc.modified.measurement import Measurement
from datamodel_b07_tc.modified.data import Data
from datamodel_b07_tc.modified.metadata import Metadata


class GCParser(BaseModel):


    def extract_experimental_data(self, experimental_data_path: Path) -> pd.DataFrame:
        """Extract only data block as a `pandas.DataFrame`.
        Args:
            experimental_data_path (Path): path to the file from which the experimental data are to be extracted.

        Returns:
            pandas.DataFrame: DataFrame containing the experimental data from the file read in.
        """
        quantity_unit_dict = {
            "Peak_number": None,
            "Retention_time": 's',
            "Signal": None,
            "Peak_type": None,
            "Peak_area": None,
            "Peak_height": None,
            "Peak_area_percentage": '%'
        }
        experimental_data_df = pd.read_csv(
            experimental_data_path,
            sep=",",
            names=[name for name in quantity_unit_dict.keys],
            engine="python",
            encoding="utf-16_le",
        )
        experimental_data_list=[]
        for quantity, unit in quantity_unit_dict.items():
            experimental_data_list.append(Data(quantity=quantity, values=experimental_data_df[quantity], unit=unit))
        return experimental_data_df, experimental_data_list

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
        record = gc_metadata_df.to_dict(orient="records")
        metadata_list = []
        for data in record:
            metadata_list.append(Metadata(**data))
        return gc_metadata_df, metadata_list
